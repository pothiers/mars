###
Author: Peter Peterson
Date: 2017-06-09
Description: Serves functionality for submitting and displaying archive query forms/results
Original file: search.coffee
###
class SearchForm
  apiUrl: "/dal/search/"
  rangeInputs: ["obs_date", "exposure_time", "release_date"]
  formData:
    coordinates:
      ra: null
      dec: null
    pi: null
    search_box_min: null
    prop_id: null
    obs_date:['','', "="]
    filename: null
    original_filename: null
    telescope:[]
    exposure_time:['', '', "="]
    instrument:[]
    release_date:['', '', "="]
    image_filter:[]

  loadingMessages:[
    "Searching the cosmos..."
    "Deploying deep space probes..."
    "Is that you Dave?..."
    "There's so much S P A C E!"
  ]
  constructor: ()->
    @bindEvents()

    @form = new Vue
      el:"#search-form"
      data:
        visible: true
        loading: false
        loadingMessage: "Sweeping up star dust..."
        search: JSON.parse(JSON.stringify(@formData)) # deep copy
      methods:
        submitForm: (event)->
          event.preventDefault()
          @loading = true


          # TODO: Validate
          # strip out anything that wasn't modified
          newFormData = JSON.parse(JSON.stringify(@search))

          
          for key of newFormData
            if _.isEqual(newFormData[key], searchForm.formData[key])
              delete(newFormData[key])
            else
              if searchForm.rangeInputs.indexOf(key) >= 0
                # flatten value if it is for direct match
                if newFormData[key][2] is "="
                  newFormData[key] = newFormData[key][0]

          msgs = searchForm.loadingMessages
          message = Math.floor(Math.random()*msgs.length)
          @loadingMessage = message

          new Ajax
            url: "/dal/search/"
            method: "post"
            accept: "json"
            data:
              search: newFormData
            success: (data)->
              window.searchForm.form.loading = false
              window.searchForm.form.visible = false
              window.results.table.results = data
              window.results.table.visible = true
              console.dir data
          .send()

  bindEvents:()->
    console.log "binding yo"
    # TODO: formatting
    # TODO: save form data
    # TODO: save state data i.e. UI states

class SearchResults
  # vue ui


searchForm = new SearchForm()
# Vue clobbers previous bindings, so re-bind
window.base.bindEvents()

