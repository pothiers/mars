var Vue = require("vue");
var moment = require("moment");

import Search from "../vue/Search.vue";
import Results from "../vue/Results.vue";

var AppStyles = require("../styles/search.scss");

//import Main from "../vue/Main.vue";

class App {
  constructor(){
    window.moment = moment;
    new Vue({
      el: "#content",
      template: "<component compdata='componentData' v-bind:is='currentView' v-on:displayform='switchComponent' />",
      methods: {
        switchComponent(data){
          this.componentData = data[1];
          this.currentView = data[0];
          window.base.bindEvents();
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
}

new App();
