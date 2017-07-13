var maxLength = 500;
        $('#textareaChars').keyup(function(event) {
        var length = maxLength - $(this).val().length;
        $('#chars').text(length);
    });