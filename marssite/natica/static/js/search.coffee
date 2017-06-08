# disable console on live
if window.location.hostname isnt "localhost"
  nohup = ()->
    return ""
  console.log = nohup
  console.info = nohup
  console.dir = nohup

window.addMultiEventListener = (elem, events, fn)->
  events.split(' ').forEach (e) ->
    elem.addEventListener(e, fn, false)

class Search
  constructor: ()->
    @bindEvents()

  bindEvents:()->
    console.log "binding yo"
    els = document.querySelectorAll("input[type=text]")
    for el in els
      addMultiEventListener el, 'keyup blur', (event)->
        target = event.currentTarget
        if target.value is ""
          target.previousElementSibling.classList.remove("open")
        else
          target.previousElementSibling.classList.add("open")

    sections = document.querySelectorAll(".collapsible")
    for section in sections
      toggle = section.querySelector(".section-toggle")
      toggle.addEventListener "click", (e)->
        section.classList.toggle("open")

class SearchResults
  # vue ui


search = new Search()
