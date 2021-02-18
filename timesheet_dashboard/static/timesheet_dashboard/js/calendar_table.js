var row_count = 1;
var indexes = 0;
var markup = '';
var header_markup = '';
var year = parseInt($("#year").val());
var curr_month = parseInt($("#curr_month").val());

$(document).ready(function(){

    $("#add-row").click(function(){
        var task = $("#task").val();
		var no_of_weeks = parseInt($("#no_of_weeks").val());
		header_markup = '';
		markup = '';

		if (row_count <=  no_of_weeks){

			header_markup = "<tr> <td>  </td>";

	        markup = "<tr> <td> <input id='tasks' type='text' class='form-control form-control-sm' name='tasks' value='" + task + "' readonly /></td>";
			indexes = Array(7).fill().map((x,i)=>(i + (7*(row_count-1))))

			indexes.forEach(tableRows);

			header_markup += "<td colspan=\"17\"></td> </tr>";
			markup += "<td>0</td>"+
	        		"<td colspan=\"15\"></td>"+
	        		"<td><a class='btn btn-default btn-sm remove'><i class='glyphicon glyphicon-remove'></i></a></td>"
	        		"</tr>";

	        $("table tbody").append(header_markup);		
	        $("table tbody").append(markup);

			row_count += 1;}
    });

});

function tableRows(value){

	markup += "<td> "+
			 "<input id='dailyentry_set-"+value+"-day' type='hidden' value="+value+" class='form-control form-control-sm' name='dailyentry_set-"+value+"-day'/>" +
			 "<input id='dailyentry_set-"+value+"-entry_type' type='hidden' value='reg_hours' class='form-control form-control-sm' name='dailyentry_set-"+value+"-entry_type'/>" +
			"<input id='dailyentry_set-"+value+"-duration' type='number' class='form-control form-control-sm' name='dailyentry_set-"+value+"-duration'/> </td>";
	
	header_markup += "<td style='text-align:center;''> "+ value +"</td>";

}

$(document).on('click', '#save-record', function() {
	var extras ="<tr>"+
				"<td> <input id='dailyentry_set-TOTAL_FORMS' type='hidden' class='form-control form-control-sm' value='7' name='dailyentry_set-TOTAL_FORMS'/> </td>"+
			    "<td> <input id='dailyentry_set-INITIAL_FORMS' type='hidden' value='0' name='dailyentry_set-INITIAL_FORMS'/></td>"+
			    "<td> <input id='dailyentry_set-MIN_NUM_FORMS' type='hidden' value='0' name='dailyentry_set-MIN_NUM_FORMS'/> </td>"+
			    "<td> <input id='dailyentry_set-MAX_NUM_FORMS' type='hidden' value='31' name='dailyentry_set-MAX_NUM_FORMS'/></td>"+
				"</tr>";
	$("table tbody").append(extras);
});

$(document).on('click', '#nextMonth', function() {
	document.getElementById("controller").value = "next";
	$('#controlForm').submit();
});

$(document).on('click', '#prevMonth', function() {
	document.getElementById("controller").value = "prev";
	$('#controlForm').submit();
});

$(document).on('click', '.remove', function() {
   	$(this).closest("tr").remove();
});


$(document).on('click', '#auto_fill', function() {

	tableIndex = Array((row_count-1)*7).fill().map((x,i)=>i);

	tableIndex.forEach(function(entry){

		element_id = 'dailyentry_set-'+entry+'-duration';
		document.getElementById(element_id).value = 8;
	});
});
