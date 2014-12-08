"============================================================================
"File:        pigcheck.vim
"Description: Syntax checking for Hadoop pig
"Authors:     cavanaughwww@gmail.com
"
"============================================================================

if exists("g:loaded_syntastic_pig_pigcheck_checker")
    finish
endif
let g:loaded_syntastic_pig_pigcheck_checker = 1

let s:save_cpo = &cpo
set cpo&vim

function! SyntaxCheckers_pig_pigcheck_GetLocList() dict
    let makeprg = self.makeprgBuild({})

    let errorformat =
        \ 'ERROR %n: <file %f\, line %l\, column %c> %m,'.
        \ '<file %f\, line %l\, column %c> %m,'.
        \ '%-G%.%#'

    let loclist = SyntasticMake({
        \ 'makeprg': makeprg,
        \ 'errorformat': errorformat,
        \ 'returns': [0, 1] })

    for e in loclist
        if e['type'] ==? 'S'
            let e['type'] = 'E'
        elseif e['type'] ==? 'I'
            let e['type'] = 'W'
            let e['subtype'] = 'Style'
        endif
    endfor

    return loclist
endfunction

call g:SyntasticRegistry.CreateAndRegisterChecker({
    \ 'filetype': 'pig',
    \ 'name': 'pigcheck'})

let &cpo = s:save_cpo
unlet s:save_cpo

" vim: set et sts=4 sw=4:
