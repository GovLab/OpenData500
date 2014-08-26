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
        var error_message = $('.company-form-error-message');
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
                        error_message.text('Oops... Something went wrong :/').show().delay(5000).fadeOut();
                    },
                    beforeSend: function(xhr, settings) {
                        //$(event.target).attr('disabled', 'disabled'); 
                        error_message.text('Saving...').show().delay(5000).fadeOut();
                    },
                    success: function(data) {
                        document.location.href = '/' + country + '/addData/' + data['id'];
                    }
                });
            } else {
                error_message.text('You still need to fix some items.').show().delay(5000).fadeOut();
            }
            event.preventDefault();
        });
    }

    //--*****************************************************************-FINISH ADDING DATA-*****************************************************************--//
    var safe_to_submit = false;
    var rm = $('.response-message');
    $("#company-data-comment-form").parsley();
    $("#company-data-form").parsley();
    $('body').on('click', "#submit-all-forms", function() {
        if ($('#company-data-comment-form').parsley().validate() && $('#company-data-form').parsley().validate()) {
            safe_to_submit = true;
        } else {
            safe_to_submit = false;
        }
        if ($(".agency").length == 0) {
            safe_to_submit = false;
            rm.text('You need to enter at least one source of data.').css('opacity', 1).delay(5000).animate({
                'opacity': 0
            }, 500);
        } else if (!safe_to_submit) {
            rm.text('You need to fix some stuff.').css('opacity', 1).delay(5000).animate({
                'opacity': 0
            }, 500);
        }
        if (safe_to_submit) {
            console.log('all cleared');
            var data = $('#company-data-form').serializeArray().concat($('#company-data-comment-form').serializeArray());
            data.push({
                "name": "action",
                "value": "submit-form"
            })
            $.ajax({
                type: 'POST',
                url: '/' + country + '/addData/' + $('#companyID').val(),
                data: data,
                error: function(error) {
                    console.debug(JSON.stringify(error));
                    rm.text('Oops... Something went wrong :/')
                    rm.show().delay(5000).fadeOut();
                },
                beforeSend: function(xhr, settings) {},
                success: function(data) {
                    if (data['response'] != 'error') {
                        document.location.href = '/' + country + '/thanks/';
                    } else {
                        rm.text('Oops... something went wrong').css('opacity', 1).delay(5000).animate({
                            'opacity': 0
                        }, 500);
                    }

                }
            });
        }
    });

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
        $(this).closest('form').parsley().validate('revenueSource');

    });

    //------------------------------ BUSINESS MODEL
    $('.m-form-half').on('focusout', '#other_model_text_field', function(event) {
        if ($('#other_model_text_field').val() == '') {
            $('#other_model').prop('checked', false);
        }
    });
    $('.m-form-half').on('focus', '#other_model_text_field', function() {
        $('#other_model').prop('checked', true);
        $(this).closest('form').parsley().validate('businessModel');
    });

    //------------------------------ SOCIAL IMPACT
    $('.m-form-half').on('focusout', '#other_impact_text_field', function(event) {
        if ($('#other_impact_text_field').val() == '') {
            $('#other_impact').prop('checked', false);
        }
    });
    $('.m-form-half').on('focus', '#other_impact_text_field', function() {
        $('#other_impact').prop('checked', true);
        $(this).closest('form').parsley().validate('socialImpact');
    });

    //------------------------------ CATEGORY
    $('.m-form-half').on('focus', '#other_category_text_field', function() {
        $('#other_category').prop('checked', true);
        $(this).parsley().validate('category');
    });
    $('.m-form-half').on('focusout', '#other_category_text_field', function() {
        if ($('#other_category_text_field').val() == '') {
            $('#other_category').prop('checked', false);
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

    //------------------------------ DATA TYPE
    $('.m-form-half').on('focusout', '#other_data_type_text_field', function(event) {
        if ($('#other_data_type_text_field').val() == '') {
            $('#other_data_type').prop('checked', false);
        }
    });
    $('.m-form-half').on('focus', '#other_data_type_text_field', function() {
        $('#other_data_type').prop('checked', true);
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
    //--*****************************************************************-DELETE DATASET-*****************************************************************--//
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

    //--*****************************************************************-SHOW DELETE ICONS ON HOVER-*****************************************************************--//
    $('#accordionAgency, #accordionSubAgency').on({
        mouseenter: function() {
            $(this).find('.toolbar').show();
        },
        mouseleave: function() {
            $(this).find('.toolbar').hide();
        }
    }, '.agency, .subagency');


    function validURL(url) {
        var re = /^((https?|s?ftp|git):\/\/)?(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i;
        var r = new RegExp(re);
        if (r.test(url)) {
            return true;
        } else {
            return false;
        }
    }

    //--*****************************************************************-AUTOCOMPLETE AGENCIES-*****************************************************************--//
    if ($('#agencyTags') != []) {
        if (country != undefined) {
            $.getJSON("/static/files/" + country + "_Agency_List.json", function(agencies) {
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
    }
});