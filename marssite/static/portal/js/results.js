
/*
Author: Peter Peterson
Date: 2017-06-09
Description: Serves functionality for displaying and filtering result sets
Original file: results.coffee
 */
var config;

import Vue from "vue";

import Shared from "./mixins.coffee";

import "./components.coffee";


/*
  Helper functions
 */

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

export default {
  props: ['componentData'],
  mixins: [Shared.mixin],
  data: function() {
    return {
      visibleColumns: [],
      allColumns: config.allColumns,
      stageAllConfirm: false,
      stageButtonText: "Stage ALL results",
      visible: false,
      pageNum: 1,
      isLoading: false,
      recordsFrom: 1,
      recordsTo: 100,
      results: [],
      selected: [],
      searchObj: JSON.parse(localStorage.getItem('search')),
      totalItems: 0,
      toggle: false,
      error: ""
    };
  },
  methods: {
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
        ref1 = this.visibleColumns;
        for (n = j = 0, len1 = ref1.length; j < len1; n = ++j) {
          col = ref1[n];
          if (column.num < col.num) {
            first = this.visibleColumns.slice(0, n);
            last = this.visibleColumns.slice(n);
            this.visibleColumns = first.concat(column, last);
            found = true;
            break;
          }
        }
        if (found !== true) {
          this.visibleColumns.push(column);
        }
      }
      return column.checked = !column.checked;
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
      return form.submit();
    },
    confirmStage: function() {
      if (this.stageAllConfirm === true) {
        console.log("second confirm is true");
        localStorage.setItem("stage", "all");
        return window.location.href = config.stagingUrl + "?stage=all";
      } else {
        this.stageButtonText = "OK, continue";
        return this.stageAllConfirm = true;
      }
    },
    toggleResults: function() {
      this.toggle = !this.toggle;
      console.log("toggle");
      return bus.$emit("toggleselected", this.toggle);
    },
    displayForm: function() {
      window.location.hash = "#search_again";
      return this.$emit("displayform", ["search", JSON.parse(localStorage.getItem('search'))]);
    },
    handleError: function(e) {
      return console.log("There was an error", e);
    },
    pageNext: function() {
      return this.pageTo(this.pageNum + 1);
    },
    pageBack: function() {
      return this.pageTo(this.pageNum - 1);
    },
    pageTo: function(page) {
      var self;
      this.pageNum = page;
      localStorage.setItem('currentPage', page);
      this.$emit("pageto", page);
      this.isLoading = true;
      self = this;
      return this.submitForm(null, "paging", function(data) {
        self.isLoading = false;
        self.results = data;
        self.recordsFrom = data.meta.to_here_count - data.meta.page_result_count + 1;
        return self.recordsTo = data.meta.to_here_count;
      });
    }
  },
  created: function() {
    var col, i, len, ref, results;
    ref = this.allColumns;
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
    return window.base.bindEvents();
  },
  mounted: function() {
    var e, ref;
    window.results = this;
    console.log("Results mounted");
    bus.$on("toggleselected", (function(_this) {
      return function(onoff) {
        if (onoff) {
          return _this.selected = [].concat(_this.results.resultset);
        } else {
          return _this.selected = [];
        }
      };
    })(this));
    bus.$on("rowselected", (function(_this) {
      return function(data) {
        var index;
        if (data.isSelected) {
          return _this.selected.push(data.row);
        } else {
          index = _.indexOf(_this.selected, data.row);
          return _this.selected.splice(index, 1);
        }
      };
    })(this));
    if (window.location.hash === "#query") {
      try {
        this.results = JSON.parse(localStorage.getItem('results')) || [];
        this.totalItems = (ref = this.results) != null ? ref.meta.total_count : void 0;
        this.visible = true;
        this.pageNum = parseInt(localStorage.getItem("currentPage"));
      } catch (error) {
        e = error;
        this.results = [];
        this.totalItems = 0;
        this.visible = true;
        this.error = "There was an error parsing results from server";
        this.handleError(e);
      }
    }
    return console.log(document.querySelectorAll(".collapsible"));
  }
};
