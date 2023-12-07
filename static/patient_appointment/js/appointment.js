$("#date").datepicker({
    todayHighlight: true,
    startDate: new Date(),
    autoclose: true
  });
  
  var doctorlist = null;
  
  $("#date").on('changeDate', function() {
    $("#appointmentFormError").html("");
    var date = $("#date").val();
    var branch = $("input:radio[name='branch']:checked").val();
    var weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    var weekday = new Date(date).getDay();
    var day = weekdays[weekday];
    $("#doctor").empty();
    $("#doctor").append($("<option>", { 'value': '', 'disabled': true, 'text': 'Select A Doctor', 'selected': true }));
    $("#schedule").empty();
    $("#schedule").append($("<option>", { 'value': '', 'text': "Select A Doctor First", 'disabled': true, 'selected': true }));
  
    $.ajax({
      url: "appointment/doctor_schedules/",
      type: "POST",
      data: { "day": day, 'branch': branch },
      dataType: "json",
      success: function(response) {
        doctorlist = response.data;
        for (var i = 0; i < doctorlist.length; i++) {
          $("#doctor").append($("<option>", { 'value': doctorlist[i].id, 'data-idx': i, 'text': doctorlist[i].name }));
        }
      },
      error: function(xhr, textStatus, errorThrown) {
        if (xhr.status == 404) {
          var errmsg = "No Doctors available in the selected date";
          $("#appointmentFormError").append("<p>" + errmsg + "</p>");
        }
      }
    });
  });
  
  $("#doctor").on("change", function() {
    var idx = $("#doctor option:selected").attr('data-idx');
    var schedules = doctorlist[idx].schedules;
    $("#schedule").empty();
    for (var i = 0; i < schedules.length; i++) {
      $("#schedule").append($("<option>", { 'value': schedules[i].id, 'text': schedules[i].weekday + " From: " + schedules[i].start + " To: " + schedules[i].end }));
    }
  });
  
  $("#contact_number").inputmask({
    "mask": "+880 9999-999999"
  });
  
  $("#appointmentForm").validate();
  
  $(document).ready(function() {
    $("#appointmentConfirmPrint").on('click', function() {
      $("#appointmentPrintable").printThis();
    });
  });