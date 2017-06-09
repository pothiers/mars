
/*
Author: Peter Peterson
Date: 2017-06-09
Description: Serves functionality for submitting and displaying archive query forms/results
Original file: search.coffee
 */
var Search, SearchResults, search;

Search = (function() {
  function Search() {
    this.bindEvents();
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
