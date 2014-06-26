$(document).ready(function() {

    var is_chrome = navigator.userAgent.toLowerCase().indexOf('chrome') > -1;
    var is_firefox = navigator.userAgent.toLowerCase().indexOf('firefox') > -1;
    //----------------------------------ADMIN ACCORDIONS--------------------------------------
    $(function() {
        $("#accordionUnvetted").accordion({
            collapsible: true,
            autoHeight: false
        });
    });

    $(function() {
        $("#accordionVetted").accordion({
            collapsible: true
        });
    });

    $(function() {
        $("#accordionSubmitted").accordion({
            collapsible: true,
            autoHeight: false
        });
    });

    var companyID = $('.companyID').val();
    //----------------------------------UNCHECK OTHER BOX IF INPUT EMPTY--------------------------------------
    $('.m-form-half').on('focusout', '#otherRevenueSource', function(event) {
        if ($('#otherRevenueSource').val() == '') {
            $('input[name="revenueSource"][value="Other"').prop('checked', false);
        }
    });
    $('.m-form-half').on('focus', '#otherRevenueSource', function() {
        $('input[name="revenueSource"][value="Other"').prop('checked', true);
    });
    $('.m-form-half').on('focus', '#otherCategory', function() {
        $('input[name="category"][value="Other"').prop('checked', true);
    });
    $('.m-form-half').on('focusout', '#otherCategory', function() {
        if ($('#otherCategory').val() == '') {
            $('input[name="category"][value="Other"').prop('checked', false);
        }
    });

    //----------------------------------EXAMPLE POPUP--------------------------------------
    var dialogOptions = {
        autoOpen: false,
        height: 560,
        width: 730,
        modal: true,
        //close: function(event, ui) { $('.example-popup').dialog('close'); },
        open: function(event, ui) {
            $('.ui-widget-overlay').bind('click', function() {
                $(this).siblings('.ui-dialog').find('.ui-dialog-content').dialog('close');
            });
        }
    };
    $(".m-form-box").on('click', '.example-popup', function() {
        $(".dialog-example").dialog(dialogOptions).dialog("open");
        //$("#dialog").dialog({autoOpen : false, modal : true, show : "blind", hide : "blind"});
    });

    //----------------------------------DATA ACCORDIONS--------------------------------------
    $("#accordionAgency, #accordionSubAgency").accordion({
        active: false,
        collapsible: true,
        autoHeight: false,
        heightStyle: "content"
    });
    //----------------------------------DELETE AGENCIES AND SUBAGENCIES--------------------------------------
    $('#accordionAgency, #accordionSubAgency').on('click', '.toolbar', function(event) {
        agency = $(this).attr('agency').replace("delete", "").replace(/-/g, " ");
        a_id = $(this).attr('a_id');
        subagency = $(this).attr('subagency').replace("delete", "").replace(/-/g, " ");
        //console.log(agency + subagency);
        data = {
            "agency": agency,
            "subagency": subagency,
            "a_id": a_id,
            "action": "delete agency",
            "_xsrf": $("[name='_xsrf']").val()
        };
        //console.log($(this).closest('h3'));
        $(this).parent().next().remove();
        $(this).closest('h3').remove();
        if (subagency == '') {
            $("#accordionAgency").accordion({
                active: false,
                collapsible: true,
                autoHeight: false,
                heightStyle: "content"
            });
        } else {
            $("#accordionSubAgency").accordion({
                active: false,
                collapsible: true,
                autoHeight: false,
                heightStyle: "content"
            });
        }
        $.ajax({
            type: 'POST',
            url: '/addData/' + companyID,
            data: data,
            error: function(error) {
                console.debug(JSON.stringify(error));
                $('.savingMessage_companyEdit').hide();
                $('.errorMessage_companyEdit').show();
            },
            beforeSend: function(xhr, settings) {
                $(event.target).attr('disabled', 'disabled');
            },
            success: function(success) {
                $('.toolbar').removeAttr('disabled');
                console.log(success);
            }
        });
    });
    //----------------------------------SAVE NEW DATASET AND ADD NEW EMPTY FORM--------------------------------------
    $('.agencyList').on('click', '#saveDataset', function(event) {
        currentDatasetForm = $(this).parent().parent();
        //--CHECK IF EDITING OR SAVING NEW DATASET--
        if (currentDatasetForm.parent().find('tr').last().find('#datasetName').val() == '') {
            //console.log("editing!");
            action = "edit dataset";
            previousDatasetName = currentDatasetForm.attr('name');
        } else {
            //console.log('saving new!');
            action = "add dataset";
            previousDatasetName = '';
        }
        datasetName = currentDatasetForm.find('#datasetName').val();
        datasetURL = currentDatasetForm.find('#datasetURL').val();
        rating = currentDatasetForm.find('#rating').val();
        agency = currentDatasetForm.attr('agency').replace(/-/g, " ");
        subagency = currentDatasetForm.attr('subagency').replace(/-/g, " ");
        var datasetForm = '<tr class="dataset-row" name="" subagency="' + subagency.replace(/ /g, "-") + '" agency="' + agency.replace(/ /g, "-") + '">' +
            '<td><input type="text" name="datasetName" id="datasetName" value=""></td>' +
            '<td><input type="text" name="datasetURL" id="datasetURL" value=""></td>' +
            '<td><input type="text" name="rating" id="rating" size="3" value=""></td>' +
            '<td><input type="button" class="l-button" id="saveDataset" value="Save"><input type="button" class="l-button" id="deleteDataset" value="Delete" style="display:none">' +
            '<span class="error-dataset" style="display:none"></span>' +
            '<span class="message-dataset" style="display:none"></span></td>' +
            '</tr>';
        data = {
            "agency": agency,
            "subagency": subagency,
            "datasetName": datasetName,
            "previousDatasetName": previousDatasetName,
            "datasetURL": datasetURL,
            "rating": rating,
            "action": action,
            "_xsrf": $("[name='_xsrf']").val()
        }
        var validForm = true;
        if (datasetName == '') {
            validForm = false;
            currentDatasetForm.find('.message-dataset').hide();
            currentDatasetForm.find('.error-dataset').text('Dataset name required')
            currentDatasetForm.find('.error-dataset').show().delay(5000).fadeOut();
        } else if (!validURL(datasetURL) && datasetURL != '') {
            validForm = false;
            currentDatasetForm.find('.message-dataset').hide();
            currentDatasetForm.find('.error-dataset').text('Invalid URL')
            currentDatasetForm.find('.error-dataset').show().delay(5000).fadeOut();
        } else if (isNaN(rating) || rating > 4 || (rating != '' && rating < 1)) {
            validForm = false;
            currentDatasetForm.find('.message-dataset').hide();
            currentDatasetForm.find('.error-dataset').text('Invalid Rating')
            currentDatasetForm.find('.error-dataset').show().delay(5000).fadeOut();
        }
        if (validForm) {
            currentDatasetForm.find('.error-dataset').hide();
            $.ajax({
                type: 'POST',
                url: '/addData/' + companyID,
                data: data,
                error: function(error) {
                    console.debug(JSON.stringify(error));
                    currentDatasetForm.find('.message-dataset').hide();
                    currentDatasetForm.find('.error-dataset').text('Oops... Server Error :/');
                    currentDatasetForm.find('.error-dataset').show().delay(5000).fadeOut();
                },
                beforeSend: function(xhr, settings) {
                    //$(event.target).attr('disabled', "true"); 
                    currentDatasetForm.find('.error-dataset').hide();
                    currentDatasetForm.find('.message-dataset').text('Saving...');
                    currentDatasetForm.find('.message-dataset').show().delay(5000).fadeOut();
                },
                success: function(success) {
                    //$(event.target).removeAttr('disabled');
                    currentDatasetForm.find('.error-dataset').hide();
                    currentDatasetForm.find('.message-dataset').text('Saved!');
                    currentDatasetForm.find('.message-dataset').show().delay(5000).fadeOut();
                    if (action == "add dataset") {
                        currentDatasetForm.attr('name', datasetName);
                        currentDatasetForm.parent().append(datasetForm);
                        currentDatasetForm.next().find('#datasetName').focus();
                        currentDatasetForm.find('#deleteDataset').show();
                    } else {
                        //--EDITING, CHANGE ALL ATTRIBUTES--
                        currentDatasetForm.attr('name', datasetName);
                    }
                    console.log(success);
                }
            });
        }
    });
    //----------------------------------DELETE DATASET--------------------------------------
    $('.agencyList').on('click', '#deleteDataset', function(event) {
        currentDatasetForm = $(this).parent().parent();
        datasetName = currentDatasetForm.find('#datasetName').val();
        agency = currentDatasetForm.attr('agency').replace(/-/g, " ");
        subagency = currentDatasetForm.attr('subagency').replace(/-/g, " ");
        data = {
            "agency": agency,
            "subagency": subagency,
            "datasetName": datasetName,
            "action": "delete dataset",
            "_xsrf": $("[name='_xsrf']").val()
        };
        if (datasetName != '') {
            $.ajax({
                type: 'POST',
                url: '/addData/' + companyID,
                data: data,
                error: function(error) {
                    console.debug(JSON.stringify(error));
                    currentDatasetForm.find('.error-dataset').text('Oops... Server Error :/');
                    currentDatasetForm.find('.error-dataset').show().delay(5000).fadeOut();
                },
                beforeSend: function(xhr, settings) {
                    //$(event.target).attr('disabled', "true"); 
                    currentDatasetForm.find('.error-dataset').hide();
                },
                success: function(success) {
                    //$(event.target).removeAttr('disabled');
                    currentDatasetForm.find('.error-dataset').hide();
                    currentDatasetForm.remove();
                    console.log(success);
                }
            });
        }
    });
    //----------------------------------ADD AGENCY FROM SEARCH BAR--------------------------------------
    $('body').on('click', '#addSearchResult', function(event) {
        //console.log("clicked to add");
        a = $('#searchval').val().trim().split(" - ");
        if (a == 0) {
            $('.invalidInput').show().delay(5000).fadeOut();
        } else {
            agency = a[0];
            if (a[1] != undefined) {
                subagency = a[1];
            } else {
                subagency = '';
            }
            data = {
                "agency": agency,
                "subagency": subagency,
                "action": "add agency",
                "_xsrf": $("[name='_xsrf']").val()
            };
            var safeToAdd = false;
            var newAgency = '<h3 class="agency" name="' + agency.replace(/ /g, "-") + '"><a href="#">' + agency + '</a>' +
                '<span style="float:right; display:none;" class="toolbar ui-corner-all ui-icon ui-icon-circle-close red" subagency="" agency="' + agency.replace(/ /g, "-") + '"></span>' +
                '</h3>' +
                '<div id="' + agency.replace(/ /g, "-") + 'Accordion">' +
                '<br><h3>Agency Level Datasets</h3><br>' +
                '<table class="datasetTable">' +
                '<tr>' +
                '<th class="table-header-name">Dataset Name</th>' +
                '<th class="table-header-url">Dataset URL</th>' +
                '<th class="table-header-rating">Rating (1-4)</th>' +
                '<th class="table-header-buttons"></th>' +
                '</tr>' +
                '<tr class="dataset-row" subagency="" agency="' + agency.replace(/ /g, "-") + '">' +
                '<td><input type="text" name="datasetName" id="datasetName" value=""></td>' +
                '<td><input type="text" name="datasetURL" id="datasetURL" value=""></td>' +
                '<td><input type="text" name="rating" id="rating" size="3" value=""></td>' +
                '<td><input type="button" class="l-button" id="saveDataset" value="Save"><input type="button" class="l-button" id="deleteDataset" value="Delete" style="display:none">' +
                '<span class="error-dataset" style="display:none"></span>' +
                '<span class="message-dataset" style="display:none"></span></td>' +
                '</tr>' +
                '</table>' +
                '</div>';
            var newSubagency = '<h3 class="subagency" name="' + subagency.replace(/ /g, "-") + '"><a href="#">' + subagency + '</a>' +
                '<span style="float:right; display:none;" class="toolbar ui-corner-all ui-icon ui-icon-circle-close red" subagency="' + subagency.replace(/ /g, "-") + '" agency="' + agency.replace(/ /g, "-") + '"></span>' +
                '</h3>' +
                '<div class="' + subagency.replace(/ /g, "-") + 'Accordion">' +
                '<table class="subagencyDatasetTable">' +
                '<tr>' +
                '<th class="table-header-name">Dataset Name</th>' +
                '<th class="table-header-url">Dataset URL</th>' +
                '<th class="table-header-rating">Rating (1-4)</th>' +
                '<th class="table-header-buttons"></th>' +
                '</tr>' +
                '<tr class="dataset-row" subagency="' + subagency.replace(/ /g, "-") + '" agency="' + agency.replace(/ /g, "-") + '">' +
                '<td><input type="text" name="datasetName" id="datasetName" value=""></td>' +
                '<td><input type="text" name="datasetURL" id="datasetURL" value=""></td>' +
                '<td><input type="text" name="rating" id="rating" size="3" value=""></td>' +
                '<td><input type="button" class="l-button" id="saveDataset" value="Save"><input type="button" class="l-button" id="deleteDataset" value="Delete" style="display:none">' +
                '<span class="error-dataset" style="display:none"></span>' +
                '<span class="message-dataset" style="display:none"></span></td>' +
                '</tr>' +
                '</table>' +
                '</div>';
            if ($('.agency').find('*:contains("' + agency + '")').parent().length != 0) {
                //--AGENCY ALREADY EXISTS, JUST ADD SUBAGENCY--
                if (a[1] == undefined) {
                    //no subagency, and agency already exists, nothing to add. Display error, or just go to that agency/subagency
                    $('.agenciesExist').show().delay(5000).fadeOut();
                    safeToAdd = false;
                } else {
                    // --THERE IS A SUBAGENCY TO ADD, CHECK TO SEE IF ALREADY THERE FIRST:
                    if ($('#' + agency.replace(/ /g, "-") + 'Accordion').find('*:contains("' + subagency + '")').length != 0) {
                        //subagency exists, show error. 
                        $('.agenciesExist').show().delay(5000).fadeOut();
                        safeToAdd = false;
                    } else {
                        //--ADD SUBAGENCY-----IS THIS THE FIRST ONE?----
                        if ($('#' + agency.replace(/ /g, "-") + 'Accordion').find('#accordionSubAgency').length == 0) {
                            //first time adding a subagency, add header. 
                            //console.log("First time adding a subagency");
                            $('#' + agency.replace(/ /g, "-") + 'Accordion').append('<br><h3>Sub-Agencies</h3><br>');
                            $('#' + agency.replace(/ /g, "-") + 'Accordion').append('<div id="accordionSubAgency" class="' + agency.replace(/ /g, "-") + 'Subagencies">');
                            $('#' + agency.replace(/ /g, "-") + 'Accordion').find('#accordionSubAgency').append(newSubagency).accordion({
                                active: false,
                                collapsible: true,
                                autoHeight: false,
                                heightStyle: "content"
                            });
                            safeToAdd = true;
                        } else {
                            //--ADD SUBAGENCY-----NOT THE FIRST ONE, APPEND TO ACCORDION----
                            console.log("adding subagency");
                            $('.' + agency.replace(/ /g, "-") + 'Subagencies').append(newSubagency).accordion('destroy').accordion({
                                active: false,
                                collapsible: true,
                                autoHeight: false,
                                heightStyle: "content"
                            });
                            safeToAdd = true;
                        }
                    }
                }
            } else {
                //--ADD BOTH AGENCY AND SUBAGENCY TO ACCORDION--
                if (a[1] == undefined) { //no subagency, just add agency
                    $('#accordionAgency').append(newAgency).accordion('destroy').accordion({
                        active: false,
                        collapsible: true,
                        autoHeight: false,
                        heightStyle: "content"
                    });
                    safeToAdd = true;
                } else { //---FIRST ADD THE AGENCY TO THE ACCORDION--
                    $('#accordionAgency').append(newAgency).accordion('destroy').accordion({
                        active: false,
                        collapsible: true,
                        autoHeight: false,
                        heightStyle: "content"
                    });
                    $('#' + agency.replace(/ /g, "-") + 'Accordion').append('<br><h3>Sub-Agencies</h3><br>');
                    $('#' + agency.replace(/ /g, "-") + 'Accordion').append('<div id="accordionSubAgency" class="' + agency.replace(/ /g, "-") + 'Subagencies">');
                    $('#' + agency.replace(/ /g, "-") + 'Accordion').find('#accordionSubAgency').append(newSubagency).accordion({
                        active: false,
                        collapsible: true,
                        autoHeight: false,
                        heightStyle: "content"
                    });
                    safeToAdd = true;
                }
            }
            //---SAVE ADDED AGENCIES TO COMPANY---
            if (safeToAdd) {
                $.ajax({
                    type: 'POST',
                    url: '/addData/' + companyID,
                    data: data,
                    error: function(error) {
                        console.debug(JSON.stringify(error));
                        $('.savingMessage_companyEdit').hide();
                        $('.errorMessage_companyEdit').show();
                    },
                    beforeSend: function(xhr, settings) {
                        $(event.target).attr('disabled', 'disabled');
                    },
                    success: function(success) {
                        $('#addSearchResult').removeAttr('disabled');
                        $('#agencyTags').val('');
                        console.log(success);
                    }
                });
            }
        }
    });

    //----------------------------------SHOW DELETE ICONS ON HOVER--------------------------------------
    $('#accordionAgency, #accordionSubAgency').on({
        mouseenter: function() {
            $(this).find('.toolbar').show();
        },
        mouseleave: function() {
            $(this).find('.toolbar').hide();
        }
    }, '.agency, .subagency');
    //----------------------------------SUBMIT DATASET QUESTION--------------------------------------
    $('.finish-data-submit').on('click', '.data-submit-button', function(event) {
        if ($('.data-comment-form').parsley('validate')) {
            if ($(".agency").length > 0) {
                var companyID = $('.companyID').val();
                //console.log(companyID);
                var data = {
                    "dataComments": $('#dataComments').val(),
                    "action": "dataComments",
                    "_xsrf": $("[name='_xsrf']").val()
                };
                $.ajax({
                    type: 'POST',
                    url: '/addData/' + companyID,
                    data: data,
                    error: function(error) {
                        console.debug(JSON.stringify(error));
                    },
                    beforeSend: function(xhr, settings) {
                        $(event.target).attr('disabled', 'disabled');
                    },
                    success: function(success) {
                        console.log(success);
                        document.location.href = '/thanks/';
                    }
                });
            } else {
                console.log("Must enter at least one data source.")
                $(".noInput").show().delay(5000).fadeOut();
            }
        } else {
            console.log("form not valid");
        }
    })

    //----------------------------------SUBMIT FORM--------------------------------------
    $('.submitCompanyForm').on('click', '#companySubmit', function(event) {
        console.log($('#dataComments').parsley('validate'));
        //weird parsley thing evaluates empty field to null.
        if ($('.companyForm').parsley('validate') && ($('#dataComments').parsley('validate') || $('#dataComments').parsley('validate') == null)) {
            console.log('valid');
            $('.savingMessage_companyEdit').show();
            var companyID = $('.companyID').val();
            var data = $('.companyForm').serializeArray();
            data.push({
                "name": "dataComments",
                "value": $('#dataComments').val()
            });
            //console.log(data);
            $.ajax({
                type: 'POST',
                url: '/edit/' + companyID,
                data: data,
                error: function(error) {
                    console.debug(JSON.stringify(error));
                    $('.savingMessage_companyEdit').hide();
                    $('.errorMessage_companyEdit').show().delay(5000).fadeOut();
                },
                beforeSend: function(xhr, settings) {
                    $(event.target).attr('disabled', 'disabled');
                },
                success: function(success) {
                    console.log(success);
                    $('.savingMessage_companyEdit').hide();
                    $('.savedMessage_companyEdit').show();
                    document.location.href = '/thanks/';
                }
            });
        } else {
            $('.savingMessage_companyEdit').hide();
            $('.errorMessage_companyEdit').show().delay(5000).fadeOut();
            //console.log('not valid');
        }
    });
    //----------------------------------SAVE FORM--------------------------------------
    $('.saveCompanyForm').on('click', '#companySave', function(event) {
        if ($('.companyForm').parsley('validate')) {
            console.log('valid');
            $('.message-form').text('Saving...');
            // $('.message-form').show();
            var companyID = $('.companyID').val();
            var data = $('.companyForm').serializeArray();
            $.ajax({
                type: 'POST',
                url: '/edit/' + companyID,
                data: data,
                error: function(error) {
                    console.debug(JSON.stringify(error));
                    $('.message-form');
                    $('.error-form').text('Oops... Something went wrong :/')
                    $('.error-form').show().delay(5000).fadeOut();
                },
                beforeSend: function(xhr, settings) {
                    //$(event.target).attr('disabled', 'disabled'); 
                },
                success: function(success) {
                    //console.log(success);
                    $('.error-form').hide();
                    $('.message-form').text('Saved!')
                    $('.message-form').show().delay(5000).fadeOut();
                    console.log("regular saved!");
                }
            });
        } else {
            $('.savingMessage_companyEdit').hide();
            $('.error-form').show().delay(5000).fadeOut();
            //console.log('not valid');
        }
    });

    //----------------------------------SAVE FORM NEW COMPANY--------------------------------------
    var dataForm = '<br><br><h2>Agency and Data Information</h2><br>' +
        '<div class="m-form-box data">' +
        '<h3>Please tell us more about the data your company uses. First tell us which agencies and/or subagencies provide the data your company uses. Then, optionally, tell us specifically which datasets from those agencies/subagencies does your company use. Use the search bar to find agencies and subagencies and select from the list provided.</h3><br>' +
        '<div class="ui-widget">' +
        '<label for="tags">Agency/Sub-agency Search: </label>' +
        '<input id="agencyTags" value="">' +
        '<input type="hidden" id="searchval" />' +
        '<input type="button" class="l-button" id="addSearchResult" value="Add Agency/Sub-Agency">' +
        '<div class="errors-search">' +
        '<span class="agenciesExist error-agency-search" style="display:none">Agency or Sub-Agency already on list.</span>' +
        '<span class="emptyInput error-agency-search" style="display:none">Nothing to add.</span>' +
        '<span class="invalidInput error-agency-search" style="display:none">Please select an item from the provided list.</span>' +
        '</div>' +
        '</div>' +
        '<div class="agencyList">' +
        '<div id="accordionAgency">' +
        '</div><br>' +
        '</div>' +
        '</div>';
    var submitFormHTML = '<h2 class="disclaimer-text">Are you ready to submit this information? You will not be able to come back to this form afterwards. If you wish to make more changes, you will need to contact <a href="mailto:opendata500@thegovlab.org">opendata500@thegovlab.org</a></h2>' +
        '<div class="submitCompanyForm">' +
        '<input type="hidden" class="companyID" name="companyID" value="{{ id }}">' +
        '<input type="button" class="l-button" id="companySubmit" name="submit" value="Save and Finish">' +
        '<span class="message-form" style="display:none"></span>' +
        '<span class="error-form" style="display:none"></span>' +
        '</div>';
    $('body').on('click', '#companySave-new', function(event) {
        if ($('.companyForm').parsley('validate')) {
            console.log('valid');
            $('.message-form').text('Saving...');
            $('.message-form').show();
            //var companyID = $('.companyID').val();
            var data = $('.companyForm').serializeArray();
            $.ajax({
                type: 'POST',
                url: '/submitCompany/',
                data: data,
                error: function(error) {
                    console.debug(JSON.stringify(error));
                    $('.message-form').hide();
                    $('.error-form').text('Oops... Something went wrong :/')
                    $('.error-form').show().delay(5000).fadeOut();
                },
                beforeSend: function(xhr, settings) {
                    //$(event.target).attr('disabled', 'disabled'); 
                },
                success: function(data) {
                    document.location.href = '/addData/' + data['id'];
                    //console.log(success);
                    // $('.error-form').hide();
                    // $('.message-form').text('Saved!')
                    // $('.message-form').show().delay(5000).fadeOut();
                    // //------APPEND DATASET AND AGENCY FORMS---------
                    // $('.companyID').val(data['id']);
                    // $('.submit-data-information').slideDown().append(dataForm);
                    // $('.saveCompanyForm-new').attr('class', 'saveCompanyForm');
                    // $('.companySave-new').attr('id', 'companySave');
                    // $(submitFormHTML).insertAfter('.submit-data-information');
                    // $( "#agencyTags" ).autocomplete({
                    //   minLength: 2,
                    //   source: agencies,
                    //   select: function(event, ui) { 
                    //     $("#searchval").val(ui.item.value); 
                    //   }
                    // });
                    //   $( "#accordionAgency" ).accordion({
                    //     active: false,
                    //     collapsible: true,
                    //     autoHeight: false,
                    //     heightStyle: "content"
                    //   });
                    // console.log("new company added!");
                }
            });
        } else {
            $('.savingMessage_companyEdit').hide();
            $('.error-form').show().delay(5000).fadeOut();
            //console.log('not valid');
        }
    });

    function clearForm() {
        $('.dataForm')[0].reset();
        $('.dataForm input:checkbox').removeAttr('checked');
        $('#datasetID').val('');
        $('#action').val('');
    }

    function validURL(url) {
        var re = /^((https?|s?ftp|git):\/\/)?(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i;
        var r = new RegExp(re);
        if (r.test(url)) {
            return true;
        } else {
            return false;
        }
    }

    function validateForm(form) {
        var pass = true;
        var a = $("input[name='datasetName']", form).val();
        var b = $("input[name='datasetURL']", form).val();
        var re = /^(https?|s?ftp|git):\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i;
        var r = new RegExp(re);
        var c = $("input[name='agency']", form).val();
        var typeOfDataset = []
        $("input[name='typeOfDataset']", form).each(function() {
            if (this.checked) {
                typeOfDataset.push($(this).val());
            }
        });
        var d = $("input[name='otherTypeOfDataset']", form).val();
        var e = $("input[name='rating']", form).val();
        var f = $("input[name='reason']", form).val();
        if (a == '') {
            pass = false;
        } //need a name for dataset
        if (!r.test(b)) {
            pass = false;
        } //need valid URL
        if (c == '') {
            pass = false;
        } // need agency
        if (!$.inArray('Other', typeOfDataset) > -1) {
            if (d == '') {
                pass = false;
            }
        } //need to enter 'other' if other checked
        if (typeOfDataset.length == 0) {
            pass = false;
        } //at least 1 value
        if (!isNaN(e)) {
            pass = false;
        } //needs to be a number
        return pass;
    }
    //----------------------------------AUTCOMPLETE SEARCH BAR--------------------------------------
    $.getJSON("/static/files/us_Agency_List.json", function(agencies) {
        //console.log(agencies);
        try {
            $("#agencyTags").autocomplete({
                minLength: 2,
                source: agencies,
                focus: function(event, ui) {
                    if (ui.item.s == '') {
                        $('#agencyTags').val(ui.item.a);
                    } else {
                        $('#agencyTags').val(ui.item.a + " - " + ui.item.s);
                    }
                    return false;
                },
                select: function(event, ui) {
                    if (ui.item.s == '') {
                        $("#searchval").val(ui.item.a);
                        $("#agencyTags").val(ui.item.a);
                    } else {
                        $("#searchval").val(ui.item.a + ' - ' + ui.item.s);
                        $("#agencyTags").val(ui.item.a + ' - ' + ui.item.s);
                    }
                    return false;
                }
            }).data("ui-autocomplete")._renderItem = function(ul, item) {
                if (item.s == '') {
                    return $("<li></li>")
                        .data("ui-autocomplete-item", item)
                        .append("<a>" + item.a + "</a>")
                        .appendTo(ul);
                } else {
                    return $("<li></li>")
                        .data("ui-autocomplete-item", item)
                        .append("<a>" + item.a + " - " + item.s + "</a>")
                        .appendTo(ul);
                }
            };
        } catch (err) {
            console.log(err.message);
        }
    });
    // var agencies = [{
    //     "label": "Administrative Office of the United States Courts (AO)",
    //     "a": "Administrative Office of the United States Courts",
    //     "aa": "AO",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Alabama (AL)",
    //     "a": "Alabama",
    //     "aa": "AL",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Alabama (AL)",
    //     "a": "Alabama",
    //     "aa": "AL",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Alaska (AK)",
    //     "a": "Alaska",
    //     "aa": "AK",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Albuquerque (ABQ)",
    //     "a": "Albuquerque",
    //     "aa": "ABQ",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Ann Arbor (AA)",
    //     "a": "Ann Arbor",
    //     "aa": "AA",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Arctic Landscape Conservation Cooperative (ALCC)",
    //     "a": "Arctic Landscape Conservation Cooperative",
    //     "aa": "ALCC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Arizona (AZ)",
    //     "a": "Arizona",
    //     "aa": "AZ",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Arizona (AZ) - Arizona Geological Survey (AZGS)",
    //     "a": "Arizona",
    //     "aa": "AZ",
    //     "s": "Arizona Geological Survey",
    //     "sa": "AZGS"
    // }, {
    //     "label": "Arkansas (AR)",
    //     "a": "Arkansas",
    //     "aa": "AR",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Arvada",
    //     "a": "Arvada",
    //     "aa": "",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Asheville",
    //     "a": "Asheville",
    //     "aa": "",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Atlanta (ATL)",
    //     "a": "Atlanta",
    //     "aa": "ATL",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Austin (AUS)",
    //     "a": "Austin",
    //     "aa": "AUS",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Baltimore (BAL)",
    //     "a": "Baltimore",
    //     "aa": "BAL",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Belleville (BVW)",
    //     "a": "Belleville",
    //     "aa": "BVW",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Boston (BOS)",
    //     "a": "Boston",
    //     "aa": "BOS",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Boston (BOS) - Boston Enterprise GIS",
    //     "a": "Boston",
    //     "aa": "BOS",
    //     "s": "Boston Enterprise GIS",
    //     "sa": ""
    // }, {
    //     "label": "Broadcasting Board of Governors (BBG)",
    //     "a": "Broadcasting Board of Governors",
    //     "aa": "BBG",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "California (CA)",
    //     "a": "California",
    //     "aa": "CA",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "California (CA) - California Environmental Health Tracking Program (CEHTP)",
    //     "a": "California",
    //     "aa": "CA",
    //     "s": "California Environmental Health Tracking Program",
    //     "sa": "CEHTP"
    // }, {
    //     "label": "California (CA) - Department of Resources (CDR)",
    //     "a": "California",
    //     "aa": "CA",
    //     "s": "Department of Resources",
    //     "sa": "CDR"
    // }, {
    //     "label": "California (CA) - Department of Education (DOE)",
    //     "a": "California",
    //     "aa": "CA",
    //     "s": "Department of Education",
    //     "sa": "DOE"
    // }, {
    //     "label": "Champaign",
    //     "a": "Champaign",
    //     "aa": "",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Chicago (CHI)",
    //     "a": "Chicago",
    //     "aa": "CHI",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "City of Orem",
    //     "a": "City of Orem",
    //     "aa": "",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Colorado (CO)",
    //     "a": "Colorado",
    //     "aa": "CO",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Colorado (CO) - Denver Regional Council (DRCOG)",
    //     "a": "Colorado",
    //     "aa": "CO",
    //     "s": "Denver Regional Council",
    //     "sa": "DRCOG"
    // }, {
    //     "label": "Columbia University (CU) - Center for International Earth Science Information Network (CIESIN)",
    //     "a": "Columbia University",
    //     "aa": "CU",
    //     "s": "Center for International Earth Science Information Network",
    //     "sa": "CIESIN"
    // }, {
    //     "label": "Commodity Futures Trading Commission (CFTC)",
    //     "a": "Commodity Futures Trading Commission",
    //     "aa": "CFTC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Connecticut (CT)",
    //     "a": "Connecticut",
    //     "aa": "CT",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Consumer Financial Protection Bureau (CFPB)",
    //     "a": "Consumer Financial Protection Bureau",
    //     "aa": "CFPB",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Cook County (CC)",
    //     "a": "Cook County",
    //     "aa": "CC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Cornell University (CU)",
    //     "a": "Cornell University",
    //     "aa": "CU",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Corporation for National and Community Service (CNCS)",
    //     "a": "Corporation for National and Community Service",
    //     "aa": "CNCS",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Court Services and Offender Supervision Agency (CSOSA)",
    //     "a": "Court Services and Offender Supervision Agency",
    //     "aa": "CSOSA",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Delaware (DE)",
    //     "a": "Delaware",
    //     "aa": "DE",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Denver (DV)",
    //     "a": "Denver",
    //     "aa": "DV",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Department of Agriculture (USDA) - Agricultural Marketing Service (AMS)",
    //     "a": "Department of Agriculture",
    //     "aa": "USDA",
    //     "s": "Agricultural Marketing Service",
    //     "sa": "AMS"
    // }, {
    //     "label": "Department of Agriculture (USDA) - Agricultural Research Service (ARS)",
    //     "a": "Department of Agriculture",
    //     "aa": "USDA",
    //     "s": "Agricultural Research Service",
    //     "sa": "ARS"
    // }, {
    //     "label": "Department of Agriculture (USDA) - Animal and Plant Health Inspection Service (APHIS)",
    //     "a": "Department of Agriculture",
    //     "aa": "USDA",
    //     "s": "Animal and Plant Health Inspection Service",
    //     "sa": "APHIS"
    // }, {
    //     "label": "Department of Agriculture (USDA)",
    //     "a": "Department of Agriculture",
    //     "aa": "USDA",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Department of Agriculture (USDA) - Departmental Management (DM)",
    //     "a": "Department of Agriculture",
    //     "aa": "USDA",
    //     "s": "Departmental Management",
    //     "sa": "DM"
    // }, {
    //     "label": "Department of Agriculture (USDA) - Economic Research Service (ERS)",
    //     "a": "Department of Agriculture",
    //     "aa": "USDA",
    //     "s": "Economic Research Service",
    //     "sa": "ERS"
    // }, {
    //     "label": "Department of Agriculture (USDA) - Farm Service Agency (FSA)",
    //     "a": "Department of Agriculture",
    //     "aa": "USDA",
    //     "s": "Farm Service Agency",
    //     "sa": "FSA"
    // }, {
    //     "label": "Department of Agriculture (USDA) - Food and Nutrition Service (FNS)",
    //     "a": "Department of Agriculture",
    //     "aa": "USDA",
    //     "s": "Food and Nutrition Service",
    //     "sa": "FNS"
    // }, {
    //     "label": "Department of Agriculture (USDA) - Food Safety and Inspection Service (FSIS)",
    //     "a": "Department of Agriculture",
    //     "aa": "USDA",
    //     "s": "Food Safety and Inspection Service",
    //     "sa": "FSIS"
    // }, {
    //     "label": "Department of Agriculture (USDA) - Foreign Agricultural Service (FAS)",
    //     "a": "Department of Agriculture",
    //     "aa": "USDA",
    //     "s": "Foreign Agricultural Service",
    //     "sa": "FAS"
    // }, {
    //     "label": "Department of Agriculture (USDA) - National Agricultural Statistics Service (NASS)",
    //     "a": "Department of Agriculture",
    //     "aa": "USDA",
    //     "s": "National Agricultural Statistics Service",
    //     "sa": "NASS"
    // }, {
    //     "label": "Department of Agriculture (USDA) - National Appeals Division (NAD)",
    //     "a": "Department of Agriculture",
    //     "aa": "USDA",
    //     "s": "National Appeals Division",
    //     "sa": "NAD"
    // }, {
    //     "label": "Department of Agriculture (USDA) - National Institute of Food and Agriculture (NIFA)",
    //     "a": "Department of Agriculture",
    //     "aa": "USDA",
    //     "s": "National Institute of Food and Agriculture",
    //     "sa": "NIFA"
    // }, {
    //     "label": "Department of Agriculture (USDA) - Natural Resources Conservation Service (NRCS)",
    //     "a": "Department of Agriculture",
    //     "aa": "USDA",
    //     "s": "Natural Resources Conservation Service",
    //     "sa": "NRCS"
    // }, {
    //     "label": "Department of Agriculture (USDA) - Office of the Chief Economist (OCE)",
    //     "a": "Department of Agriculture",
    //     "aa": "USDA",
    //     "s": "Office of the Chief Economist",
    //     "sa": "OCE"
    // }, {
    //     "label": "Department of Agriculture (USDA) - Rural Development (RD)",
    //     "a": "Department of Agriculture",
    //     "aa": "USDA",
    //     "s": "Rural Development",
    //     "sa": "RD"
    // }, {
    //     "label": "Department of Agriculture (USDA) - US Forest Service (FS)",
    //     "a": "Department of Agriculture",
    //     "aa": "USDA",
    //     "s": "US Forest Service",
    //     "sa": "FS"
    // }, {
    //     "label": "Department of Commerce (USDC)",
    //     "a": "Department of Commerce",
    //     "aa": "USDC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Department of Commerce (USDC) - Bureau of Economic Analysis (BEA)",
    //     "a": "Department of Commerce",
    //     "aa": "USDC",
    //     "s": "Bureau of Economic Analysis",
    //     "sa": "BEA"
    // }, {
    //     "label": "Department of Commerce (USDC) - Bureau of Industry and Security (BIS)",
    //     "a": "Department of Commerce",
    //     "aa": "USDC",
    //     "s": "Bureau of Industry and Security",
    //     "sa": "BIS"
    // }, {
    //     "label": "Department of Commerce (USDC) - US Patent and Trademark Office (USPTO)",
    //     "a": "Department of Commerce",
    //     "aa": "USDC",
    //     "s": "US Patent and Trademark Office",
    //     "sa": "USPTO"
    // }, {
    //     "label": "Department of Commerce (USDC) - International Trade Administration (ITA)",
    //     "a": "Department of Commerce",
    //     "aa": "USDC",
    //     "s": "International Trade Administration",
    //     "sa": "ITA"
    // }, {
    //     "label": "Department of Commerce (USDC) - National Institute of Standards and Technology (NIST)",
    //     "a": "Department of Commerce",
    //     "aa": "USDC",
    //     "s": "National Institute of Standards and Technology",
    //     "sa": "NIST"
    // }, {
    //     "label": "Department of Commerce (USDC) - National Oceanic and Atmospheric Administration (NOAA)",
    //     "a": "Department of Commerce",
    //     "aa": "USDC",
    //     "s": "National Oceanic and Atmospheric Administration",
    //     "sa": "NOAA"
    // }, {
    //     "label": "Department of Commerce (USDC) - National Technical Information Service (NTIS)",
    //     "a": "Department of Commerce",
    //     "aa": "USDC",
    //     "s": "National Technical Information Service",
    //     "sa": "NTIS"
    // }, {
    //     "label": "Department of Commerce (USDC) - National Telecommunication and Information Administration (NTIA)",
    //     "a": "Department of Commerce",
    //     "aa": "USDC",
    //     "s": "National Telecommunication and Information Administration",
    //     "sa": "NTIA"
    // }, {
    //     "label": "Department of Commerce (USDC) - National Weather Service (NWS)",
    //     "a": "Department of Commerce",
    //     "aa": "USDC",
    //     "s": "National Weather Service",
    //     "sa": "NWS"
    // }, {
    //     "label": "Department of Commerce (USDC) - US Census Bureau (Census)",
    //     "a": "Department of Commerce",
    //     "aa": "USDC",
    //     "s": "US Census Bureau",
    //     "sa": "Census"
    // }, {
    //     "label": "Department of Defense (DOD) - Army Corps of Engineers (ACE)",
    //     "a": "Department of Defense",
    //     "aa": "DOD",
    //     "s": "Army Corps of Engineers",
    //     "sa": "ACE"
    // }, {
    //     "label": "Department of Defense (DOD) - Acquisition Technology and Logistics (AT&L)",
    //     "a": "Department of Defense",
    //     "aa": "DOD",
    //     "s": "Acquisition Technology and Logistics",
    //     "sa": "AT&L"
    // }, {
    //     "label": "Department of Defense (DOD)",
    //     "a": "Department of Defense",
    //     "aa": "DOD",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Department of Defense (DOD) - National Geospatial Intelligence Agency (NGA)",
    //     "a": "Department of Defense",
    //     "aa": "DOD",
    //     "s": "National Geospatial Intelligence Agency",
    //     "sa": "NGA"
    // }, {
    //     "label": "Department of Defense (DOD) - Defense Logistics Agency (DLA)",
    //     "a": "Department of Defense",
    //     "aa": "DOD",
    //     "s": "Defense Logistics Agency",
    //     "sa": "DLA"
    // }, {
    //     "label": "Department of Defense (DOD) - Defense Technical Information Center (DTIC)",
    //     "a": "Department of Defense",
    //     "aa": "DOD",
    //     "s": "Defense Technical Information Center",
    //     "sa": "DTIC"
    // }, {
    //     "label": "Department of Defense (DOD) - Department of the Army (Army)",
    //     "a": "Department of Defense",
    //     "aa": "DOD",
    //     "s": "Department of the Army",
    //     "sa": "Army"
    // }, {
    //     "label": "Department of Defense (DOD) - Federal Voting Assistance Program (FVAP)",
    //     "a": "Department of Defense",
    //     "aa": "DOD",
    //     "s": "Federal Voting Assistance Program",
    //     "sa": "FVAP"
    // }, {
    //     "label": "Department of Defense (DOD) - Defense Advanced Research Projects Agency (DARPA)",
    //     "a": "Department of Defense",
    //     "aa": "DOD",
    //     "s": "Defense Advanced Research Projects Agency",
    //     "sa": "DARPA"
    // }, {
    //     "label": "Department of Education (ED / DOED)",
    //     "a": "Department of Education",
    //     "aa": "ED / DOED",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Department of Education (ED / DOED) - Federal Student Aid (FAFSA)",
    //     "a": "Department of Education",
    //     "aa": "ED / DOED",
    //     "s": "Federal Student Aid",
    //     "sa": "FAFSA"
    // }, {
    //     "label": "Department of Education (ED / DOED) - Institute of Education Sciences (IES)",
    //     "a": "Department of Education",
    //     "aa": "ED / DOED",
    //     "s": "Institute of Education Sciences",
    //     "sa": "IES"
    // }, {
    //     "label": "Department of Education (ED / DOED) - National Center for Education Statistics (NCES)",
    //     "a": "Department of Education",
    //     "aa": "ED / DOED",
    //     "s": "National Center for Education Statistics",
    //     "sa": "NCES"
    // }, {
    //     "label": "Department of Education (ED / DOED) - Office for Civil Rights (OCR)",
    //     "a": "Department of Education",
    //     "aa": "ED / DOED",
    //     "s": "Office for Civil Rights",
    //     "sa": "OCR"
    // }, {
    //     "label": "Department of Education (ED / DOED) - Office of Hearings and Appeals (OHA)",
    //     "a": "Department of Education",
    //     "aa": "ED / DOED",
    //     "s": "Office of Hearings and Appeals",
    //     "sa": "OHA"
    // }, {
    //     "label": "Department of Education (ED / DOED) - Office of Innovation and Improvement (OII)",
    //     "a": "Department of Education",
    //     "aa": "ED / DOED",
    //     "s": "Office of Innovation and Improvement",
    //     "sa": "OII"
    // }, {
    //     "label": "Department of Education (ED / DOED) - Office of Postsecondary Education (OPE)",
    //     "a": "Department of Education",
    //     "aa": "ED / DOED",
    //     "s": "Office of Postsecondary Education",
    //     "sa": "OPE"
    // }, {
    //     "label": "Department of Education (ED / DOED) - Office of Special Education and Rehabilitative Services (OSERS)",
    //     "a": "Department of Education",
    //     "aa": "ED / DOED",
    //     "s": "Office of Special Education and Rehabilitative Services",
    //     "sa": "OSERS"
    // }, {
    //     "label": "Department of Education (ED / DOED) - Office of Vocational and Adult Education (OVAE)",
    //     "a": "Department of Education",
    //     "aa": "ED / DOED",
    //     "s": "Office of Vocational and Adult Education",
    //     "sa": "OVAE"
    // }, {
    //     "label": "Department of Energy (DOE)",
    //     "a": "Department of Energy",
    //     "aa": "DOE",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Department of Energy (DOE) - Energy Information Administration (EIA)",
    //     "a": "Department of Energy",
    //     "aa": "DOE",
    //     "s": "Energy Information Administration",
    //     "sa": "EIA"
    // }, {
    //     "label": "Department of Energy (DOE) - Office of Scientific and Technical Information (OSTI)",
    //     "a": "Department of Energy",
    //     "aa": "DOE",
    //     "s": "Office of Scientific and Technical Information",
    //     "sa": "OSTI"
    // }, {
    //     "label": "Department of Health and Human Services (HHS) - Centers for Medicare and Medicaid Services (CMS)",
    //     "a": "Department of Health and Human Services",
    //     "aa": "HHS",
    //     "s": "Centers for Medicare and Medicaid Services",
    //     "sa": "CMS"
    // }, {
    //     "label": "Department of Health and Human Services (HHS)",
    //     "a": "Department of Health and Human Services",
    //     "aa": "HHS",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Department of Health and Human Services (HHS) - Food and Drug Administration (FDA)",
    //     "a": "Department of Health and Human Services",
    //     "aa": "HHS",
    //     "s": "Food and Drug Administration",
    //     "sa": "FDA"
    // }, {
    //     "label": "Department of Health and Human Services (HHS) - National Institutes of Health (NIH)",
    //     "a": "Department of Health and Human Services",
    //     "aa": "HHS",
    //     "s": "National Institutes of Health",
    //     "sa": "NIH"
    // }, {
    //     "label": "Department of Health and Human Services (HHS) - Substance Abuse and Mental Health Services Administration (SAMHSA)",
    //     "a": "Department of Health and Human Services",
    //     "aa": "HHS",
    //     "s": "Substance Abuse and Mental Health Services Administration",
    //     "sa": "SAMHSA"
    // }, {
    //     "label": "Department of Health and Human Services (HHS) - Centers for Disease Control and Prevention (CDC)",
    //     "a": "Department of Health and Human Services",
    //     "aa": "HHS",
    //     "s": "Centers for Disease Control and Prevention",
    //     "sa": "CDC"
    // }, {
    //     "label": "Department of Health and Human Services (HHS) - Office of the National Coordinator for Health IT (ONC)",
    //     "a": "Department of Health and Human Services",
    //     "aa": "HHS",
    //     "s": "Office of the National Coordinator for Health IT",
    //     "sa": "ONC"
    // }, {
    //     "label": "Department of Health and Human Services (HHS) - Agency for Healthcare Research and Quality (AHRQ)",
    //     "a": "Department of Health and Human Services",
    //     "aa": "HHS",
    //     "s": "Agency for Healthcare Research and Quality",
    //     "sa": "AHRQ"
    // }, {
    //     "label": "Department of Homeland Security (DHS) - U.S. Coast Guard",
    //     "a": "Department of Homeland Security",
    //     "aa": "DHS",
    //     "s": "U.S. Coast Guard",
    //     "sa": ""
    // }, {
    //     "label": "Department of Homeland Security (DHS)",
    //     "a": "Department of Homeland Security",
    //     "aa": "DHS",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Department of Homeland Security (DHS) - Federal Emergency Management Agency (FEMA)",
    //     "a": "Department of Homeland Security",
    //     "aa": "DHS",
    //     "s": "Federal Emergency Management Agency",
    //     "sa": "FEMA"
    // }, {
    //     "label": "Department of Homeland Security (DHS) - United States Coast Guard (USCG)",
    //     "a": "Department of Homeland Security",
    //     "aa": "DHS",
    //     "s": "United States Coast Guard",
    //     "sa": "USCG"
    // }, {
    //     "label": "Department of Homeland Security (DHS) - Office of Health Affairs (OHA)",
    //     "a": "Department of Homeland Security",
    //     "aa": "DHS",
    //     "s": "Office of Health Affairs",
    //     "sa": "OHA"
    // }, {
    //     "label": "Department of Homeland Security (DHS) - Office of Immigration Statistics (OIS)",
    //     "a": "Department of Homeland Security",
    //     "aa": "DHS",
    //     "s": "Office of Immigration Statistics",
    //     "sa": "OIS"
    // }, {
    //     "label": "Department of Homeland Security (DHS) - U.S. Citizenship and Immigration Services (USCIS)",
    //     "a": "Department of Homeland Security",
    //     "aa": "DHS",
    //     "s": "U.S. Citizenship and Immigration Services",
    //     "sa": "USCIS"
    // }, {
    //     "label": "Department of Housing and Urban Development (HUD) - Office of Housing",
    //     "a": "Department of Housing and Urban Development",
    //     "aa": "HUD",
    //     "s": "Office of Housing",
    //     "sa": ""
    // }, {
    //     "label": "Department of Justice (DOJ)",
    //     "a": "Department of Justice",
    //     "aa": "DOJ",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Department of Justice (DOJ) - Antitrust Division (Antitrust)",
    //     "a": "Department of Justice",
    //     "aa": "DOJ",
    //     "s": "Antitrust Division",
    //     "sa": "Antitrust"
    // }, {
    //     "label": "Department of Justice (DOJ) - Bureau of Justice Statistics (BJS)",
    //     "a": "Department of Justice",
    //     "aa": "DOJ",
    //     "s": "Bureau of Justice Statistics",
    //     "sa": "BJS"
    // }, {
    //     "label": "Department of Justice (DOJ) - Civil Division (CD)",
    //     "a": "Department of Justice",
    //     "aa": "DOJ",
    //     "s": "Civil Division",
    //     "sa": "CD"
    // }, {
    //     "label": "Department of Justice (DOJ) - Civil Rights Division (CRD)",
    //     "a": "Department of Justice",
    //     "aa": "DOJ",
    //     "s": "Civil Rights Division",
    //     "sa": "CRD"
    // }, {
    //     "label": "Department of Justice (DOJ) - Federal Bureau of Investigation (FBI)",
    //     "a": "Department of Justice",
    //     "aa": "DOJ",
    //     "s": "Federal Bureau of Investigation",
    //     "sa": "FBI"
    // }, {
    //     "label": "Department of Justice (DOJ) - US Trustee Program (USTP)",
    //     "a": "Department of Justice",
    //     "aa": "DOJ",
    //     "s": "US Trustee Program",
    //     "sa": "USTP"
    // }, {
    //     "label": "Department of Justice (DOJ) - Office of Legal Counsel (OLC)",
    //     "a": "Department of Justice",
    //     "aa": "DOJ",
    //     "s": "Office of Legal Counsel",
    //     "sa": "OLC"
    // }, {
    //     "label": "Department of Justice (DOJ) - US Attorney's Office (USAO)",
    //     "a": "Department of Justice",
    //     "aa": "DOJ",
    //     "s": "US Attorney's Office",
    //     "sa": "USAO"
    // }, {
    //     "label": "Department of Labor (DOL) - Benefits Review Board (BRB)",
    //     "a": "Department of Labor",
    //     "aa": "DOL",
    //     "s": "Benefits Review Board",
    //     "sa": "BRB"
    // }, {
    //     "label": "Department of Labor (DOL) - Bureau of Labor Statistics (BLS)",
    //     "a": "Department of Labor",
    //     "aa": "DOL",
    //     "s": "Bureau of Labor Statistics",
    //     "sa": "BLS"
    // }, {
    //     "label": "Department of Labor (DOL) - Employee Benefits Security Administration (EBSA)",
    //     "a": "Department of Labor",
    //     "aa": "DOL",
    //     "s": "Employee Benefits Security Administration",
    //     "sa": "EBSA"
    // }, {
    //     "label": "Department of Labor (DOL) - Employees' Compensation Appeals Board (ECAB)",
    //     "a": "Department of Labor",
    //     "aa": "DOL",
    //     "s": "Employees' Compensation Appeals Board",
    //     "sa": "ECAB"
    // }, {
    //     "label": "Department of Labor (DOL) - Employment and Training Administration (ETA)",
    //     "a": "Department of Labor",
    //     "aa": "DOL",
    //     "s": "Employment and Training Administration",
    //     "sa": "ETA"
    // }, {
    //     "label": "Department of Labor (DOL) - Mine Safety and Health Administration (MSHA)",
    //     "a": "Department of Labor",
    //     "aa": "DOL",
    //     "s": "Mine Safety and Health Administration",
    //     "sa": "MSHA"
    // }, {
    //     "label": "Department of Labor (DOL)",
    //     "a": "Department of Labor",
    //     "aa": "DOL",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Department of Labor (DOL) - Occupational Safety and Health Administration (OSHA)",
    //     "a": "Department of Labor",
    //     "aa": "DOL",
    //     "s": "Occupational Safety and Health Administration",
    //     "sa": "OSHA"
    // }, {
    //     "label": "Department of Labor (DOL) - Office of Administrative Law Judges (OALJ)",
    //     "a": "Department of Labor",
    //     "aa": "DOL",
    //     "s": "Office of Administrative Law Judges",
    //     "sa": "OALJ"
    // }, {
    //     "label": "Department of Labor (DOL) - Wage and Hour Division (WHD)",
    //     "a": "Department of Labor",
    //     "aa": "DOL",
    //     "s": "Wage and Hour Division",
    //     "sa": "WHD"
    // }, {
    //     "label": "Department of Labor (DOL) - Office of Job Corps (OJC)",
    //     "a": "Department of Labor",
    //     "aa": "DOL",
    //     "s": "Office of Job Corps",
    //     "sa": "OJC"
    // }, {
    //     "label": "Department of Labor (DOL) - Office of the Assistant Secretary for Policy (OASP)",
    //     "a": "Department of Labor",
    //     "aa": "DOL",
    //     "s": "Office of the Assistant Secretary for Policy",
    //     "sa": "OASP"
    // }, {
    //     "label": "Department of State (DOS)",
    //     "a": "Department of State",
    //     "aa": "DOS",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Department of State (DOS) - Organisation for Economic Cooperation and Development (OECD)",
    //     "a": "Department of State",
    //     "aa": "DOS",
    //     "s": "Organisation for Economic Cooperation and Development",
    //     "sa": "OECD"
    // }, {
    //     "label": "Department of the Interior (DOI)",
    //     "a": "Department of the Interior",
    //     "aa": "DOI",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Department of the Interior (DOI) - Bureau of Indian Education (BIE)",
    //     "a": "Department of the Interior",
    //     "aa": "DOI",
    //     "s": "Bureau of Indian Education",
    //     "sa": "BIE"
    // }, {
    //     "label": "Department of the Interior (DOI) - Bureau of Land Management (BLM)",
    //     "a": "Department of the Interior",
    //     "aa": "DOI",
    //     "s": "Bureau of Land Management",
    //     "sa": "BLM"
    // }, {
    //     "label": "Department of the Interior (DOI) - Bureau of Ocean Energy Management (BOEM)",
    //     "a": "Department of the Interior",
    //     "aa": "DOI",
    //     "s": "Bureau of Ocean Energy Management",
    //     "sa": "BOEM"
    // }, {
    //     "label": "Department of the Interior (DOI) - National Park Service (NPS)",
    //     "a": "Department of the Interior",
    //     "aa": "DOI",
    //     "s": "National Park Service",
    //     "sa": "NPS"
    // }, {
    //     "label": "Department of the Interior (DOI) - Office of Hearings and Appeals (OHA)",
    //     "a": "Department of the Interior",
    //     "aa": "DOI",
    //     "s": "Office of Hearings and Appeals",
    //     "sa": "OHA"
    // }, {
    //     "label": "Department of the Interior (DOI) - Federal Geographic Data Committee (FGDC)",
    //     "a": "Department of the Interior",
    //     "aa": "DOI",
    //     "s": "Federal Geographic Data Committee",
    //     "sa": "FGDC"
    // }, {
    //     "label": "Department of the Interior (DOI) - U.S. Geological Survey (USGS)",
    //     "a": "Department of the Interior",
    //     "aa": "DOI",
    //     "s": "U.S. Geological Survey",
    //     "sa": "USGS"
    // }, {
    //     "label": "Department of the Interior (DOI) - Office of the Solicitor (SOL)",
    //     "a": "Department of the Interior",
    //     "aa": "DOI",
    //     "s": "Office of the Solicitor",
    //     "sa": "SOL"
    // }, {
    //     "label": "Department of the Interior (DOI) - US Bureau of Reclamation (USBR)",
    //     "a": "Department of the Interior",
    //     "aa": "DOI",
    //     "s": "US Bureau of Reclamation",
    //     "sa": "USBR"
    // }, {
    //     "label": "Department of the Interior (DOI) - US Fish and Wildlife Service (FWS)",
    //     "a": "Department of the Interior",
    //     "aa": "DOI",
    //     "s": "US Fish and Wildlife Service",
    //     "sa": "FWS"
    // }, {
    //     "label": "Department of the Treasury",
    //     "a": "Department of the Treasury",
    //     "aa": "",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Department of the Treasury - Bureau of Engraving and Printing (BEP)",
    //     "a": "Department of the Treasury",
    //     "aa": "",
    //     "s": "Bureau of Engraving and Printing",
    //     "sa": "BEP"
    // }, {
    //     "label": "Department of the Treasury - Bureau of the Public Debt (BPD)",
    //     "a": "Department of the Treasury",
    //     "aa": "",
    //     "s": "Bureau of the Public Debt",
    //     "sa": "BPD"
    // }, {
    //     "label": "Department of the Treasury - Departmental Offices (DO)",
    //     "a": "Department of the Treasury",
    //     "aa": "",
    //     "s": "Departmental Offices",
    //     "sa": "DO"
    // }, {
    //     "label": "Department of the Treasury - Financial Crimes Enforcement Network (FINCEN)",
    //     "a": "Department of the Treasury",
    //     "aa": "",
    //     "s": "Financial Crimes Enforcement Network",
    //     "sa": "FINCEN"
    // }, {
    //     "label": "Department of the Treasury - Financial Management Service (FMS)",
    //     "a": "Department of the Treasury",
    //     "aa": "",
    //     "s": "Financial Management Service",
    //     "sa": "FMS"
    // }, {
    //     "label": "Department of the Treasury - Internal Revenue Service (IRS)",
    //     "a": "Department of the Treasury",
    //     "aa": "",
    //     "s": "Internal Revenue Service",
    //     "sa": "IRS"
    // }, {
    //     "label": "Department of the Treasury - United States Mint",
    //     "a": "Department of the Treasury",
    //     "aa": "",
    //     "s": "United States Mint",
    //     "sa": ""
    // }, {
    //     "label": "Department of Transportation (DOT) - National Highway Traffic Safety Administration (NHTSA)",
    //     "a": "Department of Transportation",
    //     "aa": "DOT",
    //     "s": "National Highway Traffic Safety Administration",
    //     "sa": "NHTSA"
    // }, {
    //     "label": "Department of Transportation (DOT)",
    //     "a": "Department of Transportation",
    //     "aa": "DOT",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Department of Transportation (DOT) - Bureau of Transportation Statistics (BTS)",
    //     "a": "Department of Transportation",
    //     "aa": "DOT",
    //     "s": "Bureau of Transportation Statistics",
    //     "sa": "BTS"
    // }, {
    //     "label": "Department of Transportation (DOT) - Federal Aviation Administration (FAA)",
    //     "a": "Department of Transportation",
    //     "aa": "DOT",
    //     "s": "Federal Aviation Administration",
    //     "sa": "FAA"
    // }, {
    //     "label": "Department of Transportation (DOT) - Federal Highway Administration (FHWA)",
    //     "a": "Department of Transportation",
    //     "aa": "DOT",
    //     "s": "Federal Highway Administration",
    //     "sa": "FHWA"
    // }, {
    //     "label": "Department of Transportation (DOT) - Federal Motor Carrier Safety Administration (FMCSA)",
    //     "a": "Department of Transportation",
    //     "aa": "DOT",
    //     "s": "Federal Motor Carrier Safety Administration",
    //     "sa": "FMCSA"
    // }, {
    //     "label": "Department of Transportation (DOT) - Federal Railroad Administration (FRA)",
    //     "a": "Department of Transportation",
    //     "aa": "DOT",
    //     "s": "Federal Railroad Administration",
    //     "sa": "FRA"
    // }, {
    //     "label": "Department of Transportation (DOT) - Federal Transit Administration (FTA)",
    //     "a": "Department of Transportation",
    //     "aa": "DOT",
    //     "s": "Federal Transit Administration",
    //     "sa": "FTA"
    // }, {
    //     "label": "Department of Transportation (DOT) - Maritime Administration (MARAD)",
    //     "a": "Department of Transportation",
    //     "aa": "DOT",
    //     "s": "Maritime Administration",
    //     "sa": "MARAD"
    // }, {
    //     "label": "Department of Transportation (DOT) - National Highway Traffice Safety Administration (NHTSA)",
    //     "a": "Department of Transportation",
    //     "aa": "DOT",
    //     "s": "National Highway Traffice Safety Administration",
    //     "sa": "NHTSA"
    // }, {
    //     "label": "Department of Transportation (DOT) - Office of the Secretary of Transportation (OST)",
    //     "a": "Department of Transportation",
    //     "aa": "DOT",
    //     "s": "Office of the Secretary of Transportation",
    //     "sa": "OST"
    // }, {
    //     "label": "Department of Transportation (DOT) - Pipeline and Hazardous Materials Safety Administration (PHMSA)",
    //     "a": "Department of Transportation",
    //     "aa": "DOT",
    //     "s": "Pipeline and Hazardous Materials Safety Administration",
    //     "sa": "PHMSA"
    // }, {
    //     "label": "Department of Transportation (DOT) - Research and Innovative Technology Administration (RITA)",
    //     "a": "Department of Transportation",
    //     "aa": "DOT",
    //     "s": "Research and Innovative Technology Administration",
    //     "sa": "RITA"
    // }, {
    //     "label": "Department of Transportation (DOT) - Saint Lawrence Seaway Development Corporation (SLSDC)",
    //     "a": "Department of Transportation",
    //     "aa": "DOT",
    //     "s": "Saint Lawrence Seaway Development Corporation",
    //     "sa": "SLSDC"
    // }, {
    //     "label": "Department of Transportation (DOT) - Surface Transportation Board (STB)",
    //     "a": "Department of Transportation",
    //     "aa": "DOT",
    //     "s": "Surface Transportation Board",
    //     "sa": "STB"
    // }, {
    //     "label": "Department of Veterans Affairs (VA) - National Cemetery Administration (NCA)",
    //     "a": "Department of Veterans Affairs",
    //     "aa": "VA",
    //     "s": "National Cemetery Administration",
    //     "sa": "NCA"
    // }, {
    //     "label": "Department of Veterans Affairs (VA)",
    //     "a": "Department of Veterans Affairs",
    //     "aa": "VA",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Department of Veterans Affairs (VA) - Veterans Benefits Administration (VBA)",
    //     "a": "Department of Veterans Affairs",
    //     "aa": "VA",
    //     "s": "Veterans Benefits Administration",
    //     "sa": "VBA"
    // }, {
    //     "label": "Department of Veterans Affairs (VA) - Veterans Health Administration (VHA)",
    //     "a": "Department of Veterans Affairs",
    //     "aa": "VA",
    //     "s": "Veterans Health Administration",
    //     "sa": "VHA"
    // }, {
    //     "label": "District of Columbia (DC)",
    //     "a": "District of Columbia",
    //     "aa": "DC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Election Assistance Commission (EAC)",
    //     "a": "Election Assistance Commission",
    //     "aa": "EAC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Executive Office of the President (EOP) - Networking and Information Technology Research and Development (NITRD)",
    //     "a": "Executive Office of the President",
    //     "aa": "EOP",
    //     "s": "Networking and Information Technology Research and Development",
    //     "sa": "NITRD"
    // }, {
    //     "label": "Executive Office of the President (EOP) - Council on Environmental Quality (CEQ)",
    //     "a": "Executive Office of the President",
    //     "aa": "EOP",
    //     "s": "Council on Environmental Quality",
    //     "sa": "CEQ"
    // }, {
    //     "label": "Executive Office of the President (EOP) - Office of Management and Budget (OMB)",
    //     "a": "Executive Office of the President",
    //     "aa": "EOP",
    //     "s": "Office of Management and Budget",
    //     "sa": "OMB"
    // }, {
    //     "label": "Executive Office of the President (EOP) - Office of National Drug Control Policy (ONDCP)",
    //     "a": "Executive Office of the President",
    //     "aa": "EOP",
    //     "s": "Office of National Drug Control Policy",
    //     "sa": "ONDCP"
    // }, {
    //     "label": "Executive Office of the President (EOP) - Office of Science and Technology Policy (OSTP)",
    //     "a": "Executive Office of the President",
    //     "aa": "EOP",
    //     "s": "Office of Science and Technology Policy",
    //     "sa": "OSTP"
    // }, {
    //     "label": "Executive Office of the President (EOP)",
    //     "a": "Executive Office of the President",
    //     "aa": "EOP",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Executive Office of the President (EOP) - US Trade Representative (USTR)",
    //     "a": "Executive Office of the President",
    //     "aa": "EOP",
    //     "s": "US Trade Representative",
    //     "sa": "USTR"
    // }, {
    //     "label": "Executive Office of the President (EOP) - White House (WH)",
    //     "a": "Executive Office of the President",
    //     "aa": "EOP",
    //     "s": "White House",
    //     "sa": "WH"
    // }, {
    //     "label": "Export-Import Bank of the US (EX-IM)",
    //     "a": "Export-Import Bank of the US",
    //     "aa": "EX-IM",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Federal Communications Commission (FCC)",
    //     "a": "Federal Communications Commission",
    //     "aa": "FCC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Federal Deposit Insurance Corporation (FDIC)",
    //     "a": "Federal Deposit Insurance Corporation",
    //     "aa": "FDIC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Federal Election Commission (FED)",
    //     "a": "Federal Election Commission",
    //     "aa": "FED",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Federal Geographic Data Committee (FGDC)",
    //     "a": "Federal Geographic Data Committee",
    //     "aa": "FGDC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Federal Government - Department of Housing and Urban Development (HUD)",
    //     "a": "Federal Government",
    //     "aa": "",
    //     "s": "Department of Housing and Urban Development",
    //     "sa": "HUD"
    // }, {
    //     "label": "Federal Housing Finance Agency (FHFA)",
    //     "a": "Federal Housing Finance Agency",
    //     "aa": "FHFA",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Federal Reserve Board (FED)",
    //     "a": "Federal Reserve Board",
    //     "aa": "FED",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Florida (FL)",
    //     "a": "Florida",
    //     "aa": "FL",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "General Services Administration (GSA)",
    //     "a": "General Services Administration",
    //     "aa": "GSA",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "General Services Administration (GSA) - Federal Acquisition Service (FAS)",
    //     "a": "General Services Administration",
    //     "aa": "GSA",
    //     "s": "Federal Acquisition Service",
    //     "sa": "FAS"
    // }, {
    //     "label": "General Services Administration (GSA) - Office of Citizen Services and Innovative Technologies (OCSIT)",
    //     "a": "General Services Administration",
    //     "aa": "GSA",
    //     "s": "Office of Citizen Services and Innovative Technologies",
    //     "sa": "OCSIT"
    // }, {
    //     "label": "General Services Administration (GSA) - Office of Governmentwide Policy (OGP)",
    //     "a": "General Services Administration",
    //     "aa": "GSA",
    //     "s": "Office of Governmentwide Policy",
    //     "sa": "OGP"
    // }, {
    //     "label": "General Services Administration (GSA) - Office of Performance Improvement (OPI)",
    //     "a": "General Services Administration",
    //     "aa": "GSA",
    //     "s": "Office of Performance Improvement",
    //     "sa": "OPI"
    // }, {
    //     "label": "General Services Administration (GSA) - Office of the Chief Financial Officer (OCFO)",
    //     "a": "General Services Administration",
    //     "aa": "GSA",
    //     "s": "Office of the Chief Financial Officer",
    //     "sa": "OCFO"
    // }, {
    //     "label": "General Services Administration (GSA) - Office of the Chief People Officer (OCPO)",
    //     "a": "General Services Administration",
    //     "aa": "GSA",
    //     "s": "Office of the Chief People Officer",
    //     "sa": "OCPO"
    // }, {
    //     "label": "General Services Administration (GSA) - Public Buildings Service (PBS)",
    //     "a": "General Services Administration",
    //     "aa": "GSA",
    //     "s": "Public Buildings Service",
    //     "sa": "PBS"
    // }, {
    //     "label": "Georgia (GA)",
    //     "a": "Georgia",
    //     "aa": "GA",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Gilpin County (GC)",
    //     "a": "Gilpin County",
    //     "aa": "GC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Great Lakes Commission (GLC)",
    //     "a": "Great Lakes Commission",
    //     "aa": "GLC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Hawaii (HI)",
    //     "a": "Hawaii",
    //     "aa": "HI",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Hawaii (HI) - Hawaii GIS",
    //     "a": "Hawaii",
    //     "aa": "HI",
    //     "s": "Hawaii GIS",
    //     "sa": ""
    // }, {
    //     "label": "Honolulu (HNL)",
    //     "a": "Honolulu",
    //     "aa": "HNL",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Houston",
    //     "a": "Houston",
    //     "aa": "",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Idaho (ID) - Coeur d'Alene Tribe (CDATRIBE)",
    //     "a": "Idaho",
    //     "aa": "ID",
    //     "s": "Coeur d'Alene Tribe",
    //     "sa": "CDATRIBE"
    // }, {
    //     "label": "Idaho State University (ISU)",
    //     "a": "Idaho State University",
    //     "aa": "ISU",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Illinois (IL)",
    //     "a": "Illinois",
    //     "aa": "IL",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Illinois (IL) - South Suburban Mayors and Managers (SSMMA)",
    //     "a": "Illinois",
    //     "aa": "IL",
    //     "s": "South Suburban Mayors and Managers",
    //     "sa": "SSMMA"
    // }, {
    //     "label": "Indiana (IN)",
    //     "a": "Indiana",
    //     "aa": "IN",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Information Sharing Environment (ISE)",
    //     "a": "Information Sharing Environment",
    //     "aa": "ISE",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Institute of Museum and Library Services (IMLS)",
    //     "a": "Institute of Museum and Library Services",
    //     "aa": "IMLS",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Iowa (IA)",
    //     "a": "Iowa",
    //     "aa": "IA",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Iowa State University GIS Support and Research Facility (ISU GIS)",
    //     "a": "Iowa State University GIS Support and Research Facility",
    //     "aa": "ISU GIS",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Kansas (KS)",
    //     "a": "Kansas",
    //     "aa": "KS",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Kansas (KS) - Kansas Data Access and Support Center (DASC)",
    //     "a": "Kansas",
    //     "aa": "KS",
    //     "s": "Kansas Data Access and Support Center",
    //     "sa": "DASC"
    // }, {
    //     "label": "Kansas City (KC)",
    //     "a": "Kansas City",
    //     "aa": "KC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Kentucky (KY)",
    //     "a": "Kentucky",
    //     "aa": "KY",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Kentucky (KY) - Kentucky Geography Network (KYGEONET)",
    //     "a": "Kentucky",
    //     "aa": "KY",
    //     "s": "Kentucky Geography Network",
    //     "sa": "KYGEONET"
    // }, {
    //     "label": "King County",
    //     "a": "King County",
    //     "aa": "",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Las Vegas (LV)",
    //     "a": "Las Vegas",
    //     "aa": "LV",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Lexington",
    //     "a": "Lexington",
    //     "aa": "",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Los Angeles (LA)",
    //     "a": "Los Angeles",
    //     "aa": "LA",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Louisiana (LA)",
    //     "a": "Louisiana",
    //     "aa": "LA",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Louisiana (LA) - Louisiana Geographic Information Center (LAGIC)",
    //     "a": "Louisiana",
    //     "aa": "LA",
    //     "s": "Louisiana Geographic Information Center",
    //     "sa": "LAGIC"
    // }, {
    //     "label": "Louisville (LVL)",
    //     "a": "Louisville",
    //     "aa": "LVL",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Madison",
    //     "a": "Madison",
    //     "aa": "",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Maine (ME)",
    //     "a": "Maine",
    //     "aa": "ME",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Maryland (MD)",
    //     "a": "Maryland",
    //     "aa": "MD",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Massachusetts (MA)",
    //     "a": "Massachusetts",
    //     "aa": "MA",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Merit Systems Protection Board (MSPB)",
    //     "a": "Merit Systems Protection Board",
    //     "aa": "MSPB",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Michigan (MI)",
    //     "a": "Michigan",
    //     "aa": "MI",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Millenium Challenge Corporation (MCC)",
    //     "a": "Millenium Challenge Corporation",
    //     "aa": "MCC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Minneapolis-St Paul (MSP) - MetroGIS (Minneapolis-St. Paul Regional GIS Consortium) (METROGIS)",
    //     "a": "Minneapolis-St Paul",
    //     "aa": "MSP",
    //     "s": "MetroGIS (Minneapolis-St. Paul Regional GIS Consortium)",
    //     "sa": "METROGIS"
    // }, {
    //     "label": "Minnesota (MN) - Minnesota Department of Natural Resources (DNR)",
    //     "a": "Minnesota",
    //     "aa": "MN",
    //     "s": "Minnesota Department of Natural Resources",
    //     "sa": "DNR"
    // }, {
    //     "label": "Minnesota (MN)",
    //     "a": "Minnesota",
    //     "aa": "MN",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Missouri (MO)",
    //     "a": "Missouri",
    //     "aa": "MO",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Missouri (MO) - Accountability Portal (MAP)",
    //     "a": "Missouri",
    //     "aa": "MO",
    //     "s": "Accountability Portal",
    //     "sa": "MAP"
    // }, {
    //     "label": "Missouri (MO) - Missouri Spatial Data Information Service (MSDIS)",
    //     "a": "Missouri",
    //     "aa": "MO",
    //     "s": "Missouri Spatial Data Information Service",
    //     "sa": "MSDIS"
    // }, {
    //     "label": "Montana (MT)",
    //     "a": "Montana",
    //     "aa": "MT",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Montgomery County",
    //     "a": "Montgomery County",
    //     "aa": "",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "National Aeronautics and Space Administration (NASA) - Jet Propulsion Laboratory (JPL)",
    //     "a": "National Aeronautics and Space Administration",
    //     "aa": "NASA",
    //     "s": "Jet Propulsion Laboratory",
    //     "sa": "JPL"
    // }, {
    //     "label": "National Aeronautics and Space Administration (NASA)",
    //     "a": "National Aeronautics and Space Administration",
    //     "aa": "NASA",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "National Archives and Records Administration (NARA)",
    //     "a": "National Archives and Records Administration",
    //     "aa": "NARA",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "National Archives and Records Administration (NARA) - Office of the Federal Register (OFR)",
    //     "a": "National Archives and Records Administration",
    //     "aa": "NARA",
    //     "s": "Office of the Federal Register",
    //     "sa": "OFR"
    // }, {
    //     "label": "National Capital Planning Commission (NCPC)",
    //     "a": "National Capital Planning Commission",
    //     "aa": "NCPC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "National Endowment for the Arts (NEA)",
    //     "a": "National Endowment for the Arts",
    //     "aa": "NEA",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "National Endowment for the Humanities (NEH)",
    //     "a": "National Endowment for the Humanities",
    //     "aa": "NEH",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "National Labor Relations Board (NLRB)",
    //     "a": "National Labor Relations Board",
    //     "aa": "NLRB",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "National Science Foundation (NSF)",
    //     "a": "National Science Foundation",
    //     "aa": "NSF",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "National States Geographic Information Council (NSGIC) - GIS Inventory (aka Ramona) (RAMONA)",
    //     "a": "National States Geographic Information Council",
    //     "aa": "NSGIC",
    //     "s": "GIS Inventory (aka Ramona)",
    //     "sa": "RAMONA"
    // }, {
    //     "label": "National Transportation Safety Board (NTSB)",
    //     "a": "National Transportation Safety Board",
    //     "aa": "NTSB",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Nebraska (NE)",
    //     "a": "Nebraska",
    //     "aa": "NE",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "New Hampshire (NH)",
    //     "a": "New Hampshire",
    //     "aa": "NH",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "New Mexico (NM)",
    //     "a": "New Mexico",
    //     "aa": "NM",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "New Orleans (NO)",
    //     "a": "New Orleans",
    //     "aa": "NO",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "New York (NY)",
    //     "a": "New York",
    //     "aa": "NY",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "New York (NY) - NY State Senate (Senate)",
    //     "a": "New York",
    //     "aa": "NY",
    //     "s": "NY State Senate",
    //     "sa": "Senate"
    // }, {
    //     "label": "New York (NY) - New York State Data Center (SDC)",
    //     "a": "New York",
    //     "aa": "NY",
    //     "s": "New York State Data Center",
    //     "sa": "SDC"
    // }, {
    //     "label": "New York (NY) - NY Department of Health (DOH)",
    //     "a": "New York",
    //     "aa": "NY",
    //     "s": "NY Department of Health",
    //     "sa": "DOH"
    // }, {
    //     "label": "New York City (NYC)",
    //     "a": "New York City",
    //     "aa": "NYC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "North Carolina (NC) - NC OpenBook",
    //     "a": "North Carolina",
    //     "aa": "NC",
    //     "s": "NC OpenBook",
    //     "sa": ""
    // }, {
    //     "label": "North Carolina (NC)",
    //     "a": "North Carolina",
    //     "aa": "NC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "North Dakota (ND) - North Dakota GIS Hub (ND GIS)",
    //     "a": "North Dakota",
    //     "aa": "ND",
    //     "s": "North Dakota GIS Hub",
    //     "sa": "ND GIS"
    // }, {
    //     "label": "North Dakota (ND)",
    //     "a": "North Dakota",
    //     "aa": "ND",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Nuclear Regulatory Commission (NRC)",
    //     "a": "Nuclear Regulatory Commission",
    //     "aa": "NRC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Nuna Technologies",
    //     "a": "Nuna Technologies",
    //     "aa": "",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Oak Ridge National Laboratory (ORNL)",
    //     "a": "Oak Ridge National Laboratory",
    //     "aa": "ORNL",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Occupational Safety and Health Review Commission (OSHRC)",
    //     "a": "Occupational Safety and Health Review Commission",
    //     "aa": "OSHRC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Office of Navajo and Hopi Indian Relocation (ONHIR)",
    //     "a": "Office of Navajo and Hopi Indian Relocation",
    //     "aa": "ONHIR",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Office of Personnel Management (OPM)",
    //     "a": "Office of Personnel Management",
    //     "aa": "OPM",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Ohio (OH)",
    //     "a": "Ohio",
    //     "aa": "OH",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Oklahoma (OK)",
    //     "a": "Oklahoma",
    //     "aa": "OK",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Open Door Kentucky",
    //     "a": "Open Door Kentucky",
    //     "aa": "",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Oregon (OR)",
    //     "a": "Oregon",
    //     "aa": "OR",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Oregon State University (OSU)",
    //     "a": "Oregon State University",
    //     "aa": "OSU",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Overseas Private Investment Corporation (OPIC)",
    //     "a": "Overseas Private Investment Corporation",
    //     "aa": "OPIC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Pacific States Marine Fisheries Commission (PSMFC)",
    //     "a": "Pacific States Marine Fisheries Commission",
    //     "aa": "PSMFC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Palo Alto (PA)",
    //     "a": "Palo Alto",
    //     "aa": "PA",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Pension Benefit Guaranty Corporation (PBGC)",
    //     "a": "Pension Benefit Guaranty Corporation",
    //     "aa": "PBGC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Philadelphia (PHILA)",
    //     "a": "Philadelphia",
    //     "aa": "PHILA",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Portland (PDX)",
    //     "a": "Portland",
    //     "aa": "PDX",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Providence",
    //     "a": "Providence",
    //     "aa": "",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Railroad Retirement Board (RRB)",
    //     "a": "Railroad Retirement Board",
    //     "aa": "RRB",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Raleigh",
    //     "a": "Raleigh",
    //     "aa": "",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Rhode Island (RI)",
    //     "a": "Rhode Island",
    //     "aa": "RI",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Rockford (RFD)",
    //     "a": "Rockford",
    //     "aa": "RFD",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "San Francisco (SF)",
    //     "a": "San Francisco",
    //     "aa": "SF",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "San Mateo County (SMC)",
    //     "a": "San Mateo County",
    //     "aa": "SMC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Santa Cruz (SC)",
    //     "a": "Santa Cruz",
    //     "aa": "SC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Scottsdale (SDL)",
    //     "a": "Scottsdale",
    //     "aa": "SDL",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Seattle (SEA)",
    //     "a": "Seattle",
    //     "aa": "SEA",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Securities and Exchange Commission (SEC)",
    //     "a": "Securities and Exchange Commission",
    //     "aa": "SEC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Selective Service System (SSS)",
    //     "a": "Selective Service System",
    //     "aa": "SSS",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Small Business Administration (SBA)",
    //     "a": "Small Business Administration",
    //     "aa": "SBA",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Social Security Administration (SSA)",
    //     "a": "Social Security Administration",
    //     "aa": "SSA",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Somerville",
    //     "a": "Somerville",
    //     "aa": "",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "South Bend (SBN)",
    //     "a": "South Bend",
    //     "aa": "SBN",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "South Dakota (SD)",
    //     "a": "South Dakota",
    //     "aa": "SD",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Tennessee (TN)",
    //     "a": "Tennessee",
    //     "aa": "TN",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Texas (TX)",
    //     "a": "Texas",
    //     "aa": "TX",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Texas (TX) - Texas Transparency",
    //     "a": "Texas",
    //     "aa": "TX",
    //     "s": "Texas Transparency",
    //     "sa": ""
    // }, {
    //     "label": "U.S. Environmental Protection Agency (EPA)",
    //     "a": "U.S. Environmental Protection Agency",
    //     "aa": "EPA",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Univ of South Carolina (SC) - Baruch Institute for Marine and Coastal Sciences",
    //     "a": "Univ of South Carolina",
    //     "aa": "SC",
    //     "s": "Baruch Institute for Marine and Coastal Sciences",
    //     "sa": ""
    // }, {
    //     "label": "University of Alaska (UA) - Geographic Information Network of Alaska - University of Alaska (GINA)",
    //     "a": "University of Alaska",
    //     "aa": "UA",
    //     "s": "Geographic Information Network of Alaska - University of Alaska",
    //     "sa": "GINA"
    // }, {
    //     "label": "University of Arizona (UA)",
    //     "a": "University of Arizona",
    //     "aa": "UA",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "University of California San Diego (UCSD)",
    //     "a": "University of California San Diego",
    //     "aa": "UCSD",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "University of Idaho (UI)",
    //     "a": "University of Idaho",
    //     "aa": "UI",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "University of New Hampshire (UNH)",
    //     "a": "University of New Hampshire",
    //     "aa": "UNH",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "University of New Mexico (UNH) - Earth Data Analysis Center (EDAC)",
    //     "a": "University of New Mexico",
    //     "aa": "UNH",
    //     "s": "Earth Data Analysis Center",
    //     "sa": "EDAC"
    // }, {
    //     "label": "University of Rhode Island (URI) - University of Rhode Island Geospatial Extension Program (GEP)",
    //     "a": "University of Rhode Island",
    //     "aa": "URI",
    //     "s": "University of Rhode Island Geospatial Extension Program",
    //     "sa": "GEP"
    // }, {
    //     "label": "University of Washington (UW)",
    //     "a": "University of Washington",
    //     "aa": "UW",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "US Agency for International Development (USAID)",
    //     "a": "US Agency for International Development",
    //     "aa": "USAID",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "US Consumer Product Safety Commission (CPSC)",
    //     "a": "US Consumer Product Safety Commission",
    //     "aa": "CPSC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "US Equal Employment Opportunity Commission (EEOC)",
    //     "a": "US Equal Employment Opportunity Commission",
    //     "aa": "EEOC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "US International Trade Commission (USITC)",
    //     "a": "US International Trade Commission",
    //     "aa": "USITC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "US Office of the Special Counsel (OSC)",
    //     "a": "US Office of the Special Counsel",
    //     "aa": "OSC",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Utah (UT)",
    //     "a": "Utah",
    //     "aa": "UT",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Virginia (VA)",
    //     "a": "Virginia",
    //     "aa": "VA",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Virginia (VA) - Virginia Department of Environmental Quality (DEQ)",
    //     "a": "Virginia",
    //     "aa": "VA",
    //     "s": "Virginia Department of Environmental Quality",
    //     "sa": "DEQ"
    // }, {
    //     "label": "Wake County",
    //     "a": "Wake County",
    //     "aa": "",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Washington (WA)",
    //     "a": "Washington",
    //     "aa": "WA",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Weatherford (WF)",
    //     "a": "Weatherford",
    //     "aa": "WF",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Wellington (WEF)",
    //     "a": "Wellington",
    //     "aa": "WEF",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Multiple government open data sources",
    //     "a": "Multiple government open data sources",
    //     "aa": "",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Multiple city and local data sources",
    //     "a": "Multiple city and local data sources",
    //     "aa": "",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Multiple state data sources",
    //     "a": "Multiple state data sources",
    //     "aa": "",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "Multiple federal data sources",
    //     "a": "Multiple federal data sources",
    //     "aa": "",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "US Government Printing Office (GPO)",
    //     "a": "US Government Printing Office",
    //     "aa": "GPO",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "US Government Printing Office (GPO) - Congressional Committee Prints",
    //     "a": "US Government Printing Office",
    //     "aa": "GPO",
    //     "s": "Congressional Committee Prints",
    //     "sa": ""
    // }, {
    //     "label": "US Copyright Office",
    //     "a": "US Copyright Office",
    //     "aa": "",
    //     "s": "",
    //     "sa": ""
    // }, {
    //     "label": "United States Postal Service (USPS)",
    //     "a": "United States Postal Service",
    //     "aa": "USPS",
    //     "s": "",
    //     "sa": ""
    // }]
    // try {
    //     $("#agencyTags").autocomplete({
    //         minLength: 2,
    //         source: agencies,
    //         focus: function(event, ui) {
    //             if (ui.item.s == '') {
    //                 $('#agencyTags').val(ui.item.a);
    //             } else {
    //                 $('#agencyTags').val(ui.item.a + " - " + ui.item.s);
    //             }
    //             return false;
    //         },
    //         select: function(event, ui) {
    //             if (ui.item.s == '') {
    //                 $("#searchval").val(ui.item.a);
    //                 $("#agencyTags").val(ui.item.a);
    //             } else {
    //                 $("#searchval").val(ui.item.a + ' - ' + ui.item.s);
    //                 $("#agencyTags").val(ui.item.a + ' - ' + ui.item.s);
    //             }
    //             return false;
    //         }
    //     }).data("ui-autocomplete")._renderItem = function(ul, item) {
    //         if (item.s == '') {
    //             return $("<li></li>")
    //                 .data("ui-autocomplete-item", item)
    //                 .append("<a>" + item.a + "</a>")
    //                 .appendTo(ul);
    //         } else {
    //             return $("<li></li>")
    //                 .data("ui-autocomplete-item", item)
    //                 .append("<a>" + item.a + " - " + item.s + "</a>")
    //                 .appendTo(ul);
    //         }
    //     };
    // } catch (err) {
    //     console.log(err.message);
    // }



});