$(document).ready(function(){
    var table = $('table');
    $(".sortable")
        .wrapInner('<span title="sort this column"/>')
        .each(function(){
            var th = $(this),
                thIndex = th.index(),
                inverse = false;

            th.click(function(){
                table.find('td').filter(function(){

                    return $(this).index() === thIndex;

                }).sortElements(function(a, b){

                    return $.text([a]) > $.text([b]) ?
                        inverse ? -1 : 1
                        : inverse ? 1 : -1;

                }, function(){

                    // parentNode is the element we want to move
                    return this.parentNode;

                });

                inverse = !inverse;

            });

        });

    $("#searchInput").keyup(function () {
        //split the current value of searchInput
        var data = this.value.toUpperCase().split(" ");
        //create a jquery object of the rows
        var jo = $("#fbody").find("tr");
        if (this.value == "") {
            jo.show();
            return;
        }
        //hide all the rows
        jo.hide();

        //Recusively filter the jquery object to get results.
        jo.filter(function (i, v) {
            var $t = $(this);
            for (var d = 0; d < data.length; ++d) {
                if ($t.text().toUpperCase().indexOf(data[d]) > -1) {
                    return true;
                }
            }
            return false;
        })
        //show the rows that match.
        .show();
    }).focus(function () {
        this.value = "";
        $(this).css({
            "color": "black"
        });
        $(this).unbind('focus');
    }).css({
        "color": "#C0C0C0"
    });

$(function () {
    $('table').on('contextmenu', 'tr', function(e){
        $(this).find('.contextmenu')
            .addClass('visible')
            .css({
                top: e.pageY,
                left: e.pageX
            });
        return false;
    }).on('mouseleave', 'tr', function(){
        $('.contextmenu.visible').removeClass('visible');
    });
});

    // var frm = $('#otherOrderform');
    // frm.submit(function () {
    //     $.ajax({
    //         type: frm.attr('method'),
    //         url: frm.attr('action'),
    //         data: frm.serialize(),
    //         success: function (data) {
    //              alert('test')
    //         },
    //         error: function(data) {
    //              alert("Error");
    //         }
    //     });
    //     return false;
    // });
});
