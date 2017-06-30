import Vue from "vue"
#import Results from "./js/results.coffee"
import moment from "moment"
import _ from "lodash"
import Search from "./vue/Search.vue"
import AppStyles from "./styles/search.scss"

class App
  constructor: ()->
    window.moment = moment
    window._ = _
    new Vue
      el: "#content"
      template: "<app/>"
      components:
        app: Search




new App()
