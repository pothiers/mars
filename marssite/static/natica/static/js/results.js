
/*
Author: Peter Peterson
Date: 2017-06-09
Description: Serves functionality for displaying and filtering result sets
Original file: results.coffee
 */

/*
  Helper functions
 */
var Results, results;

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
   App - Results Class
 */

Results = (function() {
  function Results() {
    console.log("Results set created");
    window.base.bindEvents();
    this.table = new Vue({
      el: "#query-results",
      data: {
        visibleColumns: JSON.parse(JSON.stringify(this.defaultColumns)),
        visible: false,
        results: []
      },
      methods: {
        displayForm: function() {
          window.results.table.visible = false;
          return window.searchForm.form.visible = true;
        }
      }
    });
  }

  Results.prototype.defaultColumns = [
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
  ];

  return Results;

})();

results = new Results();
