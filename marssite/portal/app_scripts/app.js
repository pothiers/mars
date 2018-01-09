var Vue = require("vue");
var moment = require("moment");

import Search from "../vue/Search.vue";
import Results from "../vue/Results.vue";
var AppStyles = require("../styles/search.scss");

var initDone = false;

class App {
  constructor(){
    window.moment = moment;
    new Vue({
      el: "#content",
      template: "<component compdata='componentData' v-bind:is='currentView' v-on:displayform='switchComponent' />",
      created: function(){
        this.pushState();
        console.log("setting popstate function");
        window.onpopstate = this.popState;

        // create an event bus for inter component communication
        window.bus = new Vue();
      },
      methods: {
        popState(state){
          console.log("state changed", state);
          // replace state...
          if( state.state ){
            var data = [state.state.view, state.state.data];
            this.switchComponent(data, false);
            return true;
          }
          return true;
        },
        pushState(){
          var url = window.location.pathname;
          if( url.endsWith("/") == false){ url += "/";}

          console.log("Pushstate called", {"initstate:":initDone, "url": url});
          // the only time this doesn't fit is when the "Search Again" button is clicked in the results
          if( this.currentView === "search" && url.match("results") !== null && window.search_again !== true){
            this.currentView = "results";
          }
          if( this.currentView === "results" && url.match("results") === null){
            url += "results/";
          }
          // check for condition where we want to search again
          if( window.search_again === true){
            url = "/portal/search/";
          }
          if( initDone == false){
            initDone = true;
            history.replaceState({'view':this.currentView, data:this.componentData}, this.currentView, url);
          }else{
            history.pushState({'view':this.currentView, data:this.componentData}, this.currentView, url);
          }
        },
        switchComponent(data, doPushState){
          this.componentData = data[1];
          this.currentView = data[0];
          if( doPushState !== false){
            this.pushState();
          }
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
