
$(document).ready(function() { 

  var agencies = ["Alabama","Alaska","Albuquerque","Ann Arbor","Arctic Landscape Conservation Cooperative","Arizona","Arizona - Arizona Geological Survey","Arkansas","Arvada","Asheville","Atlanta","Austin","Baltimore","Belleville","Boston","Boston - Boston Enterprise GIS","Broadcasting Board of Governors","California","California - California Environmental Health Tracking Program","California - California Department of Resources","Champaign","Chicago","City of Orem","Colorado","Colorado - Denver Regional Council","Columbia University - Center for International Earth Science Information Network","Commodity Futures Trading Commission","Connecticut","Consumer Financial Protection Bureau","Cook County","Cornell University","Corporation for National and Community Service","Court Services and Offender Supervision Agency","Delaware","Denver","Department of Agriculture - Agricultural Marketing Service","Department of Agriculture - Agricultural Research Service","Department of Agriculture - Animal and Plant Health Inspection Service","Department of Agriculture","Department of Agriculture - Departmental Management","Department of Agriculture - Economic Research Service","Department of Agriculture - Farm Service Agency","Department of Agriculture - Food and Nutrition Service","Department of Agriculture - Food Safety and Inspection Service","Department of Agriculture - Foreign Agricultural Service","Department of Agriculture - National Agricultural Statistics Service","Department of Agriculture - National Appeals Division","Department of Agriculture - National Institute of Food and Agriculture","Department of Agriculture - Natural Resources Conservation Service","Department of Agriculture - Office of the Chief Economist","Department of Agriculture - Rural Development","Department of Agriculture - US Forest Service","Department of Commerce","Department of Commerce - Bureau of Economic Analysis","Department of Commerce - Bureau of Industry and Security","Department of Commerce - US Patent and Trademark Office","Department of Commerce - International Trade Administration","Department of Commerce - National Institute of Standards and Technology","Department of Commerce - National Oceanic and Atmospheric Administration","Department of Commerce - National Technical Information Service","Department of Commerce - National Telecommunication and Information Administration","Department of Commerce - National Weather Service","Department of Commerce - US Census Bureau","Department of Defense - Army Corps of Engineers","Department of Defense - Acquisition Technology and Logistics","Department of Defense","Department of Defense - National Geospatial Intelligence Agency","Department of Defense - Defense Logistics Agency","Department of Defense - Defense Technical Information Center","Department of Defense - Department of the Army","Department of Defense - Federal Voting Assistance Program","Department of Education","Department of Education - Federal Student Aid","Department of Education - Institute of Education Sciences","Department of Education - National Center for Education Statistics","Department of Education - Office for Civil Rights","Department of Education - Office of Hearings and Appeals","Department of Education - Office of Innovation and Improvement","Department of Education - Office of Postsecondary Education","Department of Education - Office of Special Education and Rehabilitative Services","Department of Education - Office of Vocational and Adult Education","Department of Energy","Department of Energy - Energy Information Administration","Department of Energy - Office of Scientific and Technical Information","Department of Health and Human Services - Centers for Medicare and Medicaid Services","Department of Health and Human Services","Department of Health and Human Services - National Institutes of Health","Department of Health and Human Services - Substance Abuse and Mental Health Services Administration","Department of Homeland Security - U.S. Coast Guard","Department of Homeland Security","Department of Homeland Security - Federal Emergency Management Agency","Department of Homeland Security - United States Coast Guard","Department of Homeland Security - Office of Health Affairs","Department of Homeland Security - Office of Immigration Statistics","Department of Homeland Security - U.S. Citizenship and Immigration Services","Department of Housing and Urban Development - Office of Housing","Department of Justice","Department of Justice - Antitrust Division","Department of Justice - Bureau of Justice Statistics","Department of Justice - Civil Division","Department of Justice - Civil Rights Division","Department of Justice - Federal Bureau of Investigation","Department of Justice - US Trustee Program","Department of Justice - Office of Legal Counsel","Department of Justice - US Attorney's Office","Department of Labor - Benefits Review Board","Department of Labor - Bureau of Labor Statistics","Department of Labor - Employee Benefits Security Administration","Department of Labor - Employees' Compensation Appeals Board","Department of Labor - Employment and Training Administration","Department of Labor - Mine Safety and Health Administration","Department of Labor","Department of Labor - Occupational Safety and Health Administration","Department of Labor - Office of Administrative Law Judges","Department of Labor - Wage and Hour Division","Department of Labor - Office of Job Corps","Department of Labor - Office of the Assistant Secretary for Policy","Department of State","Department of State - Organisation for Economic Cooperation and Development","Department of the Interior","Department of the Interior - Bureau of Indian Education","Department of the Interior - Bureau of Land Management","Department of the Interior - Bureau of Ocean Energy Management","Department of the Interior - National Park Service","Department of the Interior - Office of Hearings and Appeals","Department of the Interior - Federal Geographic Data Committee","Department of the Interior - U.S. Geological Survey","Department of the Interior - Office of the Solicitor","Department of the Interior - US Bureau of Reclamation","Department of the Interior - US Fish and Wildlife Service","Department of the Treasury","Department of the Treasury - Bureau of Engraving and Printing","Department of the Treasury - Bureau of the Public Debt","Department of the Treasury - Departmental Offices","Department of the Treasury - Financial Crimes Enforcement Network","Department of the Treasury - Financial Management Service","Department of the Treasury - Internal Revenue Service","Department of the Treasury - United States Mint","Department of Transportation - National Highway Traffic Safety Administration","Department of Transportation","Department of Transportation - Bureau of Transportation Statistics","Department of Transportation - Federal Aviation Administration","Department of Transportation - Federal Highway Administration","Department of Transportation - Federal Motor Carrier Safety Administration","Department of Transportation - Federal Railroad Administration","Department of Transportation - Federal Transit Administration","Department of Transportation - Maritime Administration","Department of Transportation - National Highway Traffice Safety Administration","Department of Transportation - Office of the Secretary of Transportation","Department of Transportation - Pipeline and Hazardous Materials Safety Administration","Department of Transportation - Research and Innovative Technology Administration","Department of Transportation - Saint Lawrence Seaway Development Corporation","Department of Transportation - Surface Transportation Board","Department of Veterans Affairs - National Cemetery Administration","Department of Veterans Affairs","Department of Veterans Affairs - Veterans Benefits Administration","Department of Veterans Affairs - Veterans Health Administration","Department of Veterans Affairs - Environmental Protection Agency","District of Columbia","Election Assistance Commission","Executive Office of the President - Networking and Information Technology Research and Development","Executive Office of the President - Council on Environmental Quality","Executive Office of the President - Office of Management and Budget","Executive Office of the President - Office of National Drug Control Policy","Executive Office of the President - Office of Science and Technology Policy","Executive Office of the President","Executive Office of the President - US Trade Representative","Executive Office of the President - White House","Export-Import Bank of the US","Federal Communications Commission","Federal Deposit Insurance Corporation","Federal Election Commission","Federal Geographic Data Committee","Federal Government - Department of Housing and Urban Development","Federal Housing Finance Agency","Federal Reserve Board","Florida","General Services Administration","General Services Administration - Federal Acquisition Service","General Services Administration - Office of Citizen Services and Innovative Technologies","General Services Administration - Office of Governmentwide Policy","General Services Administration - Office of Performance Improvement","General Services Administration - Office of the Chief Financial Officer","General Services Administration - Office of the Chief People Officer","General Services Administration - Public Buildings Service","Georgia","Gilpin County","Great Lakes Commission","Hawaii","Hawaii - Hawaii GIS","Honolulu","Houston","Idaho - Coeur d'Alene Tribe","Idaho State University","Illinois","Illinois - South Suburban Mayors and Managers","Indiana","Information Sharing Environment","Institute of Museum and Library Services","Iowa","Iowa State University GIS Support and Research Facility","Kansas","Kansas - Kansas Data Access and Support Center","Kansas City","Kentucky","Kentucky - Kentucky Geography Network","King County","Las Vegas","Lexington","Los Angeles","Louisiana","Louisiana - Louisiana Geographic Information Center","Louisville","Madison","Maine","Maryland","Massachusetts","Merit Systems Protection Board","Michigan","Millenium Challenge Corporation","Minneapolis-St Paul - MetroGIS (Minneapolis-St. Paul Regional GIS Consortium)","Minnesota - Minnesota Department of Natural Resources","Minnesota","Missouri","Missouri - Accountability Portal","Missouri - Missouri Spatial Data Information Service","Montana","Montgomery County","National Aeronautics and Space Administration - Jet Propulsion Laboratory","National Aeronautics and Space Administration","National Archives and Records Administration","National Archives and Records Administration - Office of the Federal Register","National Capital Planning Commission","National Endowment for the Arts","National Endowment for the Humanities","National Labor Relations Board","National Science Foundation","National States Geographic Information Council - GIS Inventory (aka Ramona)","National Transportation Safety Board","Nebraska","New Hampshire","New Mexico","New Orleans","New York","New York - NY State Senate","New York - New York State Data Center","New York - NY Department of Health","New York City","North Carolina - NC OpenBook","North Carolina","North Dakota - North Dakota GIS Hub","North Dakota","Nuclear Regulatory Commission","Nuna Technologies","Oak Ridge National Laboratory","Occupational Safety and Health Review Commission","Office of Navajo and Hopi Indian Relocation","Office of Personnel Management","Ohio","Oklahoma","Open Door Kentucky","Oregon","Oregon State University","Overseas Private Investment Corporation","Pacific States Marine Fisheries Commission","Palo Alto","Pension Benefit Guaranty Corporation","Philadelphia","Portland","Providence","Railroad Retirement Board","Raleigh","Rhode Island","Rockford","San Francisco","San Mateo County","Santa Cruz","Scottsdale","Seattle","Securities and Exchange Commission","Selective Service System","Small Business Administration","Social Security Administration","Somerville","South Bend","South Dakota","Tennessee","Texas","Texas - Texas Transparency","U.S. Department of Health & Human Services","U.S. Environmental Protection Agency","Univ of South Carolina - Baruch Institute for Marine and Coastal Sciences","University of Alaska - Geographic Information Network of Alaska - University of Alaska","University of Arizona","University of California San Diego","University of Idaho","University of New Hampshire","University of New Mexico - Earth Data Analysis Center","University of Rhode Island - University of Rhode Island Geospatial Extension Program","University of Washington","US Agency for International Development","US Consumer Product Safety Commission","US Equal Employment Opportunity Commission","US International Trade Commission","US Office of the Special Counsel","Utah","Virginia","Virginia - Virginia Department of Environmental Quality","Wake County","Washington","Weatherford","Wellington","Department of Defense - Defense Advanced Research Projects Agency"];
  //----------------------------------ADMIN ACCORDIONS--------------------------------------
  $(function() {
      $( "#accordionUnvetted" ).accordion({
        collapsible: true,
        autoHeight: false
      });
    });

  $(function() {
      $( "#accordionVetted" ).accordion({
        collapsible: true
      });
    });

  $(function() {
      $( "#accordionSubmitted" ).accordion({
        collapsible: true,
        autoHeight: false
      });
    });

  var companyID = $('.companyID').val();
  //----------------------------------UNCHECK OTHER BOX IF INPUT EMPTY--------------------------------------
  $('.m-form-half').on('focusout', '#otherRevenueSource', function() {
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
  var dialogOptions ={
      autoOpen: false,
      height: 560,
      width: 730,
      modal: true,
      //close: function(event, ui) { $('.example-popup').dialog('close'); },
      open: function(event, ui) { $('.ui-widget-overlay').bind('click', function () { $(this).siblings('.ui-dialog').find('.ui-dialog-content').dialog('close'); }); }
    };
  $(".m-form-box").on('click', '.example-popup', function() {
    $( ".dialog-example" ).dialog(dialogOptions).dialog( "open" );
    //$("#dialog").dialog({autoOpen : false, modal : true, show : "blind", hide : "blind"});
  });

  //----------------------------------DATA ACCORDIONS--------------------------------------
  $( "#accordionAgency, #accordionSubAgency" ).accordion({
    active: false,
    collapsible: true,
    autoHeight: false,
    heightStyle: "content"
  });
  //----------------------------------DELETE AGENCIES AND SUBAGENCIES--------------------------------------
  $('#accordionAgency, #accordionSubAgency').on('click', '.toolbar', function(e){
    agency = $(this).attr('agency').replace("delete", "").replace(/-/g, " ");
    subagency = $(this).attr('subagency').replace("delete", "").replace(/-/g, " ");
    //console.log(agency + subagency);
    data = { "agency": agency, "subagency": subagency, "action": "delete agency", "_xsrf": $("[name='_xsrf']").val() };
    //console.log($(this).closest('h3'));
    $(this).parent().next().remove();
    $(this).closest('h3').remove();
    if (subagency == '') {
      $( "#accordionAgency" ).accordion({
        active: false,
        collapsible: true,
        autoHeight: false,
        heightStyle: "content"
      });
    } else {
      $( "#accordionSubAgency" ).accordion({
          active: false,
          collapsible: true,
          autoHeight: false,
          heightStyle: "content"
        });
    }
      $.ajax({
      type: 'POST',
      url: '/addData/'+companyID,
      data: data,
      error: function(error) {
          console.debug(JSON.stringify(error));
          $('.savingMessage_companyEdit').hide();
          $('.errorMessage_companyEdit').show(); },
      beforeSend: function(xhr, settings) {
        $(event.target).attr('disabled', 'disabled'); },
      success: function(success) {
        $('.toolbar').removeAttr('disabled');
        console.log(success);
      }
    });
  });
  //----------------------------------SAVE NEW DATASET AND ADD NEW EMPTY FORM--------------------------------------
  $('.agencyList').on('click', '#saveDataset', function() {
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
    var datasetForm = '<tr class="dataset-row" name="" subagency="'+subagency.replace(/ /g, "-")+'" agency="'+agency.replace(/ /g, "-")+'">'+
                '<td><input type="text" name="datasetName" id="datasetName" value=""></td>'+
                '<td><input type="text" name="datasetURL" id="datasetURL" value=""></td>'+
                '<td><input type="text" name="rating" id="rating" size="3" value=""></td>'+
                '<td><input type="button" class="l-button" id="saveDataset" value="Save"><input type="button" class="l-button" id="deleteDataset" value="Delete" style="display:none">'+
                  '<span class="error-dataset" style="display:none"></span>'+
                  '<span class="message-dataset" style="display:none"></span></td>'+
              '</tr>';
    data = { "agency": agency, "subagency": subagency, "datasetName":datasetName, "previousDatasetName": previousDatasetName, "datasetURL": datasetURL, "rating": rating, "action": action, "_xsrf": $("[name='_xsrf']").val() }
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
      } else if ( isNaN(rating) || rating > 4 || (rating != '' && rating < 1)) {
        validForm = false;
        currentDatasetForm.find('.message-dataset').hide();
        currentDatasetForm.find('.error-dataset').text('Invalid Rating')
        currentDatasetForm.find('.error-dataset').show().delay(5000).fadeOut();
      }
      if (validForm) {
        currentDatasetForm.find('.error-dataset').hide();
        $.ajax({
        type: 'POST',
        url: '/addData/'+companyID,
        data: data,
        error: function(error) {
            console.debug(JSON.stringify(error));
              currentDatasetForm.find('.message-dataset').hide();
              currentDatasetForm.find('.error-dataset').text('Oops... Server Error :/');
              currentDatasetForm.find('.error-dataset').show().delay(5000).fadeOut(); },
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
  $('.agencyList').on('click', '#deleteDataset', function() {
    currentDatasetForm = $(this).parent().parent();
    datasetName = currentDatasetForm.find('#datasetName').val();
    agency = currentDatasetForm.attr('agency').replace(/-/g, " ");
    subagency = currentDatasetForm.attr('subagency').replace(/-/g, " ");
    data = { "agency": agency, "subagency": subagency, "datasetName": datasetName, "action": "delete dataset", "_xsrf": $("[name='_xsrf']").val() };
    if (datasetName != '') {
      $.ajax({
        type: 'POST',
        url: '/addData/'+companyID,
        data: data,
        error: function(error) {
            console.debug(JSON.stringify(error));
              currentDatasetForm.find('.error-dataset').text('Oops... Server Error :/');
              currentDatasetForm.find('.error-dataset').show().delay(5000).fadeOut(); },
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
  $('body').on('click', '#addSearchResult', function () {
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
      data = { "agency": agency, "subagency": subagency, "action": "add agency", "_xsrf": $("[name='_xsrf']").val() };
      var safeToAdd = false;
      var newAgency = '<h3 class="agency" name="'+agency.replace(/ /g, "-")+'"><a href="#">'+ agency +'</a>'+
                '<span style="float:right; display:none;" class="toolbar ui-corner-all ui-icon ui-icon-circle-close red" subagency="" agency="'+agency.replace(/ /g, "-")+'"></span>'+
              '</h3>'+
              '<div id="'+ agency.replace(/ /g, "-") +'Accordion">'+
                '<br><h3>Agency Level Datasets</h3><br>'+
                '<table class="datasetTable">'+
                  '<tr>'+
                    '<th class="table-header-name">Dataset Name</th>'+
                    '<th class="table-header-url">Dataset URL</th>'+
                    '<th class="table-header-rating">Rating (1-4)</th>'+
                    '<th class="table-header-buttons"></th>'+
                  '</tr>'+
                  '<tr class="dataset-row" subagency="" agency="'+agency.replace(/ /g, "-")+'">'+
                    '<td><input type="text" name="datasetName" id="datasetName" value=""></td>'+
                    '<td><input type="text" name="datasetURL" id="datasetURL" value=""></td>'+
                    '<td><input type="text" name="rating" id="rating" size="3" value=""></td>'+
                    '<td><input type="button" class="l-button" id="saveDataset" value="Save"><input type="button" class="l-button" id="deleteDataset" value="Delete" style="display:none">'+
                      '<span class="error-dataset" style="display:none"></span>'+
                      '<span class="message-dataset" style="display:none"></span></td>'+
                  '</tr>'+
                '</table>'+
              '</div>';
      var newSubagency = '<h3 class="subagency" name="'+subagency.replace(/ /g, "-")+'"><a href="#">' +subagency+ '</a>'+
                  '<span style="float:right; display:none;" class="toolbar ui-corner-all ui-icon ui-icon-circle-close red" subagency="'+subagency.replace(/ /g, "-")+'" agency="'+agency.replace(/ /g, "-")+'"></span>'+
                '</h3>'+
                '<div class="' + subagency.replace(/ /g, "-") + 'Accordion">'+
                  '<table class="subagencyDatasetTable">'+
                    '<tr>'+
                      '<th class="table-header-name">Dataset Name</th>'+
                      '<th class="table-header-url">Dataset URL</th>'+
                      '<th class="table-header-rating">Rating (1-4)</th>'+
                      '<th class="table-header-buttons"></th>'+
                    '</tr>'+
                    '<tr class="dataset-row" subagency="'+subagency.replace(/ /g, "-")+'" agency="'+agency.replace(/ /g, "-")+'">'+
                      '<td><input type="text" name="datasetName" id="datasetName" value=""></td>'+
                      '<td><input type="text" name="datasetURL" id="datasetURL" value=""></td>'+
                      '<td><input type="text" name="rating" id="rating" size="3" value=""></td>'+
                      '<td><input type="button" class="l-button" id="saveDataset" value="Save"><input type="button" class="l-button" id="deleteDataset" value="Delete" style="display:none">'+
                        '<span class="error-dataset" style="display:none"></span>'+
                        '<span class="message-dataset" style="display:none"></span></td>'+
                    '</tr>'+
                  '</table>'+
                '</div>';
      if ($('.agency').find('*:contains("'+agency+'")').parent().length != 0) {
        //--AGENCY ALREADY EXISTS, JUST ADD SUBAGENCY--
        if (a[1] == undefined ){
          //no subagency, and agency already exists, nothing to add. Display error, or just go to that agency/subagency
          $('.agenciesExist').show().delay(5000).fadeOut();
          safeToAdd = false;
        } else {
          // --THERE IS A SUBAGENCY TO ADD, CHECK TO SEE IF ALREADY THERE FIRST:
          if ($('#'+agency.replace(/ /g, "-")+'Accordion').find('*:contains("'+subagency+'")').length !=0 ) {
            //subagency exists, show error. 
            $('.agenciesExist').show().delay(5000).fadeOut();
            safeToAdd = false;
          } else {
            //--ADD SUBAGENCY-----IS THIS THE FIRST ONE?----
            if ($('#'+agency.replace(/ /g, "-")+'Accordion').find('#accordionSubAgency').length == 0) {
              //first time adding a subagency, add header. 
              //console.log("First time adding a subagency");
              $('#'+agency.replace(/ /g, "-")+'Accordion').append('<br><h3>Sub-Agencies</h3><br>');
              $('#'+agency.replace(/ /g, "-")+'Accordion').append('<div id="accordionSubAgency" class="' + agency.replace(/ /g, "-") + 'Subagencies">');
              $('#'+agency.replace(/ /g, "-")+'Accordion').find('#accordionSubAgency').append(newSubagency).accordion({
                active: false,
                collapsible: true,
                autoHeight: false,
                heightStyle: "content"
                });
                safeToAdd = true;
            } else {
              //--ADD SUBAGENCY-----NOT THE FIRST ONE, APPEND TO ACCORDION----
              console.log("adding subagency");
              $('.'+agency.replace(/ /g, "-")+'Subagencies').append(newSubagency).accordion('destroy').accordion({
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
            safeToAdd =true;
        } else { //---FIRST ADD THE AGENCY TO THE ACCORDION--
          $('#accordionAgency').append(newAgency).accordion('destroy').accordion({
            active: false,
            collapsible: true,
            autoHeight: false,
            heightStyle: "content"
            });
            $('#'+agency.replace(/ /g, "-")+'Accordion').append('<br><h3>Sub-Agencies</h3><br>');
            $('#'+agency.replace(/ /g, "-")+'Accordion').append('<div id="accordionSubAgency" class="'+agency.replace(/ /g, "-")+'Subagencies">');
            $('#'+agency.replace(/ /g, "-")+'Accordion').find('#accordionSubAgency').append(newSubagency).accordion({
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
          url: '/addData/'+companyID,
          data: data,
          error: function(error) {
              console.debug(JSON.stringify(error));
              $('.savingMessage_companyEdit').hide();
              $('.errorMessage_companyEdit').show(); },
          beforeSend: function(xhr, settings) {
            $(event.target).attr('disabled', 'disabled'); },
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
  //----------------------------------SUBMIT FORM--------------------------------------
  $('.submitCompanyForm').on('click', '#companySubmit', function() {
    if ($('.companyForm').parsley('validate')) {
      console.log('valid');
      $('.savingMessage_companyEdit').show();
      var companyID = $('.companyID').val();
      var data = $('.companyForm').serializeArray();
      $.ajax({
        type: 'POST',
        url: '/edit/' + companyID,
        data: data,
        error: function(error) {
            console.debug(JSON.stringify(error));
            $('.savingMessage_companyEdit').hide();
            $('.errorMessage_companyEdit').show().delay(5000).fadeOut(); },
        beforeSend: function(xhr, settings) {
          $(event.target).attr('disabled', 'disabled'); },
        success: function(success) {
          console.log(success);
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
  $('.saveCompanyForm').on('click', '#companySave', function() {
    if ($('.companyForm').parsley('validate')) {
      console.log('valid');
      $('.message-form').text('Saving...');
      $('.message-form').show();
      var companyID = $('.companyID').val();
      var data = $('.companyForm').serializeArray();
      $.ajax({
        type: 'POST',
        url: '/edit/' + companyID,
        data: data,
        error: function(error) {
            console.debug(JSON.stringify(error));
            $('.message-form').hide();
            $('.error-form').text('Oops... Something went wrong :/')
            $('.error-form').show().delay(5000).fadeOut(); },
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
  var dataForm =  '<br><br><h2>Agency and Data Information</h2><br>'+
                          '<div class="m-form-box data">'+
                          '<h3>Please tell us more about the data your company uses. First tell us which agencies and/or subagencies provide the data your company uses. Then, optionally, tell us specifically which datasets from those agencies/subagencies does your company use. Use the search bar to find agencies and subagencies and select from the list provided.</h3><br>'+
                          '<div class="ui-widget">'+
                            '<label for="tags">Agency/Sub-agency Search: </label>'+
                            '<input id="agencyTags" value="">'+
                            '<input type="hidden" id="searchval" />'+
                            '<input type="button" class="l-button" id="addSearchResult" value="Add Agency/Sub-Agency">'+
                            '<div class="errors-search">'+
                              '<span class="agenciesExist error-agency-search" style="display:none">Agency or Sub-Agency already on list.</span>'+
                              '<span class="emptyInput error-agency-search" style="display:none">Nothing to add.</span>'+
                              '<span class="invalidInput error-agency-search" style="display:none">Please select an item from the provided list.</span>'+
                            '</div>'+
                          '</div>'+
                          '<div class="agencyList">'+
                            '<div id="accordionAgency">'+
                            '</div><br>'+
                          '</div>'+
                        '</div>';
  var submitFormHTML = '<h2 class="disclaimer-text">Are you ready to submit this information? You will not be able to come back to this form afterwards. If you wish to make more changes, you will need to contact <a href="mailto:opendata500@thegovlab.org">opendata500@thegovlab.org</a></h2>'+
                                '<div class="submitCompanyForm">'+
                                  '<input type="hidden" class="companyID" name="companyID" value="{{ id }}">'+
                                  '<input type="button" class="l-button" id="companySubmit" name="submit" value="Save and Finish">'+
                                  '<span class="message-form" style="display:none"></span>'+
                                  '<span class="error-form" style="display:none"></span>'+
                                '</div>';
  $('body').on('click', '#companySave-new', function() {
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
            $('.error-form').show().delay(5000).fadeOut(); },
        beforeSend: function(xhr, settings) {
          //$(event.target).attr('disabled', 'disabled'); 
        },
        success: function(data) {
          document.location.href = '/addData/'+data['id'];
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
  //----------------------------------OLD DATA HANDLERS TO DEPRECATE--------------------------------------
  // var form = '<div class="m-form-half left">'+
  //         '<div class="dataFormTitle"></div>'+
  //         '<div class="m-form-line"><label for="datasetName">Name of Dataset: * </label><input type="text" name="datasetName" parsley-trigger="change" parsley-required="true">'+
  //         '</div>'+
  //         '<div class="m-form-line"><label for="datasetURL">URL of Dataset: * </label><input type="text" name="datasetURL" parsley-required="true" parsley-trigger="change" parsley-type="url">'+
  //         '</div>'+
  //         '<div class="m-form-line"><label for="agency">Agency or Source: * </label><input type="text" name="agency" parsley-required="true" parsley-trigger="change"></div>'+
  //         '<h3>Type of Dataset: *</h3>'+
  //         '<label for=""><input type="checkbox" name="typeOfDataset" value="Federal Open Data">Federal Open Data</label><br>'+
  //         '<label for=""><input type="checkbox" name="typeOfDataset" value="State Open Data">State Open Data</label><br>'+
  //         '<label for=""><input type="checkbox" name="typeOfDataset" value="City/Local Open Data">City/Local Open Data</label><br>'+
  //         '<label for=""><input type="checkbox" name="typeOfDataset" parsley-required="true" value="Other">Other <label for=""><input type="text" parsley-regexp="[a-zA-Z0-9.,-\s\/\)\(]" parsley-regexp-flag="i" parsley-trigger="keyup" name="otherTypeOfDataset"></label></label>'+
  //         '<h3>On a scale of 1 to 4, how would you rate the usefulness of this dataset? (1- poor, 4- excellent) Your answer can reflect your experience with data quality, format of the data, or other factors.</h3>'+
  //         '<input type="text" name="rating" parsley-trigger="change" parsley-range="[0, 4]">'+
  //         '<h3>Why did you give it this rating? [50 words or less]</h3>'+
  //         '<textarea rows="6" cols="70" name="reason" parsley-trigger="keyup" parsley-maxwords="50"></textarea><br>'+
  //         '<input type="hidden" id="companyID" name="companyID" value="{{ id }}">'+
  //         '<input type="hidden" id="datasetID" name="datasetID" value="">'+
  //         '<input type="hidden" id="action" name="action" value="Add New">'+
  //         '{% raw xsrf_form_html() %}'+
  //         '<input type="button" name="addData" class="m-button" id="addNew" value="Add" style="display:none">'+
  //         '<input type="button" name="saveData" class="m-button" id="saveData" value="Save Edits" style="display:none">'+
  //         '<input type="button" name="cancel" class="m-button" id="cancel" value="Cancel">'+
  //         '<input type="button" name="deleteData" class="m-button" id="deleteData" value="Delete Dataset" style="display:none">'+
  //         '<span class="errorMessage" style="display:none">Oops, something went wrong</span>'+
  //         '<span class="savingMessage" style="display:none">Saving...</span>'+
  //     '</div>'+
  //     '<div class="m-form-half right">'+
  //       '<div class="m-form-line"><label for="agencySearch">Search For Agency: </label><input type="text" name="agencySearch"></div>'+
  //       '<div class="m-form-line"><label for="agencyName">Agency Name</label><input type="text" name="agencyName" parsley-required="true" parsley-trigger="change"></div>'+
  //       '<div class="m-form-line"><label for="subagencyName">Sub Agency Name</label><input type="text" name="subagencyName"></div>'+
  //     '</div>';
  // var currentDataset = '';
  // $('.newSingleDataset').on( 'click', '#addDataset', function( event ) {
  //   $('#addDataset').hide();
  //   $.each($('.dataForm'), function() {
  //     $(this).hide();
  //     $(this).html('');
  //     currentDataset = '';
  //   });
  //   $.each($('.editData'), function() {
  //     $(this).show();
  //   });
  //   $('#dataFormContainer').show();
  //   $('#dataFormContainer').html(form);
  //   $('.dataFormTitle').html('<h3>New Dataset</h3>');
  //   $('#addNew').show();
  // });
  // $('.dataList').on( 'click', '.editData', function( event ) {
  //   currentDataset = '';
  //   $.each($('.editData'), function() {
  //     $(this).show();
  //   });
  //   $.each($('.dataForm'), function() {
  //     $(this).hide();
  //     $(this).html('');
  //   });
  //   var datasetName = $(this).attr('datasetname');
  //   console.log(datasetName);
  //   currentDataset = datasetName;
  //   $('.editData[datasetname='+currentDataset+']').hide();
  //   $('#dataFormContainer_'+currentDataset).show();
  //   $('#dataFormContainer_'+currentDataset).html(form);
  //   $('.dataFormTitle').html('<h3>Editing '+currentDataset.replace(/_/g, " ")+'</h3>');
  //   $('#saveData').show();
  //   $('#deleteData').show();
  //   //Get Values to Fill Fields, then fill fields
  //   $("input[name='datasetName']").val(currentDataset.replace(/_/g, " "));
  //   var datasetURL = $("div[datasetname='"+currentDataset+"']").attr('dataseturl');
  //   $("input[name='datasetURL']").val(datasetURL);
  //   var agency = $("div[datasetname='"+currentDataset+"']").attr('agency');
  //   $("input[name='agency']").val(agency);
  //   var otherTypeOfDataset = $("div[datasetname='"+currentDataset+"']").attr('otherTypeOfDataset');
  //   if (otherTypeOfDataset != '') {
  //     $(".singleDataset input:checkbox[value='Other']").prop("checked", true);
  //     $("input[name='otherTypeOfDataset']").val(otherTypeOfDataset);
  //   } else {
  //     $(".singleDataset input:checkbox[value='Other']").prop("checked", false);
  //     $("input[name='otherTypeOfDataset']").val();
  //   }
  //   var typeOfDataset = $("div[datasetname='"+currentDataset+"']").attr('typeOfDataset').split(",");
  //   for (var i = 0; i < typeOfDataset.length; i++) {
  //     $(".dataForm input:checkbox[value='" + typeOfDataset[i] + "']").prop("checked", true);
  //   }
  //   var rating = $("div[datasetname='"+currentDataset+"']").attr('rating');
  //   $("input[name='rating']").val(rating);
  //   var reason = $("div[datasetname='"+currentDataset+"']").attr('reason');
  //   $("textarea[name='reason']").val(reason);
  //   var datasetID = $("div[datasetname='"+currentDataset+"']").attr('datasetID');
  //   $("input[name='datasetID']").val(datasetID);
  // });
  // $('.datasets').on( 'click', '#cancel', function( event ) {
  //   $.each($('.dataForm'), function() {
  //     $(this).hide();
  //     $(this).html('');
  //   });
  //   $.each($('.editData'), function() {
  //     $(this).show();
  //   });
  //   currentDataset = '';
  // });
  // $('.datasets').on( 'click', '#deleteData', function( event ) {
  //   event.preventDefault();
  //   var id_to_delete = $('#datasetID').val();
  //   var data = $('#dataFormContainer_'+currentDataset).serializeArray();
  //   $.ajax({
  //     type: 'POST',
  //     url: '/deleteData/' + id_to_delete,
  //     data: data,
  //     error: function(error) {
  //         console.debug(JSON.stringify(error)); },
  //     beforeSend: function(xhr, settings) {
  //       $(event.target).attr('disabled', 'disabled'); },
  //     success: function(success) {
  //       $(event.target).removeAttr('disabled');
  //       console.log(success);
  //       $('.singleDataset[id='+currentDataset+']').remove();
  //       $.each($('.dataForm'), function() {
  //         $(this).hide();
  //         $(this).html('');
  //       });
  //       $.each($('.editData'), function() {
  //         $(this).show();
  //       });
  //       currentDataset = '';
  //       $('#addDataset').show();
  //     }
  //   });
  // });
  //   $('.datasets').on( 'click', '#saveData', function( event ) {
  //     event.preventDefault();
  //     if($('#dataFormContainer_'+currentDataset).parsley('validate') ) {
  //       $('.savingMessage').show();
  //       var id = $('#datasetID').val();
  //       var data = $('#dataFormContainer_'+currentDataset).serializeArray();
  //       $.ajax({
  //       type: 'POST',
  //       url: '/editData/' + $('#datasetID').val(),
  //             data: data,
  //       error: function(error) {
  //         console.debug(JSON.stringify(error));
  //         $('.savingMessage').hide();
  //         $('.errorMessage').fadeIn(); },
  //       beforeSend: function(xhr, settings) {
  //         $(event.target).attr('disabled', 'disabled'); },
  //       success: function() {
  //         $(event.target).removeAttr('disabled');
  //         $('.savingMessage').hide();
  //         $('.errorMessage').hide();
  //         //----------------------CREATE A TON OF NEW STUFF--------------------------//
  //         //get all the varbs:
  //         var datasetName = '';
  //         var datasetURL = '';
  //         var agency = '';
  //         var typeOfDataset = [];
  //         var otherTypeOfDataset = '';
  //         var rating = '';
  //         var reason = '';
  //         var datasetID = id;
  //         for (var i=0; i < data.length; i++) {
  //           if (data[i]['name'] == 'datasetName') { datasetName = data[i]['value'].replace(/ /g, "_"); }
  //           if (data[i]['name'] == 'datasetURL') { datasetURL = data[i]['value']; }
  //           if (data[i]['name'] == 'agency') { agency = data[i]['value']; }
  //           if (data[i]['name'] == 'typeOfDataset') { typeOfDataset.push(data[i]['value']); }
  //           if (data[i]['name'] == 'otherTypeOfDataset') { if ($.inArray('Other', typeOfDataset) > -1) { otherTypeOfDataset = data[i]['value'];} }
  //           if (data[i]['name'] == 'rating') { rating = data[i]['value']; }
  //           if (data[i]['name'] == 'reason') { reason = data[i]['value']; }
  //         }
  //         //new HTML
  //         var newHTMLforDataset = '<p><span class="datasetName '+datasetName+'">'+datasetName.replace(/_/g, " ")+'</span>'+
  //             '<input type="button" name="editData" datasetName="'+datasetName+'" class="m-button editData" id="editData" value="Edit">'+
  //             '<span class="savedMessage_'+datasetName+'" style="display:none">Saved!</span>'+
  //           '</p>'+
  //           '<div datasetName="'+datasetName+'" '+
  //             'datasetURL="'+datasetURL+'" '+
  //             'agency="'+agency+'" '+
  //             'typeOfDataset="'+typeOfDataset.toString()+'" '+
  //             'otherTypeOfDataset="'+otherTypeOfDataset+'" '+
  //             'rating="'+rating+'" '+
  //             'reason="'+reason+'" '+
  //             'datasetid="'+datasetID+'">'+
  //           '</div>'+
  //           '<form method="post" class="m-form dataForm" id="dataFormContainer_'+datasetName+'" style="display:none">'+
  //           '</form>';
  //         //Out with the Old, in with the new
  //         $('.singleDataset[id='+currentDataset+']').html('');
  //         $('.singleDataset[id='+currentDataset+']').append(newHTMLforDataset);
  //         $('.singleDataset[id='+currentDataset+']').attr('id', datasetName);
  //         $.each($('.editData'), function() { //show all edit buttons
  //           $(this).show();
  //         });
  //         $.each($('.dataForm'), function() { // clear all forms
  //           $(this).hide();
  //           $(this).html('');
  //         });
  //         $('.savedMessage_'+datasetName).show().delay(5000).fadeOut();
  //         $('#addDataset').show();

  //       }
  //     });
  //     } else {
  //       console.log('not valid');
  //     }
  //   });
  // $('.newSingleDataset').on( 'click', '#addNew', function( event ) {
  //   if ( $('#dataFormContainer').parsley('validate') ) {
  //     console.log('valid');
  //           $('.savingMessage').show();
  //           var data = $('#dataFormContainer').serializeArray();
  //           $.ajax({
  //             type: 'POST',
  //             url: '/addData/' + $('#companyID').val(),
  //             data: data,
  //             error: function(error) {
  //         console.debug(JSON.stringify(error));
  //         $('.savingMessage').hide();
  //         $('.errorMessage').fadeIn(); },
  //       beforeSend: function(xhr, settings) {
  //         $(event.target).attr('disabled', 'disabled'); },
  //       success: function(id) {
  //         $(event.target).removeAttr('disabled');
  //         $('.savingMessage').hide();
  //         $('.errorMessage').hide();
  //         $.each($('.dataForm'), function() { // clear all forms
  //           $(this).hide();
  //           $(this).html('');
  //         });
  //         $('#addDataset').show();
  //         //----------------------CREATE A TON OF NEW STUFF--------------------------//
  //         //get all the varbs:
  //         var datasetName = '';
  //         var datasetURL = '';
  //         var agency = '';
  //         var typeOfDataset = [];
  //         var otherTypeOfDataset = '';
  //         var rating = '';
  //         var reason = '';
  //         var datasetID = id;
  //         for (var i=0; i < data.length; i++) {
  //           if (data[i]['name'] == 'datasetName') { datasetName = data[i]['value'].replace(/ /g, "_"); }
  //           if (data[i]['name'] == 'datasetURL') { datasetURL = data[i]['value']; }
  //           if (data[i]['name'] == 'agency') { agency = data[i]['value']; }
  //           if (data[i]['name'] == 'typeOfDataset') { typeOfDataset.push(data[i]['value']); }
  //           if (data[i]['name'] == 'otherTypeOfDataset') { if ($.inArray('Other', typeOfDataset) > -1) { otherTypeOfDataset = data[i]['value'];} }
  //           if (data[i]['name'] == 'rating') { rating = data[i]['value']; }
  //           if (data[i]['name'] == 'reason') { reason = data[i]['value']; }
  //         }
  //         //new HTML
  //         var newHTMLforNewDataset = '<div id="'+datasetName+'" class="singleDataset">'+
  //           '<p><span class="datasetName '+datasetName+'">'+datasetName.replace(/_/g, " ")+'</span>'+
  //             '<input type="button" name="editData" datasetName="'+datasetName+'" class="m-button editData" id="editData" value="Edit">'+
  //             '<span class="savedMessage_'+datasetName+'" style="display:none">Saved!</span>'+
  //           '</p>'+
  //           '<div datasetName="'+datasetName+'" '+
  //             'datasetURL="'+datasetURL+'" '+
  //             'agency="'+agency+'" '+
  //             'typeOfDataset="'+typeOfDataset.toString()+'" '+
  //             'otherTypeOfDataset="'+otherTypeOfDataset+'" '+
  //             'rating="'+rating+'" '+
  //             'reason="'+reason+'" '+
  //             'datasetid="'+datasetID+'">'+
  //           '</div>'+
  //           '<form method="post" class="m-form dataForm" id="dataFormContainer_'+datasetName+'" style="display:none">'+
  //           '</form>'+
  //         '</div>';
  //         $(newHTMLforNewDataset).appendTo('.dataList');
  //         $('.savedMessage_'+datasetName).show().delay(5000).fadeOut();
  //       }
  //     });
  //       } else {
  //         console.log("not valid");
  //       }
  //   });
  function clearForm() {
    $('.dataForm')[0].reset();
    $('.dataForm input:checkbox').removeAttr('checked');
    $('#datasetID').val('');
    $('#action').val('');
  }
  function validURL(url) {
    var re = /^((https?|s?ftp|git):\/\/)?(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i;
    var r = new RegExp(re);
    if (r.test(url)) { return true; } else { return false; }
  }
  function validateForm(form) {
    var pass = true;
    var a = $("input[name='datasetName']", form).val();
    var b = $("input[name='datasetURL']", form).val();
    var re = /^(https?|s?ftp|git):\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i;
    var r = new RegExp(re);
    var c = $("input[name='agency']", form).val();
    var typeOfDataset = []
    $("input[name='typeOfDataset']", form).each( function() {
      if (this.checked) {
        typeOfDataset.push($(this).val());
      }
    });
    var d = $("input[name='otherTypeOfDataset']", form).val();
    var e = $("input[name='rating']", form).val();
    var f = $("input[name='reason']", form).val();
    if (a == '') {  pass=false; } //need a name for dataset
    if (!r.test(b)) { pass=false; } //need valid URL
    if (c == '') { pass=false; } // need agency
    if (!$.inArray('Other', typeOfDataset) > -1) { if (d == '') { pass=false; } } //need to enter 'other' if other checked
    if (typeOfDataset.length == 0) { pass=false; } //at least 1 value
    if (!isNaN(e)) {pass=false;} //needs to be a number
    return pass;
  }
  //----------------------------------AUTCOMPLETE SEARCH BAR--------------------------------------
  $( "#agencyTags" ).autocomplete({
    minLength: 2,
    source: agencies,
    select: function(event, ui) { 
      $("#searchval").val(ui.item.value) 
    }
  });



}); 















