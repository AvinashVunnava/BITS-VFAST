"use strict";

(function($) {
    
  var availabilityAPI = "http://localhost:9609/rooms/check_availability",
      bookingAPI      = "http://localhost:9609/rooms/student_booking",
      bookingType     = "student";
  
  
  function getParams(){
    var params = {  _type       : 'normal',//$('input[type=radio][name=room-type]:checked')[0].id,
                    student     : $('#student_name').val(), 
                    _id         : $("#student_id").val(),
                    mobile_num  : $("#student_mobile").val(),
                    dept        : $('#course :selected').val(),
                    purpose     : $("#reason").val(),
                }
    var values = Object.values(params)
    if(values.includes('')){ return {} };
    return params
  }

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
