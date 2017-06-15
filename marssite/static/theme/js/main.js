
/*
Author: Peter Peterson
Date: 2017-06-09
Description: Base functionality/interactions + helper functions
Original file: main.coffee
 */
var Ajax, Base,
  bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

Ajax = (function() {
  function Ajax(_opts) {
    this._response = bind(this._response, this);
    this.settings = {
      url: window.location.path,
      method: "GET",
      accept: "html",
      data: {},
      success: function() {
        return "";
      },
      fail: function() {
        return "";
      }
    };
    this.settings = _.extend(this.settings, _opts);
    this.xhr = new XMLHttpRequest();
    this.xhr.onload = this._response;
    this.xhr.onerror = this.settings.fail;
  }

  Ajax.prototype._response = function(e) {
    return this.settings.success(e.target.response);
  };

  Ajax.prototype.send = function() {
    var path, settings;
    settings = this.settings;
    path = settings.url;

    /*
    unless _.isEmpty(settings.data)
      params = Object.keys(settings.data).map (k) ->
        return encodeURIComponent(k) + '=' + encodeURIComponent(settings.data[k])
      .join('&')
      path += "?"+params
     */
    this.xhr.responseType = settings.accept;
    this.xhr.open(settings.method.toUpperCase(), path, true);
    this.xhr.setRequestHeader('Content-Type', 'application/json');
    this.xhr.setRequestHeader('x-hello-world', '1.0');
    return this.xhr.send(JSON.stringify(settings.data));
  };

  return Ajax;

})();

Base = (function() {
  function Base() {

    /*
    Bind multiple events to one function
    Usage: addMutiEventListener($el, "click blur", function(){})
     */
    var nohup;
    window.addMultiEventListener = function(elem, events, fn) {
      return events.split(' ').forEach(function(e) {
        return elem.addEventListener(e, fn, false);
      });
    };
    if (window.location.hostname !== "localhost") {
      nohup = function() {
        return "Console commands (log, info, dir, debug) have been mapped into `console.live` in production environments";
      };
      console.live = {
        log: console.log,
        info: console.info,
        dir: console.dir,
        debug: console.debug
      };
      console.debug = nohup;
      console.log = nohup;
      console.info = nohup;
      console.dir = nohup;
      console.live.info("%c " + nohup(), "color: red");
    }
    return "";
  }

  Base.prototype.bindEvents = function() {
    var el, els, fn1, i, j, k, len, len1, len2, results, section, sections, select, splitVals, splits, toggle;
    els = document.querySelectorAll("input[type=text],input[type=textarea],input[type=password],input[type=date]");
    for (i = 0, len = els.length; i < len; i++) {
      el = els[i];
      addMultiEventListener(el, 'keyup blur', function(event) {
        var ref, ref1, target, targetId;
        targetId = event.currentTarget.id;
        target = event.currentTarget;
        if (target.value === "") {
          return (ref = document.querySelector("label[for=" + targetId + "].floating")) != null ? ref.classList.remove("open") : void 0;
        } else {
          return (ref1 = document.querySelector("label[for=" + targetId + "].floating")) != null ? ref1.classList.add("open") : void 0;
        }
      });
    }
    sections = document.querySelectorAll(".collapsible");
    fn1 = function(thisSection) {
      return toggle.addEventListener("click", function(e) {
        return thisSection.classList.toggle("open");
      });
    };
    for (j = 0, len1 = sections.length; j < len1; j++) {
      section = sections[j];
      toggle = section.querySelector(".section-toggle");
      fn1(section);
    }
    splitVals = document.querySelectorAll(".split-val");
    results = [];
    for (k = 0, len2 = splitVals.length; k < len2; k++) {
      splits = splitVals[k];
      select = splits.querySelector("select");
      results.push((function(select, container) {
        return select.addEventListener("change", function(event) {
          if (event.currentTarget.selectedOptions[0].classList.contains("toggle-option")) {
            return container.classList.add("display-hidden");
          } else {
            return container.classList.remove("display-hidden");
          }
        });
      })(select, splits));
    }
    return results;
  };

  return Base;

})();

window.base = new Base();

window.base.bindEvents();
