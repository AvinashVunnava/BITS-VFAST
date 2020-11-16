"use strict";

(function($) {
  
  var overviewAPI = "http://localhost:9609/rooms/get_bookings";
  
  function showInfo(res){
    var dataSet     = [],
        normalResp  = [],
        columns     = [],
        column      = res.normal_rooms[0];
    Object.keys(column).forEach(function(i){
        columns.push({ 'title': i });
    });
    res.normal_rooms.forEach(function(i){
        var innerList = [];
        Object.values(i).forEach(function(j){
            innerList.push(j)
        });
        normalResp.push(innerList);
    });

    $("#loader_new").addClass("no-display");
    $("#normalHeader").removeClass("no-display");

    var normTable = $("#normalTable").DataTable({
        "lengthChange": false,
        "buttons": [ 'copy', 'excel', 'pdf', 'colvis' ],
        "order": [[3, 'asc']],
        "data": normalResp,
        "columns": columns
    });
    normTable.buttons().container()
             .appendTo( $('div.eight.column:eq(0)', normTable.table().container()) );
  }

  setTimeout(function(){
      $.ajax({
        url: overviewAPI,
        type: 'GET',
        crossDomain : true,
        success: function(res, status) {
            if(status != "success"){
                toastr.info(status);
                return;
            }
            if(res && !res.normal_rooms && !res.deluxe_rooms){
                toastr.info("Sorry No Info available");
                return;
            }
            showInfo(res);
        },
        error: function(data, status){
            toastr.error(status);
        }
      });

  }, 1500);

})(jQuery);
