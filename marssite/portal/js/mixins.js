var _config;

_config = {
  stagingUrl: "/portal/staging/",
  apiUrl: "/dal/search/",
  rangeInputs: ["obs_date", "exposure_time", "release_date"],
  validatorConfig: {
    delay: 800,
    events: "input|blur",
    inject: true,
    dependsOn: "dependson"
  },
  allColumns: [
    {
      "checked": true,
      "mapping": "prop_id",
      "name": "Program Number",
      "num": 1
    }, {
      "checked": true,
      "mapping": "obs_date",
      "name": "Observed date",
      "num": 2
    }, {
      "checked": false,
      "mapping": "pi",
      "name": "Principle Investigator",
      "num": 3
    }, {
      "checked": false,
      "mapping": "ra",
      "name": "RA",
      "num": 4
    }, {
      "checked": false,
      "mapping": "dec",
      "name": "Dec",
      "num": 5
    }, {
      "checked": false,
      "mapping": "product",
      "name": "Product",
      "num": 6
    }, {
      "checked": false,
      "mapping": "depth",
      "name": "Depth",
      "num": 7
    }, {
      "checked": true,
      "mapping": "exposure",
      "name": "Exposure",
      "num": 8
    }, {
      "checked": true,
      "mapping": "filter",
      "name": "Filter",
      "num": 9
    }, {
      "checked": true,
      "mapping": "telescope",
      "name": "Telescope",
      "num": 10
    }, {
      "checked": true,
      "mapping": "instrument",
      "name": "Instrument",
      "num": 11
    }, {
      "checked": false,
      "mapping": "image_type",
      "name": "Image Type",
      "num": 12
    }, {
      "checked": false,
      "mapping": "filename",
      "name": "Filename",
      "num": 13
    }, {
      "checked": false,
      "mapping": "md5sum",
      "name": "MD5 sum",
      "num": 14
    }, {
      "checked": false,
      "mapping": "filesize",
      "name": "File size",
      "num": 15
    }, {
      "checked": false,
      "mapping": "original_filename",
      "name": "Original filename",
      "num": 16
    }, {
      "checked": false,
      "mapping": "reference",
      "name": "Reference",
      "num": 17
    }, {
      "checked": true,
      "mapping": "survey_id",
      "name": "Survey Id",
      "num": 18
    }, {
      "checked": false,
      "mapping": "release_date",
      "name": "Release Date",
      "num": 19
    }, {
      "checked": false,
      "mapping": "seeing",
      "name": "Seeing",
      "num": 20
    }
  ],
  formData: {
    coordinates: {
      ra: "",
      dec: ""
    },
    pi: null,
    search_box_min: null,
    prop_id: null,
    obs_date: ['', '', "="],
    filename: null,
    original_filename: null,
    telescope_instrument: [],
    exposure_time: ['', '', "="],
    release_date: ['', '', "="],
    image_filter: []
  },
  loadingMessages: ["Searching the cosmos...", "Deploying deep space probes...", "There's so much S P A C E!"]
};

var Mixin;
export default Mixin = {
  config: _config,
  mixin: {
    data: function() {
      return {
        config: _config // local access within methods
      };
    },
    config: _config,
    methods: {
      stripData: function() {
        var key, newFormData, ref;
        newFormData = this.search !== void 0 ? JSON.parse(JSON.stringify(this.search)) : JSON.parse(localStorage.getItem("searchData"));
        for (key in newFormData) {
          if (_.isEqual(newFormData[key], this.config.formData[key])) {
            delete newFormData[key];
          } else {
            if (this.config.rangeInputs.indexOf(key) >= 0) {
              if (newFormData[key][2] === "=") {
                newFormData[key] = newFormData[key][0];
              }
            }
          }
        }
        if (newFormData.telescope_instrument) {
          newFormData.telescope_instrument = _.map(newFormData.telescope_instrument, function(item) {
              return item.split(",");
          });
        }
        if ((ref = newFormData.coordinates) != null ? ref.ra : void 0) {
          newFormData.coordinates.ra = parseFloat(newFormData.coordinates.ra);
          newFormData.coordinates.dec = parseFloat(newFormData.coordinates.dec);
        }
        return newFormData;
        },

      /**
       *  Preps data for sending the query to the server
       */
      submitForm: function(event, paging, cb) {
        var newFormData, page, self, url;
        if (event != null) {
          event.preventDefault();
        }
        if (!paging) {
          this.loading = true;

          this.url = this.config.apiUrl;
          window.location.hash = "";
          this.$emit('setpagenum', 1);
          page = 1;
          localStorage.setItem("currentPage", 1);
          localStorage.setItem("searchData", JSON.stringify(this.search));
        } else {
          page = localStorage.getItem("currentPage");
        }
        newFormData = this.stripData();
        url = this.config.apiUrl + ("?page=" + page);
        localStorage.setItem("search", JSON.stringify(newFormData));
        this.submitQuery(url, newFormData, null, cb);
      },

      /**
       * Async submits query to the server
       */
      submitQuery: function (url, query, filter, cb) {
        var resultsStorage = "results";
        var msgs = this.config.loadingMessages;
        var message = Math.floor(Math.random() * msgs.length);
        this.loadingMessage = msgs[message];

        if( typeof(filter) !== "undefined" && filter !== null){
          resultsStorage = "filter_results_"+filter;
        }
        self = this;

        new Ajax({
        url: url,
        method: "post",
        accept: "json",
        data: query,
        success: function(data) {
          var saveData;
          window.location.hash = "#query";
          self.loading = false;
          saveData = typeof data === "object" ? JSON.stringify(data) : data;
          localStorage.setItem(resultsStorage, saveData);
          self.$emit("displayform", ["results", saveData]);
          if (cb) {
            cb(data);
          }
        },
        fail: function(statusMsg, status, xhr) {
          console.log("Request failed, got this");
          message = "" + statusMsg;
          if (xhr.response) {
            message += ":  " + xhr.response.errorMessage;
          }
          self.loading = false;
          self.modalTitle = "Request Error";
          self.modalBody = "<div class='alert alert-danger'>There was an error with your request.<br> <strong>" + message + "</strong></div>";
          ToggleModal("#search-modal");
        }
      });

      }

    }
  }
};
