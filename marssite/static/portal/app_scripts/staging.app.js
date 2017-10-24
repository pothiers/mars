var App;

import Staging from "../vue/Staging.vue";

import Vue from 'vue';

import AppStyles from "../styles/search.scss";

App = (function() {
  function App() {
    new Vue({
      el: "#content",
      template: "<component compdata='componentData' v-bind:is='currentView' v-on:displayform='switchComponent' />",
      methods: {
        switchComponent: function(data) {
          return this.currentView = data[0];
        }
      },
      data: {
        currentView: "staging",
        componentData: []
      },
      components: {
        staging: Staging
      }
    });
  }

  return App;

})();

new App();
