
/*
Author: Peter Peterson
Date: 2017-06-09
Description: Serves functionality for submitting and displaying archive query forms/results
Original file: search.coffee
 */
var config, searchFormComponent;

import Vue from 'vue';

import VeeValidate from 'vee-validate';

config = {
  apiUrl: "/dal/search/",
  rangeInputs: ["obs_date", "exposure_time", "release_date"],
  validatorConfig: {
    delay: 800,
    events: "input|blur",
    inject: true
  },
  formData: {
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
  },
  loadingMessages: ["Searching the cosmos...", "Deploying deep space probes...", "Is that you Dave?...", "There's so much S P A C E!"]
};

(function() {
  window.addEventListener('searchLoaded', function(e) {
    console.log("Search loaded", e);
    return window.base.bindEvents();
  });
  return Vue.use(VeeValidate, config.validatorConfig);
})();

searchFormComponent = {
  created: function() {
    return this.getTelescopes();
  },
  mounted: function() {
    var search;
    search = this.$parent.$data.componentData;
    if (search != null ? search.hasOwnProperty("coordinates") : void 0) {
      this.search = search;
    }
    return window.base.bindEvents();
  },
  data: function() {
    return {
      url: config.apiUrl,
      visible: true,
      loading: false,
      loadingMessage: "Sweeping up star dust...",
      search: JSON.parse(JSON.stringify(config.formData)),
      showExposureMax: false,
      showObsDateMax: false,
      showReleaseDateMax: false,
      showBothExposureFields: false,
      showBothObsDateFields: false,
      showBothReleaseDateFields: false,
      telescopes: [],
      relatedSplitFieldFlags: {
        "exposure_time": {
          "fieldFlag": 'showExposureMax',
          "bothFieldFlag": "showBothExposureFields"
        },
        "obs_date": {
          "fieldFlag": "showObsDateMax",
          "bothFieldFlag": "showBothObsDateFields"
        },
        "release_date": {
          "fieldFlag": "showReleaseDateMax",
          "bothFieldFlag": "showBothReleaseDateFields"
        }
      }
    };
  },
  methods: {
    getTelescopes: function() {
      var now, self, telescopes;
      telescopes = JSON.parse(localStorage.getItem("telescopes") || "0");
      self = this;
      now = moment();
      if (telescopes && moment(telescopes != null ? telescopes.expires : void 0) > now) {
        return self.telescopes = telescopes.telescopes;
      } else {
        return new Ajax({
          url: window.location.origin + "/dal/ti-pairs",
          method: "get",
          accept: "json",
          success: function(data) {
            self.telescopes = data;
            telescopes = {
              expires: moment().add(7, 'days'),
              telescopes: data
            };
            return localStorage.setItem("telescopes", JSON.stringify(telescopes));
          }
        }).send();
      }
    },
    splitSelection: function(val) {
      var bothFlag, fieldFlag;
      fieldFlag = this.relatedSplitFieldFlags[val]['fieldFlag'];
      bothFlag = this.relatedSplitFieldFlags[val]['bothFieldFlag'];
      if (this.search[val][2] === "(]" || this.search[val][2] === "[]") {
        this[fieldFlag] = true;
      } else {
        this[fieldFlag] = false;
      }
      if (this.search[val][2] === "[]") {
        return this[bothFlag] = true;
      } else {
        return this[bothFlag] = false;
      }
    },
    submitForm: function(event, paging, cb) {
      var key, message, msgs, newFormData, self;
      if (paging == null) {
        paging = null;
      }
      if (cb == null) {
        cb = null;
      }
      if (event != null) {
        event.preventDefault();
      }
      if (!paging) {
        this.loading = true;
        this.url = config.apiUrl;
        window.location.hash = "";
        this.$emit('setpagenum', 1);
        localStorage.setItem("currentPage", 1);
      }
      newFormData = JSON.parse(JSON.stringify(this.search));
      for (key in newFormData) {
        if (_.isEqual(newFormData[key], config.formData[key])) {
          delete newFormData[key];
        } else {
          if (config.rangeInputs.indexOf(key) >= 0) {
            if (newFormData[key][2] === "=") {
              newFormData[key] = newFormData[key][0];
            }
          }
        }
      }
      msgs = config.loadingMessages;
      message = Math.floor(Math.random() * msgs.length);
      this.loadingMessage = msgs[message];
      localStorage.setItem('search', JSON.stringify(this.search));
      self = this;
      return new Ajax({
        url: this.url,
        method: "post",
        accept: "json",
        data: {
          search: newFormData
        },
        success: function(data) {
          window.location.hash = "#query";
          self.loading = false;
          localStorage.setItem('results', JSON.stringify(data));
          self.$emit("displayform", ["results", data]);
          if (cb) {
            return cb();
          }
        }
      }).send();
    }
  }
};

export default searchFormComponent;
