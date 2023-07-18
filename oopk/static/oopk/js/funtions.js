$(document).ready(function() {
    $('input[name="radioReportType"]').change(function() {
      if($(this).attr('id') == 'radioReportTypeSecond') {

        $('#report_name_label').show();
        $('#report_name').show();
        $('#report_name').prop('required', true);
        $('#comment_label').show();
        $('#comment').show();
        
      }
      else {
        $('#report_name_label').hide();
        $('#report_name').hide();
        $('#report_name').prop('required', false);
        $('#comment_label').hide();
        $('#comment').hide();
      }
    });
  });

  $(document).ready(function() {
    $('#checkboxMinRating').change(function() {
      if ($(this).is(':checked')) {

        $('#minrating').show();
        $('#minrating').prop('required', true);
        
      }
      else {
        $('#minrating').hide();
        $('#minrating').prop('required', false);
      }
    });
  });