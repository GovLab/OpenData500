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
                    window.ParsleyUI.addError(companyName, 'name-exists', "Error: This company has already been submitted.");
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
                        error_message.text('Saving...').show();
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
                beforeSend: function(xhr, settings) {
                    rm.text('Saving...').css('opacity', 1);
                },
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

});