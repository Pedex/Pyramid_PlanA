
// This script is released to the public domain and may be used, modified and
// distributed without restrictions. Attribution not necessary but appreciated.
// Source: https://weeknumber.net/how-to/javascript

// Returns the ISO week of the date.
Date.prototype.getWeek = function() {
  var date = new Date(this.getTime());
   date.setHours(0, 0, 0, 0);
  // Thursday in current week decides the year.
  date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);
  // January 4 is always in week 1.
  var week1 = new Date(date.getFullYear(), 0, 4);
  // Adjust to Thursday in week 1 and count number of weeks from date to week1.
  return 1 + Math.round(((date.getTime() - week1.getTime()) / 86400000
                        - 3 + (week1.getDay() + 6) % 7) / 7);
};

function getISOWeeks(y) {
    var d,
        isLeap;

    d = new Date(y, 0, 1);
    isLeap = new Date(y, 1, 29).getMonth() === 1;

    //check for a Jan 1 that's a Thursday or a leap year that has a
    //Wednesday jan 1. Otherwise it's 52
    return d.getDay() === 4 || isLeap && d.getDay() === 3 ? 53 : 52
}



function getDays(year, week) {
    var j10 = new Date(year, 0, 10, 1, 0, 0),
        j4 = new Date(year, 0, 4, 1, 0, 0),
        mon = j4.getTime() - j10.getDay() * 86400000,
        result = [];

    for (var i = 0; i < 7; i++) {
        result.push(new Date(mon + ((week - 1) * 7 + i) * 86400000));
    }

    return result;
}

