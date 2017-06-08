var Search, SearchResults, nohup, search;

if (window.location.hostname !== "localhost") {
  nohup = function() {
    return "";
  };
  console.log = nohup;
  console.info = nohup;
  console.dir = nohup;
}

window.addMultiEventListener = function(elem, events, fn) {
  return events.split(' ').forEach(function(e) {
    return elem.addEventListener(e, fn, false);
  });
};

Search = (function() {
  function Search() {
    this.bindEvents();
  }

  Search.prototype.bindEvents = function() {
    var el, els, i, j, len, len1, results, section, sections, toggle;
    console.log("binding yo");
    els = document.querySelectorAll("input[type=text]");
    for (i = 0, len = els.length; i < len; i++) {
      el = els[i];
      addMultiEventListener(el, 'keyup blur', function(event) {
        var target;
        target = event.currentTarget;
        if (target.value === "") {
          return target.previousElementSibling.classList.remove("open");
        } else {
          return target.previousElementSibling.classList.add("open");
        }
      });
    }
    sections = document.querySelectorAll(".collapsible");
    results = [];
    for (j = 0, len1 = sections.length; j < len1; j++) {
      section = sections[j];
      toggle = section.querySelector(".section-toggle");
      results.push(toggle.addEventListener("click", function(e) {
        return section.classList.toggle("open");
      }));
    }
    return results;
  };

  return Search;

})();

SearchResults = (function() {
  function SearchResults() {}

  return SearchResults;

})();

search = new Search();
