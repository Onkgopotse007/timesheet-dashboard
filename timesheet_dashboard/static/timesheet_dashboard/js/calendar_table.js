$(document).ready(function(){
    $("#add-row").click(function(){
        var task = $("#task").val();
        
        var markup =
        			"<tr>"+
        				"<td></td>"+
        				"<td> <input id='dailyentry_set-0-duration' type='number' class='form-control form-control-sm' name='dailyentry_set-0-duration'/></td>"+
        				"<td> <input id='dailyentry_set-1-duration' type='number' class='form-control form-control-sm' name='dailyentry_set-1-duration'/></td>"+
        				"<td> <input id='dailyentry_set-2-duration' type='number' class='form-control form-control-sm' name='dailyentry_set-2-duration'/></td>"+
        				"<td> <input id='dailyentry_set-3-duration' type='number' class='form-control form-control-sm' name='dailyentry_set-3-duration'/></td>"+
        				"<td> <input id='dailyentry_set-4-duration' type='number' class='form-control form-control-sm' name='dailyentry_set-4-duration'/></td>"+
        				"<td> <input id='dailyentry_set-5-duration' type='number' class='form-control form-control-sm' name='dailyentry_set-5-duration'/></td>"+
        				"<td> <input id='dailyentry_set-6-duration' type='number' class='form-control form-control-sm' name='dailyentry_set-6-duration'/></td>"+
        				"<td> <input id='dailyentry_set-TOTAL_FORMS' type='hidden' class='form-control form-control-sm' value='7' name='dailyentry_set-TOTAL_FORMS'/> </td>"+
		                "<td> <input id='dailyentry_set-INITIAL_FORMS' type='hidden' value='0' name='dailyentry_set-INITIAL_FORMS'/></td>"+
		                "<td> <input id='dailyentry_set-MIN_NUM_FORMS' type='hidden' value='0' name='dailyentry_set-MIN_NUM_FORMS'/> </td>"+
		                "<td> <input id='dailyentry_set-MAX_NUM_FORMS' type='hidden' value='31' name='dailyentry_set-MAX_NUM_FORMS'/></td>"+
        				"<td>0</td>"+
        				"<td></td>"+
        				"<td><a class='btn btn-default btn-sm remove'><i class='glyphicon glyphicon-remove'></i></a></td>"
        			"</tr>";
        $("table tbody").append(markup);
    });
    
});

$(document).on('click', '.remove', function() {
	var trIndex = $(this).closest("tr").index();
   	$(this).closest("tr").remove();
});

$(document).on('click', '#nextWeek', function() {
	document.getElementById("controller").value = "next";
	$('#controlForm').submit();
});

$(document).on('click', '#prevWeek', function() {
	document.getElementById("controller").value = "prev";
	$('#controlForm').submit();
});
