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


/**
   --------------------------
*/

$(function(){
    $('#calendar').fullCalendar({
        displayEventTime: false,
        // put your options and callbacks here
        // example api call to fetch events
        events: '/schedule/api/occurrences?calendar_slug='

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