function compareTime(time1, time2) {
    //return new Date(time1) > new Date(time2); // true if time1 is later
    return time1 < time2;
}

    function fillPlannerEvents(dupEventList, viewWeeks) {
          $(".eCol").remove();  //Delete all events planned earlier
             var eventList = [...new Map(dupEventList.map( o => [JSON.stringify(o), o])).values()];
          var length = eventList.length;

          for (var eLI = 0; eLI<length ;eLI++) {
              //Set viewWeeks in right format:
              var weekListLength = viewWeeks["week"].length;
              var weekListBothContain = [];
              //Iterate all weeks:
              for (var weekI = 0; weekI < weekListLength; weekI++) {
                  var stringFor = viewWeeks["week"][weekI] + " " + viewWeeks["year"][weekI];
                  if (eventList[eLI]["event_coversWeeks"].indexOf(stringFor) > -1) {
                      weekListBothContain.push(stringFor);

                  }
              }
              // var pixelPerWeek = $(".weekdayCol").width();
              var bothContainLength = weekListBothContain.length;
              var widthPerMilliseconds = 100 / 432000000;
              var convertedWeeks = [];
              var convertedYears = [];
              for (var wI = 0; wI < bothContainLength; wI++) {
                  var fields = weekListBothContain[wI].split(' ');
                  convertedWeeks.push(fields[0]);
                  convertedYears.push(fields[1]);
              }
              eventList[eLI]["event_begin_date"] = moment(eventList[eLI]["event_begin_date"] + " +0000", "YYYY-MM-DD HH:mm:ss Z").toDate();
              eventList[eLI]["event_end_date"] = moment(eventList[eLI]["event_end_date"] + "+0000", "YYYY-MM-DD HH:mm:ss Z").toDate();
              var beginOverflow = widthPerMilliseconds * (eventList[eLI]["event_begin_date"] - getDays(convertedYears[0], convertedWeeks[0])[0]);
              var endOverflow = widthPerMilliseconds * (getDays(convertedYears[convertedYears.length - 1], convertedWeeks[convertedWeeks.length - 1]).slice(-2)[0] - eventList[eLI]["event_end_date"]);

              //var beginOverflow = 20*(eventList[eLI]["event_begin_date"]-getDays(convertedYears[0],convertedWeeks[0])[0])/8600000;
              if (beginOverflow <= 0) {
                  beginOverflow = 0;

              }
              if (endOverflow <= 0) {
                  endOverflow = 0;
              }

              var resultWeekWidthList = [];
              var resultWeekMarginList = [];
              if (weekListBothContain.length >= 2) {
                  resultWeekWidthList.push(100 - beginOverflow);
                  resultWeekMarginList.push(beginOverflow);
                  for (var weekpart = 1; weekpart < (weekListBothContain.length - 1); weekpart++) {
                      resultWeekWidthList.push(100);
                      resultWeekMarginList.push(0);
                  }
                  resultWeekWidthList.push(100 - endOverflow);
                  resultWeekMarginList.push(0);
              }
              else if (weekListBothContain.length == 1) {
                  resultWeekWidthList.push(100 - beginOverflow - endOverflow);
                  resultWeekMarginList.push(beginOverflow);

              }



               splitList = moment(eventList[eLI]["event_begin_date"]).format("HH:mm").split(':');
               newHour = parseInt(splitList[0])-2;
              var momConvert = newHour+":"+splitList[1];
              //Fill in calculated data:
              for (var i = 0; i < convertedWeeks.length; i++) {
               if (viewedAmountWeeks <= 10) {
                   var eventContainer = $("<div></div>").attr({
                       "class": "eCol eventEdit_popup_open " + eventList[eLI]["event_type"],
                       "id": "eventCollum" + eventList[eLI]["event_id"]
                   })
                       .css({
                           "border-style": "ridge",
                           "font-size": (0.12 * resultWeekWidthList[i]) + "px",
                           "height": "45px",
                           "width": resultWeekWidthList[i] + "%",
                           "margin-left": resultWeekMarginList[i] + "%",
                           "overflow": "hidden",
                       })
                       .append("<label>" + eventList[eLI]["event_title"] + "</label><br><label>Beginn: " + momConvert + "</label>");
               }
               else {
                     var eventContainer = $("<div></div>").attr({
                       "class": "eCol eventEdit_popup_open " + eventList[eLI]["event_type"],
                       "id": "eventCollum" + eventList[eLI]["event_id"]
                   })
                       .css({
                           "border-style": "ridge",
                           "font-size": "0px",
                           "height": "45px",
                           "width": resultWeekWidthList[i] + "%",
                           "margin-left": resultWeekMarginList[i] + "%",
                           "overflow": "hidden",
                       })

               }


                  var a = viewWeeks["week"].indexOf(parseInt(convertedWeeks[i])) + 1;
                  var b = "#weekday" + a + eventList[eLI]["event_employer_id"];


                  $("#weekday" + a + eventList[eLI]["event_employer_id"]).append(eventContainer);


              }
          }
    }

    function updatePlannerDateEntries(cvWeeks) {
         var aLength = cvWeeks["week"].length;
         for (var w = 0; w < aLength; w++) {
          var days = getDays(cvWeeks["year"][w],cvWeeks["week"][w]);
          var daysLength = days.length - 1;
          var eWeekNumber = w+1;

          for (var d = 0; d<daysLength;  d++) {
              var formattedDay = moment(days[d]).locale("de").format("dd");
           var formattedDate = moment(days[d]).locale("de").format("D.MM");
           var eDayNumber = d+1;
           $("#daysIndicator"+eDayNumber+""+eWeekNumber).html("<strong>"+formattedDay+", <br>"+formattedDate+"</strong>");

          }
          //update also header for weeknumbers:
             $("#weekIndicator"+eWeekNumber).html("<strong> KW "+cvWeeks["week"][w]+", "+cvWeeks["year"][w]+"</strong>");
                }
                 }

    var updatePlannerEventEntries = function(viewWeeks) {
        postData = viewWeeks;
        $.ajax({
        url: "../multiweekPost",
        type: "post",
        data: postData,
        dataType: 'json',
        success: function(response, textStatus, jqXHR) {
            response = JSON.parse(response);
            fillPlannerEvents(response, viewWeeks)
            },
        error: function(jqXHR, textStatus, errorThrown){
            alert(textStatus, errorThrown);
        }
    });
            };


