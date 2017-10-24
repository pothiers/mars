
/*
Author: Peter Peterson
Date: 2017-06-09
Description: Base functionality/interactions + helper functions
Original file: main.coffee
 */
var Ajax, Base, ToggleModal,
  bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

ToggleModal = function(selector) {
  var b, backdrop, body, m;
  m = document.querySelector(selector);
  b = document.querySelector('.modal-backdrop');
  m.style.display = 'block';
  m.classList.toggle('in');
  if (b === null) {
    backdrop = document.createElement('div');
    body = document.querySelector('body');
    backdrop.setAttribute('class', 'modal-backdrop fade in');
    body.appendChild(backdrop);
  } else {
    b.remove();
  }
};

Ajax = (function() {
  function Ajax(_opts) {
    this._response = bind(this._response, this);
    var settings;
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
    settings = _.extend(this.settings, _opts);
    this.settings = settings;
    this.xhr = new XMLHttpRequest();
    this.xhr.onload = this._response;
    this.xhr.onerror = settings.fail;
    this.xhr.open(settings.method.toUpperCase(), settings.url, true);
    this.xhr.setRequestHeader('Content-Type', 'application/json');
    this.xhr.setRequestHeader('Accepts', settings.accepts);
    this.xhr.setRequestHeader('x-mars-ajax-handler', '1.0');
    this.xhr.responseType = settings.accept;
    this.xhr.send(JSON.stringify(settings.data));
  }

  Ajax.prototype._response = function(e) {
    if (e.target.status !== 200) {
      this.settings.fail(e.target.statusText, e.target.status, e.target);
      return;
    }
    this.settings.success(e.target.response);
  };

  Ajax.prototype.send = function() {
    var path, settings;
    settings = this.settings;
    return path = settings.url;

    /*
    unless _.isEmpty(settings.data)
      params = Object.keys(settings.data).map (k) ->
        return encodeURIComponent(k) + '=' + encodeURIComponent(settings.data[k])
      .join('&')
      path += "?"+params
     */
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
    if (window.location.hostname.indexOf('local') < 0) {
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
    var el, els, i, j, len, len1, results, section, sections, toggle;
    els = document.querySelectorAll("input[type=text],input[type=textarea],input[type=password],input[type=date]");
    for (i = 0, len = els.length; i < len; i++) {
      el = els[i];
      addMultiEventListener(el, 'keyup blur', function(event) {
        var ref, ref1, target, targetId;
        targetId = event.currentTarget.id;
        target = event.currentTarget;
        if (!targetId) {
          return false;
        }
        if (target.value === "") {
          return (ref = document.querySelector("label[for=" + targetId + "].floating")) != null ? ref.classList.remove("open") : void 0;
        } else {
          return (ref1 = document.querySelector("label[for=" + targetId + "].floating")) != null ? ref1.classList.add("open") : void 0;
        }
      });
    }
    sections = document.querySelectorAll(".collapsible");
    results = [];
    for (j = 0, len1 = sections.length; j < len1; j++) {
      section = sections[j];
      toggle = section.querySelector(".section-toggle");
      results.push((function(thisSection) {
        return toggle.addEventListener("click", function(e) {
          return thisSection.classList.toggle("open");
        });
      })(section));
    }
    return results;
  };

  return Base;

})();


/*
    splitVals = document.querySelectorAll(".split-val")
    for splits in splitVals
      select = splits.querySelector("select")
      ((select, container)->
        select.addEventListener "change", (event)->
          if event.currentTarget.selectedOptions[0].classList.contains("toggle-option")
            container.classList.add("display-hidden")
          else
            container.classList.remove("display-hidden")
      )(select, splits)
 */

window.base = new Base();

window.base.bindEvents();
