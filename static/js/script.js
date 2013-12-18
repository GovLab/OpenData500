/*
    Sample script.js JavaScript file

    Author: Mike Dory
    11.12.11, updated 11.24.12
*/








// your fancy JS code goes here!

$(function() {
    $( "#accordionUnvetted" ).accordion({
      collapsible: true
    });
  });

$(function() {
    $( "#accordionVetted" ).accordion({
      collapsible: true
    });
  });

$(function() {
    $( "#accordionSubmitted" ).accordion({
      collapsible: true
    });
  });











// $("input.otherInput").focus(function() {
// 	$("input.otherOption").prop('checked', true);
// });
// $("input.otherInput").focusout(function() {
// 	if ($("input.otherInput").val() == '') {
// 		$("input.otherOption").prop('checked', false);
// 	}
// });



//This messes up Parsley

// $("input.otherSector:text").focus(function() {
// 	$("input.otherSector:checkbox").prop('checked', true);
// });
// $("input.otherSector:text").focusout(function() {
// 	if ($("input.otherSector:text").val() == '') {
// 		$("input.otherSector:checkbox").prop('checked', false);
// 	}
// });

// $("input.otherRevenueSource:text").focus(function() {
// 	$("input.otherRevenueSource:checkbox").prop('checked', true);
// });
// $("input.otherRevenueSource:text").focusout(function() {
// 	if ($("input.otherRevenueSource:text").val() == '') {
// 		$("input.otherRevenueSource:checkbox").prop('checked', false);
// 	}
// });

// $("input.otherCriticalDataTypes:text").focus(function() {
// 	$("input.otherCriticalDataTypes:checkbox").prop('checked', true);
// });
// $("input.otherCriticalDataTypes:text").focusout(function() {
// 	if ($("input.otherCriticalDataTypes:text").val() == '') {
// 		$("input.otherCriticalDataTypes:checkbox").prop('checked', false);
// 	}
// });

// $("input.otherCompanyFunction:text").focus(function() {
// 	$("input.otherCompanyFunction:radio").prop('checked', true);
// });
// $("input.otherCompanyFunction:text").focusout(function() {
// 	if ($("input.otherCompanyFunction:text").val() == '') {
// 		$("input.otherCompanyFunction:radio").prop('checked', false);
// 	}
// });

// $("input.otherCompanyType:text").focus(function() {
// 	$("input.otherCompanyType:radio").prop('checked', true);
// });
// $("input.otherCompanyType:text").focusout(function() {
// 	if ($("input.otherCompanyType:text").val() == '') {
// 		$("input.otherCompanyType:radio").prop('checked', false);
// 	}
// });



// $('button#saveDataset').click(function(event) {
// 	$('.error').hide();
// 	var datasetID = $(this).val();
// 	console.log(datasetID);
// 	var datasetName = $('#datasetName_'+datasetID).val();
// 	var datasetURL = $('#datasetURL_'+datasetID).val();
// 	var dataTypes = [];
//     $('#dataType_'+datasetID+':checked').each(function() {
//     	dataTypes.push($(this).val());
//     });
//     var otherDataType = $('#otherDataType_'+datasetID).val();
//     if (otherDataType != '') {
//     	dataTypes.push(otherDataType);
//     } 
//     var rating = $('#rating_'+datasetID).val();
//     var reason = $('#reason_'+datasetID).val();
//     var authorID = $('#author_'+datasetID).val();
//     var data = {
// 					'datasetName': datasetName,
// 					'datasetURL': datasetURL,
// 					'dataTypes': dataTypes.join(),
// 					'rating': rating,
// 					'reason': reason,
// 					'authorID': authorID
// 				}
//     if (datasetName != '' && datasetURL != '' && dataTypes.length > 0) {
//     	$('.saving').fadeIn(200);
// 		$.ajax({
// 			type: 'POST',
// 			url: '/editData/' + datasetID,
// 			data: data,
// 			error: function(error) {
// 				console.debug("error is " +JSON.stringify(error));
// 				console.log("error, bro");
// 				$('.saving').hide();
// 				$('.error').fadeIn(200);
// 			},
// 			beforeSend: function(xhr, settings) {
// 				$(event.target).attr('disabled', 'disabled'); },
// 			success: function() {
// 				$('.saving').hide(200);
// 				$('.saved').fadeIn(200);
// 				$(event.target).removeAttr('disabled');
// 			}
// 		});
// 	}
// 	$('.error').fadeOut(1000);
// 	return false;
// });


