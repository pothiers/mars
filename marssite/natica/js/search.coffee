###
Author: Peter Peterson
Date: 2017-06-09
Description: Serves functionality for submitting and displaying archive query forms/results
Original file: search.coffee
###

import Vue from 'vue'
import VeeValidate from 'vee-validate'

config =
  apiUrl: "/dal/search/"
  rangeInputs: ["obs_date", "exposure_time", "release_date"]

  validatorConfig:
    delay: 800
    events: "input|blur"
    inject: true


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


(()->
  # This gets called after the component has been mounted
  window.addEventListener 'searchLoaded', (e)->
    console.log("Search loaded", e)
    # re-bind since the template will render after the page is loaded.
    window.base.bindEvents()


  # Use vee-validate, and assign before component is loaded
  Vue.use(VeeValidate, config.validatorConfig) # validation plugin
)()

export default {
  mounted: ()->
    # done loading, trigger event
    event = new CustomEvent("searchLoaded", {detail:"Search Vue Component Loaded"})
    event.search = @
    console.log("dispatching event", event)
    window.dispatchEvent(event)

  data: ()->
    return {
      url: config.apiUrl
      visible: true
      loading: false
      loadingMessage: "Sweeping up star dust..."
      search: JSON.parse(JSON.stringify(config.formData)) # deep copy
      showExposureMax: false
      showObsDateMax: false
      showReleaseDateMax: false
      showBothExposureFields: false
      showBothObsDateFields: false
      showBothReleaseDateFields: false
      relatedSplitFieldFlags :
        "exposure_time":
          {"fieldFlag":'showExposureMax', "bothFieldFlag":"showBothExposureFields"}
        "obs_date":
          {"fieldFlag":"showObsDateMax", "bothFieldFlag":"showBothObsDateFields"}
        "release_date":
          {"fieldFlag":"showReleaseDateMax","bothFieldFlag":"showBothReleaseDateFields"}
    }
  methods:
    splitSelection: (val)->
      # for toggling conditional form inputs, one and sometimes both
      fieldFlag = @relatedSplitFieldFlags[val]['fieldFlag']
      bothFlag = @relatedSplitFieldFlags[val]['bothFieldFlag']

      if @search[val][2] is "(]" or @search[val][2] is "[]"
        @[fieldFlag] = true
      else
        @[fieldFlag] = false

      if @search[val][2] is "[]"
        @[bothFlag] = true
      else
        @[bothFlag] = false

    submitForm: (event, paging=null, cb=null)->
      event?.preventDefault()
      unless paging
        @loading = true
        @url = searchForm.apiUrl
        window.location.hash = ""
        window.results.table.pageNum = 1
        localStorage.setItem("currentPage", 1)

      # strip out anything that wasn't modified
      newFormData = JSON.parse(JSON.stringify(@search))

      for key of newFormData
        if _.isEqual(newFormData[key], config.formData[key])
          delete(newFormData[key])
        else
          if config.rangeInputs.indexOf(key) >= 0
            # flatten value if it is for direct match
            if newFormData[key][2] is "="
              newFormData[key] = newFormData[key][0]

      msgs = config.loadingMessages
      message = Math.floor(Math.random()*msgs.length)
      @loadingMessage = msgs[message]
      localStorage.setItem('search', JSON.stringify(@search))

      new Ajax
        url: @url
        method: "post"
        accept: "json"
        data:
          search: newFormData
        success: (data)->
          window.location.hash = "#query"
          window.searchForm.form.loading = false
          window.searchForm.form.visible = false
          window.results.table.results = data
          window.results.table.visible = true
          localStorage.setItem('results', JSON.stringify(data))
          if cb
            cb()
      .send()
}
