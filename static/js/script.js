$(document).ready(function() {


    var country = $('#country').attr('country');
    if (country == undefined) {
        var url = document.URL;
        if (url.indexOf("/submit") != -1) {
            country = url.substr(url.indexOf('/submit') - 2, 2);
        } else if (url.indexOf("/add") != -1) {
            country = url.substr(url.indexOf('/add') - 2, 2);
        } else if (url.indexOf("/edit") != -1) {
            country = url.substr(url.indexOf('/edit') - 2, 2);
        }
    }
    if (country == "om" || country == "00") {
        country = "us";
    }

    var is_chrome = navigator.userAgent.toLowerCase().indexOf('chrome') > -1;
    var is_firefox = navigator.userAgent.toLowerCase().indexOf('firefox') > -1;

    //----------------------------------VALIDATE AND SUBMIT COMPANY FORM--------------------------------------
    if ($(location).attr('pathname').indexOf('/submitCompany/') > -1) {
        var _xsrf = $("[name='_xsrf']").val();
        var companyName = $("#companyName").parsley()
            .addAsyncValidator('validateName', function(xhr) {
                window.ParsleyUI.removeError(companyName, 'name-exists');
                if (xhr.status === 404) {
                    window.ParsleyUI.addError(companyName, 'name-exists', "This company has already been submitted. Please contact opendata500@thegovlab.org if you have any questions.");
                }

                return xhr.status === 200;
            }, '/validate/?country=' + country + '&_xsrf=' + _xsrf);
        //var parsley_company_form = $("#submitCompany").parsley();
        $("#submitCompany").parsley();

        $("#submitCompany").submit(function(event) {
            $(this).parsley("validate");
            if ($(this).parsley("isValid")) {
                $('.message-form').text('Saving...');
                $('.message-form').show();
                var data = $('.companyForm').serializeArray();
                $.ajax({
                    type: 'POST',
                    url: '/' + country + '/submitCompany/',
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
                        document.location.href = '/' + country + '/addData/' + data['id'];
                    }
                });
            }
            event.preventDefault();
            $('.savingMessage_companyEdit').hide();
            $('.error-form').show().delay(5000).fadeOut();
        });
    }

    //     $('body').on('click', '#companySave-new', function(event) {
    //     //console.log(company_form.validate());
    //     $("#submitCompany").parsley('validate');
    //     if ($("#submitCompany").parsley('isValid')) {
    //         console.log('valid');
    //         $('.message-form').text('Saving...');
    //         $('.message-form').show();
    //         //var companyID = $('.companyID').val();
    //         var data = $('.companyForm').serializeArray();
    //         $.ajax({
    //             type: 'POST',
    //             url: '/' + country + '/submitCompany/',
    //             data: data,
    //             error: function(error) {
    //                 console.debug(JSON.stringify(error));
    //                 $('.message-form').hide();
    //                 $('.error-form').text('Oops... Something went wrong :/')
    //                 $('.error-form').show().delay(5000).fadeOut();
    //             },
    //             beforeSend: function(xhr, settings) {
    //                 //$(event.target).attr('disabled', 'disabled'); 
    //             },
    //             success: function(data) {
    //                 document.location.href = '/' + country + '/addData/' + data['id'];
    //             }
    //         });
    //     } else {
    //         $('.savingMessage_companyEdit').hide();
    //         $('.error-form').show().delay(5000).fadeOut();
    //         console.log('not valid');
    //     }
    // });

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
    $('.m-form-half').on('focusout', '#other_revenue_text_field', function(event) {
        if ($('#other_revenue_text_field').val() == '') {
            $('#other_revenue').prop('checked', false);
        }
    });
    $('.m-form-half').on('focus', '#other_revenue_text_field', function() {
        $('#other_revenue').prop('checked', true);
        $('#submitCompany').parsley().validate('revenueSource');

    });
    $('.m-form-half').on('focus', '#other_category_text_field', function() {
        $('input[name="category"][value="Other"').prop('checked', true);
        $('#submitCompany').parsley().validate('category');
    });
    $('.m-form-half').on('focusout', '#other_category_text_field', function() {
        if ($('#other_category_text_field').val() == '') {
            $('input[name="category"][value="Other"').prop('checked', false);
            //$('#submitCompany').parsley().validate('category');
        }
    });

    $('.m-form-half').on('focus', "#other-company-type", function() {
        $('[name="companyType"]').each(function() {
            this.checked = false;
        });
    });
    $('.m-form-half').on('change', "input[type='radio'][name='companyType']", function() {
        $("#other-company-type").val('');
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
            url: '/' + country + '/addData/' + companyID,
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
                url: '/' + country + '/addData/' + companyID,
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
                url: '/' + country + '/addData/' + companyID,
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
                    url: '/' + country + '/addData/' + companyID,
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
                    url: '/' + country + '/addData/' + companyID,
                    data: data,
                    error: function(error) {
                        console.debug(JSON.stringify(error));
                    },
                    beforeSend: function(xhr, settings) {
                        $(event.target).attr('disabled', 'disabled');
                    },
                    success: function(data) {
                        console.log(data['result']);
                        document.location.href = data['redirect'];
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
                url: '/' + country + '/edit/' + companyID,
                data: data,
                error: function(error) {
                    console.debug(JSON.stringify(error));
                    $('.savingMessage_companyEdit').hide();
                    $('.errorMessage_companyEdit').show().delay(5000).fadeOut();
                },
                beforeSend: function(xhr, settings) {
                    $(event.target).attr('disabled', 'disabled');
                },
                success: function(data) {
                    console.log(data);
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

    //----------------------------------SUBMIT NEW COMPANY-------------------------------------- (USED)
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
    if (country != undefined) {
        $.getJSON("/static/files/" + country + "_Agency_List.json", function(agencies) {
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
    }
});