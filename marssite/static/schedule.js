
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
var initialized = false;
$(function(){
    if(window.initialized){ return;}
    window.initialized = true;
    // this is getting called twice for some reason

    $('#calendar').fullCalendar({
        displayEventTime: false,
        // put your options and callbacks here
        // example api call to fetch events
        events: '/schedule/api/occurrences?calendar_slug=',
        dayClick: dayClick,
        eventClick: eventClick,
        //defaultDate: t.currentDate()
    });

    var t = new Timeline(document.querySelectorAll(".timeline-wrapper")[0], {});
    console.log("done");

});

function getHashStringPairs(){
    var pairs = {},
        query = window.location.hash.substr(1);

    var tmp = query.split('&');
    for(var couples in tmp){
        var sep = tmp[couples].split('=');
        pairs[decodeURIComponent(sep[0])] = decodeURIComponent(sep[1]);
    }
    return pairs;
}

(function(window, undefined){
    'use strict';
    window.Timeline = function(elem, opts){
        var query = getHashStringPairs(),
            section = [
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
                "May",
                "June",
                "July"
               ]
            ],
            thisDate = new Date(),
            curYear = (query.year) ? query.year | 0 : thisDate.getFullYear(),
            curSection = (query.section) ? query.section | 0 : (thisDate.getMonth() <= 6) | 0, // use bitwise to conver to 1,0
            curMonth = (query.month) ? query.month | 0 : thisDate.getMonth()%7,
            yearWrapper = document.querySelectorAll('.timeline')[0],
            monthsWrapper = document.querySelectorAll('.timeline-wrapper .links ul')[0],
            linkElem = document.createElement("div"),
            linkLabel = document.createElement("span"),
            monthElem = document.createElement("button");

        linkElem.setAttribute("class", "blip");
        linkLabel.setAttribute("class", "blip-label");
        monthElem.setAttribute("class", "btn btn-link");

        // gets a string for the date used by the calendar
        function currentDate(setMonth=false){
            var stub = '__year__-__month__-01',
                dateStr = '',
                realMonth = curSection === 0 ? curMonth+8 : curMonth+1;
            realMonth = "0"+realMonth; // pad the month with a zero
            dateStr = stub.replace('__year__', curYear).replace('__month__', realMonth.slice(-2)); //remove extra zeros 
            // if we don't have any query info, just use today's date
            if( window.location.hash === "" ){
                realMonth = "0"+(thisDate.getMonth()+1);
                dateStr = thisDate.getFullYear()+"-"+(realMonth.slice(-2))+"-"+thisDate.getDate();
            }
            return dateStr;
        }

        // sets the calendar to the date for the current state
        function setCalendarDate(setMonth = false){
            $("#calendar").fullCalendar('gotoDate', currentDate(setMonth) );
        }

        // helper function - generates year element
        function yearElement(data){
            var nu_elem = data.linkElem.cloneNode(),
                nu_label = data.linkLabel.cloneNode();

            nu_label.innerText = ""+data.year+data.sectionLabel;
            nu_elem.setAttribute('data-year', data.year);
            nu_elem.setAttribute('data-section', data.section);
            nu_elem.appendChild(nu_label);
            return nu_elem;
        };

        // helper function - generates month element
        function monthElement(data){
            var listElem = document.createElement("li"),
                nu_elem = monthElem.cloneNode();

            nu_elem.innerText = data.monthName;
            nu_elem.setAttribute("data-month", data.monthNum);
            listElem.appendChild(nu_elem);

            return listElem;
        }

        // generate the year/semester links
        function generateYearLinks(){
            yearWrapper.innerHTML = "";
            for(var yr=curYear - 1; yr<curYear + 2; yr++){
                // first semester
                var data = {
                    linkElem: linkElem,
                    linkLabel: linkLabel,
                    year: yr,
                    section: 0,
                    sectionLabel: 'A'
                };
                var firstSem = yearElement(data);

                // second semester
                data.section = 1;
                data.sectionLabel = 'B';
                var secondSem = yearElement(data);

                if(curSection === 0){
                    if(yr == curYear){
                        firstSem.className += " active";
                    }
                }else{
                    if(yr == curYear){
                        secondSem.className += " active";
                    }
                }
                blipClickEvents(firstSem);
                blipClickEvents(secondSem);
                yearWrapper.appendChild(firstSem);
                yearWrapper.appendChild(secondSem);
            }
        }

        function generateMonthLinks(){
            monthsWrapper.innerHTML = "";
            var months = section[curSection];
            for(var x = 0; x < months.length; x++){
                var _data = {
                    monthNum: x,
                    monthName: months[x]
                };
                var el = monthElement(_data);
                if( x == curMonth){
                    el.className += " active";
                }
                monthClickEvents(el);
                monthsWrapper.appendChild(el);
            }
        }

        function monthClickEvents(el){
            el.addEventListener("click", function(e){
                e.stopPropagation();
                // this event triggered on the parent <li> element
                var month = e.currentTarget.firstChild.dataset.month;
                // set the month 
                curMonth = month | 0;
                // set the hash
                var query = [
                    "year="+curYear,
                    "section="+curSection,
                    "month="+curMonth
                ];
                window.location.hash = query.join("&");
                // change the controls
                setCalendarDate(true);
                generateMonthLinks();

            });
        }


        function blipClickEvents(el){
            el.addEventListener("click", function(e){
                e.stopPropagation();
                var semester = e.currentTarget.dataset;
                curYear = semester.year | 0;
                curMonth = 0;
                curSection = semester.section | 0;
                var query = [
                    "year="+semester.year,
                    "section="+semester.section,
                    "month=0" // start at the first month for a given section 
                ];
                window.location.hash = query.join("&");
                setCalendarDate();
                generateYearLinks();
                generateMonthLinks();
            });
        }


        setCalendarDate();
        generateYearLinks();
        generateMonthLinks();

        return {
            generateYearLinks : generateYearLinks,
            generateMonthLinks : generateMonthLinks,
            currentDate: currentDate
        };
    };
})(this);
