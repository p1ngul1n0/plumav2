$(document).ready(function() {
    $('.enum-table').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ]
    });
    $('.response-button').click(function() {
        $(this).closest('tr').next('.response-tr').toggle();
    })

    $('.open-details').click(function() {
        $('#response-text').text($(this).closest('td').next('.response-td').text());
        console.log($(this).closest('td'));
        $('#request-id').text($(this).closest('td').prevAll('.response-id').first().text());
        $('#request-payload').text($(this).closest('td').prevAll('.response-payload').first().text());
        $('#request-status').text($(this).closest('td').prevAll('.response-status').first().text());
        $('#modal').toggle();
    })

    $('#close-modal').click(function() {
        $('#modal').toggle();
    })
});
