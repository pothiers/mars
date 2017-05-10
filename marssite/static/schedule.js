function openCancelDialog(node, cancel_url, delete_url, event){
  event.stopPropagation();
  var btns = {"This":function(){window.location=cancel_url;}, "All":function(){window.location=delete_url}, "Do nothing":function(){$(this).dialog("destroy");}};
  dia = $("#delete_dialog").dialog({'buttons':btns, 'modal':true});
  dia.dialog('open');
  return false;
}

function openEditDialog(node, occurrence_url, event_url, event){
  event.stopPropagation();
  var btns = {"This":function(){window.location=occurrence_url;}, "All":function(){window.location=event_url}, "Do nothing":function(){$(this).dialog("destroy");}};
  dia = $("#edit_dialog").dialog({'buttons':btns, 'modal':true});
  dia.dialog('open');
  return false;
}

function openDetail(node){
  var btns = { "Close":function(){$(this).dialog("destroy");}};
  dia = $($(node).attr("href")).dialog({'buttons':btns, 'modal':true, 'title':'Details'});
  dia.dialog('open');
  return false;
}

function openURL(url, event){
    event.stopPropagation();
    window.location=url;
}

function dayClick(date, event, view){
    event.preventDefault();
    event.stopPropagation();
    // link through to the obsdate in the admin view
    // admin/schedule/slot/?obsdate__day=24&obsdate__month=6&obsdate__year=2017
    var url_path = "/admin/schedule/slot/?obsdate__day=__day__&obsdate__month=__month__&obsdate__year=__year__";
    url_path = url_path.replace("__day__", date.date()).replace("__month__", date.month()+1).replace("__year__", date.year());
    window.location.href = url_path;
    
}

/*
  Normal event clicks are mitigated and a manual process of triggering the underlying day is
  implemented since there isn't any useful click through to the proposal id.
  This might be useful if a page of dates any given proposal showes up on existed.
*/
function eventClick(calEvent, event, view){
    event.preventDefault();
    var x, y, el, els = null;
    // this doesn't take into account page position i.e. scroll etc
    x = event.clientX;
    y = event.clientY;
    els = document.elementsFromPoint(x, y);
    var trigger = new MouseEvent("click", {
        view: window,
        bubbles: true,
        cancelable: true,
        clientX: x,
        clientY: y
    });
    // day element is 5th in stack
    el = els[5];
    date = moment(el.dataset.date);
    dayClick(date, trigger, null);
    return false;
}

/**
   --------------------------
*/

$(function(){
    $('#calendar').fullCalendar({
        displayEventTime: false,
        // put your options and callbacks here
        // example api call to fetch events
        events: '/schedule/api/occurrences?calendar_slug=',
        dayClick: dayClick,
        eventClick: eventClick
    });

    $(".links button").on("click", function(e){
        var d = new Date();
        var month = e.currentTarget.dataset.month;
        d.setMonth(month);
        $("#calendar").fullCalendar("gotoDate", d);
    });

    t = new Timeline(document.querySelectorAll(".timeline-wrapper")[0], {});

});

(function(window, undefined){
    'use strict';
    window.Timeline = function(elem, opts){
        var section = [
            [
                "August",
                "September",
                "October",
                "November",
                "December"
            ],
            [
                "January",
                "February",
                "March",
                "April",
                "May"
            ]
        ];


        elem.querySelectorAll(".blip").forEach(function(el){
            el.addEventListener("click", function(e){
                e.stopPropagation();
                var semester = e.currentTarget.dataset;
                console.log(section[semester.section]);
            });
        });
    };
})(this);
