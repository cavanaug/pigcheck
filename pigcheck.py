#!/bin/env python
""" 
# pigcheck.py 
#
#
# Simple lint like tool to provide basic syntax aware checking for 
# editors like vim & syntastic
#
"""

VERSION = '1.0.1'

import re
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Simple pig latin linting tool')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('file', nargs='?', help='file to process')
group.add_argument('--version', dest='version', action='store_true',
                   help='show version information')
parser.add_argument('--debug', dest='debug', action='store_true',
                   help='show debug information')
args = parser.parse_args()

if args.version:
    print VERSION
    exit(0)


#
# This is a hack.  Why doesnt the subprocess module provide this...
def subprocess_check_all(cmdargs):
    """
    Execute external command and get its exitcode, stdout and stderr.
    """
    proc = subprocess.Popen(cmdargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode
    #
    return exitcode, out, err

# Initial pig command for execution
cli = [ 'pig', '-c', '-l', '/dev/null', '-x', 'local', '-useHCatalog' ]

#
# Need to discover all the possible params in use
# We will create surrogate params in the pig -c call
re_comment = re.compile('--.*')
re_param = re.compile('\$[a-zA-Z][a-zA-Z0-9]*')
params = set()
for line in open(args.file).readlines():
    line = re_comment.sub('', line)
    pa1 = re_param.findall(line)
    pa = [ x[1:]+'='+x[1:] for x in re_param.findall(line) ]
    map(params.add, pa)
for x in params:
    cli.append('-param')
    cli.append(x)

#
# Execute the pig checker
cli.append(args.file)
(pig_exit, pig_out, pig_error) = subprocess_check_all(cli)
if pig_exit == 0: 
    exit(0)

#
# Process & Format the results
#print pig_out
re_GRUNTERROR = re.compile('^.* ERROR org.apache.pig.tools.grunt.Grunt - (ERROR.*)$')
for line in pig_error.splitlines():
    m=re_GRUNTERROR.match(line)
    if m:
        print m.group(1)
    elif args.debug:
        print line

#print pig_error

#exit(pig_exit)
exit(0)
