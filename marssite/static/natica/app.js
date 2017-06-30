var App;

import Vue from "vue";

import moment from "moment";

import _ from "lodash";

import Search from "./vue/Search.vue";

import Results from "./vue/Results.vue";

import AppStyles from "./styles/search.scss";

App = (function() {
  function App() {
    window.moment = moment;
    window._ = _;
    new Vue({
      el: "#content",
      template: "<component data='componentData' v-bind:is='currentView' v-on:displayform='switchComponent' />",
      methods: {
        switchComponent: function(data) {
          this.componentData = data[1];
          return this.currentView = data[0];
        }
      },
      data: {
        currentView: "search",
        componentData: []
      },
      components: {
        search: Search,
        results: Results
      }
    });
  }

  return App;

})();

new App();
