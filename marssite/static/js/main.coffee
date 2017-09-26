###
Author: Peter Peterson
Date: 2017-06-09
Description: Base functionality/interactions + helper functions
Original file: main.coffee
###

ToggleModal = (selector) ->
  m = document.querySelector(selector)
  b = document.querySelector('.modal-backdrop')
  m.style.display = 'block'
  m.classList.toggle 'in'
  if b == null
    backdrop = document.createElement('div')
    body = document.querySelector('body')
    backdrop.setAttribute 'class', 'modal-backdrop fade in'
    body.appendChild backdrop
  else
    b.remove()
  return

class Ajax
  constructor:(_opts)->
    @settings =
        url : window.location.path
        method: "GET"
        accept: "html"
        data: {}
        success: ()-> return ""
        fail: ()-> return ""
    settings = _.extend(@settings, _opts)
    @settings = settings
    @xhr = new XMLHttpRequest()
    @xhr.onload = @_response
    @xhr.onerror = settings.fail
    # FF throws an error if setting the response type...wth?
    @xhr.open(settings.method.toUpperCase(), settings.url, true)
    @xhr.setRequestHeader('Content-Type', 'application/json')
    @xhr.setRequestHeader('Accepts', settings.accepts)
    @xhr.setRequestHeader('x-mars-ajax-handler', '1.0')
    @xhr.responseType = settings.accept
    @xhr.send(JSON.stringify(settings.data) )


  _response: (e)=>
    if e.target.status != 200
      @settings.fail e.target.statusText, e.target.status, e.target
      return
    @settings.success e.target.response
    return

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
        unless targetId
          return false
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
###
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
###
window.base = new Base()
window.base.bindEvents()
