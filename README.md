PigCheck
========

Simple Hadoop pig latin syntax checker for use with syntastic or other IDEs


Features
--------
The biggest feature pigcheck has over just running "pig -c" is that it will autodiscover
any parameters in use in your pig script and will build a command line passing surrogate
params so that the "pig -c" can actually proceed


Installation
------------

- cp pigcheck.py ~/bin/pigcheck
- cp -rf syntax_checkers to ~/.vim/bundle/syntastic


