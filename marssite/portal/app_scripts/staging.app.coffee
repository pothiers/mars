import Staging from "../vue/Staging.vue"
import Vue from 'vue'
import AppStyles from "../styles/search.scss"

class App
  constructor: ()->
    new Vue
      el: "#content"
      template: "<component compdata='componentData' v-bind:is='currentView' v-on:displayform='switchComponent' />"
      methods:
        switchComponent: (data)->
          @currentView = data[0]
      data:
        currentView: "staging"
        componentData: []
      components:
        staging: Staging
new App()
