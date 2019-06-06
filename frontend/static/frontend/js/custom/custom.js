$(document).ready(function () {

    $('.likebutton').click(function () {
        var catid;
        catid = $(this).attr("data-catid");


        $.ajax(
            {
                type: "GET",
                url: "/marketplace/add_dev_to_wish_list",
                data: {
                    dev_id: catid

                },
                success: function (data, dev_count) {
                    $('#like' + catid).hide();
                    $('#message').text(data);
                    $('#picked').show();


                }
            })
    });




    $('#myTable').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ]
    });
    $('#myDevs').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ]
    });
    $('#Takenquizzes').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ]
    });
    $('#Failedquizzes').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ]
    });
    $('#Transactions').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ]
    });
    $("#myInput").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#myGroup #mycard").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
    $("#dev").click(function () {
        $("#data").toggle();
    });
    $(function () {
        $('#tags').tagsly({
            suggestions: function (input, cb) {
                cb(['jQuery', 'Html', 'CSS', 'JavaScript']);
            },
            placeholder: 'Enter tags!',
            maxItems: 10


        });

    });





});

