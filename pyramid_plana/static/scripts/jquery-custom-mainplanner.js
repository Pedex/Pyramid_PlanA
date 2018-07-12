    function updatePlannerDateEntries(start, end) {
        var daysOfView = [];
        for (var d = start; d <= end; d.setDate(d.getDate() + 1)) {
            var unDate = new Date(d);
             var formattedDate = moment(unDate).locale("de").format("dddd, D MMMM YYYY");
            daysOfView.push(formattedDate);
             //convert to right format and language!
        var arrayLength = daysOfView.length;
        for (var i = 0; i < arrayLength; i++) {
            var c_selector = ".headerCollum"+i;
             $(c_selector).html(daysOfView[i]);
    //insert daysOfView[i]
}
             }
       }

    var updatePlannerEventEntries = function(startDate, endDate) {
       // $("#specialdiv").text("Yes, begin on: "+startDate.toString()+" and end on "+endDate.toString()+" in week "+week+".")
       // var now = new Date();
       // var daysOfYear = [];
       // for (var d = startDate; d <= endDate; d.setDate(d.getDate() + 1)) {
        //   daysOfYear.push(new Date(d));

        var stringStartDate = new Date("2018-07-02");
        var stringEndDate = new Date("2018-07-06");
        var encodedStart = stringStartDate.toLocaleDateString('de-DE');
        var encodedEnd = stringEndDate.toLocaleDateString('de-DE');
        $.ajax({
        url: "./",
        type: "post",
        data: {"start_date":encodedStart, "end_date": encodedEnd},
        dataType: 'json',
        success: function(response, textStatus, jqXHR) {
            //Get the eventdata packed out:
            var eventsListed = $.parseJSON(response);
            var arrayL = eventsListed.length;
            for (var i = 0; i < arrayL; i++) {
                //Convert dates.
                //---------------Old code:-----------------
                $(".eCol").remove();
                var eventCollum = $("<div></div>").attr({"class": "eCol", "id": "eventCollum"+event_id})
                    .css({"background-color": "yellow", "height": "45px", "width": "40%", "margin-left": "40%"})
                    .resizable()
                    .resizable({
                        maxHeight: "45",   // Handles left right and bottom right corner
                        handles: 'e, w',
                    })
                    .draggable()
                    .draggable({axis: "x", containment: "parent"});

                $(".employerMCol"+eventsListed[i]["event_employer_id"]).append(eventCollum)

                //------------------------------------------------------


            }
        },
        error: function(jqXHR, textStatus, errorThrown){
            alert(textStatus, errorThrown);
        }
    });
            };


$(document).ready(function () {

    // Initilize dates in mainplanner:
    var todayDate = new Date()
    var day = todayDate.getDay();
    var init_start_date = new Date();
    init_start_date.setDate(init_start_date.getDate() - (init_start_date.getDay() + 6) % 7);
    var init_end_date;


    //Also calc next friday date:
    var ret = new Date(todayDate || new Date());
    ret.setDate(ret.getDate() + (5 - 1 - ret.getDay() + 7) % 7 + 1); //5 = friday
    init_end_date = ret;

    //Fill the intial values finally in:
    updatePlannerDateEntries(init_start_date, init_end_date);

});
