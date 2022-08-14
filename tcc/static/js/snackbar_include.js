'use strict'

r(function(){
    let attr = $('#vt-snackbar').attr('data-text');
    if (typeof attr !== typeof undefined && attr !== false && attr.length != 0) {
        let data = {
            message: attr,
            timeout: 5000
        };
        $('#vt-snackbar')[0].MaterialSnackbar.showSnackbar(data);
    }
});
function r(f){/in/.test(document.readyState)?setTimeout('r('+f+')',9):f()}
