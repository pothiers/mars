
/*
Author: Peter Peterson
Date: 2017-06-09
Description: Serves functionality for displaying and filtering result sets
Original file: results.coffee
 */
var config;

import Vue from "vue";


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
  props: ['data'],
  template: "<td v-if='data'>{{ format }}</td><td class='empty' v-else></td>",
  computed: {
    format: function() {
      var d, dateStr;
      if (this.data === null) {
        return this.data;
      }
      if (this.data.toString().match(/\d{4}-\d{2}-[0-9T:]+/) !== null) {
        try {
          d = new Date(this.data);
          dateStr = (d.getFullYear()) + "-" + ((d.getMonth() + 1).pad()) + "-" + ((d.getDate()).pad());
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
  template: "<tr v-on:click='selectRow' v-bind:class='{selected:isSelected}'><td class='select-row'><input type='checkbox' name='' v-bind:checked='isSelected' v-bind:name='row.reference'></td><table-cell v-for='vis in cols' v-bind:data='row[vis.mapping]' :key='row.id'></table-cell></tr>",
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

config = {
  defaultColumns: [
    {
      "mapping": "dec",
      "name": "Dec"
    }, {
      "mapping": "depth",
      "name": "Depth"
    }, {
      "mapping": "exposure",
      "name": "Exposure"
    }, {
      "mapping": "filename",
      "name": "Filename"
    }, {
      "mapping": "filesize",
      "name": "File size"
    }, {
      "mapping": "filter",
      "name": "Filter"
    }, {
      "mapping": "image_type",
      "name": "Image Type"
    }, {
      "mapping": "instrument",
      "name": "Instrument"
    }, {
      "mapping": "md5sum",
      "name": "MD5 sum"
    }, {
      "mapping": "obs_date",
      "name": "Observed date"
    }, {
      "mapping": "original_filename",
      "name": "Original filename"
    }, {
      "mapping": "pi",
      "name": "Principle Investigator"
    }, {
      "mapping": "product",
      "name": "Product"
    }, {
      "mapping": "prop_id",
      "name": "Program Number"
    }, {
      "mapping": "ra",
      "name": "RA"
    }, {
      "mapping": "reference",
      "name": "Reference"
    }, {
      "mapping": "release_date",
      "name": "Release Date"
    }, {
      "mapping": "seeing",
      "name": "Seeing"
    }, {
      "mapping": "telescope",
      "name": "Telescope"
    }, {
      "mapping": "survey_id",
      "name": "Survey Id"
    }
  ]
};

export default {
  props: ['componentData'],
  data: function() {
    return {
      visibleColumns: JSON.parse(JSON.stringify(config.defaultColumns)),
      visible: false,
      pageNum: 1,
      isLoading: false,
      results: []
    };
  },
  methods: {
    displayForm: function() {
      window.location.hash = "";
      return this.$emit("displayform", ["search", JSON.parse(localStorage.getItem('search'))]);
    },
    pageNext: function() {
      return this.pageTo(this.pageNum + 1);
    },
    pageBack: function() {
      return this.pageTo(this.pageNum - 1);
    },
    pageTo: function(page) {
      var self;
      this.$data.pageNum = page;
      localStorage.setItem('currentPage', page);
      this.$emit("pageto", page);
      this.$data.isLoading = true;
      self = this;
      return this.$emit("submitform", [
        null, "paging", function() {
          return self.$data.isLoading = false;
        }
      ]);
    }
  },
  mounted: function() {
    window.base.bindEvents();
    if (window.location.hash === "#query") {
      this.results = JSON.parse(localStorage.getItem('results'));
      this.visible = true;
      return this.pageNum = parseInt(localStorage.getItem("currentPage"));
    }
  }
};
