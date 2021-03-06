$(document).ready(function() {
    $('.enum-table').DataTable({
        dom: 'lBfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ]
    });

    $('#render-button').click(function (){
        $('.raw-response').hide();
        htmlsource = $('.raw-content').text().replace(/(\r\n|\n|\r)/gm, "");
        $('.render-content').attr("srcdoc",htmlsource);
        $('.render-content').show();
    })

    $('#raw-button').click(function (){
        $('.raw-response').show();
        $('.render-content').hide();
    })

    $('.open-details').click(function() {
        $('#response-text').text($(this).closest('td').next('.response-td').text());
        $('#request-id').text($(this).closest('td').prevAll('.response-id').first().text());
        $('#request-payload').text($(this).closest('td').prevAll('.response-payload').first().text());
        $('#request-status').text($(this).closest('td').prevAll('.response-status').first().text());
        findString()
        $('#modal').toggle();
        
    })

    $('#close-modal').click(function() {
        $('#modal').toggle();
    })

    $('#search-input').keyup(function () {
        findString();
        
    })
    function findString () {
        $('#response-text').unhighlight();
        $('#response-text').highlight($('#search-input').val());
        $('#search-results').text($('.highlight').length + ' results.')
    }

});
