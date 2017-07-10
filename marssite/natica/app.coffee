import Vue from "vue"
#import Results from "./js/results.coffee"
import moment from "moment"
import _ from "lodash"
import Search from "./vue/Search.vue"
import Results from "./vue/Results.vue"

import AppStyles from "./styles/search.scss"

class App
  constructor: ()->
    window.moment = moment
    window._ = _
    new Vue
      el: "#content"
      template: "<component compdata='componentData' v-bind:is='currentView' v-on:displayform='switchComponent' />"
      methods:
        switchComponent: (data)->
          @componentData = data[1]
          @currentView = data[0]
      data:
        currentView: "search"
        componentData: []
      components:
        search: Search
        results: Results

new App()
