function initializeEmployerForm(answer, key) {
            var formquery = $(answer);
         $("#employerEditFormContainer").append(formquery);
         if (key == "editEm") {
              $("#item-deformField3").hide();
}
}

function initializeEventForm(answer, key) {
    var formquery = $(answer);
    $("#eventEditFormContainer").append(formquery);
    if (key == "editEv") {
              $(".item-event_id").hide();
}
}

    $(document).ready(function() {

      // Initialize the plugin
      $('#employerInsert_popup').popup({
          type: 'overlay',
          openelement: '.employerInsert_popup_open',
          closeelement: '.employerInsert_popup_close',
      });
      $('#eventInsert_popup').popup({
          type: 'overlay',
          openelement: '.eventInsert_popup_open',
          closeelement: '.eventInsert_popup_close',
      });
      $('#eventEdit_popup').popup({
          type: 'overlay',
          openelement: '.eventEdit_popup_open',
          closeelement: '.eventEdit_popup_close',
      });
      $('#employerEdit_popup').popup({
          type: 'overlay',
          openelement: '.employerEdit_popup_open',
          closeelement: '.employerEdit_popup_close',
      });
var globalCurrentEmployerEdit = 0;
      $(".employerInfoCollum").on('click', function (){
          $("#employerEditFormContainer").empty();
          $("#employerEdit_editToolbar").hide();
          $(".emEditTools").show();
         globalCurrentEmployerEdit = parseInt($(this).attr('id').replace('employerInfoCollum',''));
          var postData = {"requestType": "employer", "identifier": globalCurrentEmployerEdit, "readonly": true};

          $.ajax({
        url: "../multiweekForm",
        type: "post",
        data: postData,
        dataType: 'json',
        success: function (response, textStatus, jqXHR) {
            var answer = response["form"];
            initializeEmployerForm(answer, 'showEm');
        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert(textStatus, errorThrown);
        }
    });

      });
var globalCurrentEventEdit = 0;


      $(document).on('click', '.eCol', function(){
   $("#eventEditFormContainer").empty();
          $("#eventEdit_editToolbar").hide();
          $(".evEditTools").show();
         globalCurrentEventEdit = parseInt($(this).attr('id').replace('eventCollum',''));
          var postData = {"requestType": "event", "identifier": globalCurrentEventEdit, "readonly": true};

          $.ajax({
        url: "../multiweekForm",
        type: "post",
        data: postData,
        dataType: 'json',
        success: function (response, textStatus, jqXHR) {
            var answer = response["form"];
            initializeEventForm(answer, 'showEv');

        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert(textStatus, errorThrown);
        }
    });

       });

       $(".employerEdit_edit").on('click', function () {
          $("#employerEditFormContainer").empty();
          $("#employerEditToolbar").hide();
          $("#employerEdit_editToolbar").show();
     var postData = {"requestType": "employer", "identifier": globalCurrentEmployerEdit, "readonly": false};

          $.ajax({
        url: "../multiweekForm",
        type: "post",
        data: postData,
        dataType: 'json',
        success: function (response, textStatus, jqXHR) {
            var answer = response["form"];
            initializeEmployerForm(answer, 'editEm');

        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert(textStatus, errorThrown);
        }
    });
      });

      $(".employerEdit_delete").on('click',function () {

            var result = confirm("Soll der Mitarbeiter wirklich gelöscht werden?");
          if (result) {
   var postData = {"object": "employer", "identifier": globalCurrentEmployerEdit};
          $.ajax({
        url: "../multiweekDelete",
        type: "post",
        data: postData,
        dataType: 'json',
        success: function (response, textStatus, jqXHR) {
              alert("Mitarbeiter wurde erfolgreich gelöscht");
              location.reload();
        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert(textStatus, errorThrown);
        }
    });
      }});
    //----------------- Eventedits::--------------------
       $(".eventEdit_edit").on('click', function () {
          $("#eventEditFormContainer").empty();
          $("#eventEditToolbar").hide();
          $("#eventEdit_editToolbar").show();
     var postData = {"requestType": "event", "identifier": globalCurrentEventEdit, "readonly": false};

          $.ajax({
        url: "../multiweekForm",
        type: "post",
        data: postData,
        dataType: 'json',
        success: function (response, textStatus, jqXHR) {
            var answer = response["form"];
            initializeEventForm(answer, 'editEv');

        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert(textStatus, errorThrown);
        }
    });
      });

      $(".eventEdit_delete").on('click',function () {

          var result = confirm("Soll das Ereignis wirklich gelöscht werden?");
          if (result) {
   var postData = {"object": "event", "identifier": globalCurrentEventEdit};
          $.ajax({
        url: "../multiweekDelete",
        type: "post",
        data: postData,
        dataType: 'json',
        success: function (response, textStatus, jqXHR) {
              alert("Ereignis wurde erfolgreich gelöscht");
              location.reload();
        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert(textStatus, errorThrown);
        }
    });
      }});



    });