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



$('button#saveDataset').click(function() {
	console.log($(this).val());
	datasetID = $(this).val();
	var name = $('#datasetName_'+datasetID).val();
	var url = $('#datasetURL_'+datasetID).val();
	var dataTypes = [];
    $('#dataType_'+datasetID).each(function() {
    	dataTypes.push($(this).val());
    });
    var otherDataType = $('#otherDataType_'+datasetID)
    if (otherDataType != '') {
    	dataTypes.push(otherDataType);
    }
    var rating = $('#rating_'+datasetID).val();
    var reason = $('#reason_'+datasetID).val();
    if (name != '' && url != '', dataTypes.length == 0) {
    	$('.saving').fadeIn(200);
		data 
		$.ajax({
			type: 'POST',
			url: '/editData/' + datasetID,
			data: {
					'datasetName': name,
					'datasetURL': url,
					'dataType': dataTypes,
					'rating': rating,
					'reason': reason
				},
			dataType: 'json',
			success: function() {
				$('.saving').hide(200);
				$('.saved').fadeIn(200);
			}
		});
	}
	return false;
});




// 	$("#linkSubmit").click(function() {
// 		var links = $(".links").val();
// 		if (links =='') {
// 			$('.success').fadeOut(200).hide();
// 			$('.error').fadeOut(200).show();
// 		} else {
//       		$('.sending').show();
// 			$.ajax({
// 				type: "POST",
// 				url: "/reporte/agregar/",
// 				data: {'links': links},
// 				success: function(){
// 					$('.sending').hide();
// 			        $('.success').show('slow');
// 			        $('.error').fadeOut(200).hide();
// 			        $(".success").delay(3200).fadeOut(300);
// 					$('.links').val('');
// 				}
// 			});
// 		}
// 		return false;
// 	});
// });