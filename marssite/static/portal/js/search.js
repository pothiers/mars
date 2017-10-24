
/*
Author: Peter Peterson
Date: 2017-06-09
Description: Serves functionality for submitting and displaying archive query forms/results
Original file: search.coffee
 */
var config, dateLookup, searchFormComponent, validateDependsOn;

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

dateLookup = {
  "obs-date": {
    "field": "obs_date",
    "index": 0
  },
  "obs-date-max": {
    "field": 'obs_date',
    "index": 1
  },
  "release-date": {
    "field": "release_date",
    "index": 0
  },
  "release-date-max": {
    "field": "release_date",
    "index": 1
  },
  "parent": {
    "obj": this
  }
};

searchFormComponent = {
  mixins: [Shared.mixin],
  created: function() {
    return this.getTelescopes();
  },
  mounted: function() {
    var oldSearch;
    if (window.location.hash.indexOf("search_again") > -1) {
      oldSearch = JSON.parse(localStorage.getItem("searchData"));
      this.search = oldSearch;
    } else if (window.location.hash.indexOf("query") > -1) {
      this.$emit("displayform", ["results", []]);
    }
    window.base.bindEvents();
    $("input.date").datepicker({
      changeMonth: true,
      changeYear: true,
      onSelect: (function(_this) {
        return function(dateText, datePicker) {
          var e, field, fieldName;
          fieldName = datePicker.input[0].name;
          field = _this.search[dateLookup[fieldName].field];
          field[dateLookup[fieldName].index] = dateText;
          e = new CustomEvent("datechanged", {
            'detail': {
              'date': dateText
            }
          });
          document.dispatchEvent(e);
          return _this.code = new Date().getTime();
        };
      })(this)
    });
    $("input.date").datepicker("option", "dateFormat", "yy-mm-dd");
    window.searchVue = this;
    return document.addEventListener("datechanged", function() {
      return console.log("update code view");
    });
  },
  computed: {
    code: {
      get: function() {
        this.codeView = JSON.stringify({
          search: this.stripData()
        }, null, 2);
        return this.codeView;
      },
      set: function(update) {
        this.codeUpdate = update;
        this.codeView = JSON.stringify({
          search: this.stripData()
        }, null, 2);
        return null;
      }
    }
  },
  data: function() {
    return {
      url: config.apiUrl,
      visible: true,
      loading: false,
      codeUpdate: 0,
      codeView: "",
      modalTitle: "",
      modalBody: "",
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
      },
      option: {
        format: 'YYYY-MM-DD'
      }
    };
  },
  methods: {
    closeModal: function() {
      return ToggleModal("#search-modal");
    },
    newSearch: function() {
      this.search = JSON.parse(JSON.stringify(this.config.formData));
      return localStorage.setItem("searchData", JSON.stringify(this.search));
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
        });
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
