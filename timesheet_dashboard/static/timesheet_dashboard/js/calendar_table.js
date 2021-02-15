var row_count = 1;
$(document).ready(function(){
    $("#add-row").click(function(){
		
        var task = $("#task").val();
        var day_count = (row_count*7);
		var no_of_weeks = parseInt($("#no_of_weeks").val());
		var blank_days = parseInt($("#blank_days").val());
		
		/*if (row_count==1){
			for days in blank_days
		}*/
        
		if (row_count <=  no_of_weeks){
	        var markup = "<tr>"+
	        				"<td> <input id='tasks' type='text' class='form-control form-control-sm' name='tasks' value='" + task + "' readonly /></td>"+
	        				"<td> <input id='dailyentry_set-'+(day_count)+-duration' type='number' class='form-control form-control-sm' name='dailyentry_set-0-duration'/> </td>"+
	        				"<td> <input id='dailyentry_set-'+(day_count+1)+'-duration' type='number' class='form-control form-control-sm' name='dailyentry_set-1-duration'/></td>"+
	        				"<td> <input id='dailyentry_set-'+(day_count+2)+'-duration' type='number' class='form-control form-control-sm' name='dailyentry_set-2-duration'/></td>"+
	        				"<td> <input id='dailyentry_set-'+(day_count+3)+'-duration' type='number' class='form-control form-control-sm' name='dailyentry_set-3-duration'/></td>"+
	        				"<td> <input id='dailyentry_set-'+(day_count+4)+'-duration' type='number' class='form-control form-control-sm' name='dailyentry_set-4-duration'/></td>"+
	        				"<td> <input id='dailyentry_set-'+(day_count+5)+'-duration' type='number' class='form-control form-control-sm' name='dailyentry_set-5-duration'/></td>"+
	        				"<td> <input id='dailyentry_set-'+(day_count+6)+'-duration' type='number' class='form-control form-control-sm' name='dailyentry_set-6-duration'/></td>"+
	        				"<td >0</td>"+
	        				"<td colspan=\"15\"></td>"+
	        				"<td><a class='btn btn-default btn-sm remove'><i class='glyphicon glyphicon-remove'></i></a></td>"
	        			"</tr>";
	        $("table tbody").append(markup);
	row_count += 1;}
    });	

	
	    
});

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

$(document).on('click', '.remove', function() {
   	$(this).closest("tr").remove();
});

$(document).on('click', '#prevMonth', function() {
	document.getElementById("controller").value = "prev";
	$('#controlForm').submit();
});
