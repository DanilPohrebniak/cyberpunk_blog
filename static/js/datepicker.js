$(document).ready(function() {
    $('input[name="date_of_birth"]').datepicker({
      format: 'yyyy-mm-dd',
      autoclose: true,
      todayHighlight: true,
      clearBtn: true,
      orientation: "auto"
    });
});