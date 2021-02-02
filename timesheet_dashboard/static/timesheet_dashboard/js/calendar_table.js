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

function getISOWeekDates(isoWeekNum = 1, year = new Date().getFullYear()) {
  let d = moment().isoWeek(1).startOf('isoWeek').add(isoWeekNum - 1, 'weeks');
  for (var dates=[], i=0; i < 7; i++) {
    dates.push(d.format('ddd DD MMM YYYY'));
    d.add(1, 'day');
  }
  return dates;
}

console.log(getISOWeekDates())

function getThisWeekDates() {
	var weekDays = [];
	var weekDates= []; 
	var currentDate = moment();
	var weekStart = currentDate.clone().startOf('week');
	var weekEnd = currentDate.clone().endOf('week');

	for (var i = 1; i <= 7; i++) {
		weekDates.push(moment().day(i).format('dd') + '\n' + moment().day(i).format('DD MMM')); 
	}

  return weekDates; 
}

const thisWeekDates = getThisWeekDates();

function createNewTableHeader(headerTitle){
	const temp = document.createElement('th');
	temp.style.textAlign = "center";
	temp.style.color = "#808080";
	temp.appendChild(document.createTextNode(headerTitle));
	return temp
}

function addHeader() {
	var tableHeaderPlaceHolder = document.getElementById('table-header');
	tableHeaderPlaceHolder.appendChild(createNewTableHeader('Project/Task'));
	for (var i=0; i<thisWeekDates.length; i++) {
		tableHeaderPlaceHolder.appendChild(createNewTableHeader(thisWeekDates[i]));
		tableHeaderPlaceHolder.style = "white-space: pre;"	
	}
	tableHeaderPlaceHolder.appendChild(createNewTableHeader('Total'));
	tableHeaderPlaceHolder.appendChild(createNewTableHeader(''));
}

document.addEventListener("DOMContentLoaded", function(event) { 
	addHeader();
});