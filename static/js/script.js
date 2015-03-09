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

    //--*****************************************************************-FINISH ADDING DATA-*****************************************************************--//
    //This submits infor from two different form modules (formData and AddAgency), so it's included in the main script.js file.
    //This is because parsely has to validate fields from both forms. 
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


});