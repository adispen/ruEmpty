// Get the current day of the week and set it as the pre populated option for Day (there are no weekend classes so we set them to Monday).
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

  // On page load we clear the buildings in the Building selector and reset the Campus selector.  This is to prevent invalid queries and force the GET request to fire on switching options for campus.
  $('#building').html("<select type='select' required='' name='building' id='building' class='form-control'><option value='Please choose a campus first'>Please choose a campus first</option></select>");
  $("#campus").val("Please choose a campus");
});

// Detects a change in the Building selector.  When this fires, it checks to make sure that you have anything but the default option selected.  If you, do it will reenable the submit button.
$('#building').change(function () {
  if ($('#building option:selected').text() == 'Please choose a campus first') {
    $('#submitQ').prop('disabled', true);
  } else {
    $('#submitQ').prop('disabled', false);
  }
});

// Detects a change in the campus selector, making sure that you have anything but the default option chosen.  If so it will reenable the submit button.
$('#campus').change(function () {
  if ($('#campus option:selected').text() == 'Please choose a campus') {
    $('#submitQ').prop('disabled', true);
  }
});

// Detect a change in the campus selector.  This fires a GET request which gets the buildings for the chosen campus.
$('#campus').change(function () {

  // Resets the Building selector so that when we change campuses we dont just add to the choices already populated.
  $('#building').html("<select type='select' required='' name='building' id='building' class='form-control'><option value='Please choose a campus first'>Please choose a campus first</option></select>")
  $.get('/_getBuildings', {
    campus: $('#campus option:selected').text()
  }, function(responseArr){

	  // Populates the Building selector with each item from the server response.
	  var numItems = responseArr.buildings.length;
	  for(items in responseArr.buildings){
		  var selForm = document.myForm.building
		  selForm.options[selForm.options.length] = new Option(responseArr.buildings[items], responseArr.buildings[items]);
	  }
  })
});
