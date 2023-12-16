import { IMask } from 'imask';

$(document).ready(function() {
  $('input').iCheck({
    checkboxClass: 'icheckbox_flat-green',
    radioClass: 'iradio_flat-green',
    increaseArea: '20%'
  });

  const searchButton = document.getElementById('appointmentSearchBtn');
  const inputElement = document.getElementById('search_param');
  const maskOptions = {
    mask: '+234 000 000 0000'
  };
  const mask = IMask(inputElement, maskOptions);

  searchButton.addEventListener('click', function() {
    if (mask.unmaskedValue.length === 11) {
      document.getElementById('appointmentSearchForm').submit();
    }
  });

  $("#appointmentTable").DataTable();
  $("#medicineTable").DataTable();
  $("#testTable").DataTable();
  $("#historyTable").DataTable();

  const contactInputElement = document.getElementById('contact_number');
  const contactMaskOptions = {
    mask: '+234 000 000 0000'
  };
  const contactMask = IMask(contactInputElement, contactMaskOptions);

  $("#date").datepicker({
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
    $("#schedule").append($("<option>", {
      'value': '',
      'text': "Select A Date First",
      'disabled': true,
      'selected': true
    }));

    $.ajax({
      url: "appointment/schedules/",
      type: "POST",
      data: {
        "day": day,
        'branch': branch
      },
      dataType: "json",
      success: function(response) {
        var schedules = response.data;
        for (var i = 0; i < schedules.length; i++) {
          $("#schedule").append($("<option>", {
            'value': schedules[i].id,
            'text': schedules[i].weekday + " From: " + schedules[i].start + " To: " + schedules[i].end
          }));
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
    afterAdd: function(source, clone) {
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
    afterAdd: function(source, clone) {
      $(".test-results").select2();
    }
  });
});