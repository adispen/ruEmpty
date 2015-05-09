//console.log("Hello world");
//console.log($('#building option:selected').text())

$(document).ready( function() {
  switch (new Date().getDay()) {
    case 0:
        day = "Monday";
        break;
    case 1:
        day = "Monday";
        break;
    case 2:
        day = "Tuesday";
        break;
    case 3:
        day = "Wednesday";
        break;
    case 4:
        day = "Thursday";
        break;
    case 5:
        day = "Friday";
        break;
    case 6:
        day = "Monday";
        break;
  }  
  $("#day").val(day);
  $('#building').html("<select type='select' required='' name='building' id='building' class='form-control'><option value='Please choose a campus first'>Please choose a campus first</option></select>");
  $("#campus").val("Please choose a campus");
});

$('#building').change(function () {
  if ($('#building option:selected').text() == 'Please choose a campus first') {
    $('#submitQ').prop('disabled', true);
    //console.log('disabled');
  } else {
    $('#submitQ').prop('disabled', false);
    //console.log('enabled');
  }
  //console.log($('#building option:selected').text())
});
$('#campus').change(function () {
  if ($('#campus option:selected').text() == 'Please choose a campus') {
    $('#submitQ').prop('disabled', true);
    //console.log('disabled');
  }
});

$('#campus').change(function () {
  $('#building').html("<select type='select' required='' name='building' id='building' class='form-control'><option value='Please choose a campus first'>Please choose a campus first</option></select>")
  $.get('/_getBuildings', {
    campus: $('#campus option:selected').text()
  }, function(data){
	  var numItems = data.buildings.length;
	  for(items in data.buildings){
		  var selForm = document.myForm.building
		  selForm.options[selForm.options.length] = new Option(data.buildings[items], data.buildings[items]);
	  }
  })
});
