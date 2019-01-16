$(function() {
  $('a#start').bind('click', function() {
    $.getJSON('/_add_numbers', {
      num_day: $('input[name="num_day"]').val(),
      coin: $('#selected_coin').val(),
      feature: $("#selected_feature").val()
    }, function(data) {
      // $("#result").text(data.result);
      if ( $.fn.dataTable.isDataTable( '#example' ) ) {
        table.destroy();
        table = $("#example").DataTable({
          data: data,
          columns: [
            { title: "Date" },
            { title: "Value" },
            ],
        searching: false
        })
    }
    else {
        table = $("#example").DataTable({
          data: data,
          columns: [
            { title: "Date" },
            { title: "Value" },
            ],
        searching: false
        })
    }

    });
    return false;
  });
});