$(document).ready(function () {

    //resize font for day indication:
    if (viewedAmountWeeks<10) {
    var actualWidth = $(".daysIndicator").width();
    $(".daysIndicator").css("font-size", 3.8*Math.pow(actualWidth,1/4)+"px");
}
else {
        $(".daysIndicator").css("font-size","0px");
    }



    //Fill the intial values finally in:
    today = new Date();
    todaysWeek = today.getWeek();
    var init_currentView = {};
    init_currentView["week"] = [];
    init_currentView["year"] = [];
    for (var a = 0; a < viewedAmountWeeks; a++) {
        init_currentView["week"].push(todaysWeek+a);
        init_currentView["year"].push(today.getFullYear());

            today.setDate(today.getDate() + 6);
    }
    updatePlannerDateEntries(init_currentView);
    updatePlannerEventEntries(init_currentView)


    $(".viewShiftController").click(function () {
        var idClicked = $(this).attr('id');
        if (idClicked == "viewShiftLeft") {
            for(var ML = 0; ML < init_currentView["week"].length; ML++){
                 init_currentView["week"][ML] -= 1;
                 if (init_currentView["week"][ML]<1){
                     diff = getISOWeeks(init_currentView["year"][ML]-1)+init_currentView["week"][ML];
                     init_currentView["week"][ML] = diff;
                     init_currentView["year"][ML] -= 1;
                 }
            }
            updatePlannerDateEntries(init_currentView);
            updatePlannerEventEntries(init_currentView);

        }
        else if (idClicked == "viewShiftRight") {
            for(var MR = 0; MR < init_currentView["week"].length; MR++){
                 init_currentView["week"][MR] += 1;
                 if (init_currentView["week"][MR]>getISOWeeks(init_currentView["year"][MR])){
                     diff = init_currentView["week"][MR]-getISOWeeks(init_currentView["year"][MR]);
                     init_currentView["week"][MR] = diff;
                     init_currentView["year"][MR] += 1;
                 }
            }
            updatePlannerDateEntries(init_currentView);
            updatePlannerEventEntries(init_currentView);

        }
         else if (idClicked == "viewShiftLeftMonth") {
            for(var ML = 0; ML < init_currentView["week"].length; ML++){
                 init_currentView["week"][ML] -= 4;
                 if (init_currentView["week"][ML]<1){
                     diff = getISOWeeks(init_currentView["year"][ML]-1)+init_currentView["week"][ML];
                     init_currentView["week"][ML] = diff;
                     init_currentView["year"][ML] -= 1;
                 }
            }

            updatePlannerDateEntries(init_currentView);
            updatePlannerEventEntries(init_currentView);

        }
        else if (idClicked == "viewShiftRightMonth") {
            for(var MR = 0; MR < init_currentView["week"].length; MR++){
                 init_currentView["week"][MR] += 4;
                 if (init_currentView["week"][MR]>getISOWeeks(init_currentView["year"][MR])){
                     diff = init_currentView["week"][MR]-getISOWeeks(init_currentView["year"][MR]);
                     init_currentView["week"][MR] = diff;
                     init_currentView["year"][MR] += 1;
                 }
            }
            updatePlannerDateEntries(init_currentView);
            updatePlannerEventEntries(init_currentView);

        }
        else if (idClicked == "viewShiftZoomIn" && viewedAmountWeeks>1) {
            var newAmountWeeks =viewedAmountWeeks-1;
            window.location.replace("./"+ newAmountWeeks);
        }
        else if (idClicked == "viewShiftZoomOut") {
            var newAmountWeeks = viewedAmountWeeks+1;
            window.location.replace("./"+ newAmountWeeks);
        }
    });
    
    
    
});
