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

    //--*****************************************************************-VALIDATE & SUBMIT COMPANY FORM-*****************************************************************--//
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

    //--*****************************************************************-ACCORDIONS-*****************************************************************--//
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

    ///--*****************************************************************-CHECKBOX INTERACTIONS-*****************************************************************--//
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
        }
    });

    $('.m-form-half').on('focus', "#other_company_type_field", function() {
        $('input[name="companyType"][value="Other"').prop('checked', true);
    });
    $('.m-form-half').on('focusout', '#other_company_type_field', function() {
        if ($('#other_company_type_field').val() == '') {
            $('input[name="companyType"][value="Other"').prop('checked', false);
        }
    });


    //--*****************************************************************-EXAMPLE POPUP-*****************************************************************--//
    var dialogOptions = {
        autoOpen: false,
        height: 560,
        width: 730,
        modal: true,
        open: function(event, ui) {
            $('.ui-widget-overlay').bind('click', function() {
                $(this).siblings('.ui-dialog').find('.ui-dialog-content').dialog('close');
            });
        }
    };
    $(".m-form-box").on('click', '.example-popup', function() {
        $(".dialog-example").dialog(dialogOptions).dialog("open");
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
        var error_message = $('.agency-search-error-message');
        var this_form = $(this);
        var agency = this_form.attr('agency').replace("delete", "").replace(/-/g, " ");
        var a_id = this_form.attr('a_id');
        var subagency = this_form.attr('subagency').replace("delete", "").replace(/-/g, " ");
        var action = subagency == '' ? 'delete agency' : 'delete subagency';
        this_form.parent().next().remove();
        this_form.closest('h3').remove();
        data = {
            "agency": agency,
            "subagency": subagency,
            "a_id": a_id,
            "action": action,
            "_xsrf": $("[name='_xsrf']").val()
        };
        $.ajax({
            type: 'POST',
            url: '/' + country + '/addData/' + companyID,
            data: data,
            error: function(error) {
                console.debug(JSON.stringify(error));
                error_message.text('Oops... Something went wrong.').css('opacity', 1).delay(5000).animate({
                    'opacity': 0
                }, 500);
            },
            beforeSend: function(xhr, settings) {},
            success: function(response) {
                console.log(response);
                if (response['agency'] == -1) {
                    $("#accordionAgency").accordion({
                        active: false,
                        collapsible: true,
                        autoHeight: false,
                        heightStyle: "content",
                        disabled: false
                    });
                } else if (response['subagency'] == -1) {
                    $("#accordionSubAgency").accordion({
                        active: false,
                        collapsible: true,
                        autoHeight: false,
                        heightStyle: "content",
                        disabled: false
                    });
                } else {
                    error_message.text('Oops... Something went wrong.').css('opacity', 1).delay(5000).animate({
                        'opacity': 0
                    }, 500);
                }
            }
        });
    });
    //--*****************************************************************-ADD/EDIT DATASET-*****************************************************************--//
    var new_dataset_template = '<tr class="dataset-row" name="" subagency="<%= subagency %>" agency="<%= agency %>">' +
        '<td><input type="text" name="<%= dataset_name %>" id="datasetName" value=""></td>' +
        '<td><input type="text" name="datasetURL" id="datasetURL" value=""></td>' +
        '<td><input type="text" name="rating" id="rating" size="3" value=""></td>' +
        '<td><input type="button" class="l-button" id="saveDataset" value="Save"><input type="button" class="l-button" id="deleteDataset" value="Delete" style="display:none">' +
        '<span class="dataset-error-message" style="display:inline-block;"></span></td>' +
        '</tr>';
    $('.agencyList').on('click', '#saveDataset', function(event) {
        var currentDatasetForm = $(this).parent().parent();
        if (currentDatasetForm.parent().find('tr').last().find('#datasetName').val() == '') {
            action = "edit dataset";
            previous_dataset_name = currentDatasetForm.attr('name');
        } else {
            action = "add dataset";
            previous_dataset_name = '';
        }
        var dataset_name = currentDatasetForm.find('#datasetName').val();
        var dataset_url = currentDatasetForm.find('#datasetURL').val();
        var rating = currentDatasetForm.find('#rating').val() == "" ? 0 : currentDatasetForm.find('#rating').val();
        var agency = currentDatasetForm.attr('agency').replace(/-/g, " ");;
        var subagency = currentDatasetForm.attr('subagency').replace(/-/g, " ");
        var error_message = currentDatasetForm.find('.dataset-error-message');
        var validForm = true;
        data = {
            "agency": agency,
            "subagency": subagency,
            "dataset_name": dataset_name,
            "previous_dataset_name": previous_dataset_name,
            "dataset_url": dataset_url,
            "rating": rating,
            "action": action,
            "_xsrf": $("[name='_xsrf']").val()
        }
        if (dataset_name == '') {
            validForm = false;
            error_message.text('You need to at least enter a dataset name.').css('opacity', 1).delay(5000).animate({
                'opacity': 0
            }, 500);
        } else if (!validURL(dataset_url) && dataset_url != '') {
            validForm = false;
            error_message.text('Please enter a valid URL.').css('opacity', 1).delay(5000).animate({
                'opacity': 0
            }, 500);
        } else if (isNaN(rating) || rating > 4 || (rating != '' && rating < 1)) {
            validForm = false;
            error_message.text('Please enter a rating from 1 and 4').css('opacity', 1).delay(5000).animate({
                'opacity': 0
            }, 500);
        }
        console.log(data);
        if (validForm) {
            error_message.text('');
            $.ajax({
                type: 'POST',
                url: '/' + country + '/addData/' + companyID,
                data: data,
                error: function(error) {
                    console.debug(JSON.stringify(error));
                    error_message.text('Oops... Something went wrong.').css('opacity', 1).delay(5000).animate({
                        'opacity': 0
                    }, 500);
                },
                beforeSend: function(xhr, settings) {
                    error_message.text('Saving...').css('opacity', 1).delay(5000).animate({
                        'opacity': 0
                    }, 500);
                },
                success: function(response) {
                    if (response['message'] == 'error') {
                        error_message.text('Oops... Something went wrong.').css('opacity', 1).delay(5000).animate({
                            'opacity': 0
                        }, 500);
                    } else {
                        error_message.text('Saved!').css('opacity', 1).delay(5000).animate({
                            'opacity': 0
                        }, 500);
                        if (action == "add dataset") {
                            var new_dataset = _.template(new_dataset_template);
                            currentDatasetForm.parent().append(new_dataset(data));
                            currentDatasetForm.attr('name', dataset_name);
                            currentDatasetForm.find('#datasetName').attr('name', dataset_name);
                            currentDatasetForm.next().find('#datasetName').focus();
                            currentDatasetForm.find('#deleteDataset').show();
                        } else {
                            currentDatasetForm.attr('name', dataset_name);
                        }
                        console.log(response);
                    }
                }
            });
        }
    });
    //----------------------------------DELETE DATASET--------------------------------------
    $('.agencyList').on('click', '#deleteDataset', function(event) {
        var currentDatasetForm = $(this).parent().parent();
        var dataset_name = currentDatasetForm.find('#datasetName').val();
        var agency = currentDatasetForm.attr('agency').replace(/-/g, " ");
        var subagency = currentDatasetForm.attr('subagency').replace(/-/g, " ");
        var error_message = currentDatasetForm.find('.dataset-error-message');
        data = {
            "agency": agency,
            "subagency": subagency,
            "dataset_name": dataset_name,
            "action": "delete dataset",
            "_xsrf": $("[name='_xsrf']").val()
        };
        if (dataset_name != '') {
            $.ajax({
                type: 'POST',
                url: '/' + country + '/addData/' + companyID,
                data: data,
                error: function(error) {
                    console.debug(JSON.stringify(error));
                    error_message.text('Oops... Something went wrong.').css('opacity', 1).delay(5000).animate({
                        'opacity': 0
                    }, 500);
                },
                beforeSend: function(xhr, settings) {},
                success: function(response) {
                    currentDatasetForm.remove();
                    console.log(response);
                }
            });
        }
    });


    //--*****************************************************************-TEMPLATES FOR AGENCY/DATA FORM-*****************************************************************--//
    var new_agency_template = '<h3 class="agency" name="<%= agency_pretty %>"><a href="#"><%= agency %></a>' +
        '<span style="float:right; display:none;" class="toolbar ui-corner-all ui-icon ui-icon-circle-close red" subagency="" agency="<%= agency_pretty %>"></span>' +
        '</h3>' +
        '<div id="<%= agency_pretty %>Accordion">' +
        '<br><h3>Agency Level Datasets</h3><br>' +
        '<table class="datasetTable">' +
        '<tr>' +
        '<th class="table-header-name">Dataset Name</th>' +
        '<th class="table-header-url">Dataset URL</th>' +
        '<th class="table-header-rating">Rating (1-4)</th>' +
        '<th class="table-header-buttons"></th>' +
        '</tr>' +
        '<tr class="dataset-row" name="" subagency="" agency="<%= agency %>">' +
        '<td><input type="text" name="datasetName" id="datasetName" value="" ></td>' +
        '<td><input type="text" name="datasetURL" id="datasetURL" value="" ></td>' +
        '<td><input type="text" name="rating" id="rating" size="3" value="" ></td>' +
        '<td><input type="button" class="l-button" id="saveDataset" value="Save"><input type="button" class="l-button" id="deleteDataset" value="Delete" style="display:none">' +
        '<span class="dataset-error-message" style="display:inline-block;"></span></td>' +
        '</tr>' +
        '</div>';

    var new_subagency_template = '<h3 class="subagency" name="<%= subagency_pretty %>"><a href="#"><%= subagency %></a>' +
        '<span style="float:right; display:none;" class="toolbar ui-corner-all ui-icon ui-icon-circle-close red" subagency="<%= subagency_pretty %>" agency="<%= agency_pretty %>"></span>' +
        '</h3>' +
        '<div class="<%= subagency_pretty %>Accordion">' +
        '<table class="subagencyDatasetTable">' +
        '<tr>' +
        '<th class="table-header-name">Dataset Name</th>' +
        '<th class="table-header-url">Dataset URL</th>' +
        '<th class="table-header-rating">Rating (1-4)</th>' +
        '<th class="table-header-buttons"></th>' +
        '</tr>' +
        '<tr class="dataset-row" name="" subagency="<%= subagency %>" agency="<%= agency %>">' +
        '<td><input type="text" name="datasetName" id="datasetName" value=""></td>' +
        '<td><input type="text" name="datasetURL" id="datasetURL" value=""></td>' +
        '<td><input type="text" name="rating" id="rating" size="3" value=""></td>' +
        '<td><input type="button" class="l-button" id="saveDataset" value="Save"><input type="button" class="l-button" id="deleteDataset" value="Delete" style="display:none">' +
        '<span class="dataset-error-message" style="display:inline-block;"></span></td>' +
        '</tr>' +
        '</div>';

    //--*****************************************************************-ADD AGENCY FROM SEARCH BAR-*****************************************************************--//
    $('body').on('click', '#addSearchResult', function(event) {
        var error_message = $('.agency-search-error-message');
        var a = $('#searchval').val().trim().split(" - ");
        var agency = a[0];
        var subagency = a[1] != undefined ? a[1] : '';
        var agency_pretty = agency.replace(/ /g, "-");
        var subagency_pretty = subagency.replace(/ /g, "-");
        //var action = subagency == '' ? 'add agency' : 'add subagency';
        var data = {
            "agency": agency,
            "subagency": subagency,
            "agency_pretty": agency_pretty,
            "subagency_pretty": subagency_pretty,
            "action": 'add',
            "_xsrf": $("[name='_xsrf']").val()
        };
        var agency_exists = $('.agency').find('*:contains("' + agency + '")').parent().length != 0;
        var subagency_exists = $('#' + agency_pretty + 'Accordion').find('*:contains("' + subagency + '")').length != 0;
        var response = {
            "message": "",
            "agency": 0,
            "subagency": 0
        };
        var new_agency = _.template(new_agency_template);
        var new_subagency = _.template(new_subagency_template);
        if (agency_exists && subagency_exists) {
            error_message.text('This item is already on the list.').css('opacity', 1).delay(5000).animate({
                'opacity': 0
            }, 500);
        } else if ($('#searchval').val().trim().split(" - ")[0] == "") {
            error_message.text('Please select an item from the list.').css('opacity', 1).delay(5000).animate({
                'opacity': 0
            }, 500);
        } else {
            $.ajax({
                type: 'POST',
                url: '/' + country + '/addData/' + companyID,
                data: data,
                error: function(error) {
                    console.debug(JSON.stringify(error));
                    error_message.text('Oops... Something went wrong.').css('opacity', 1).delay(5000).animate({
                        'opacity': 0
                    }, 500);
                },
                beforeSend: function(xhr, settings) {},
                success: function(_response) {
                    $('#agencyTags').val('');
                    response = _response;
                    console.log(_response);
                    if (response['agency'] == 1) {
                        $('#accordionAgency').append(new_agency(data)).accordion('destroy').accordion({
                            active: false,
                            collapsible: true,
                            autoHeight: false,
                            heightStyle: "content"
                        });
                    }
                    if (response['agency'] == 0 && response['subagency'] == 1) {
                        if ($('#' + agency_pretty + 'Accordion').find('#accordionSubAgency').length == 0) { //first subagency? then add headers
                            $('#' + agency_pretty + 'Accordion').append('<br><h3>Sub-Agencies</h3><br>');
                            $('#' + agency_pretty + 'Accordion').append('<div id="accordionSubAgency" class="' + agency.replace(/ /g, "-") + 'Subagencies">');
                        }
                        $('.' + agency_pretty + 'Subagencies').append(new_subagency(data)).accordion('destroy').accordion({
                            active: false,
                            collapsible: true,
                            autoHeight: false,
                            heightStyle: "content"
                        });
                    }
                    if (response['agency'] == 1 && response['subagency'] == 1) {
                        $('#' + agency_pretty + 'Accordion').append('<br><h3>Sub-Agencies</h3><br>');
                        $('#' + agency_pretty + 'Accordion').append('<div id="accordionSubAgency" class="' + agency_pretty + 'Subagencies">');
                        $('.' + agency_pretty + 'Subagencies').append(new_subagency(data)).accordion({
                            active: false,
                            collapsible: true,
                            autoHeight: false,
                            heightStyle: "content"
                        });
                    }
                }
            });
        }
    });
    // if (agency_exists) {
    //     if (only_add_agency) {
    //         error_message.text('This agency has already been added.').show().delay(5000).animate({
    //             opacity: 0
    //         });
    //     } else if (adding_subagency) {
    //         if (subagency_exists) {
    //             error_message.text('This subagency has already been added.').show().delay(5000).animate({
    //                 opacity: 0
    //             });
    //         } else {
    //             new_subagency = _.template(new_subagency_template);
    //         }
    //     }
    // }
    // var newAgency = '<h3 class="agency" name="' + agency.replace(/ /g, "-") + '"><a href="#">' + agency + '</a>' +
    //     '<span style="float:right; display:none;" class="toolbar ui-corner-all ui-icon ui-icon-circle-close red" subagency="" agency="' + agency.replace(/ /g, "-") + '"></span>' +
    //     '</h3>' +
    //     '<div id="' + agency.replace(/ /g, "-") + 'Accordion">' +
    //     '<br><h3>Agency Level Datasets</h3><br>' +
    //     '<table class="datasetTable">' +
    //     '<tr>' +
    //     '<th class="table-header-name">Dataset Name</th>' +
    //     '<th class="table-header-url">Dataset URL</th>' +
    //     '<th class="table-header-rating">Rating (1-4)</th>' +
    //     '<th class="table-header-buttons"></th>' +
    //     '</tr>' +
    //     '<tr class="dataset-row" subagency="" agency="' + agency.replace(/ /g, "-") + '">' +
    //     '<td><input type="text" name="datasetName" id="datasetName" value=""></td>' +
    //     '<td><input type="text" name="datasetURL" id="datasetURL" value=""></td>' +
    //     '<td><input type="text" name="rating" id="rating" size="3" value=""></td>' +
    //     '<td><input type="button" class="l-button" id="saveDataset" value="Save"><input type="button" class="l-button" id="deleteDataset" value="Delete" style="display:none">' +
    //     '<span class="error-dataset" style="display:none"></span>' +
    //     '<span class="message-dataset" style="display:none"></span></td>' +
    //     '</tr>' +
    //     '</table>' +
    //     '</div>';
    // var newSubagency = '<h3 class="subagency" name="' + subagency.replace(/ /g, "-") + '"><a href="#">' + subagency + '</a>' +
    //     '<span style="float:right; display:none;" class="toolbar ui-corner-all ui-icon ui-icon-circle-close red" subagency="' + subagency.replace(/ /g, "-") + '" agency="' + agency.replace(/ /g, "-") + '"></span>' +
    //     '</h3>' +
    //     '<div class="' + subagency.replace(/ /g, "-") + 'Accordion">' +
    //     '<table class="subagencyDatasetTable">' +
    //     '<tr>' +
    //     '<th class="table-header-name">Dataset Name</th>' +
    //     '<th class="table-header-url">Dataset URL</th>' +
    //     '<th class="table-header-rating">Rating (1-4)</th>' +
    //     '<th class="table-header-buttons"></th>' +
    //     '</tr>' +
    //     '<tr class="dataset-row" subagency="' + subagency.replace(/ /g, "-") + '" agency="' + agency.replace(/ /g, "-") + '">' +
    //     '<td><input type="text" name="datasetName" id="datasetName" value=""></td>' +
    //     '<td><input type="text" name="datasetURL" id="datasetURL" value=""></td>' +
    //     '<td><input type="text" name="rating" id="rating" size="3" value=""></td>' +
    //     '<td><input type="button" class="l-button" id="saveDataset" value="Save"><input type="button" class="l-button" id="deleteDataset" value="Delete" style="display:none">' +
    //     '<span class="error-dataset" style="display:none"></span>' +
    //     '<span class="message-dataset" style="display:none"></span></td>' +
    //     '</tr>' +
    //     '</table>' +
    //     '</div>';
    //     if ($('.agency').find('*:contains("' + agency + '")').parent().length != 0) {
    //         //--AGENCY ALREADY EXISTS, JUST ADD SUBAGENCY--
    //         if (a[1] == undefined) {
    //             //no subagency, and agency already exists, nothing to add. Display error, or just go to that agency/subagency
    //             $('.agenciesExist').show().delay(5000).fadeOut();
    //             safeToAdd = false;
    //         } else {
    //             // --THERE IS A SUBAGENCY TO ADD, CHECK TO SEE IF ALREADY THERE FIRST:
    //             if ($('#' + agency.replace(/ /g, "-") + 'Accordion').find('*:contains("' + subagency + '")').length != 0) {
    //                 //subagency exists, show error. 
    //                 $('.agenciesExist').show().delay(5000).fadeOut();
    //                 safeToAdd = false;
    //             } else {
    //                 //--ADD SUBAGENCY-----IS THIS THE FIRST ONE?----
    //                 if ($('#' + agency.replace(/ /g, "-") + 'Accordion').find('#accordionSubAgency').length == 0) {
    //                     //first time adding a subagency, add header. 
    //                     //console.log("First time adding a subagency");
    //                     $('#' + agency.replace(/ /g, "-") + 'Accordion').append('<br><h3>Sub-Agencies</h3><br>');
    //                     $('#' + agency.replace(/ /g, "-") + 'Accordion').append('<div id="accordionSubAgency" class="' + agency.replace(/ /g, "-") + 'Subagencies">');
    //                     $('#' + agency.replace(/ /g, "-") + 'Accordion').find('#accordionSubAgency').append(newSubagency).accordion({
    //                         active: false,
    //                         collapsible: true,
    //                         autoHeight: false,
    //                         heightStyle: "content"
    //                     });
    //                     safeToAdd = true;
    //                 } else {
    //                     //--ADD SUBAGENCY-----NOT THE FIRST ONE, APPEND TO ACCORDION----
    //                     console.log("adding subagency");
    //                     $('.' + agency.replace(/ /g, "-") + 'Subagencies').append(newSubagency).accordion('destroy').accordion({
    //                         active: false,
    //                         collapsible: true,
    //                         autoHeight: false,
    //                         heightStyle: "content"
    //                     });
    //                     safeToAdd = true;
    //                 }
    //             }
    //         }
    //     } else {
    //         //--ADD BOTH AGENCY AND SUBAGENCY TO ACCORDION--
    //         if (a[1] == undefined) { //no subagency, just add agency
    //             $('#accordionAgency').append(newAgency).accordion('destroy').accordion({
    //                 active: false,
    //                 collapsible: true,
    //                 autoHeight: false,
    //                 heightStyle: "content"
    //             });
    //             safeToAdd = true;
    //         } else { //---FIRST ADD THE AGENCY TO THE ACCORDION--
    //             $('#accordionAgency').append(newAgency).accordion('destroy').accordion({
    //                 active: false,
    //                 collapsible: true,
    //                 autoHeight: false,
    //                 heightStyle: "content"
    //             });
    //             $('#' + agency.replace(/ /g, "-") + 'Accordion').append('<br><h3>Sub-Agencies</h3><br>');
    //             $('#' + agency.replace(/ /g, "-") + 'Accordion').append('<div id="accordionSubAgency" class="' + agency.replace(/ /g, "-") + 'Subagencies">');
    //             $('#' + agency.replace(/ /g, "-") + 'Accordion').find('#accordionSubAgency').append(newSubagency).accordion({
    //                 active: false,
    //                 collapsible: true,
    //                 autoHeight: false,
    //                 heightStyle: "content"
    //             });
    //             safeToAdd = true;
    //         }
    //     }
    //     //---SAVE ADDED AGENCIES TO COMPANY---
    //     if (safeToAdd) {
    //         $.ajax({
    //             type: 'POST',
    //             url: '/' + country + '/addData/' + companyID,
    //             data: data,
    //             error: function(error) {
    //                 console.debug(JSON.stringify(error));
    //                 $('.savingMessage_companyEdit').hide();
    //                 $('.errorMessage_companyEdit').show();
    //             },
    //             beforeSend: function(xhr, settings) {
    //                 $(event.target).attr('disabled', 'disabled');
    //             },
    //             success: function(success) {
    //                 $('#addSearchResult').removeAttr('disabled');
    //                 $('#agencyTags').val('');
    //                 console.log(success);
    //             }
    //         });
    //     }
    // } else {
    //     error_message.text('Please select an item from the provided list.').show().delay(5000).animate({
    //         opacity: 0
    //     });
    // }
    // if (a == 0) {
    //     error_message.text('Please select an item from the provided list.').show().delay(5000).animate({
    //         opacity: 0
    //     });
    // } else {
    //     agency = a[0];
    //     if (a[1] != undefined) {
    //         subagency = a[1];
    //         action = 'add subagency';
    //     } else {
    //         subagency = '';
    //         action = 'add agency';
    //     }
    //     data = {
    //         "agency": agency,
    //         "subagency": subagency,
    //         "action": action,
    //         "_xsrf": $("[name='_xsrf']").val()
    //     };
    //});

    //--*****************************************************************-SHOW DELETE ICONS ON HOVER-*****************************************************************--//
    $('#accordionAgency, #accordionSubAgency').on({
        mouseenter: function() {
            $(this).find('.toolbar').show();
        },
        mouseleave: function() {
            $(this).find('.toolbar').hide();
        }
    }, '.agency, .subagency');

    //--*****************************************************************-FINISH ADDING DATA-*****************************************************************--//
    var rm = $('.response-message');
    $(".data-comment-form").parsley();
    $(".data-comment-form").submit(function(event) {
        $(this).parsley("validate");
        if ($(this).parsley("isValid") && $(".agency").length > 0) {
            var id = $('#companyID').val();
            var data = {
                "dataComments": $('#dataComments').val(),
                "action": "dataComments",
                "id": id,
                "_xsrf": $("[name='_xsrf']").val()
            }
            $.ajax({
                type: 'POST',
                url: '/' + country + '/addData/' + id,
                data: data,
                error: function(error) {
                    console.debug(JSON.stringify(error));
                    rm.text('Oops... Something went wrong :/')
                    rm.show().delay(5000).fadeOut();
                },
                beforeSend: function(xhr, settings) {},
                success: function(data) {
                    document.location.href = '/' + country + '/thanks/';
                }
            });
        } else {
            rm.text('You need to enter at least one source of data.');
        }
        event.preventDefault();
    });



    // $('.finish-data-submit').on('click', '.data-submit-button', function(event) {
    //     if ($('.data-comment-form').parsley().validate()) {
    //         if ($(".agency").length > 0) {
    //             var companyID = $('.companyID').val();
    //             //console.log(companyID);
    //             var data = {
    //                 "dataComments": $('#dataComments').val(),
    //                 "action": "dataComments",
    //                 "_xsrf": $("[name='_xsrf']").val()
    //             };
    //             $.ajax({
    //                 type: 'POST',
    //                 url: '/' + country + '/addData/' + companyID,
    //                 data: data,
    //                 error: function(error) {
    //                     console.debug(JSON.stringify(error));
    //                 },
    //                 beforeSend: function(xhr, settings) {
    //                     $(event.target).attr('disabled', 'disabled');
    //                 },
    //                 success: function(data) {
    //                     console.log(data['result']);
    //                     document.location.href = data['redirect'];
    //                 }
    //             });
    //         } else {
    //             console.log("Must enter at least one data source.")
    //             $(".noInput").show().delay(5000).fadeOut();
    //         }
    //     } else {
    //         console.log("form not valid");
    //     }
    // })

    //----------------------------------SUBMIT FORM--------------------------------------
    // $('.submitCompanyForm').on('click', '#companySubmit', function(event) {
    //     console.log($('#dataComments').parsley('validate'));
    //     //weird parsley thing evaluates empty field to null.
    //     if ($('.companyForm').parsley('validate') && ($('#dataComments').parsley('validate') || $('#dataComments').parsley('validate') == null)) {
    //         $('.savingMessage_companyEdit').show();
    //         var companyID = $('.companyID').val();
    //         var data = $('.companyForm').serializeArray();
    //         data.push({
    //             "name": "dataComments",
    //             "value": $('#dataComments').val()
    //         });
    //         //console.log(data);
    //         $.ajax({
    //             type: 'POST',
    //             url: '/' + country + '/edit/' + companyID,
    //             data: data,
    //             error: function(error) {
    //                 console.debug(JSON.stringify(error));
    //                 $('.savingMessage_companyEdit').hide();
    //                 $('.errorMessage_companyEdit').show().delay(5000).fadeOut();
    //             },
    //             beforeSend: function(xhr, settings) {
    //                 $(event.target).attr('disabled', 'disabled');
    //             },
    //             success: function(data) {
    //                 console.log(data);
    //                 $('.savingMessage_companyEdit').hide();
    //                 $('.savedMessage_companyEdit').show();
    //                 document.location.href = '/thanks/';
    //             }
    //         });
    //     } else {
    //         $('.savingMessage_companyEdit').hide();
    //         $('.errorMessage_companyEdit').show().delay(5000).fadeOut();
    //         //console.log('not valid');
    //     }
    // });
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
    // var dataForm = '<br><br><h2>Agency and Data Information</h2><br>' +
    //     '<div class="m-form-box data">' +
    //     '<h3>Please tell us more about the data your company uses. First tell us which agencies and/or subagencies provide the data your company uses. Then, optionally, tell us specifically which datasets from those agencies/subagencies does your company use. Use the search bar to find agencies and subagencies and select from the list provided.</h3><br>' +
    //     '<div class="ui-widget">' +
    //     '<label for="tags">Agency/Sub-agency Search: </label>' +
    //     '<input id="agencyTags" value="">' +
    //     '<input type="hidden" id="searchval" />' +
    //     '<input type="button" class="l-button" id="addSearchResult" value="Add Agency/Sub-Agency">' +
    //     '<div class="errors-search">' +
    //     '<span class="agenciesExist error-agency-search" style="display:none">Agency or Sub-Agency already on list.</span>' +
    //     '<span class="emptyInput error-agency-search" style="display:none">Nothing to add.</span>' +
    //     '<span class="invalidInput error-agency-search" style="display:none">Please select an item from the provided list.</span>' +
    //     '</div>' +
    //     '</div>' +
    //     '<div class="agencyList">' +
    //     '<div id="accordionAgency">' +
    //     '</div><br>' +
    //     '</div>' +
    //     '</div>';
    // var submitFormHTML = '<h2 class="disclaimer-text">Are you ready to submit this information? You will not be able to come back to this form afterwards. If you wish to make more changes, you will need to contact <a href="mailto:opendata500@thegovlab.org">opendata500@thegovlab.org</a></h2>' +
    //     '<div class="submitCompanyForm">' +
    //     '<input type="hidden" class="companyID" name="companyID" value="{{ id }}">' +
    //     '<input type="button" class="l-button" id="companySubmit" name="submit" value="Save and Finish">' +
    //     '<span class="message-form" style="display:none"></span>' +
    //     '<span class="error-form" style="display:none"></span>' +
    //     '</div>';


    // function clearForm() {
    //     $('.dataForm')[0].reset();
    //     $('.dataForm input:checkbox').removeAttr('checked');
    //     $('#datasetID').val('');
    //     $('#action').val('');
    // }

    function validURL(url) {
        var re = /^((https?|s?ftp|git):\/\/)?(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i;
        var r = new RegExp(re);
        if (r.test(url)) {
            return true;
        } else {
            return false;
        }
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