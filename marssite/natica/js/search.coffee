###
Author: Peter Peterson
Date: 2017-06-09
Description: Serves functionality for submitting and displaying archive query forms/results
Original file: search.coffee
###

import Vue from 'vue'
import VeeValidate, {Validator} from 'vee-validate'
import Shared from './mixins.coffee'

validateDependsOn =
  getMessage: (field, params, data)->
    id = params[0].replace("#", "")
    dependsOn = document.querySelector("label[for=#{id}]").innerText
    return (data && data.message) || "This field depends on #{dependsOn}"
  validate: (value, args)->
    return (document.querySelector(args[0]).value isnt "")



config = Shared.config

(()->
  # This gets called after the component has been mounted
  window.addEventListener 'searchLoaded', (e)->
    console.log("Search loaded", e)
    # re-bind since the template will render after the page is loaded.
    window.base.bindEvents()

  Validator.extend('dependson', validateDependsOn)
  validation = new Validator({dependant:"dependson"})
  # Use vee-validate, and assign before component is loaded
  Vue.use(VeeValidate, config.validatorConfig) # validation plugin
)()

dateLookup = {
      "obs-date": {
        "field" : "obs_date",
        "index" : 0
      },
      "obs-date-max": {
        "field" : 'obs_date',
        "index" : 1
      },
      "release-date": {
        "field": "release_date",
        "index": 0
      },
      "release-date-max":{
        "field": "release_date",
        "index": 1
      },
      "parent":{
        "obj": this
      }
}

searchFormComponent = {
  mixins: [Shared.mixin]
  created: ()->
    this.getTelescopes()

  mounted: ()->
    # check if this is a new search
    if window.location.hash.indexOf("search_again") > -1
      oldSearch = JSON.parse(localStorage.getItem("searchData"))
      @search = oldSearch
    else if window.location.hash.indexOf("query") > -1
      this.$emit("displayform", ["results", []]) 
    window.base.bindEvents()
    ### 
    $("#obs-date").datepicker({
      onSelect: (dateText)=>
        this.search.obs_date[0] = dateText
    })

    $("#obs-date").datepicker("option", "dateFormat", "yy-mm-dd")
    ###
    $("input.date").datepicker({
            onSelect: (dateText, datePicker)=>
              fieldName = datePicker.input[0].name
              field = this.search[dateLookup[fieldName].field]
              field[dateLookup[fieldName].index] = dateText
              e = new CustomEvent("datechanged", {'detail':{'date':dateText} }) 
              document.dispatchEvent(e)
              this.$forceUpdate()
      })
    $("input.date").datepicker("option", "dateFormat", "yy-mm-dd")
    window.searchVue = this
    # Datepicker doesn't trigger change in the model data, so...
    # bind to datepicker changes
    document.addEventListener("datechanged", ()->
      console.log("update code view")
    )
  computed:
    code: ()->
      return JSON.stringify(@stripData(), null, 2)
  data: ()->
    return {
      url: config.apiUrl
      visible: true
      loading: false
      modalTitle: ""
      modalBody: ""
      loadingMessage: "Sweeping up star dust..."
      search: JSON.parse(JSON.stringify(config.formData)) # deep copy
      showExposureMax: false
      showObsDateMax: false
      showReleaseDateMax: false
      showBothExposureFields: false
      showBothObsDateFields: false
      showBothReleaseDateFields: false
      telescopes: []
      relatedSplitFieldFlags :
        "exposure_time":
          {"fieldFlag":'showExposureMax', "bothFieldFlag":"showBothExposureFields"}
        "obs_date":
          {"fieldFlag":"showObsDateMax", "bothFieldFlag":"showBothObsDateFields"}
        "release_date":
          {"fieldFlag":"showReleaseDateMax","bothFieldFlag":"showBothReleaseDateFields"}
      option:{
        format: 'YYYY-MM-DD'
      }
    }
  methods:
    closeModal: ()->
      ToggleModal("#search-modal")
    newSearch: ()->
      # clear current search and storage
      @search = JSON.parse(JSON.stringify(@config.formData))
      localStorage.setItem("searchData", JSON.stringify(@search))
    getTelescopes: ()->
      # check if we have a cached set to use
      telescopes = JSON.parse(localStorage.getItem("telescopes")||"0")
      self = @
      now = moment()
      if telescopes and moment(telescopes?.expires) > now
        self.telescopes = telescopes.telescopes
      else
        new Ajax
          url: window.location.origin+"/dal/ti-pairs"
          method: "get"
          accept: "json"
          success: (data)->
            self.telescopes = data
            telescopes = {
              expires: moment().add(7,'days')
              telescopes: data
            }
            localStorage.setItem("telescopes", JSON.stringify(telescopes))

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

}

export default searchFormComponent 
