$(document).ready(function(){
    $("#add-row").click(function(){
        var task = $("#task").val();
        var markup = "<tr>"+
        				"<td><input type='text' class='form-control form-control-sm' name='tasks[]' value='" + task + "' readonly /></td>"+
        				"<td><input type='time' class='form-control form-control-sm' name='time1[]'></td>"+
        				"<td><input type='time' class='form-control form-control-sm' name='time2[]'></td>"+
        				"<td><input type='time' class='form-control form-control-sm' name='time3[]'></td>"+
        				"<td><input type='time' class='form-control form-control-sm' name='time4[]'></td>"+
        				"<td><input type='time' class='form-control form-control-sm' name='time5[]'></td>"+
        				"<td><input type='time' class='form-control form-control-sm' name='time6[]'></td>"+
        				"<td><input type='time' class='form-control form-control-sm' name='time7[]'></td>"+
        				"<td>0</td>"+
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
