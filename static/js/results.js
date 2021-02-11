$(document).ready(function() {
    $('.response-button').click(function() {
        $(this).closest('tr').next('.response-tr').toggle();
    })
});