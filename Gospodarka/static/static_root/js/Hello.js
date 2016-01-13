    var table = $('table');
    alert("Dupa1");
    $("#dupa").css( "border", "3px solid red" );
    $( ".sortable" ).css( "border", "3px solid red" );
    $(".sortable")
        .wrapInner('<span title="sort this column"/>')
        .each(function(){
            var th = $(this),
                thIndex = th.index(),
                inverse = false;

            th.click(function(){
                alert("Dupa");
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
