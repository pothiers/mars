var App;

import Vue from "vue";

import moment from "moment";

import _ from "lodash";

import Search from "./vue/Search.vue";

import AppStyles from "./styles/search.scss";

App = (function() {
  function App() {
    window.moment = moment;
    window._ = _;
    new Vue({
      el: "#content",
      template: "<app/>",
      components: {
        app: Search
      }
    });
  }

  return App;

})();

new App();
