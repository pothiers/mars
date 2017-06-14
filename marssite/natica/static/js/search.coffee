###
Author: Peter Peterson
Date: 2017-06-09
Description: Serves functionality for submitting and displaying archive query forms/results
Original file: search.coffee
###



class SearchForm
  apiUrl: "/dal/search/"
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

  constructor: ()->
    @bindEvents()

    @form = new Vue
      el:"#search-form"
      data:
        view: null # future home of state data
        search: JSON.parse(JSON.stringify(@formData)) # deep copy
      methods:
        submitForm: (event)->
          event.preventDefault()
          # TODO: Validate
          # strip out anything that wasn't modified
          newFormData = JSON.parse(JSON.stringify(@search))
          console.dir newFormData
          console.dir searchForm.formData
          for key of newFormData
            if _.isEqual(newFormData[key], searchForm.formData[key])
              delete(newFormData[key])

          new Ajax
            url: "/dal/search/"
            method: "post"
            accept: "json"
            data:
              search: newFormData
            success: (data)->
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
