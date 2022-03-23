$(document).ready(function() {
    $("#playlistSortSelector").change(function() {
        var option;
        option = $(this).val();

        $.get('/crescendo/playlistSort/',
        {'sortBy':option},
        function(data) {
            $("#playlist-menu").html(data);
        })

    })

});