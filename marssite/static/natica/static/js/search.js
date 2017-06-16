
/*
Author: Peter Peterson
Date: 2017-06-09
Description: Serves functionality for submitting and displaying archive query forms/results
Original file: search.coffee
 */
var SearchForm, SearchResults, searchForm;

SearchForm = (function() {
  SearchForm.prototype.apiUrl = "/dal/search/";

  SearchForm.prototype.rangeInputs = ["obs_date", "exposure_time", "release_date"];

  SearchForm.prototype.formData = {
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

  SearchForm.prototype.loadingMessages = ["Searching the cosmos...", "Deploying deep space probes...", "Is that you Dave?...", "There's so much S P A C E!"];

  function SearchForm() {
    this.bindEvents();
    this.form = new Vue({
      el: "#search-form",
      data: {
        visible: true,
        loading: false,
        loadingMessage: "Sweeping up star dust...",
        search: JSON.parse(JSON.stringify(this.formData))
      },
      methods: {
        submitForm: function(event) {
          var key, message, msgs, newFormData;
          event.preventDefault();
          this.loading = true;
          newFormData = JSON.parse(JSON.stringify(this.search));
          for (key in newFormData) {
            if (_.isEqual(newFormData[key], searchForm.formData[key])) {
              delete newFormData[key];
            } else {
              if (searchForm.rangeInputs.indexOf(key) >= 0) {
                if (newFormData[key][2] === "=") {
                  newFormData[key] = newFormData[key][0];
                }
              }
            }
          }
          msgs = searchForm.loadingMessages;
          message = Math.floor(Math.random() * msgs.length);
          this.loadingMessage = message;
          return new Ajax({
            url: "/dal/search/",
            method: "post",
            accept: "json",
            data: {
              search: newFormData
            },
            success: function(data) {
              window.searchForm.form.loading = false;
              window.searchForm.form.visible = false;
              window.results.table.results = data;
              window.results.table.visible = true;
              return console.dir(data);
            }
          }).send();
        }
      }
    });
  }

  SearchForm.prototype.bindEvents = function() {
    return console.log("binding yo");
  };

  return SearchForm;

})();

SearchResults = (function() {
  function SearchResults() {}

  return SearchResults;

})();

searchForm = new SearchForm();

window.base.bindEvents();