//SECONT ATTEMPT AT DATA FORMS
// var newDatasetForm = '<h3 class="datasetHeader">New Dataset</h3>' +
// 			'<form class="m-form datasetForm" data-validate="parsley">' +
// 				'<div class="m-form-line"><label for="datasetName">Name of Dataset: *</label><input type="text" name="datasetName" data-required="true"></div>' +
// 				'<div class="m-form-line"><label for="datasetURL">URL of Dataset: *</label><input type="text" name="datasetURL" data-required="true" data-trigger="change" data-type="url"></div>'+
// 				'<div class="m-form-box">Type of Dataset: *<br>'+
// 					'<label for=""><input type="checkbox" name="dataType" data-trigger="change" data-group="typeofdataset" data-mincheck="1" value="Federal Open Data">Federal Open Data</label><br>'+
// 					'<label for=""><input type="checkbox" name="dataType" data-trigger="change" data-group="typeofdataset" data-mincheck="1" value="State Open Data">State Open Data</label><br>'+
// 					'<label for=""><input type="checkbox" name="dataType" data-trigger="change" data-group="typeofdataset" data-mincheck="1" value="City/Local Open Data">City/Local Open Data</label><br>'+
// 					'<label for=""><input type="checkbox" name="dataType" data-trigger="change" data-group="typeofdataset" data-mincheck="1" value="Other">Other</label>'+
// 					'<label for=""><input type="text" name="otherDataType"></label>'+
// 				'</div>'+
// 				'<p>How would you rate the usefulness of this dataset? Your answer can reflect your experience with data quality, format of the data, or other factors.</p>'+
// 				'<input type="text" name="rating">'+
// 				'<p>Why did you give it this rating? [50 words or less]</p>'+
// 				'<textarea rows="6" cols="70" name="reason" data-trigger="keyup" data-maxwords="50"></textarea><br>'+
// 				'<br>'+
// 				'<button class="l-button createDataset" type="button">Save</button>' +
// 				'<span class="saving" style="display:none">Saving...</span>' +
// 				'<span class="saved" style="display:none">Saved!</span>' +
// 				'<span class="error" style="display:none">Something went wrong :/</span><br>' +
// 			'</form>';

// $('.data').on('click', '#addDatasetForm', function() {
// 	$('.dataForms').append(newDatasetForm).accordion('destroy').accordion({ collapsible: true });
// })

// //Make a new dataset:

// $('.dataForms').on('click', '.createDataset', function(event) {
// 	//console.log($(this).parent().find('.datasetForm').first());
// 	//if ($(this).parent().find('.datasetForm').parsley( 'validate' )) {
// 		var currentForm = $(this).parent();
// 		console.log($(this).parent().parent());
// 		$(this).parent().parent().find('.datasetHeader').text(currentForm.find('[name="datasetName"]').val());
// 		currentForm.find('.error').hide();
// 		var id = $('#companyID').val();
// 		$.ajax({
// 					type: 'POST',
// 					url: '/editData/' + id,
// 					data: $(this).parent().serializeArray(),
// 					error: function(error) {
// 						console.debug(JSON.stringify(error));
// 						currentForm.find('.saving').hide();
// 						currentForm.find('.error').fadeIn();
// 					},
// 					beforeSend: function(xhr, settings) {
// 						$(event.target).attr('disabled', 'disabled'); },
// 					success: function() {
// 						currentForm.find('.saving').hide();
// 						currentForm.find('.saved').fadeIn().delay(5000).fadeOut();
// 						$(event.target).removeAttr('disabled');
// 						//$('#addDatasetForm').show();
// 					}
// 				});
// 		return false;
// 	//}
// });






//Istopes
// init Isotope
// var $container = $('.isotopes-container').isotope({
// 	layoutMode: 'masonry',
// 	resizesContainer : false,
// });
// // filter items on button click
// $('#filters').on( 'click', 'button', function( event ) {
//   var filtr = $(this).attr('data-filter');
//   $container.isotope({ filter: filtr });
// });

// $('.states').on('click', 'path', function(event) {
// 	var filtr = $(this).attr('class').split(' ')[1];
// 	//$container.isotope({ filter: filtr });
// 	console.log(filtr);
// });

// $container.delegate( '.m-candidates-item', 'click', function(){
//         $(this).toggleClass('large');
//         $container.isotope();
// });





