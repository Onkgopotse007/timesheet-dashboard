$(document).ready(function(){
	var prefilled_rows = parseInt($("#prefilled_rows").val());
	var row_count = prefilled_rows;
	var last_day = parseInt($("#last_day").val());
	var indexes = 0;
	var markup = '';
	var total_forms = 0;
	var header_markup = '';
	var blank_days = parseInt($("#blank_days").val());

	var entry_types = JSON.parse(document.getElementById('entry_types').textContent);
    var select = document.createElement("select");

    $("#add-row").click(function(){
		var no_of_weeks = parseInt($("#no_of_weeks").val());
		header_markup = '';
		markup = '';
		spaces = 7;

		header_markup = "<tr> ";

	    markup = "<tr> ";

		if (row_count  < no_of_weeks){
			spaces = spaces - blank_days;

			if(prefilled_rows==0 && row_count == 0){
				count = blank_days;
				while(count != 0){
					header_markup += "<td>  </td>";
					markup += "<td class='blank_cells' type = 'hidden' value='' colspan='1'></td>";
					count --;
				}
				indexes = Array(spaces).fill().map((x,i)=>(i));
			}
			else{
				var cols = (((row_count-prefilled_rows) * 7));
				if(prefilled_rows==0){
					cols = (((row_count-1) * 7)+spaces);
				}

				indexes = Array(7).fill().map((x,i)=>(i + cols));
			}

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


function tableRows(value){
	var day = value+1;
	if(prefilled_rows != 0){
		day = (((prefilled_rows-1) * 7)+spaces) + (value+1);
	}
	if(day <= last_day){
		markup += "<td> "+
				 "<div class='input-group'> <input id='dailyentry_set-"+value+"-duration' type='number' value='0' class='form-control form-control-sm' name='dailyentry_set-"+value+"-duration max='24' style='width:48px; padding:4px 8px; border-right:0;'/>"+
				 '<button title="entry_type" type="button" class="btn btn-default btn-sm dropdown-toggle form-control form-control-sm" data-toggle="dropdown" style="width:44px; ">'+
				 'RH <span class="caret"></span></button> <ul class="dropdown-menu" role="menu" > <li class="dropdown-header">Leave Type </li>' +
				 '{% for e in et %} <li>{{ e}}</li> {% endfor %} </ul> </div>'+
				 "<input id='dailyentry_set-"+value+"-entry_type' type='hidden' value='RH' class='form-control form-control-sm' name='dailyentry_set-"+value+"-entry_type'/>" +
				"<input id='dailyentry_set-"+value+"-day' type='hidden' value="+day+" class='form-control form-control-sm' name='dailyentry_set-"+value+"-day'/>" +
				"<input id='dailyentry_set-"+value+"-row' type='hidden' value="+row_count+" class='form-control form-control-sm' name='dailyentry_set-"+value+"-row'/></td>";

		header_markup += "<td style='text-align:center;''>"+day;
		header_markup += "</td>";

		total_forms ++;
	}
	else{
		markup += "<td> </td>";
		header_markup += "<td style='text-align:center;''> </td>";
	}

}

$(document).on('click', '#save-record', function() {
	var extras ="<tr>"+
				"<td> <input id='dailyentry_set-TOTAL_FORMS' type='hidden' class='form-control form-control-sm' value='"+total_forms+"' name='dailyentry_set-TOTAL_FORMS'/>"+
			    "<input id='dailyentry_set-INITIAL_FORMS' type='hidden' value='0' name='dailyentry_set-INITIAL_FORMS'/>"+
			    "<input id='dailyentry_set-MIN_NUM_FORMS' type='hidden' value='0' name='dailyentry_set-MIN_NUM_FORMS'/>"+
			    "<input id='dailyentry_set-MAX_NUM_FORMS' type='hidden' value='31' name='dailyentry_set-MAX_NUM_FORMS'/></td>"+
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

$(document).on('click', '#save-record', function() {
	$('#timesheet_form').submit();
});

$(document).on('click', '.remove', function() {
	row_count --;
	total_forms -= 7;
	var parent = $(this).parent().parent();  // parent <tr> of the anchor tag
	var previous = parent.prev();        // <tr> before the parent <tr>

	parent.remove();
	previous.remove();
});

 $(document).on('click', '#save-submit-record', function() {
	var extras ="<tr>"+
				"<td> <input id='dailyentry_set-TOTAL_FORMS' type='hidden' class='form-control form-control-sm' value='"+total_forms+"' name='dailyentry_set-TOTAL_FORMS'/>"+
			    "<input id='dailyentry_set-INITIAL_FORMS' type='hidden' value='0' name='dailyentry_set-INITIAL_FORMS'/>"+
			    "<input id='dailyentry_set-MIN_NUM_FORMS' type='hidden' value='0' name='dailyentry_set-MIN_NUM_FORMS'/>"+
			    "<input id='dailyentry_set-MAX_NUM_FORMS' type='hidden' value='31' name='dailyentry_set-MAX_NUM_FORMS'/>"+
				"<input name='save_submit' type='hidden' value='1'/></td>"+
				"</tr>";
	$("table tbody").append(extras);
	$('#timesheet_form').submit();
});

 $(document).on('click', '#approve-record', function() {
	var extras ="<tr> <input name='timesheet_review' type='hidden' value='approved'/></td>"+
				"</tr>";
	$("table tbody").append(extras);
	$('#timesheet_form').submit();
});

 $(document).on('click', '#reject-record', function() {
	var extras ="<tr> <input name='timesheet_review' type='hidden' value='rejected'/></td>"+
				"</tr>";
	$("table tbody").append(extras);
	$('#timesheet_form').submit();
});

 $(document).on('click', '#verify-record', function() {
	var extras ="<tr> <input name='timesheet_review' type='hidden' value='verified'/></td>"+
				"</tr>";
	$("table tbody").append(extras);
	$('#timesheet_form').submit();
});


$(document).on('click', '#auto_fill', function() {

	var cols = (((row_count-1) * 7) + (7-blank_days));

	tableIndex = Array(cols).fill().map((x,i)=>i);

	tableIndex.forEach(function(entry){

		element_id = 'dailyentry_set-'+entry+'-duration';
		document.getElementById(element_id).value = 8;
	});
});

});
