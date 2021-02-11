$('.file-item').click(function() {
    if (!$(this).hasClass('selected-item')) {
        $('li').removeClass('selected-item');
        $(this).addClass('selected-item');
    } else {
        $(this).removeClass('selected-item');
    }
    console.log($(this).text())
    $('#payload_file').val($(this).text())
});