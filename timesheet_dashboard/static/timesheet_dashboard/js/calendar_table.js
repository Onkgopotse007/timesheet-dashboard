$(document).ready(function(){
    $("#add-row").click(function(){
        var task = $("#task").val();
        var day_count = $("#day_count").val()

        var markup = "<tr>"+
        				"<td> <input id='tasks' type='text' class='form-control form-control-sm' name='tasks' value='" + task + "' readonly /></td>"+
        				"<td> <input id='dailyentry_set-'+(day_count)+-duration' type='number' class='form-control form-control-sm' name='dailyentry_set-0-duration'/> </td>"+
        				"<td> <input id='dailyentry_set-'+(day_count+1)+'-duration' type='number' class='form-control form-control-sm' name='dailyentry_set-1-duration'/></td>"+
        				"<td> <input id='dailyentry_set-'+(day_count+2)+'-duration' type='number' class='form-control form-control-sm' name='dailyentry_set-2-duration'/></td>"+
        				"<td> <input id='dailyentry_set-'+(day_count+3)+'-duration' type='number' class='form-control form-control-sm' name='dailyentry_set-3-duration'/></td>"+
        				"<td> <input id='dailyentry_set-'+(day_count+4)+'-duration' type='number' class='form-control form-control-sm' name='dailyentry_set-4-duration'/></td>"+
        				"<td> <input id='dailyentry_set-'+(day_count+5)+'-duration' type='number' class='form-control form-control-sm' name='dailyentry_set-5-duration'/></td>"+
        				"<td> <input id='dailyentry_set-'+(day_count+6)+'-duration' type='number' class='form-control form-control-sm' name='dailyentry_set-6-duration'/></td>"+
        				"<td> <input id='dailyentry_set-TOTAL_FORMS' type='hidden' class='form-control form-control-sm' value='7' name='dailyentry_set-TOTAL_FORMS'/> </td>"+
		                "<td> <input id='dailyentry_set-INITIAL_FORMS' type='hidden' value='0' name='dailyentry_set-INITIAL_FORMS'/></td>"+
		                "<td> <input id='dailyentry_set-MIN_NUM_FORMS' type='hidden' value='0' name='dailyentry_set-MIN_NUM_FORMS'/> </td>"+
		                "<td> <input id='dailyentry_set-MAX_NUM_FORMS' type='hidden' value='31' name='dailyentry_set-MAX_NUM_FORMS'/></td>"+
        				"<td>0</td>"+
        				"<td></td>"+
        				"<td><a class='btn btn-default btn-sm remove'><i class='glyphicon glyphicon-remove'></i></a></td>"
        				"</tr>";
        $("table tbody").append(markup);
        $("#addModal").modal('hide');
    });
    
});

$(document).on('click', '.remove', function() {
	var trIndex = $(this).closest("tr").index();
   	$(this).closest("tr").remove();
});

$(document).on('click', '#nextWeek', function() {
	$('#controlForm').submit();
});

$('#controlForm').on('submit', function (e) {
 e.preventDefault();
 var url = nextWeek();
console.log(url);
 $.ajax({
 		url: url,
      type: "POST",
      data: $('form').serialize(),
      success : function(json) {
        alert("Successfully sent the URL to Django");
      },
      error : function(xhr,errmsg,err) {
        alert("Could not send URL to Django. Error: " + xhr.status + ": " + xhr.responseText);
      }
	});
});

function nextWeek(){
	var js_variable = JSON.parse(document.getElementById('currDate').textContent);
	var date = new Date(js_variable);
	var nextWeekStart = date.getDate() - date.getDay() + 8;
	var nextWeekFrom = new Date(date.setDate(nextWeekStart));
	
    var id = JSON.parse(document.getElementById('employee_id').textContent);
    return "{% url 'timesheet_dashboard:timesheet_calendar_table_url' 123 %}".replace('123', id) + "/" + convertDate(nextWeekFrom);
}

Date.prototype.getNextWeekDay = function(d) {
  if (d) {
    var next = this;
    next.setDate(this.getDate() - this.getDay() + 7 + d);
    return next;
  }
}

function convertDate(inputFormat) {
  function pad(s) { return (s < 10) ? '0' + s : s; }
  var d = new Date(inputFormat)
  return [d.getFullYear(), pad(d.getMonth()+1), pad(d.getDate())].join('/')
}
