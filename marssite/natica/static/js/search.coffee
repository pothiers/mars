###
Author: Peter Peterson
Date: 2017-06-09
Description: Serves functionality for submitting and displaying archive query forms/results
Original file: search.coffee
###


class Search
  constructor: ()->
    @bindEvents()

  bindEvents:()->
    console.log "binding yo"

class SearchResults
  # vue ui


search = new Search()
