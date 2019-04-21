"use strict";

(function($) {
    
  var availabilityAPI = "http://localhost:9609/rooms/check_availability",
      bookingAPI      = "http://localhost:9609/rooms/student_booking",
      bookingType     = "student";
  
  
  function getParams(){
    var params = {  _type       : $('input[type=radio][name=room-type]:checked')[0].id,
                    student     : $('#student_name').val(), 
                    _id         : $("#student_id").val(),
                    mobile_num  : $("#student_mobile").val(),
                    guest_name  : $("#guest_name").val(),
                    guest_num   : $("#guest_no").val(),
                    check_in    : $("#checkin").val(),
                    check_out   : $("#checkout").val(),
                    dept        : $('#course :selected').val(),
                    relation    : $("#relation").val(),
                    purpose     : $("#reason").val(),
                    food        : $('input[type=radio][name=food]:checked')[0].id
                }
    var values = Object.values(params)
    if(values.includes('')){ return {} };
    return params
  }

  function showInfo(res){
   $(".loader").addClass("no-display");
   $(".availableResp").removeClass("no-display");
   var normalRooms = res.normal.avail_count,
       deluxeRooms = res.deluxe.avail_count;
   $("#availInfo").html("<div class='fantasy-font font-large'>" +
                        "<b><span> No.of Rooms available </span></b><br />" +
                        "<span>Normal:" + normalRooms + " </span><br />" +
                        "<span>Deluxe:" + deluxeRooms + "</span>" +
                        "</div>");
  }
  
  //Will be called by default
  setTimeout(function(){
      $.ajax({
        url: availabilityAPI,
        type: 'GET',
        crossDomain : true,
        success: function(res, status) {
            if(status != "success"){
                toastr.info(status);
                return;
            }
            if(res && !res.deluxe.avail_count && !res.normal.avail_count){
                toastr.info("Sorry No Rooms available");
                return;
            }
            showInfo(res);
        },
        error: function(data, status){
            toastr.error(status);
        }
      });
  }, 3500);

  $("#showFormClick").on("click", function(){
    bookingType = $('input[type=radio][name=booking]:checked')[0].id;
    if(!bookingType){
        toastr.warinig("Please select type of booking");
        return;
    }

    var username = $("#username").val()
    var password = $("#password").val()

    if(bookingType == "student" && username != 'h20180350p@pilani.bits' && password != 'h20180350p@bits'){
        toastr.error("Enter valid student username and password");
        return;
    }
    else if(bookingType == "faculty" && username != 'faculty@pilani.bits.ac.in' && password != 'Bitsfaculty'){
        toastr.error("Enter valid faculty username and password")
        return;
    }

    $(".Info").addClass("no-display");
    $(".signup-form").removeClass("no-display");

    if(bookingType == "faculty"){
        $("#student_name_label").text("Faculty Name * :");
        $("#student_id_label").text("Faculty Id * :");
        $("#student_mobile_label").text("Faculty Mobile No * :");
    }
  });

  $('#reset').on('click', function(){
      var _confirm = confirm("Are you sure you want to reset Fields ?");
      if (_confirm){
        $('.register-form input').each(function() { this.value = ""});
        $("#course").val("");
      }
      else{
        return;
      }
  });

  $("#submit").on("click", function(){
    var params = getParams();
    if($.isEmptyObject(params)){
        toastr.warning("Please fill in all Required Fields!!");
        return;
    }
    var checkin  = Number(params.check_in.split('-')[2]),
        checkout = Number(params.check_out.split('-')[2]);
    if(checkin > checkout) {
        toastr.error("Check-out Date cannot be less than Check-in Date");
        return;
    }
    $(".signup-form").addClass("no-display");
    $(".submitInfo").removeClass("no-display")
    $.ajax({
        url: bookingAPI,
        type: 'GET',
        data: JSON.stringify(params),
        success: function(res, status) {
            if(status != "success"){
                $(".submitInfo").addClass("no-display")
                toastr.error("Unknown Error Occurred!! Please try after sometime.");
                return;
            }
            if(res && !res.success){
                $(".submitInfo").addClass("no-display")
                toastr.error("Failed to Book Room! Please try after sometime.");
                return;
            }
            $(".submitInfo").addClass("no-display")
            toastr.success("Booking Success!!!");
            $(".successInfo").removeClass("no-display")
        }
    });
  });

})(jQuery);
