
/*
Author: Peter Peterson
Date: 2017-06-09
Description: Serves functionality for submitting and displaying archive query forms/results
Original file: search.coffee
 */
var Search, SearchResults, search;

Search = (function() {
  Search.prototype.formData = {
    coordinates: {
      ra: null,
      dec: null
    },
    pi: null,
    search_box_min: null,
    prop_id: null,
    obs_date: ['', '', "="],
    filename: null,
    original_filename: null,
    telescope: [],
    exposure_time: ['', '', "="],
    instrument: [],
    release_date: ['', '', "="],
    image_filter: []
  };

  function Search() {
    this.bindEvents();
    this.form = new Vue({
      el: "#search-form",
      data: {
        view: null,
        search: Object.create(this.formData)
      },
      computed: {
        obsDateMin: function() {
          return this.search.obs_date[0];
        },
        obsDateMax: function() {
          return this.search.obs_date[1];
        },
        obsDateInterval: function() {
          return this.search.obs_date[2];
        }
      }
    });
  }

  Search.prototype.bindEvents = function() {
    return console.log("binding yo");
  };

  return Search;

})();

SearchResults = (function() {
  function SearchResults() {}

  return SearchResults;

})();

search = new Search();

window.base.bindEvents();
