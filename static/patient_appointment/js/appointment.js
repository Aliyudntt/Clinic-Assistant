$(document).ready(function() {
  $("#date").datepicker({
    todayHighlight: true,
    startDate: new Date(),
    autoclose: true
  });

  $("#date").on('change', function() {
    $("#appointmentFormError").html("");
    var date = $("#date").val();
    var branch = $("input:radio[name='branch']:checked").val();
    var weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    var weekday = new Date(date).getDay();
    var day = weekdays[weekday];
    $("#dentist").empty();
    $("#dentist").append($("<option>", { 'value': '', 'disabled': true, 'text': 'Select A Dentist', 'selected': true }));
    $("#schedule").empty();
    $("#schedule").append($("<option>", { 'value': '', 'text': 'Select A Doctor First', 'disabled': true, 'selected': true }));
    console.log("day:", day);
    console.log("branch:", branch);
    $.ajax({
      url: "/dentist_schedules/",
      type: "POST",
      data: { "day": day, 'branch': branch },
      dataType: "json",
      success: function(response) {
        var dentistlist = response.data;
        for (var i = 0; i < dentistlist.length; i++) {
          $("#dentist").append($("<option>", { 'value': dentistlist[i].id, 'data-idx': i, 'text': dentistlist[i].name }));
        }
      },
      error: function(xhr, textStatus, errorThrown) {
        if (xhr.status == 404) {
          var errmsg = "An error occurred while fetching doctors availability. Please try again later.";
          $("#appointmentFormError").html("<p>" + errmsg + "</p>");
        }
      }
    });
  });
});