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