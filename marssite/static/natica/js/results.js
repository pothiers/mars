
/*
Author: Peter Peterson
Date: 2017-06-09
Description: Serves functionality for displaying and filtering result sets
Original file: results.coffee
 */
var config;

import Vue from "vue";

import Shared from "./mixins.coffee";


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
   Vue components
 */

Vue.component("table-header", {
  props: ['name'],
  template: "<th>{{ name }}</th>"
});

Vue.component("table-cell", {
  props: ['data', 'field'],
  template: "<td v-if='data' v-bind:rel='field'>{{ format }}</td><td class='empty' v-else></td>",
  computed: {
    format: function() {
      var d, dateStr;
      if (this.data === null) {
        return this.data;
      }
      if (this.field === 'obs_date' || this.field === 'release_date') {
        try {
          d = moment(this.data);
          dateStr = d.format("YYYY-MM-DD");
          return dateStr;
        } catch (error) {
          return this.data;
        }
      } else {
        return this.data;
      }
    }
  }
});

Vue.component("table-row", {
  props: ['row', 'cols'],
  template: "<tr v-on:click='selectRow' v-bind:class='{selected:isSelected}'><td class='select-row'><input type='checkbox' name='' v-bind:checked='isSelected' v-bind:name='row.reference'></td><table-cell v-for='vis in cols' v-bind:data='row[vis.mapping]' v-bind:field='vis.mapping' :key='row.id'></table-cell></tr>",
  data: function() {
    return {
      isSelected: false
    };
  },
  methods: {
    selectRow: function() {
      this.isSelected = !this.isSelected;
      return console.log("Row selected");
    }
  }
});

Vue.component("table-body", {
  props: ['data', 'visibleCols'],
  template: "<tbody><table-row v-for='(item,idx) in data' v-bind:cols='visibleCols' v-bind:row='item' :key='item.id'></table-row></tbody>"
});


/*
   App - Results
 */

config = Shared.config;

export default {
  props: ['componentData'],
  mixins: [Shared.mixin],
  data: function() {
    return {
      visibleColumns: JSON.parse(JSON.stringify(config.defaultColumns)),
      visible: false,
      pageNum: 1,
      isLoading: false,
      recordsFrom: 1,
      recordsTo: 100,
      results: [],
      searchObj: JSON.parse(localStorage.getItem('search')),
      totalItems: 0,
      error: ""
    };
  },
  methods: {
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
  mounted: function() {
    var e, ref;
    window.base.bindEvents();
    if (window.location.hash === "#query") {
      try {
        this.results = JSON.parse(localStorage.getItem('results')) || [];
        this.totalItems = (ref = this.results) != null ? ref.meta.total_count : void 0;
        this.visible = true;
        return this.pageNum = parseInt(localStorage.getItem("currentPage"));
      } catch (error) {
        e = error;
        this.results = [];
        this.totalItems = 0;
        this.visible = true;
        this.error = "There was an error parsing results from server";
        return this.handleError(e);
      }
    }
  }
};
