"use strict"

$(function() {
    $('textarea[data-js]').parent().hide();

    $('select').change(checkElement);

    $('form').submit(function() {
        let option = $('select option:selected').text();
        if(option != 'Receitas') {
            $('textarea[data-js]').val('');
        }
    });

    checkElement();

    function checkElement() {
        let option = $('select option:selected').text();
        let element = $('textarea[data-js]');
        if(option == 'Receitas') {
            element.parent().fadeIn();
            element.attr({required: ''});
            if(element.val().length == 0) {
                element.parent().addClass('is-invalid');
            }
        } else {
            element.parent().fadeOut();
            let attr = element.attr('required');
            if(typeof attr !== typeof undefined && attr !== false) {
                element.removeAttr('required');
            }
            if(element.parent().is('.is-invalid')) {
                element.parent().removeClass('is-invalid');
            }
        }
    }
});