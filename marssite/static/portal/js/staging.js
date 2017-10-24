
/*
Author: Peter Peterson
Date: 2017-07-24
Description: Code for interactions with the staging page
Original file: staging.coffee
 */
var generateResultsSet, stagingComponent;

import Shared from './mixins.coffee';

import Vue from 'vue';

generateResultsSet = function() {
  var i, results, x;
  results = [];
  for (x = i = 1; i <= 100; x = ++i) {
    results.push({
      count: x,
      filename: Math.random().toString(36).substring(7)
    });
  }
  return results;
};

stagingComponent = {
  mixins: [Shared.mixin],
  data: function() {
    return {
      stagingAllFiles: false,
      loading: false,
      selectAll: false,
      results: [],
      selected: []
    };
  },
  created: function() {
    window.staging = this;
    return console.log("Staging created");
  },
  mounted: function() {
    var file, files, i, len, query, results1;
    console.log("Component mounted");
    window.base.bindEvents();
    if (localStorage.getItem("stage") === "selectedFiles") {
      files = JSON.parse(localStorage.getItem("selectedFiles"));
      results1 = [];
      for (i = 0, len = files.length; i < len; i++) {
        file = files[i];
        results1.push(this.results.push({
          'selected': false,
          'file': file
        }));
      }
      return results1;
    } else {
      this.stagingAllFiles = true;
      this.loading = true;
      query = this.stripData();
      return new Ajax({
        url: "/dal/staging/",
        method: "post",
        accept: "json",
        data: query,
        success: (function(_this) {
          return function(data) {
            console.log("got this data back from the request");
            console.log(data);
            return _this.loading = false;
          };
        })(this),
        fail: function(statusMsg, status, xhr) {
          return console.log("ajax failed");
        }
      });
    }
  },
  methods: {
    toggleAll: function() {
      var file, i, j, len, len1, ref, ref1, results1;
      this.selectAll = !this.selectAll;
      if (this.selectAll) {
        ref = this.results;
        results1 = [];
        for (i = 0, len = ref.length; i < len; i++) {
          file = ref[i];
          file.selected = true;
          results1.push(this.selected.push(file));
        }
        return results1;
      } else {
        ref1 = this.results;
        for (j = 0, len1 = ref1.length; j < len1; j++) {
          file = ref1[j];
          file.selected = false;
        }
        return this.selected = [];
      }
    },
    downloadSingleFile: function(file, event) {
      event.stopPropagation();
      window.open("/portal/downloadsinglefile/?f=" + file.reference, "_blank");
      return false;
    },
    _confirmDownloadSelected: function() {
      var query, selected;
      selected = this.selected;
      query = {
        "files": selected.slice(0, 10)
      };
      return new Ajax({
        url: "/portal/downloadselected",
        method: "post",
        accept: "json",
        data: query,
        success: (function(_this) {
          return function(data) {
            console.log("Got this from the server");
            return console.log(data);
          };
        })(this),
        fail: function(statusmsg, status, xhr) {
          return console.log("request failed");
        }
      });
    },
    downloadSelected: function() {
      var self;
      console.log("downloading selected");
      self = this;
      if (this.selected.length > 10) {
        return BootstrapDialog.confirm("Only ten files can be downloaded at one time. See download instructions for downloading more at one time", function(goAhead) {
          if (goAhead) {
            return self._confirmDownloadSelected();
          }
        });
      } else {
        return self._confirmDownloadSelected();
      }
    },
    toggleSelected: function(item) {
      var indx;
      item.selected = !item.selected;
      if (item.selected) {
        return this.selected.push(item);
      } else {
        indx = _.indexOf(this.selected, item);
        return this.selected.splice(indx, 1);
      }
    }
  }
};

export default stagingComponent;
