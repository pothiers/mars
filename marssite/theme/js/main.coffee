###
Author: Peter Peterson
Date: 2017-06-09
Description: Base functionality/interactions + helper functions
Original file: main.coffee
###

class Ajax
  constructor:(_opts)->
    @settings =
        url : window.location.path
        method: "GET"
        accept: "html"
        data: {}
        success: ()-> return ""
        fail: ()-> return ""
    @settings = _.extend(@settings, _opts)
    @xhr = new XMLHttpRequest()
    @xhr.onload = @_response
    @xhr.onerror = @settings.fail

  _response: (e)=>
    @settings.success(e.target.response)

  send: ()->
    settings = @settings
    path = settings.url
    ###
    unless _.isEmpty(settings.data)
      params = Object.keys(settings.data).map (k) ->
        return encodeURIComponent(k) + '=' + encodeURIComponent(settings.data[k])
      .join('&')
      path += "?"+params
    ###
    @xhr.responseType = settings.accept
    @xhr.open(settings.method.toUpperCase(), path, true)
    @xhr.setRequestHeader('Content-Type', 'application/json')
    @xhr.setRequestHeader('x-hello-world', '1.0')

    @xhr.send(JSON.stringify(settings.data) )



class Base
  constructor: ()->
    ###
    Bind multiple events to one function
    Usage: addMutiEventListener($el, "click blur", function(){})
    ###
    window.addMultiEventListener = (elem, events, fn)->
      events.split(' ').forEach (e) ->
        elem.addEventListener(e, fn, false)

    # disable console on live
    if window.location.hostname isnt "localhost"
      nohup = ()->
        return "Console commands (log, info, dir, debug) have been mapped into `console.live` in production environments"
      console.live = 
        log: console.log
        info: console.info
        dir: console.dir
        debug: console.debug
      console.debug = nohup
      console.log = nohup
      console.info = nohup
      console.dir = nohup

      console.live.info "%c "+nohup(), "color: red"
    return ""

  bindEvents: ()->
    els = document.querySelectorAll("input[type=text],input[type=textarea],input[type=password],input[type=date]")
    for el in els
      addMultiEventListener el, 'keyup blur', (event)->
        targetId = event.currentTarget.id
        target = event.currentTarget
        if target.value is ""
          document.querySelector("label[for=#{targetId}].floating")?.classList.remove("open")
        else
          document.querySelector("label[for=#{targetId}].floating")?.classList.add("open")

    sections = document.querySelectorAll(".collapsible")
    for section in sections
      toggle = section.querySelector(".section-toggle")
      ((thisSection)->
        toggle.addEventListener "click", (e)->
          thisSection.classList.toggle("open")
      ) section

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

window.base = new Base()
window.base.bindEvents()
