/*
    Sample script.js JavaScript file

    Author: Mike Dory
    11.12.11, updated 11.24.12
*/


// your fancy JS code goes here!
$("input.otherSector:text").focus(function() {
	$("input.otherSector:checkbox").prop('checked', true);
});
$("input.otherSector:text").focusout(function() {
	if ($("input.otherSector:text").val() == '') {
		$("input.otherSector:checkbox").prop('checked', false);
	}
});

$("input.otherRevenueSource:text").focus(function() {
	$("input.otherRevenueSource:checkbox").prop('checked', true);
});
$("input.otherRevenueSource:text").focusout(function() {
	if ($("input.otherRevenueSource:text").val() == '') {
		$("input.otherRevenueSource:checkbox").prop('checked', false);
	}
});

$("input.otherCriticalDataTypes:text").focus(function() {
	$("input.otherCriticalDataTypes:checkbox").prop('checked', true);
});
$("input.otherCriticalDataTypes:text").focusout(function() {
	if ($("input.otherCriticalDataTypes:text").val() == '') {
		$("input.otherCriticalDataTypes:checkbox").prop('checked', false);
	}
});


$("input#otherCompanyFunction:text").focus(function() {
	$("input[name='companyFunction'][value='Other']").prop('checked', true);
});

$("input#otherCompanyType:text").focus(function() {
	$("input[name='companyType'][value='Other']").prop('checked', true);
});



$('button#saveDataset').click(function(event) {
	$('.error').hide();
	var datasetID = $(this).val();
	console.log(datasetID);
	var datasetName = $('#datasetName_'+datasetID).val();
	var datasetURL = $('#datasetURL_'+datasetID).val();
	var dataTypes = [];
    $('#dataType_'+datasetID+':checked').each(function() {
    	dataTypes.push($(this).val());
    });
    var otherDataType = $('#otherDataType_'+datasetID).val();
    if (otherDataType != '') {
    	dataTypes.push(otherDataType);
    } 
    var rating = $('#rating_'+datasetID).val();
    var reason = $('#reason_'+datasetID).val();
    var authorID = $('#author_'+datasetID).val();
    var data = {
					'datasetName': datasetName,
					'datasetURL': datasetURL,
					'dataTypes': dataTypes.join(),
					'rating': rating,
					'reason': reason,
					'authorID': authorID
				}
    if (datasetName != '' && datasetURL != '' && dataTypes.length > 0) {
    	$('.saving').fadeIn(200);
		$.ajax({
			type: 'POST',
			url: '/editData/' + datasetID,
			data: data,
			error: function(error) {
				console.debug("error is " +JSON.stringify(error));
				console.log("error, bro");
				$('.saving').hide();
				$('.error').fadeIn(200);
			},
			beforeSend: function(xhr, settings) {
				$(event.target).attr('disabled', 'disabled'); },
			success: function() {
				$('.saving').hide(200);
				$('.saved').fadeIn(200);
				$(event.target).removeAttr('disabled');
			}
		});
	}
	$('.error').fadeOut(1000);
	return false;
});

var i =0;
function getDatasetForm(i){
	return '<form id="datasetForm'+i+'" class="m-form" data-validate="parsley">' +
				'<h3>New Dataset</h3>' +
				'<div class="m-form-line"><label for="datasetName">Name of Dataset: *</label><input type="text" name="datasetName" id="datasetName'+i+'" data-required="true"></div>' +
				'<div class="m-form-line"><label for="datasetURL">URL of Dataset: *</label><input type="text" name="datasetURL" id="datasetURL'+i+'" data-required="true" data-trigger="change" data-type="url"></div>'+
				'<div class="m-form-box">Type of Dataset: *<br>'+
					'<label for=""><input type="checkbox" id="dataType'+i+'" name="dataType" data-trigger="change" data-group="typeofdataset" data-mincheck="1" value="Federal Open Data">Federal Open Data</label><br>'+
					'<label for=""><input type="checkbox" id="dataType'+i+'" name="dataType" data-trigger="change" data-group="typeofdataset" data-mincheck="1" value="State Open Data">State Open Data</label><br>'+
					'<label for=""><input type="checkbox" id="dataType'+i+'" name="dataType" data-trigger="change" data-group="typeofdataset" data-mincheck="1" value="City/Local Open Data">City/Local Open Data</label><br>'+
					'<label for=""><input type="checkbox" id="dataType'+i+'" name="dataType" data-trigger="change" data-group="typeofdataset" data-mincheck="1" value="Other">Other</label>'+
					'<label for=""><input type="text" name="otherDataType" id="otherDataType'+i+'"></label>'+
				'</div>'+
				'<p>How would you rate the usefulness of this dataset? Your answer can reflect your experience with data quality, format of the data, or other factors.</p>'+
				'<input type="text" name="rating" id="rating'+i+'">'+
				'<p>Why did you give it this rating? [50 words or less]</p>'+
				'<textarea rows="6" cols="70" name="reason" id="reason'+i+'" data-trigger="keyup" data-maxwords="50"></textarea><br>'+
				'<br>'+
			'</form>';
	}

$('#dataForms').on('addDatasetForm', function() {
	i++;
	newDatasetForm = getDatasetForm(i);
	$('#dataForms').append(newDatasetForm);
	$('#addDatasetForm').hide();
});
$('#addDatasetForm').click(function() {
	$('#dataForms').trigger('addDatasetForm');
})



//Make a new dataset:

$('button#createDataset').click(function(event) {
	console.log('entering function');
	if ($('#datasetForm'+i).parsley( 'validate' )) {
		console.log("working on "+i);
		$('.error').hide();
		var datasetID = $(this).val();
		var datasetName = $('#datasetName'+i).val();
		var datasetURL = $('#datasetURL'+i).val();
		var dataTypes = [];
	    $('#dataType'+i+':checked').each(function() {
	    	dataTypes.push($(this).val());
	    });
	    var otherDataType = $('#otherDataType'+i).val();
	    if (otherDataType != '') {
	    	dataTypes.push(otherDataType);
	    } 
	    var rating = $('#rating'+i).val();
	    var reason = $('#reason'+i).val();
	    var id = $('#companyID').val();
	    var data = {
						'datasetName': datasetName,
						'datasetURL': datasetURL,
						'dataTypes': dataTypes.join(),
						'rating': rating,
						'reason': reason,
					}
	    if (datasetName != '' && datasetURL != '' && dataTypes.length > 0) {
	    	console.log('we have the required info');
	    	$('.saving').fadeIn(200);
			$.ajax({
				type: 'POST',
				url: '/editData/' + id,
				data: data,
				error: function(error) {
					console.debug("error is " +JSON.stringify(error));
					console.log("error, bro");
					$('.saving').hide();
					$('.error').fadeIn(200);
				},
				// beforeSend: function(xhr, settings) {
				// 	$(event.target).attr('disabled', 'disabled'); },
				success: function() {
					$('.saving').hide(200);
					$('.saved').fadeIn(200);
					//$(event.target).removeAttr('disabled');
					$('#addDatasetForm').show();
				}
			});
		}
		$('.error'+i).fadeOut(1000);
		//return false;
	}
});