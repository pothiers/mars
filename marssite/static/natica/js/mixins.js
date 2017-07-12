var _config;

_config = {
  apiUrl: "/dal/search/",
  rangeInputs: ["obs_date", "exposure_time", "release_date"],
  validatorConfig: {
    delay: 800,
    events: "input|blur",
    inject: true,
    dependsOn: "dependson"
  },
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
  loadingMessages: ["Searching the cosmos...", "Deploying deep space probes...", "Is that you Dave?...", "There's so much S P A C E!"]
};

export default {
  config: _config,
  mixin: {
    data: function() {
      return {
        config: _config
      };
    },
    methods: {
      stripData: function() {
        var key, newFormData, ref;
        newFormData = this.search ? JSON.parse(JSON.stringify(this.search)) : JSON.parse(localStorage.getItem("search"));
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
          newFormData.telescope_instrument = _.map(newFormData.telescope_instrument, (function(_this) {
            return function(item) {
              return item.split(",");
            };
          })(this));
        }
        if ((ref = newFormData.coordinates) != null ? ref.ra : void 0) {
          newFormData.coordinates.ra = parseFloat(newFormData.coordinates.ra);
          newFormData.coordinates.dec = parseFloat(newFormData.coordinates.dec);
        }
        localStorage.setItem('search', JSON.stringify(newFormData));
        return newFormData;
      },
      submitForm: function(event, paging, cb) {
        var message, msgs, newFormData, page, self, url;
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
        msgs = this.config.loadingMessages;
        message = Math.floor(Math.random() * msgs.length);
        this.loadingMessage = msgs[message];
        self = this;
        url = this.config.apiUrl + ("?page=" + page);
        return new Ajax({
          url: url,
          method: "post",
          accept: "json",
          data: {
            search: newFormData
          },
          success: function(data) {
            var saveData;
            window.location.hash = "#query";
            self.loading = false;
            saveData = typeof data === "object" ? JSON.stringify(data) : data;
            localStorage.setItem('results', saveData);
            self.$emit("displayform", ["results", saveData]);
            if (cb) {
              return cb(data);
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
            return console.dir(arguments);
          }
        });
      }
    }
  }
};
