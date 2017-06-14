
/*
Author: Peter Peterson
Date: 2017-06-09
Description: Serves functionality for submitting and displaying archive query forms/results
Original file: search.coffee
 */
var SearchForm, SearchResults, searchForm;

SearchForm = (function() {
  SearchForm.prototype.apiUrl = "/dal/search/";

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

  function SearchForm() {
    this.bindEvents();
    this.form = new Vue({
      el: "#search-form",
      data: {
        view: null,
        search: JSON.parse(JSON.stringify(this.formData))
      },
      methods: {
        submitForm: function(event) {
          var key, newFormData;
          event.preventDefault();
          newFormData = JSON.parse(JSON.stringify(this.search));
          console.dir(newFormData);
          console.dir(searchForm.formData);
          for (key in newFormData) {
            if (_.isEqual(newFormData[key], searchForm.formData[key])) {
              delete newFormData[key];
            }
          }
          return new Ajax({
            url: "/dal/search/",
            method: "post",
            accept: "json",
            data: {
              search: newFormData
            },
            success: function(data) {
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
