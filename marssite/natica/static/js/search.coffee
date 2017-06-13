###
Author: Peter Peterson
Date: 2017-06-09
Description: Serves functionality for submitting and displaying archive query forms/results
Original file: search.coffee
###



class Search
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
        search: Object.create(@formData) # deep copy
      computed:
        obsDateMin: ()->
          return @search.obs_date[0]
        obsDateMax: ()->
          return @search.obs_date[1]
        obsDateInterval:()->
          return @search.obs_date[2]

  bindEvents:()->
    console.log "binding yo"
    # TODO: Validation
    # TODO: formatting
    # TODO: save form data
    # TODO: save state data i.e. UI states

class SearchResults
  # vue ui


search = new Search()
# Vue clobbers previous bindings, so re-bind
window.base.bindEvents()
