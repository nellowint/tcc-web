"use strict"

$(function() {
    $('.vt-image-input').change(function() {
        let file = $(this).prop('files')[0];
        if(file.length !== 0) {
            if(validFileType(file)) {
                let reader  = new FileReader();

                reader.addEventListener("load", function () {
                    $('.vt-image').attr("src", reader.result);
                }, false);
                
                reader.readAsDataURL(file);
            } else {
                let data = {message: 'Arquivo ' + file.name + ' não contém uma extensão válida.'};
                $("#vt-snackbar")[0].MaterialSnackbar.showSnackbar(data);
            }
        }
    });

    function validFileType(file) {
        let fileTypes = ['image/jpg','image/jpeg','image/png'];

        for(let i = 0; i < fileTypes.length; i++) {
            if(file.type === fileTypes[i]) {
                return true;
            }
        }

        return false;
    }
    
});