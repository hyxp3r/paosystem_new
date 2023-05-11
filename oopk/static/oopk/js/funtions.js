$(document).ready(function() {
    $('input[name="radioReportType"]').change(function() {
      if($(this).attr('id') == 'radioReportTypeSecond') {
        $('#comment_label').show();
        $('#comment').show();
      }
      else {
        $('#comment_label').hide();
        $('#comment').hide();
      }
    });
  });