import Vue from "vue";
import "./components.js";
import Shared from "./mixins.js";
import _ from "lodash";

/*
  Helper functions
 */
var config;

Number.prototype.pad = function(size, char) {
  var s;
  if (char == null) {
    char = '0';
  }
  s = String(this);
  while (s.length < (size || 2)) {
    s = "0" + s;
  }
  return s;
};

/*
  App - Results
 */

config = Shared.config;

window.bus = new Vue();

var Results;

export default Results = {
  props : ['componentData'],
  mixins: [Shared.mixin],
  data  : function() {
    return {
      visibleColumns   : [],
      categoriesVisible: false,
      categories       : {},
      categorizeFirst  : false,
      categoryApplied  : false,
      categoryHistory  : [],
      activeTab        : 'main',
      allColumns       : config.allColumns,
      stageAllConfirm  : false,
      stageButtonText  : "Stage ALL results",
      visible          : false,
      pageNum          : 1,
      isLoading        : false,
      recordsFrom      : 1,
      recordsTo        : 100,
      results          : [],
      selected         : [],
      lastSelected     : null,
      searchObj        : JSON.parse(localStorage.getItem('search')),
      totalItems       : 0,
      toggle           : false,
      error            : ""
    };
  },
  computed: {
    categoriesLoaded: function(){
      return !_.isEmpty(this.categories);
    }
  },
  methods: {
    showResultsTable: function(){
      this.categorizeFirst = false;
      //this.categoriesVisible = false;
    },
    clearCategory: function(){
      this.categoryApplied = false;
      this.results         = JSON.parse(localStorage.getItem("results"));
      this.totalItems      = this.results.meta.total_count;
      this.categoryHistory = [];
      // clear the selected categories
      var selected = document.querySelectorAll(".results-categories input:checked");
      for( var input of selected){
        input.checked = false;
      }
      this.getCategory(localStorage.getItem("search"));
    },
    setCategory: function (category_key, category_value) {
      console.log("category_key:", category_key, "cat_value", category_value);
      //split instrument/telescope
      var key   = category_key;
      var value = category_value;

      if( this.categorizeFirst ){
        this.categorizeFirst = false;
      }

      if( key == "telescope_instrument"){
        value = [value.split(",")];
      }

      // Some values can be null or '' in the db, but not all values will
      // validate on null, so....
      if( value == null){
        value = '';
      }

      // set the category in the original search query
      var query = "";
      console.log("categoryHistory has this:");
      console.dir(this.categoryHistory);
      if( this.categoryHistory.length === 0){
        query = localStorage.getItem("search");
      }else{
        query = this.categoryHistory[this.categoryHistory.length - 1].query;
      }
      query = JSON.parse(query);
      query[key]  = value;

      // save this new query for future (paging etc)
      localStorage.setItem("category_selection", JSON.stringify(query));

      // Set history...
      // also allow for back/forward so push into browser history
      this.categoryHistory.push({"category":value, "query":JSON.stringify(query)});

      // get the category results from the server...
      this.submitQuery(config.apiUrl, query, key, (data)=>{
        console.log("got this category resultset", data);
        // create a new tab and place results there
        this.results         = data;
        this.categoryApplied = true;
        this.totalItems      = data.meta.total_count;
      });
      // get updated categories for this resultset....
      this.getCategory(JSON.stringify(query));
    },

    getCategory: function(query){
      var self      = this;
      var localCats = localStorage.getItem("categories");
      if ( (localCats = JSON.parse(localCats)) !== null && !_.isEmpty(localCats) ){
        self.categories = localCats;
      }else{
        console.log("Categories...",self.categories.length);
        new Ajax({
          url    : window.location.origin + "/dal/get-categories",
          data   : JSON.parse(query),
          method : "post",
          accept : "json",
          success: function(data) {

            if (data.status == "success"){
              var cats = {};
              /*
                categories: {
                  'name': [
                    {'name':'value', 'total': ###}
                    ...
                    n{'name':'value', 'total': ###}
                  ]
                }
              */
              for(var item in data.categories){
                for(var val in data.categories[item]){
                  // null is a valid & possible value
                  if(cats[item] == undefined){ cats[item] = [];}
                  var name   = data.categories[item][val][item];
                  var detail = {
                    "name" : name,
                    "total": data.categories[item][val]['total']
                  };
                  cats[item].push(detail);

                }
              }
              console.log("formated categories", cats);
              localStorage.setItem("categories", JSON.stringify(cats));
              self.categories = cats;
            }
          }
        });
      }
    },


    toggleCategories: function() {
      this.categoriesVisible = !this.categoriesVisible;
      if( this.categoriesVisible ){
        this.categorizeFirst = false;
      }
    },

    toggleColumn: function(column) {
      var col, first, found, i, j, last, len, len1, n, ref, ref1;
      if (column.checked) {
        ref = this.visibleColumns;
        for (n = i = 0, len = ref.length; i < len; n = ++i) {
          col = ref[n];
          if (_.isEqual(col, column)) {
            this.visibleColumns.splice(n, 1);
          }
        }
      } else {
        found = false;
        ref1  = this.visibleColumns;
        for (n = j = 0, len1 = ref1.length; j < len1; n = ++j) {
          col = ref1[n];
          if (column.num < col.num) {
            first               = this.visibleColumns.slice(0, n);
            last                = this.visibleColumns.slice(n);
            this.visibleColumns = first.concat(column, last);
            found               = true;
            break;
          }
        }
        if (found !== true) {
          this.visibleColumns.push(column);
        }
      }
      column.checked = !column.checked;
    },

    stageSelected: function() {
      var data, form;
      localStorage.setItem("stage", "selectedFiles");
      localStorage.setItem("selectedFiles", JSON.stringify(this.selected));
      form = document.createElement("form");
      form.setAttribute("method", "POST");
      form.setAttribute("action", "/portal/staging/?stage=selected");
      data = document.createElement("input");
      data.setAttribute("type", "hidden");
      data.setAttribute("value", localStorage.getItem("selectedFiles"));
      data.setAttribute("name", "selectedFiles");
      form.appendChild(data);
      document.querySelector("body").appendChild(form);
      form.submit();
    },

    cancelStageAll: function() {
      this.stageButtonText = 'Stage ALL results';
      this.stageAllConfirm = false;
    },

    confirmStage: function() {
      var data, form, searchObj;
      if (this.stageAllConfirm === true) {
        console.log("second confirm is true");
        localStorage.setItem("stage", "all");
        form = document.createElement("form");
        form.setAttribute("method", "POST");
        form.setAttribute("action", config.stagingUrl + "?stage=all");
        data = document.createElement("input");
        data.setAttribute("type", "hidden");
        searchObj = localStorage.getItem("searchData");
        data.setAttribute("value", searchObj);
        data.setAttribute("name", "searchData");
        form.appendChild(data);
        document.querySelector("body").appendChild(form);
        form.submit();
      } else {
        this.stageButtonText = "OK, continue";
        this.stageAllConfirm = true;
      }
    },

    toggleResults: function() {
      this.toggle = !this.toggle;
      console.log("toggle");
      rebus.$emit("toggleselected", this.toggle);
    },

    displayForm: function() {
      window.search_again = true;
      this.$emit("displayform", ["search", JSON.parse(localStorage.getItem('search')), "search_again"]);
    },

    handleError: function(e) {
      console.log("There was an error", e);
    },

    pageNext: function() {
      this.pageTo(this.pageNum + 1);
    },

    pageBack: function() {
      this.pageTo(this.pageNum - 1);
    },

    pageTo: function(page) {
      var self;
      this.pageNum = page;
      localStorage.setItem('currentPage', page);
      this.$emit("pageto", page);
      this.isLoading = true;
      self           = this;
      this.submitForm(null, "paging", function(data) {
        self.isLoading   = false;
        self.results     = data;
        self.recordsFrom = data.meta.to_here_count - data.meta.page_result_count + 1;
        self.recordsTo   = data.meta.to_here_count;
      });
    }
  },

  created: function() {
    var col, i, len, ref, results;
    ref     = this.allColumns;
    results = [];
    for (i = 0, len = ref.length; i < len; i++) {
      col = ref[i];
      if (col.checked) {
        results.push(this.visibleColumns.push(col));
      } else {
        results.push(void 0);
      }
    }
    return results;
  },

  updated: function() {
    window.base.bindEvents();
  },

  mounted: function() {
    var e, q, ref;
    window.results = this;
    console.log("Results mounted");
    q = localStorage.getItem("search");

    // get categories for this query
    this.getCategory(q);

    bus.$on("toggleselected", (function(_this) {
      return function(onoff) {
        if (onoff) {
          _this.selected = [].concat(_this.results.resultset);
        } else {
          _this.selected = [];
        }
      };
    })(this));
    bus.$on("rowselected", (function(_this) {
      return function(data) {
        var alreadySelected, curIdx, i, idx, index, j, k, l, len, len1, len2, obj, prevIdx, ref, ref1, ref2, ref3, ref4, row, sel;
        if (data.isSelected) {
          _this.selected.push(data.row);
          if (data.event.shiftKey) {
            prevIdx = null;
            curIdx  = null;
            ref     = _this.results.resultset;
            for (idx = i = 0, len = ref.length; i < len; idx = ++i) {
              obj = ref[idx];
              if (obj === data.row) {
                curIdx = idx;
                break;
              }
            }
            ref1 = _this.results.resultset;
            for (idx = j = 0, len1 = ref1.length; j < len1; idx = ++j) {
              obj = ref1[idx];
              if (obj === _this.lastSelected) {
                prevIdx = idx;
                break;
              }
            }
            for (idx = k = ref2 = prevIdx, ref3 = curIdx; ref2 <= ref3 ? k <= ref3 : k >= ref3; idx = ref2 <= ref3 ? ++k : --k) {
              row             = _this.results.resultset[idx];
              alreadySelected = false;
              ref4            = _this.selected;
              for (l = 0, len2 = ref4.length; l < len2; l++) {
                sel = ref4[l];
                if (row.reference === sel.reference) {
                  alreadySelected = true;
                  break;
                }
              }
              if (alreadySelected === false) {
                bus.$emit("selectrow", row);
                _this.selected.push(row);
              }
            }
          }
          _this.lastSelected = data.row;
        } else {
          index = _.indexOf(_this.selected, data.row);
          _this.selected.splice(index, 1);
        }
      };
    })(this));
    if (window.location.hash === "#query" || window.location.pathname.match("/portal/search/results") !== null) {
      try {
        this.results    = JSON.parse(localStorage.getItem('results')) || [];
        this.totalItems = (ref = this.results) != null ? ref.meta.total_count : void 0;
        this.visible    = true;
        this.pageNum    = parseInt(localStorage.getItem("currentPage"));
        if(this.totalItems > 1000){
          this.categorizeFirst = true;
        }
        } catch (_error) {
        e               = _error;
        this.results    = [];
        this.totalItems = 0;
        this.visible    = true;
        this.error      = "There was an error parsing results from server";
        this.handleError(e);
      }
    }
  }
}
