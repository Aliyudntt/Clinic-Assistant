$("#date").datepicker({
  todayHighlight: true,
  startDate: new Date(),
  autoclose: true
});

var dentistlist;

$("#date").on('changeDate', function() {
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

  $.ajax({
    url: "/appointment/dentist_schedules",
    type: "POST",
    data: { "day": day, 'branch': branch },
    dataType: "json",
    success: function(response) {
      dentistlist = response.data;
      for (var i = 0; i < dentistlist.length; i++) {
        $("#dentist").append($("<option>", { 'value': dentistlist[i].id, 'data-idx': i, 'text': dentistlist[i].name }));
      }
    },
    error: function(xhr, textStatus, errorThrown) {
      if (xhr.status == 404) {
        var errmsg = "An error occurred while fetching doctors availability. Please try again later.";
        $("#appointmentFormError").append("<p>" + errmsg + "</p>");
      }
    }
  });
});

$("#dentist").on("change", function() {
  var idx = $("#dentist option:selected").attr('data-idx');
  var schedules = dentistlist[idx].schedules;
  $("#schedule").empty();
  for (var i = 0; i < schedules.length; i++) {
    $("#schedule").append($("<option>", { 'value': schedules[i].id, 'text': schedules[i].weekday + " From: " + schedules[i].start + " To: " + schedules[i].end }));
  }
});