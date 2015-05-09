console.log("Hello world");
console.log($('#building option:selected').text())
$('#building').change(function () {
  if ($('#building option:selected').text() == 'Please choose a campus first') {
    $('#submitQ').prop('disabled', true);
    console.log('disabled');
  } else {
    $('#submitQ').prop('disabled', false);
    console.log('enabled');
  }
  console.log($('#building option:selected').text())
});
$('#campus').change(function () {
  if ($('#campus option:selected').text() == 'Please choose a campus') {
    $('#submitQ').prop('disabled', true);
    console.log('disabled');
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