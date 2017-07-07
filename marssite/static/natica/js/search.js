
/*
Author: Peter Peterson
Date: 2017-06-09
Description: Serves functionality for submitting and displaying archive query forms/results
Original file: search.coffee
 */
var config, searchFormComponent, validateDependsOn;

import Vue from 'vue';

import VeeValidate, {
  Validator
} from 'vee-validate';

import Shared from './mixins.coffee';

validateDependsOn = {
  getMessage: function(field, params, data) {
    var dependsOn, id;
    id = params[0].replace("#", "");
    dependsOn = document.querySelector("label[for=" + id + "]").innerText;
    return (data && data.message) || ("This field depends on " + dependsOn);
  },
  validate: function(value, args) {
    return document.querySelector(args[0]).value !== "";
  }
};

config = Shared.config;

(function() {
  var validation;
  window.addEventListener('searchLoaded', function(e) {
    console.log("Search loaded", e);
    return window.base.bindEvents();
  });
  Validator.extend('dependson', validateDependsOn);
  validation = new Validator({
    dependant: "dependson"
  });
  return Vue.use(VeeValidate, config.validatorConfig);
})();

searchFormComponent = {
  mixins: [Shared.mixin],
  created: function() {
    return this.getTelescopes();
  },
  mounted: function() {
    var newSearch, oldSearch;
    if (window.location.hash.indexOf("search_again") > -1) {
      oldSearch = JSON.parse(localStorage.getItem("search"));
      newSearch = JSON.parse(JSON.stringify(this.config.formData));
      this.search = _.extend(newSearch, oldSearch);
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
    newSearch: function() {
      this.search = JSON.parse(JSON.stringify(this.config.formData));
      return localStorage.setItem("search", this.search);
    },
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
    }
  }
};

export default searchFormComponent;
