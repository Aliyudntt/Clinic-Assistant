 $(function() {
     $('input').iCheck({
         checkboxClass: 'icheckbox_flat-green',
         radioClass: 'iradio_flat-green',
         increaseArea: '20%' // optional
     });
 });

 $("#search_param").inputmask({
     "mask": "+880 9999-999999"
 });
 $("#appointmentSearchBtn").click(function() {
     if ($("#search_param").val().length == 16) {
         $("#appointmentSearchForm").submit();
     }
 });

 $("#appointmentTable").DataTable();
 $("#medicineTable").DataTable();
 $("#testTable").DataTable();
 $("#historyTable").DataTable();


 $("#contact_number").inputmask({
     "mask": "+880 9999-999999"
 });

 $("#date").datepicker({
     todayHighlight: true,
     startDate: new Date(),
     autoclose: true
 });

 $("#idate").datepicker({
     todayHighlight: true,
     startDate: new Date(),
     autoclose: true
 });


 function resetForm(id) {
     $(id)[0].reset();
     $('input').iCheck('update');
 }




 $("#date").on('changeDate', function() {
    $("#appointmentFormError").html("");
    var date = $("#date").val();
    var branch = $("input:radio[name='branch']:checked").val();
    console.log(branch);
    var weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    var weekday = new Date(date).getDay();
    var day = weekdays[weekday];
    $("#schedule").empty();
    $("#schedule").append($("<option>", { 'value': '', 'text': "Select A Date First", 'disabled': true, 'selected': true }));
  
    $.ajax({
      url: "appointment/doctor/schedules/",
      type: "POST",
      data: { "day": day, 'branch': branch },
      dataType: "json",
      success: function(response) {
        var schedules = response.data;
        for (var i = 0; i < schedules.length; i++) {
          $("#schedule").append($("<option>", { 'value': schedules[i].id, 'text': schedules[i].weekday + " From: " + schedules[i].start + " To: " + schedules[i].end }));
        }
      },
      error: function(xhr, textStatus, errorThrown) {
        if (xhr.status == 404) {
          var errmsg = xhr.responseJSON.message;
          $("#appointmentFormError").append("<p>" + errmsg + "</p>");
        }
      }
    });
  });

  
 $("#appointmentForm").validate();
 $("#medicineForm").validate();
 $("#testForm").validate();

 $("#tests").select2();


 $("#medForm").sheepIt({
     separator: '',
     allowRemoveLast: true,
     allowRemoveCurrent: true,
     allowRemoveAll: true,
     allowAdd: true,
     allowAddN: true,
     iniFormsCount: 0,
     minFormsCount: 0,
     afterAdd: function(source, clonse) {
         $(".medicine_name").select2();
     }
 });

 $("#testResultForm").sheepIt({
     separator: '',
     allowRemoveLast: true,
     allowRemoveCurrent: true,
     allowRemoveAll: true,
     allowAdd: true,
     allowAddN: true,
     iniFormsCount: 0,
     minFormsCount: 0,
     afterAdd: function(source, clonse) {
         $(".test-results").select2();
     }
 });