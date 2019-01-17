$(function() {
  $('a#start').bind('click', function() {
    $.getJSON('/_add_numbers', {
      num_day: $('input[name="num_day"]').val(),
      coin: getValueUsingParentTag(),
      feature: $("#selected_feature").val()
    }, function(data) {
      // $("#result").text(data.result);
      console.log(data)
      if ( $.fn.dataTable.isDataTable( '#example' ) ) {
        table.destroy();
        $('#example').empty();
        table = $("#example").DataTable({
          data: data.rows,
          columns: data.coin_set,
          searching: false
        })
    }
    else {
        table = $("#example").DataTable({
          data: data.rows,
          columns: data.coin_set,
          searching: false
        })
    }

    });
    return false;
  });
});
function parseData(data){
  var dateParser = d3.timeParse("%m-%d-%Y")
  data.foreach(function(d){
    d[0] = dateParser(d[0])
  })
}
function drawLinePlot(data){
  console.log(data)
}
function getValueUsingParentTag(){
	var chkArray = [];
	
	/* look for all checkboes that have a parent id called 'checkboxlist' attached to it and check if it was checked */
	$("#checkboxlist input:checked").each(function() {
		chkArray.push($(this).val());
	});
	
	/* we join the array separated by the comma */
	var selected;
	selected = chkArray.join(',') ;
	
	/* check if there is selected checkboxes, by default the length is 1 as it contains one single comma */
  return selected
}