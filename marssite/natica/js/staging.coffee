###
Author: Peter Peterson
Date: 2017-07-24
Description: Code for interactions with the staging page
Original file: staging.coffee
###


import Vue from 'vue'

generateResultsSet = ()->
  results = []
  for x in [1..100]
    results.push {count:x, filename: Math.random().toString(36).substring(7)}

  return results

stagingComponent = {
  created: ()->
    window.staging = @
    console.log "Staging created"
  mounted: ()->
    console.log "Component mounted"
    @results = generateResultsSet()
  methods:
    toggleSelected:()->
      console.dir arguments
  data: ()->
    return
      results: []
      selected: []
}


export default stagingComponent
