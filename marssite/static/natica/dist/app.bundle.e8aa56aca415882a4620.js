webpackJsonp([0],[
/* 0 */,
/* 1 */,
/* 2 */,
/* 3 */,
/* 4 */,
/* 5 */
/***/ (function(module, exports) {

/* globals __VUE_SSR_CONTEXT__ */

// this module is a runtime utility for cleaner component module output and will
// be included in the final webpack user bundle

module.exports = function normalizeComponent (
  rawScriptExports,
  compiledTemplate,
  injectStyles,
  scopeId,
  moduleIdentifier /* server only */
) {
  var esModule
  var scriptExports = rawScriptExports = rawScriptExports || {}

  // ES6 modules interop
  var type = typeof rawScriptExports.default
  if (type === 'object' || type === 'function') {
    esModule = rawScriptExports
    scriptExports = rawScriptExports.default
  }

  // Vue.extend constructor export interop
  var options = typeof scriptExports === 'function'
    ? scriptExports.options
    : scriptExports

  // render functions
  if (compiledTemplate) {
    options.render = compiledTemplate.render
    options.staticRenderFns = compiledTemplate.staticRenderFns
  }

  // scopedId
  if (scopeId) {
    options._scopeId = scopeId
  }

  var hook
  if (moduleIdentifier) { // server build
    hook = function (context) {
      // 2.3 injection
      context =
        context || // cached call
        (this.$vnode && this.$vnode.ssrContext) || // stateful
        (this.parent && this.parent.$vnode && this.parent.$vnode.ssrContext) // functional
      // 2.2 with runInNewContext: true
      if (!context && typeof __VUE_SSR_CONTEXT__ !== 'undefined') {
        context = __VUE_SSR_CONTEXT__
      }
      // inject component styles
      if (injectStyles) {
        injectStyles.call(this, context)
      }
      // register component module identifier for async chunk inferrence
      if (context && context._registeredComponents) {
        context._registeredComponents.add(moduleIdentifier)
      }
    }
    // used by ssr in case component is cached and beforeCreate
    // never gets called
    options._ssrRegister = hook
  } else if (injectStyles) {
    hook = injectStyles
  }

  if (hook) {
    var functional = options.functional
    var existing = functional
      ? options.render
      : options.beforeCreate
    if (!functional) {
      // inject component registration as beforeCreate hook
      options.beforeCreate = existing
        ? [].concat(existing, hook)
        : [hook]
    } else {
      // register for functioal component in vue file
      options.render = function renderWithStyleInjection (h, context) {
        hook.call(context)
        return existing(h, context)
      }
    }
  }

  return {
    esModule: esModule,
    exports: scriptExports,
    options: options
  }
}


/***/ }),
/* 6 */,
/* 7 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
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

/* harmony default export */ __webpack_exports__["a"] = ({
  config: _config,
  mixin: {
    data: function() {
      return {
        config: _config
      };
    },
    methods: {
      submitForm: function(event, paging, cb) {
        var key, message, msgs, newFormData, page, ref, search, self, url;
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
        } else {
          page = localStorage.getItem("currentPage");
        }
        newFormData = this.search ? JSON.parse(JSON.stringify(this.search)) : JSON.parse(localStorage.getItem("search"));
        search = newFormData;
        localStorage.setItem('search', JSON.stringify(search));
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
        if ((ref = newFormData.coordinates) != null ? ref.ra : void 0) {
          newFormData.coordinates.ra = parseFloat(newFormData.coordinates.ra);
          newFormData.coordinates.dec = parseFloat(newFormData.coordinates.dec);
        }
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
            window.location.hash = "#query";
            self.loading = false;
            localStorage.setItem('results', JSON.stringify(data));
            self.$emit("displayform", ["results", data]);
            if (cb) {
              return cb(data);
            }
          }
        }).send();
      }
    }
  }
});


/***/ }),
/* 8 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_vue__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_vue___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_vue__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_moment__ = __webpack_require__(2);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_moment___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_moment__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_lodash__ = __webpack_require__(4);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_lodash___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_2_lodash__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__vue_Search_vue__ = __webpack_require__(9);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__vue_Search_vue___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_3__vue_Search_vue__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__vue_Results_vue__ = __webpack_require__(13);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__vue_Results_vue___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_4__vue_Results_vue__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__styles_search_scss__ = __webpack_require__(17);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__styles_search_scss___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_5__styles_search_scss__);
var App;













App = (function() {
  function App() {
    window.moment = __WEBPACK_IMPORTED_MODULE_1_moment___default.a;
    window._ = __WEBPACK_IMPORTED_MODULE_2_lodash___default.a;
    new __WEBPACK_IMPORTED_MODULE_0_vue___default.a({
      el: "#content",
      template: "<component compdata='componentData' v-bind:is='currentView' v-on:displayform='switchComponent' />",
      methods: {
        switchComponent: function(data) {
          this.componentData = data[1];
          return this.currentView = data[0];
        }
      },
      data: {
        currentView: "search",
        componentData: []
      },
      components: {
        search: __WEBPACK_IMPORTED_MODULE_3__vue_Search_vue___default.a,
        results: __WEBPACK_IMPORTED_MODULE_4__vue_Results_vue___default.a
      }
    });
  }

  return App;

})();

new App();


/***/ }),
/* 9 */
/***/ (function(module, exports, __webpack_require__) {

var disposed = false
var Component = __webpack_require__(5)(
  /* script */
  __webpack_require__(10),
  /* template */
  __webpack_require__(12),
  /* styles */
  null,
  /* scopeId */
  null,
  /* moduleIdentifier (server only) */
  null
)
Component.options.__file = "/Users/peter/Workspace/NOAO/dev-docker-mars/mars/marssite/natica/vue/Search.vue"
if (Component.esModule && Object.keys(Component.esModule).some(function (key) {return key !== "default" && key.substr(0, 2) !== "__"})) {console.error("named exports are not supported in *.vue files.")}
if (Component.options.functional) {console.error("[vue-loader] Search.vue: functional components are not supported with templates, they should use render functions.")}

/* hot reload */
if (false) {(function () {
  var hotAPI = require("vue-hot-reload-api")
  hotAPI.install(require("vue"), false)
  if (!hotAPI.compatible) return
  module.hot.accept()
  if (!module.hot.data) {
    hotAPI.createRecord("data-v-0a489c88", Component.options)
  } else {
    hotAPI.reload("data-v-0a489c88", Component.options)
  }
  module.hot.dispose(function (data) {
    disposed = true
  })
})()}

module.exports = Component.exports


/***/ }),
/* 10 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__js_search_coffee__ = __webpack_require__(11);
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//


 
/* harmony default export */ __webpack_exports__["default"] = (__WEBPACK_IMPORTED_MODULE_0__js_search_coffee__["a" /* default */]);


/***/ }),
/* 11 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_vue__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_vue___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_vue__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_vee_validate__ = __webpack_require__(6);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_vee_validate___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_vee_validate__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__mixins_coffee__ = __webpack_require__(7);

/*
Author: Peter Peterson
Date: 2017-06-09
Description: Serves functionality for submitting and displaying archive query forms/results
Original file: search.coffee
 */
var config, searchFormComponent, validateDependsOn;







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

config = __WEBPACK_IMPORTED_MODULE_2__mixins_coffee__["a" /* default */].config;

(function() {
  var validation;
  window.addEventListener('searchLoaded', function(e) {
    console.log("Search loaded", e);
    return window.base.bindEvents();
  });
  __WEBPACK_IMPORTED_MODULE_1_vee_validate__["Validator"].extend('dependson', validateDependsOn);
  validation = new __WEBPACK_IMPORTED_MODULE_1_vee_validate__["Validator"]({
    dependant: "dependson"
  });
  return __WEBPACK_IMPORTED_MODULE_0_vue___default.a.use(__WEBPACK_IMPORTED_MODULE_1_vee_validate___default.a, config.validatorConfig);
})();

searchFormComponent = {
  mixins: [__WEBPACK_IMPORTED_MODULE_2__mixins_coffee__["a" /* default */].mixin],
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

/* harmony default export */ __webpack_exports__["a"] = (searchFormComponent);


/***/ }),
/* 12 */
/***/ (function(module, exports, __webpack_require__) {

module.exports={render:function (){var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;
  return _c('div', {
    staticClass: "container",
    attrs: {
      "id": "search-form"
    }
  }, [_c('transition', {
    attrs: {
      "name": "fade"
    }
  }, [_c('div', {
    directives: [{
      name: "show",
      rawName: "v-show",
      value: (_vm.loading),
      expression: "loading"
    }],
    staticClass: "loading"
  }, [_c('div', {
    staticClass: "loading-message"
  }, [_c('small', [_vm._v("Loading...")]), _vm._v(" "), _c('div', {
    staticClass: "message",
    attrs: {
      "text": _vm.loadingMessage
    }
  }, [_vm._v(_vm._s(_vm.loadingMessage))])])])]), _vm._v(" "), _c('transition', {
    attrs: {
      "name": "fade"
    }
  }, [(_vm.visible) ? _c('form', {
    attrs: {
      "method": "post",
      "action": ""
    }
  }, [_c('div', {
    staticClass: "form-head row"
  }, [_c('div', {
    staticClass: "col-xs-12 col-md-6"
  }, [_c('h1', [_vm._v("NOAO Science Archive")]), _vm._v(" "), _c('p', {
    staticClass: "lead"
  }, [_vm._v("Raw and reduced data from NOAO telescopes and instruments")])]), _vm._v(" "), _c('div', {
    staticClass: "col-xs-12 col-md-6 text-right",
    attrs: {
      "rel": "form-submit"
    }
  }, [_c('div', {
    staticClass: "form-inline"
  }, [_c('label', {
    staticClass: "form-group"
  }, [_vm._v("Search wihin collections:\n                            "), _c('select', {
    staticClass: "form-control",
    attrs: {
      "id": "search-collections",
      "name": "collections"
    }
  }, [_c('option', {
    attrs: {
      "value": "all"
    }
  }, [_vm._v("All Holdings")]), _vm._v(" "), _c('option', {
    attrs: {
      "value": "my"
    }
  }, [_vm._v("My Collection")]), _vm._v(" "), _c('option', {
    attrs: {
      "value": ""
    }
  }, [_vm._v("Decam...")])])]), _vm._v(" "), _c('button', {
    staticClass: "btn btn-primary",
    attrs: {
      "type": "submit"
    },
    on: {
      "click": _vm.submitForm
    }
  }, [_vm._v("Search")]), _vm._v(" "), _c('div', [_c('a', {
    attrs: {
      "href": "#"
    },
    on: {
      "click": _vm.newSearch
    }
  }, [_vm._v("Clear Search")])])])])]), _vm._v(" "), _c('div', {
    staticClass: "row"
  }, [_c('div', {
    staticClass: "col-xs-12 form-section panel panel-default"
  }, [_c('div', {
    staticClass: "collapsible open container-fluid"
  }, [_c('div', {
    staticClass: "section-heading row"
  }, [_c('div', {
    staticClass: "col-xs-6"
  }, [_c('h4', [_vm._v("Target "), _c('small', [_vm._v("Search via coordinates or by object name")])])]), _vm._v(" "), _c('div', {
    staticClass: "col-xs-6"
  }, [_c('div', {
    staticClass: "section-toggle"
  }, [_c('span', {
    staticClass: "icon open"
  })])])]), _vm._v(" "), _c('div', {
    staticClass: "section-content row"
  }, [_c('div', {
    staticClass: "col-md-6"
  }, [_c('div', {
    staticClass: "form-group"
  }, [_c('label', {
    staticClass: "floating",
    attrs: {
      "for": "object-name"
    }
  }, [_vm._v("Object Name")]), _vm._v(" "), _c('input', {
    staticClass: "form-control",
    attrs: {
      "name": "object-name",
      "type": "text",
      "value": "",
      "placeholder": "Object Name",
      "id": "object-name"
    }
  })]), _vm._v(" "), _c('button', {
    staticClass: "btn btn-default"
  }, [_vm._v("Resolve object")])]), _vm._v(" "), _c('div', {
    staticClass: "col-md-6"
  }, [_c('div', {
    staticClass: "col-md-6"
  }, [_c('div', {
    staticClass: "form-group"
  }, [_c('label', {
    staticClass: "floating",
    attrs: {
      "for": "ra"
    }
  }, [_vm._v("Ra")]), _vm._v(" "), _c('input', {
    directives: [{
      name: "model",
      rawName: "v-model",
      value: (_vm.search.coordinates.ra),
      expression: "search.coordinates.ra"
    }, {
      name: "validate",
      rawName: "v-validate",
      value: ('decimal|dependson:#dec'),
      expression: "'decimal|dependson:#dec'"
    }],
    staticClass: "form-control",
    attrs: {
      "placeholder": "RA",
      "name": "ra",
      "id": "ra",
      "type": "text",
      "value": ""
    },
    domProps: {
      "value": (_vm.search.coordinates.ra)
    },
    on: {
      "input": function($event) {
        if ($event.target.composing) { return; }
        _vm.search.coordinates.ra = $event.target.value
      }
    }
  }), _vm._v(" "), (_vm.errors.has('ra')) ? _c('span', {
    staticClass: "error-message"
  }, [_vm._v("\n                                            " + _vm._s(_vm.errors.first('ra')) + "\n                                        ")]) : _vm._e()])]), _vm._v(" "), _c('div', {
    staticClass: "col-md-6"
  }, [_c('div', {
    staticClass: "form-group"
  }, [_c('label', {
    staticClass: "floating",
    attrs: {
      "for": "dec"
    }
  }, [_vm._v("Dec")]), _vm._v(" "), _c('input', {
    directives: [{
      name: "model",
      rawName: "v-model",
      value: (_vm.search.coordinates.dec),
      expression: "search.coordinates.dec"
    }, {
      name: "validate",
      rawName: "v-validate",
      value: ('decimal|dependson:#ra'),
      expression: "'decimal|dependson:#ra'"
    }],
    staticClass: "form-control",
    attrs: {
      "placeholder": "Dec",
      "name": "dec",
      "id": "dec",
      "type": "text",
      "value": ""
    },
    domProps: {
      "value": (_vm.search.coordinates.dec)
    },
    on: {
      "input": function($event) {
        if ($event.target.composing) { return; }
        _vm.search.coordinates.dec = $event.target.value
      }
    }
  }), _vm._v(" "), (_vm.errors.has('dec')) ? _c('span', {
    staticClass: "error-message"
  }, [_vm._v("\n                                            " + _vm._s(_vm.errors.first('dec')) + "\n                                        ")]) : _vm._e()])])])])])])]), _vm._v(" "), _c('div', {
    staticClass: "row"
  }, [_c('div', {
    staticClass: "col-xs-12 form-section"
  }, [_c('div', {
    staticClass: "collapsible open container-fluid"
  }, [_c('div', {
    staticClass: "section-heading row"
  }, [_c('div', {
    staticClass: "col-xs-6"
  }, [_c('h4', [_vm._v("Obervation "), _c('small', [_vm._v("Search by obervation details")])])]), _vm._v(" "), _c('div', {
    staticClass: "col-xs-6"
  }, [_c('div', {
    staticClass: "section-toggle"
  }, [_c('div', {
    staticClass: "icon"
  })])])]), _vm._v(" "), _c('div', {
    staticClass: "section-content row"
  }, [_c('div', {
    staticClass: "col-md-6"
  }, [_c('div', {
    staticClass: "form-group"
  }, [_c('label', {
    staticClass: "floating",
    attrs: {
      "for": "program-number"
    }
  }, [_vm._v("Program Number")]), _vm._v(" "), _c('input', {
    directives: [{
      name: "model",
      rawName: "v-model",
      value: (_vm.search.prop_id),
      expression: "search.prop_id"
    }],
    staticClass: "form-control",
    attrs: {
      "name": "program-number",
      "id": "program-number",
      "placeholder": "Program Number",
      "type": "text",
      "value": ""
    },
    domProps: {
      "value": (_vm.search.prop_id)
    },
    on: {
      "input": function($event) {
        if ($event.target.composing) { return; }
        _vm.search.prop_id = $event.target.value
      }
    }
  })]), _vm._v(" "), _c('div', {
    staticClass: "form-group"
  }, [_c('label', {
    staticClass: "floating",
    attrs: {
      "for": "principle-investigator"
    }
  }, [_vm._v("Principle Investigator")]), _vm._v(" "), _c('input', {
    directives: [{
      name: "model",
      rawName: "v-model",
      value: (_vm.search.pi),
      expression: "search.pi"
    }],
    staticClass: "form-control",
    attrs: {
      "name": "principle-investigator",
      "id": "principle-investigator",
      "placeholder": "Principle Investigator",
      "type": "text",
      "value": ""
    },
    domProps: {
      "value": (_vm.search.pi)
    },
    on: {
      "input": function($event) {
        if ($event.target.composing) { return; }
        _vm.search.pi = $event.target.value
      }
    }
  })]), _vm._v(" "), _c('div', {
    staticClass: "form-group"
  }, [_c('label', {
    staticClass: "floating",
    attrs: {
      "for": "original-filename"
    }
  }, [_vm._v("Original Filename")]), _vm._v(" "), _c('input', {
    directives: [{
      name: "model",
      rawName: "v-model",
      value: (_vm.search.original_filename),
      expression: "search.original_filename"
    }],
    staticClass: "form-control",
    attrs: {
      "id": "original-filename",
      "name": "original-filename",
      "type": "text",
      "value": "",
      "placeholder": "Original Filename"
    },
    domProps: {
      "value": (_vm.search.original_filename)
    },
    on: {
      "input": function($event) {
        if ($event.target.composing) { return; }
        _vm.search.original_filename = $event.target.value
      }
    }
  })]), _vm._v(" "), _c('div', {
    staticClass: "form-group"
  }, [_c('label', {
    staticClass: "floating",
    attrs: {
      "for": "archive-filename"
    }
  }, [_vm._v("Archive Filename")]), _vm._v(" "), _c('input', {
    directives: [{
      name: "model",
      rawName: "v-model",
      value: (_vm.search.filename),
      expression: "search.filename"
    }],
    staticClass: "form-control",
    attrs: {
      "id": "archive-filename",
      "name": "archive-filename",
      "type": "text",
      "value": "",
      "placeholder": "Archive Filename"
    },
    domProps: {
      "value": (_vm.search.filename)
    },
    on: {
      "input": function($event) {
        if ($event.target.composing) { return; }
        _vm.search.filename = $event.target.value
      }
    }
  })])]), _vm._v(" "), _c('div', {
    staticClass: "col-md-6"
  }, [_c('div', {
    staticClass: "form-group"
  }, [_c('div', {
    staticClass: "input-group select-group split-val",
    class: {
      'display-hidden': _vm.showBothObsDateFields
    }
  }, [_c('label', {
    staticClass: "floating",
    attrs: {
      "for": "obs-date"
    }
  }, [_vm._v("Observation Date "), _c('small', [_vm._v("(YYYY-MM-DD)")])]), _vm._v(" "), _c('select', {
    directives: [{
      name: "model",
      rawName: "v-model",
      value: (_vm.search.obs_date[2]),
      expression: "search.obs_date[2]"
    }],
    staticClass: "form-control input-group-addon",
    attrs: {
      "name": "obs-date-interval"
    },
    on: {
      "change": [function($event) {
        var $$selectedVal = Array.prototype.filter.call($event.target.options, function(o) {
          return o.selected
        }).map(function(o) {
          var val = "_value" in o ? o._value : o.value;
          return val
        });
        var $$exp = _vm.search.obs_date,
          $$idx = 2;
        if (!Array.isArray($$exp)) {
          _vm.search.obs_date[2] = $event.target.multiple ? $$selectedVal : $$selectedVal[0]
        } else {
          $$exp.splice($$idx, 1, $event.target.multiple ? $$selectedVal : $$selectedVal[0])
        }
      }, function($event) {
        _vm.splitSelection('obs_date')
      }]
    }
  }, [_c('option', {
    attrs: {
      "value": "="
    }
  }, [_vm._v("=")]), _vm._v(" "), _c('option', {
    attrs: {
      "value": "(]"
    }
  }, [_vm._v("≤")]), _vm._v(" "), _c('option', {
    attrs: {
      "value": "[)"
    }
  }, [_vm._v("≥")]), _vm._v(" "), _c('option', {
    staticClass: "toggle-option",
    attrs: {
      "value": "[]"
    }
  }, [_vm._v("≤ ≥")])]), _vm._v(" "), (_vm.search.obs_date[2] !== '(]') ? _c('input', {
    directives: [{
      name: "model",
      rawName: "v-model",
      value: (_vm.search.obs_date[0]),
      expression: "search.obs_date[0]"
    }, {
      name: "validate",
      rawName: "v-validate",
      value: ('date_format:YYYY-MM-DD'),
      expression: "'date_format:YYYY-MM-DD'"
    }],
    staticClass: "date form-control",
    attrs: {
      "id": "obs-date",
      "data-polyfill": "all",
      "name": "obs-date",
      "type": "text",
      "value": "",
      "placeholder": "Obervation date"
    },
    domProps: {
      "value": (_vm.search.obs_date[0])
    },
    on: {
      "input": function($event) {
        if ($event.target.composing) { return; }
        var $$exp = _vm.search.obs_date,
          $$idx = 0;
        if (!Array.isArray($$exp)) {
          _vm.search.obs_date[0] = $event.target.value
        } else {
          $$exp.splice($$idx, 1, $event.target.value)
        }
      }
    }
  }) : _vm._e(), _vm._v(" "), _c('input', {
    directives: [{
      name: "model",
      rawName: "v-model",
      value: (_vm.search.obs_date[1]),
      expression: "search.obs_date[1]"
    }, {
      name: "show",
      rawName: "v-show",
      value: (_vm.showObsDateMax),
      expression: "showObsDateMax"
    }, {
      name: "validate",
      rawName: "v-validate",
      value: ('date_format:YYYY-MM-DD'),
      expression: "'date_format:YYYY-MM-DD'"
    }],
    staticClass: "date form-control",
    class: {
      'hidden-split': _vm.showBothObsDateFields
    },
    attrs: {
      "id": "obs-date-max",
      "name": "obs-date-max",
      "type": "text",
      "value": "",
      "placeholder": "Max Observation Date"
    },
    domProps: {
      "value": (_vm.search.obs_date[1])
    },
    on: {
      "input": function($event) {
        if ($event.target.composing) { return; }
        var $$exp = _vm.search.obs_date,
          $$idx = 1;
        if (!Array.isArray($$exp)) {
          _vm.search.obs_date[1] = $event.target.value
        } else {
          $$exp.splice($$idx, 1, $event.target.value)
        }
      }
    }
  }), _vm._v(" "), (_vm.errors.has('obs-date')) ? _c('span', {
    staticClass: "error-message"
  }, [_vm._v(_vm._s(_vm.errors.first('obs-date')))]) : _vm._e(), _vm._v(" "), (_vm.errors.has('obs-date-max')) ? _c('span', {
    staticClass: "error-message"
  }, [_vm._v(_vm._s(_vm.errors.first('obs-date-max')))]) : _vm._e()])]), _vm._v(" "), _c('div', {
    staticClass: "form-group"
  }, [_c('div', {
    staticClass: "input-group select-group split-val",
    class: {
      'display-hidden': _vm.showBothExposureFields
    }
  }, [_c('label', {
    staticClass: "floating",
    attrs: {
      "for": "exposure"
    }
  }, [_vm._v("Exposure")]), _vm._v(" "), _c('select', {
    directives: [{
      name: "model",
      rawName: "v-model",
      value: (_vm.search.exposure_time[2]),
      expression: "search.exposure_time[2]"
    }],
    staticClass: "form-control input-group-addon",
    attrs: {
      "id": "",
      "name": "expore-interval"
    },
    on: {
      "change": [function($event) {
        var $$selectedVal = Array.prototype.filter.call($event.target.options, function(o) {
          return o.selected
        }).map(function(o) {
          var val = "_value" in o ? o._value : o.value;
          return val
        });
        var $$exp = _vm.search.exposure_time,
          $$idx = 2;
        if (!Array.isArray($$exp)) {
          _vm.search.exposure_time[2] = $event.target.multiple ? $$selectedVal : $$selectedVal[0]
        } else {
          $$exp.splice($$idx, 1, $event.target.multiple ? $$selectedVal : $$selectedVal[0])
        }
      }, function($event) {
        _vm.splitSelection('exposure_time')
      }]
    }
  }, [_c('option', {
    attrs: {
      "value": "="
    }
  }, [_vm._v("=")]), _vm._v(" "), _c('option', {
    attrs: {
      "value": "(]"
    }
  }, [_vm._v("≤")]), _vm._v(" "), _c('option', {
    attrs: {
      "value": "[)"
    }
  }, [_vm._v("≥")]), _vm._v(" "), _c('option', {
    staticClass: "toggle-option",
    attrs: {
      "value": "[]"
    }
  }, [_vm._v("≤ ≥")])]), _vm._v(" "), (_vm.search.exposure_time[2] !== '(]') ? _c('input', {
    directives: [{
      name: "model",
      rawName: "v-model",
      value: (_vm.search.exposure_time[0]),
      expression: "search.exposure_time[0]"
    }, {
      name: "validate",
      rawName: "v-validate",
      value: ('numeric'),
      expression: "'numeric'"
    }],
    staticClass: "form-control",
    attrs: {
      "id": "exposure",
      "name": "exposure",
      "type": "text",
      "value": "",
      "placeholder": "Exposure in seconds"
    },
    domProps: {
      "value": (_vm.search.exposure_time[0])
    },
    on: {
      "input": function($event) {
        if ($event.target.composing) { return; }
        var $$exp = _vm.search.exposure_time,
          $$idx = 0;
        if (!Array.isArray($$exp)) {
          _vm.search.exposure_time[0] = $event.target.value
        } else {
          $$exp.splice($$idx, 1, $event.target.value)
        }
      }
    }
  }) : _vm._e(), _vm._v(" "), _c('input', {
    directives: [{
      name: "model",
      rawName: "v-model",
      value: (_vm.search.exposure_time[1]),
      expression: "search.exposure_time[1]"
    }, {
      name: "show",
      rawName: "v-show",
      value: (_vm.showExposureMax),
      expression: "showExposureMax"
    }, {
      name: "validate",
      rawName: "v-validate",
      value: ('numeric'),
      expression: "'numeric'"
    }],
    staticClass: "form-control",
    class: {
      'hidden-split': _vm.showBothExposureFields
    },
    attrs: {
      "id": "exposure-max",
      "name": "exposure-max",
      "type": "text",
      "value": "",
      "placeholder": "Max exposure"
    },
    domProps: {
      "value": (_vm.search.exposure_time[1])
    },
    on: {
      "input": function($event) {
        if ($event.target.composing) { return; }
        var $$exp = _vm.search.exposure_time,
          $$idx = 1;
        if (!Array.isArray($$exp)) {
          _vm.search.exposure_time[1] = $event.target.value
        } else {
          $$exp.splice($$idx, 1, $event.target.value)
        }
      }
    }
  }), _vm._v(" "), (_vm.errors.has('exposure')) ? _c('span', {
    staticClass: "error-message"
  }, [_vm._v(_vm._s(_vm.errors.first('exposure')))]) : _vm._e(), _vm._v(" "), (_vm.errors.has('exposure-max')) ? _c('span', {
    staticClass: "error-message"
  }, [_vm._v(_vm._s(_vm.errors.first('exposure-max')))]) : _vm._e()])])])])])])]), _vm._v(" "), _c('div', {
    staticClass: "row"
  }, [_c('div', {
    staticClass: "col-xs-12 form-section panel panel-default"
  }, [_c('div', {
    staticClass: "collapsible open container-fluid"
  }, [_c('div', {
    staticClass: "section-heading row"
  }, [_c('div', {
    staticClass: "col-xs-6"
  }, [_c('h4', [_vm._v("Image & Telescope / Instrument "), _c('small', [_vm._v("Search a image processing and specific telelscope and instrument")])])]), _vm._v(" "), _c('div', {
    staticClass: "col-xs-6"
  }, [_c('div', {
    staticClass: "section-toggle"
  }, [_c('span', {
    staticClass: "icon"
  })])])]), _vm._v(" "), _c('div', {
    staticClass: "section-content row"
  }, [_c('div', {
    staticClass: "col-sm-6"
  }, [_c('div', {
    staticClass: "form-group"
  }, [_c('div', {
    staticClass: "input-group select-group split-val",
    class: {
      'display-hidden': _vm.showBothReleaseDateFields
    }
  }, [_c('label', {
    staticClass: "floating",
    attrs: {
      "for": "release-date"
    }
  }, [_vm._v("Public Release Date "), _c('small', [_vm._v("(YYYY-MM-DD)")])]), _vm._v(" "), _c('select', {
    directives: [{
      name: "model",
      rawName: "v-model",
      value: (_vm.search.release_date[2]),
      expression: "search.release_date[2]"
    }],
    staticClass: "form-control input-group-addon",
    attrs: {
      "id": "",
      "name": "release-date-interval"
    },
    on: {
      "change": [function($event) {
        var $$selectedVal = Array.prototype.filter.call($event.target.options, function(o) {
          return o.selected
        }).map(function(o) {
          var val = "_value" in o ? o._value : o.value;
          return val
        });
        var $$exp = _vm.search.release_date,
          $$idx = 2;
        if (!Array.isArray($$exp)) {
          _vm.search.release_date[2] = $event.target.multiple ? $$selectedVal : $$selectedVal[0]
        } else {
          $$exp.splice($$idx, 1, $event.target.multiple ? $$selectedVal : $$selectedVal[0])
        }
      }, function($event) {
        _vm.splitSelection('release_date')
      }]
    }
  }, [_c('option', {
    attrs: {
      "value": "="
    }
  }, [_vm._v("=")]), _vm._v(" "), _c('option', {
    attrs: {
      "value": "(]"
    }
  }, [_vm._v("≤")]), _vm._v(" "), _c('option', {
    attrs: {
      "value": "[)"
    }
  }, [_vm._v("≥")]), _vm._v(" "), _c('option', {
    staticClass: "toggle-option",
    attrs: {
      "value": "[]"
    }
  }, [_vm._v("≤ ≥")])]), _vm._v(" "), (_vm.search.release_date[2] !== '(]') ? _c('input', {
    directives: [{
      name: "model",
      rawName: "v-model",
      value: (_vm.search.release_date[0]),
      expression: "search.release_date[0]"
    }, {
      name: "validate",
      rawName: "v-validate",
      value: ('date_format:YYYY-MM-DD'),
      expression: "'date_format:YYYY-MM-DD'"
    }],
    staticClass: "date form-control",
    attrs: {
      "id": "release-date",
      "data-polyfill": "all",
      "name": "release-date",
      "type": "text",
      "value": "",
      "placeholder": "Release date"
    },
    domProps: {
      "value": (_vm.search.release_date[0])
    },
    on: {
      "input": function($event) {
        if ($event.target.composing) { return; }
        var $$exp = _vm.search.release_date,
          $$idx = 0;
        if (!Array.isArray($$exp)) {
          _vm.search.release_date[0] = $event.target.value
        } else {
          $$exp.splice($$idx, 1, $event.target.value)
        }
      }
    }
  }) : _vm._e(), _vm._v(" "), _c('input', {
    directives: [{
      name: "model",
      rawName: "v-model",
      value: (_vm.search.release_date[1]),
      expression: "search.release_date[1]"
    }, {
      name: "show",
      rawName: "v-show",
      value: (_vm.showReleaseDateMax),
      expression: "showReleaseDateMax"
    }, {
      name: "validate",
      rawName: "v-validate",
      value: ('date_format:YYYY-MM-DD'),
      expression: "'date_format:YYYY-MM-DD'"
    }],
    staticClass: "date form-control",
    class: {
      'hidden-split': _vm.showBothReleaseDateFields
    },
    attrs: {
      "id": "release-date-max",
      "name": "release-date-max",
      "type": "text",
      "value": "",
      "placeholder": "Max release date"
    },
    domProps: {
      "value": (_vm.search.release_date[1])
    },
    on: {
      "input": function($event) {
        if ($event.target.composing) { return; }
        var $$exp = _vm.search.release_date,
          $$idx = 1;
        if (!Array.isArray($$exp)) {
          _vm.search.release_date[1] = $event.target.value
        } else {
          $$exp.splice($$idx, 1, $event.target.value)
        }
      }
    }
  })])])]), _vm._v(" "), _c('div', {
    staticClass: "col-sm-3"
  }, [_c('div', {
    staticClass: "form-group"
  }, [_c('div', {
    staticClass: "input-group"
  }, [_c('label', {
    attrs: {
      "for": "image-filter"
    }
  }, [_vm._v("Image Filter")]), _vm._v(" "), _c('select', {
    directives: [{
      name: "model",
      rawName: "v-model",
      value: (_vm.search.image_filter),
      expression: "search.image_filter"
    }],
    staticClass: "form-control",
    attrs: {
      "multiple": "",
      "name": "image-filter",
      "size": "10 ",
      "id": "image-filter"
    },
    on: {
      "change": function($event) {
        var $$selectedVal = Array.prototype.filter.call($event.target.options, function(o) {
          return o.selected
        }).map(function(o) {
          var val = "_value" in o ? o._value : o.value;
          return val
        });
        _vm.search.image_filter = $event.target.multiple ? $$selectedVal : $$selectedVal[0]
      }
    }
  }, [_c('option', {
    attrs: {
      "value": "raw"
    }
  }, [_vm._v("Raw image")]), _vm._v(" "), _c('option', {
    attrs: {
      "value": "calibrated"
    }
  }, [_vm._v("Calibrated")]), _vm._v(" "), _c('option', {
    attrs: {
      "value": "reprojected"
    }
  }, [_vm._v("Reprojected")]), _vm._v(" "), _c('option', {
    attrs: {
      "value": "stacked"
    }
  }, [_vm._v("Stacked")]), _vm._v(" "), _c('option', {
    attrs: {
      "value": "master_calibration"
    }
  }, [_vm._v("Master Calibration")]), _vm._v(" "), _c('option', {
    attrs: {
      "value": "image_tiles"
    }
  }, [_vm._v("Image Tiles")]), _vm._v(" "), _c('option', {
    attrs: {
      "value": "sky_subtracted"
    }
  }, [_vm._v("Sky Subtracted")])]), _vm._v(" "), _c('p', {
    staticClass: "help-block"
  }, [_vm._v("\n                                        * "), _c('em', [_vm._v("Sky subtracted")]), _vm._v(" is for "), _c('strong', [_vm._v("NEWFIRM")]), _vm._v(" only. "), _c('em', [_vm._v("Calibrated, Reprojected, Stacked, Master calibration, Image Tiles")]), _vm._v(" are for "), _c('strong', [_vm._v("Mosiac, NEWFIRM and DECam")]), _vm._v(".\n                                    ")])])])]), _vm._v(" "), _c('div', {
    staticClass: "col-sm-3"
  }, [_c('div', {
    staticClass: "form-group"
  }, [_c('div', {
    staticClass: "input-group"
  }, [_c('label', {
    attrs: {
      "for": "telescope"
    }
  }, [_vm._v("Telescope & Intrument")]), _vm._v(" "), _c('select', {
    directives: [{
      name: "model",
      rawName: "v-model",
      value: (_vm.search.telescope_instrument),
      expression: "search.telescope_instrument"
    }],
    staticClass: "form-control",
    attrs: {
      "id": "telescope",
      "name": "telescope",
      "multiple": "",
      "size": "10"
    },
    on: {
      "change": function($event) {
        var $$selectedVal = Array.prototype.filter.call($event.target.options, function(o) {
          return o.selected
        }).map(function(o) {
          var val = "_value" in o ? o._value : o.value;
          return val
        });
        _vm.search.telescope_instrument = $event.target.multiple ? $$selectedVal : $$selectedVal[0]
      }
    }
  }, _vm._l((_vm.telescopes), function(tel) {
    return _c('option', {
      attrs: {
        "value": ""
      },
      domProps: {
        "value": tel
      }
    }, [_vm._v(_vm._s(tel[0]) + " + " + _vm._s(tel[1]))])
  }))])])])])])])])]) : _vm._e()])], 1)
},staticRenderFns: []}
module.exports.render._withStripped = true
if (false) {
  module.hot.accept()
  if (module.hot.data) {
     require("vue-hot-reload-api").rerender("data-v-0a489c88", module.exports)
  }
}

/***/ }),
/* 13 */
/***/ (function(module, exports, __webpack_require__) {

var disposed = false
var Component = __webpack_require__(5)(
  /* script */
  __webpack_require__(14),
  /* template */
  __webpack_require__(16),
  /* styles */
  null,
  /* scopeId */
  null,
  /* moduleIdentifier (server only) */
  null
)
Component.options.__file = "/Users/peter/Workspace/NOAO/dev-docker-mars/mars/marssite/natica/vue/Results.vue"
if (Component.esModule && Object.keys(Component.esModule).some(function (key) {return key !== "default" && key.substr(0, 2) !== "__"})) {console.error("named exports are not supported in *.vue files.")}
if (Component.options.functional) {console.error("[vue-loader] Results.vue: functional components are not supported with templates, they should use render functions.")}

/* hot reload */
if (false) {(function () {
  var hotAPI = require("vue-hot-reload-api")
  hotAPI.install(require("vue"), false)
  if (!hotAPI.compatible) return
  module.hot.accept()
  if (!module.hot.data) {
    hotAPI.createRecord("data-v-64670592", Component.options)
  } else {
    hotAPI.reload("data-v-64670592", Component.options)
  }
  module.hot.dispose(function (data) {
    disposed = true
  })
})()}

module.exports = Component.exports


/***/ }),
/* 14 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__js_results_coffee__ = __webpack_require__(15);
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//



/* harmony default export */ __webpack_exports__["default"] = (__WEBPACK_IMPORTED_MODULE_0__js_results_coffee__["a" /* default */]);


/***/ }),
/* 15 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_vue__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_vue___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_vue__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__mixins_coffee__ = __webpack_require__(7);

/*
Author: Peter Peterson
Date: 2017-06-09
Description: Serves functionality for displaying and filtering result sets
Original file: results.coffee
 */
var config;






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

__WEBPACK_IMPORTED_MODULE_0_vue___default.a.component("table-header", {
  props: ['name'],
  template: "<th>{{ name }}</th>"
});

__WEBPACK_IMPORTED_MODULE_0_vue___default.a.component("table-cell", {
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

__WEBPACK_IMPORTED_MODULE_0_vue___default.a.component("table-row", {
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

__WEBPACK_IMPORTED_MODULE_0_vue___default.a.component("table-body", {
  props: ['data', 'visibleCols'],
  template: "<tbody><table-row v-for='(item,idx) in data' v-bind:cols='visibleCols' v-bind:row='item' :key='item.id'></table-row></tbody>"
});


/*
   App - Results
 */

config = __WEBPACK_IMPORTED_MODULE_1__mixins_coffee__["a" /* default */].config;

/* harmony default export */ __webpack_exports__["a"] = ({
  props: ['componentData'],
  mixins: [__WEBPACK_IMPORTED_MODULE_1__mixins_coffee__["a" /* default */].mixin],
  data: function() {
    return {
      visibleColumns: JSON.parse(JSON.stringify(config.defaultColumns)),
      visible: false,
      pageNum: 1,
      isLoading: false,
      results: [],
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
        return self.results = data;
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
});


/***/ }),
/* 16 */
/***/ (function(module, exports, __webpack_require__) {

module.exports={render:function (){var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;
  return _c('div', {
    attrs: {
      "id": "query-results"
    }
  }, [_c('transition', {
    attrs: {
      "name": "fade"
    }
  }, [(_vm.visible) ? _c('div', [_c('div', {
    staticClass: "container"
  }, [_c('div', {
    staticClass: "row heading"
  }, [_c('div', {
    staticClass: "col-xs-10"
  }, [_c('h2', {
    staticClass: "text-warn"
  }, [_vm._v("Query returned "), _c('em', [_vm._v(_vm._s(_vm.totalItems))]), _vm._v(" records")])]), _vm._v(" "), _c('div', {
    staticClass: "col-xs-2 text-right"
  }, [_c('button', {
    staticClass: "btn btn-primary",
    on: {
      "click": _vm.displayForm
    }
  }, [_vm._v("New Search")])])]), _vm._v(" "), _c('div', {
    staticClass: "row results-controls"
  }, [_c('div', {
    staticClass: "col-sm-3"
  }, [_c('button', {
    staticClass: "btn-link btn page-prev",
    on: {
      "click": _vm.pageBack
    }
  }, [_vm._v("Prev")]), _vm._v(" "), _c('span', {
    staticClass: "page-num"
  }, [_vm._v(_vm._s(_vm.pageNum))]), _vm._v(" "), _c('button', {
    staticClass: "btn-link btn page-next",
    on: {
      "click": _vm.pageNext
    }
  }, [_vm._v("Next")]), _vm._v(" "), (_vm.isLoading) ? _c('span', {
    staticClass: "fa fa-spinner fa-spin fa-1x fa-fw"
  }) : _vm._e()]), _vm._v(" "), _c('div', {
    staticClass: "col-sm-9 "
  })]), _vm._v(" "), _c('div', {
    staticClass: "row table-filters"
  }), _vm._v(" "), _c('hr')]), _vm._v(" "), _c('div', {
    staticClass: "container"
  }, [_c('div', {
    staticClass: "row"
  }, [_c('div', {
    staticClass: "col-xs-12 results-wrapper"
  }, [(_vm.results.resultset) ? _c('table', {
    staticClass: "results"
  }, [_c('thead', [_c('tr', [_c('th', [_vm._v("Selected")]), _vm._v(" "), _vm._l((_vm.visibleColumns), function(col) {
    return _c('th', [_c("table-header", {
      tag: "span",
      attrs: {
        "name": col.name
      }
    })])
  })], 2)]), _vm._v(" "), _c("table-body", {
    tag: "tbody",
    attrs: {
      "data": _vm.results.resultset,
      "visible-cols": _vm.visibleColumns
    }
  }), _vm._v(" "), _c('tfoot')], 1) : _c('div', [_c('h1', {
    staticClass: "text-center"
  }, [_vm._v("No results found")]), _vm._v(" "), (_vm.error) ? _c('div', {
    staticClass: "alert alert-danger text-center"
  }, [_vm._v(_vm._s(_vm.error))]) : _vm._e()])])])])]) : _vm._e()])], 1)
},staticRenderFns: []}
module.exports.render._withStripped = true
if (false) {
  module.hot.accept()
  if (module.hot.data) {
     require("vue-hot-reload-api").rerender("data-v-64670592", module.exports)
  }
}

/***/ }),
/* 17 */
/***/ (function(module, exports, __webpack_require__) {

// style-loader: Adds some css to the DOM by adding a <style> tag

// load the styles
var content = __webpack_require__(18);
if(typeof content === 'string') content = [[module.i, content, '']];
// Prepare cssTransformation
var transform;

var options = {}
options.transform = transform
// add the styles to the DOM
var update = __webpack_require__(20)(content, options);
if(content.locals) module.exports = content.locals;
// Hot Module Replacement
if(false) {
	// When the styles change, update the <style> tags
	if(!content.locals) {
		module.hot.accept("!!../../../node_modules/css-loader/index.js!../../../node_modules/sass-loader/lib/loader.js!./search.scss", function() {
			var newContent = require("!!../../../node_modules/css-loader/index.js!../../../node_modules/sass-loader/lib/loader.js!./search.scss");
			if(typeof newContent === 'string') newContent = [[module.id, newContent, '']];
			update(newContent);
		});
	}
	// When the module is disposed, remove the <style> tags
	module.hot.dispose(function() { update(); });
}

/***/ }),
/* 18 */
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__(19)(undefined);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\ndiv[rel=form-submit] {\n  padding-top: 12px; }\n\n.form-section {\n  background-color: #D9EDF7;\n  border: 1px solid #BCE8F1;\n  border-radius: 10px;\n  padding: 1em;\n  margin-top: 2em; }\n  .form-section .section-toggle {\n    text-align: right; }\n    .form-section .section-toggle .icon:after {\n      font-family: \"FontAwesome\";\n      display: inline-block;\n      font-size: 1.2em;\n      content: \"\\F078\"; }\n  .form-section .collapsible.open .section-toggle .icon:after {\n    content: \"\\F077\"; }\n  .form-section .error-message {\n    color: #d85454;\n    font-size: 14px;\n    line-height: 1.23em;\n    position: relative;\n    display: inline-block; }\n\n.results-wrapper {\n  overflow-x: auto; }\n\n.fade-enter-active, .fade-leave-active {\n  transition: opacity .5s; }\n\n.fade-enter, .fade-leave-to {\n  opacity: 0; }\n\n.loading {\n  display: block;\n  position: fixed;\n  width: 100%;\n  height: 100%;\n  top: 0;\n  left: 0;\n  padding: 0;\n  margin: 0;\n  z-index: 1000;\n  background-color: rgba(0, 0, 0, 0.8);\n  background-image: url(/static/img/galaxy-loading.gif);\n  background-size: cover;\n  opacity: 1; }\n  .loading .loading-message {\n    position: absolute;\n    top: 30%;\n    left: 50%;\n    width: 500px;\n    margin-left: -250px;\n    text-align: center;\n    font-size: 2.3em;\n    color: yellow;\n    line-height: 1.25em; }\n    .loading .loading-message small {\n      font-size: 0.5em; }\n\ntable.results {\n  overflow: auto;\n  padding: 20px; }\n  table.results thead tr {\n    border-bottom: 2px solid #666; }\n  table.results thead th {\n    font-size: 14px;\n    white-space: nowrap;\n    padding: 5px; }\n  table.results tbody td {\n    font-size: 0.8em;\n    overflow: hidden;\n    padding: 2px 7px;\n    border: 1px solid transparent; }\n  table.results tbody td.empty {\n    background-color: #ccc;\n    border-color: #fff; }\n  table.results tbody tr:nth-child(even) {\n    background-color: aliceblue; }\n  table.results tbody tr.selected {\n    background-color: #37c0fb; }\n    table.results tbody tr.selected td.empty {\n      background-color: rgba(0, 0, 0, 0.3); }\n\nlabel.floating {\n  position: relative !important;\n  font-size: 12px;\n  top: 1em;\n  left: 1em;\n  opacity: 0;\n  transition: all 0.2s linear; }\n\nlabel.open {\n  opacity: 1;\n  top: 0; }\n\n.collapsible .section-content {\n  height: 0;\n  opacity: 0;\n  overflow: hidden;\n  transition: all 0.3s ease-in-out; }\n\n.collapsible.open .section-content {\n  height: initial;\n  opacity: 1; }\n", ""]);

// exports


/***/ }),
/* 19 */
/***/ (function(module, exports) {

/*
	MIT License http://www.opensource.org/licenses/mit-license.php
	Author Tobias Koppers @sokra
*/
// css base code, injected by the css-loader
module.exports = function(useSourceMap) {
	var list = [];

	// return the list of modules as css string
	list.toString = function toString() {
		return this.map(function (item) {
			var content = cssWithMappingToString(item, useSourceMap);
			if(item[2]) {
				return "@media " + item[2] + "{" + content + "}";
			} else {
				return content;
			}
		}).join("");
	};

	// import a list of modules into the list
	list.i = function(modules, mediaQuery) {
		if(typeof modules === "string")
			modules = [[null, modules, ""]];
		var alreadyImportedModules = {};
		for(var i = 0; i < this.length; i++) {
			var id = this[i][0];
			if(typeof id === "number")
				alreadyImportedModules[id] = true;
		}
		for(i = 0; i < modules.length; i++) {
			var item = modules[i];
			// skip already imported module
			// this implementation is not 100% perfect for weird media query combinations
			//  when a module is imported multiple times with different media queries.
			//  I hope this will never occur (Hey this way we have smaller bundles)
			if(typeof item[0] !== "number" || !alreadyImportedModules[item[0]]) {
				if(mediaQuery && !item[2]) {
					item[2] = mediaQuery;
				} else if(mediaQuery) {
					item[2] = "(" + item[2] + ") and (" + mediaQuery + ")";
				}
				list.push(item);
			}
		}
	};
	return list;
};

function cssWithMappingToString(item, useSourceMap) {
	var content = item[1] || '';
	var cssMapping = item[3];
	if (!cssMapping) {
		return content;
	}

	if (useSourceMap && typeof btoa === 'function') {
		var sourceMapping = toComment(cssMapping);
		var sourceURLs = cssMapping.sources.map(function (source) {
			return '/*# sourceURL=' + cssMapping.sourceRoot + source + ' */'
		});

		return [content].concat(sourceURLs).concat([sourceMapping]).join('\n');
	}

	return [content].join('\n');
}

// Adapted from convert-source-map (MIT)
function toComment(sourceMap) {
	// eslint-disable-next-line no-undef
	var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap))));
	var data = 'sourceMappingURL=data:application/json;charset=utf-8;base64,' + base64;

	return '/*# ' + data + ' */';
}


/***/ }),
/* 20 */
/***/ (function(module, exports, __webpack_require__) {

/*
	MIT License http://www.opensource.org/licenses/mit-license.php
	Author Tobias Koppers @sokra
*/

var stylesInDom = {};

var	memoize = function (fn) {
	var memo;

	return function () {
		if (typeof memo === "undefined") memo = fn.apply(this, arguments);
		return memo;
	};
};

var isOldIE = memoize(function () {
	// Test for IE <= 9 as proposed by Browserhacks
	// @see http://browserhacks.com/#hack-e71d8692f65334173fee715c222cb805
	// Tests for existence of standard globals is to allow style-loader
	// to operate correctly into non-standard environments
	// @see https://github.com/webpack-contrib/style-loader/issues/177
	return window && document && document.all && !window.atob;
});

var getElement = (function (fn) {
	var memo = {};

	return function(selector) {
		if (typeof memo[selector] === "undefined") {
			memo[selector] = fn.call(this, selector);
		}

		return memo[selector]
	};
})(function (target) {
	return document.querySelector(target)
});

var singleton = null;
var	singletonCounter = 0;
var	stylesInsertedAtTop = [];

var	fixUrls = __webpack_require__(21);

module.exports = function(list, options) {
	if (typeof DEBUG !== "undefined" && DEBUG) {
		if (typeof document !== "object") throw new Error("The style-loader cannot be used in a non-browser environment");
	}

	options = options || {};

	options.attrs = typeof options.attrs === "object" ? options.attrs : {};

	// Force single-tag solution on IE6-9, which has a hard limit on the # of <style>
	// tags it will allow on a page
	if (!options.singleton) options.singleton = isOldIE();

	// By default, add <style> tags to the <head> element
	if (!options.insertInto) options.insertInto = "head";

	// By default, add <style> tags to the bottom of the target
	if (!options.insertAt) options.insertAt = "bottom";

	var styles = listToStyles(list, options);

	addStylesToDom(styles, options);

	return function update (newList) {
		var mayRemove = [];

		for (var i = 0; i < styles.length; i++) {
			var item = styles[i];
			var domStyle = stylesInDom[item.id];

			domStyle.refs--;
			mayRemove.push(domStyle);
		}

		if(newList) {
			var newStyles = listToStyles(newList, options);
			addStylesToDom(newStyles, options);
		}

		for (var i = 0; i < mayRemove.length; i++) {
			var domStyle = mayRemove[i];

			if(domStyle.refs === 0) {
				for (var j = 0; j < domStyle.parts.length; j++) domStyle.parts[j]();

				delete stylesInDom[domStyle.id];
			}
		}
	};
};

function addStylesToDom (styles, options) {
	for (var i = 0; i < styles.length; i++) {
		var item = styles[i];
		var domStyle = stylesInDom[item.id];

		if(domStyle) {
			domStyle.refs++;

			for(var j = 0; j < domStyle.parts.length; j++) {
				domStyle.parts[j](item.parts[j]);
			}

			for(; j < item.parts.length; j++) {
				domStyle.parts.push(addStyle(item.parts[j], options));
			}
		} else {
			var parts = [];

			for(var j = 0; j < item.parts.length; j++) {
				parts.push(addStyle(item.parts[j], options));
			}

			stylesInDom[item.id] = {id: item.id, refs: 1, parts: parts};
		}
	}
}

function listToStyles (list, options) {
	var styles = [];
	var newStyles = {};

	for (var i = 0; i < list.length; i++) {
		var item = list[i];
		var id = options.base ? item[0] + options.base : item[0];
		var css = item[1];
		var media = item[2];
		var sourceMap = item[3];
		var part = {css: css, media: media, sourceMap: sourceMap};

		if(!newStyles[id]) styles.push(newStyles[id] = {id: id, parts: [part]});
		else newStyles[id].parts.push(part);
	}

	return styles;
}

function insertStyleElement (options, style) {
	var target = getElement(options.insertInto)

	if (!target) {
		throw new Error("Couldn't find a style target. This probably means that the value for the 'insertInto' parameter is invalid.");
	}

	var lastStyleElementInsertedAtTop = stylesInsertedAtTop[stylesInsertedAtTop.length - 1];

	if (options.insertAt === "top") {
		if (!lastStyleElementInsertedAtTop) {
			target.insertBefore(style, target.firstChild);
		} else if (lastStyleElementInsertedAtTop.nextSibling) {
			target.insertBefore(style, lastStyleElementInsertedAtTop.nextSibling);
		} else {
			target.appendChild(style);
		}
		stylesInsertedAtTop.push(style);
	} else if (options.insertAt === "bottom") {
		target.appendChild(style);
	} else {
		throw new Error("Invalid value for parameter 'insertAt'. Must be 'top' or 'bottom'.");
	}
}

function removeStyleElement (style) {
	if (style.parentNode === null) return false;
	style.parentNode.removeChild(style);

	var idx = stylesInsertedAtTop.indexOf(style);
	if(idx >= 0) {
		stylesInsertedAtTop.splice(idx, 1);
	}
}

function createStyleElement (options) {
	var style = document.createElement("style");

	options.attrs.type = "text/css";

	addAttrs(style, options.attrs);
	insertStyleElement(options, style);

	return style;
}

function createLinkElement (options) {
	var link = document.createElement("link");

	options.attrs.type = "text/css";
	options.attrs.rel = "stylesheet";

	addAttrs(link, options.attrs);
	insertStyleElement(options, link);

	return link;
}

function addAttrs (el, attrs) {
	Object.keys(attrs).forEach(function (key) {
		el.setAttribute(key, attrs[key]);
	});
}

function addStyle (obj, options) {
	var style, update, remove, result;

	// If a transform function was defined, run it on the css
	if (options.transform && obj.css) {
	    result = options.transform(obj.css);

	    if (result) {
	    	// If transform returns a value, use that instead of the original css.
	    	// This allows running runtime transformations on the css.
	    	obj.css = result;
	    } else {
	    	// If the transform function returns a falsy value, don't add this css.
	    	// This allows conditional loading of css
	    	return function() {
	    		// noop
	    	};
	    }
	}

	if (options.singleton) {
		var styleIndex = singletonCounter++;

		style = singleton || (singleton = createStyleElement(options));

		update = applyToSingletonTag.bind(null, style, styleIndex, false);
		remove = applyToSingletonTag.bind(null, style, styleIndex, true);

	} else if (
		obj.sourceMap &&
		typeof URL === "function" &&
		typeof URL.createObjectURL === "function" &&
		typeof URL.revokeObjectURL === "function" &&
		typeof Blob === "function" &&
		typeof btoa === "function"
	) {
		style = createLinkElement(options);
		update = updateLink.bind(null, style, options);
		remove = function () {
			removeStyleElement(style);

			if(style.href) URL.revokeObjectURL(style.href);
		};
	} else {
		style = createStyleElement(options);
		update = applyToTag.bind(null, style);
		remove = function () {
			removeStyleElement(style);
		};
	}

	update(obj);

	return function updateStyle (newObj) {
		if (newObj) {
			if (
				newObj.css === obj.css &&
				newObj.media === obj.media &&
				newObj.sourceMap === obj.sourceMap
			) {
				return;
			}

			update(obj = newObj);
		} else {
			remove();
		}
	};
}

var replaceText = (function () {
	var textStore = [];

	return function (index, replacement) {
		textStore[index] = replacement;

		return textStore.filter(Boolean).join('\n');
	};
})();

function applyToSingletonTag (style, index, remove, obj) {
	var css = remove ? "" : obj.css;

	if (style.styleSheet) {
		style.styleSheet.cssText = replaceText(index, css);
	} else {
		var cssNode = document.createTextNode(css);
		var childNodes = style.childNodes;

		if (childNodes[index]) style.removeChild(childNodes[index]);

		if (childNodes.length) {
			style.insertBefore(cssNode, childNodes[index]);
		} else {
			style.appendChild(cssNode);
		}
	}
}

function applyToTag (style, obj) {
	var css = obj.css;
	var media = obj.media;

	if(media) {
		style.setAttribute("media", media)
	}

	if(style.styleSheet) {
		style.styleSheet.cssText = css;
	} else {
		while(style.firstChild) {
			style.removeChild(style.firstChild);
		}

		style.appendChild(document.createTextNode(css));
	}
}

function updateLink (link, options, obj) {
	var css = obj.css;
	var sourceMap = obj.sourceMap;

	/*
		If convertToAbsoluteUrls isn't defined, but sourcemaps are enabled
		and there is no publicPath defined then lets turn convertToAbsoluteUrls
		on by default.  Otherwise default to the convertToAbsoluteUrls option
		directly
	*/
	var autoFixUrls = options.convertToAbsoluteUrls === undefined && sourceMap;

	if (options.convertToAbsoluteUrls || autoFixUrls) {
		css = fixUrls(css);
	}

	if (sourceMap) {
		// http://stackoverflow.com/a/26603875
		css += "\n/*# sourceMappingURL=data:application/json;base64," + btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))) + " */";
	}

	var blob = new Blob([css], { type: "text/css" });

	var oldSrc = link.href;

	link.href = URL.createObjectURL(blob);

	if(oldSrc) URL.revokeObjectURL(oldSrc);
}


/***/ }),
/* 21 */
/***/ (function(module, exports) {


/**
 * When source maps are enabled, `style-loader` uses a link element with a data-uri to
 * embed the css on the page. This breaks all relative urls because now they are relative to a
 * bundle instead of the current page.
 *
 * One solution is to only use full urls, but that may be impossible.
 *
 * Instead, this function "fixes" the relative urls to be absolute according to the current page location.
 *
 * A rudimentary test suite is located at `test/fixUrls.js` and can be run via the `npm test` command.
 *
 */

module.exports = function (css) {
  // get current location
  var location = typeof window !== "undefined" && window.location;

  if (!location) {
    throw new Error("fixUrls requires window.location");
  }

	// blank or null?
	if (!css || typeof css !== "string") {
	  return css;
  }

  var baseUrl = location.protocol + "//" + location.host;
  var currentDir = baseUrl + location.pathname.replace(/\/[^\/]*$/, "/");

	// convert each url(...)
	/*
	This regular expression is just a way to recursively match brackets within
	a string.

	 /url\s*\(  = Match on the word "url" with any whitespace after it and then a parens
	   (  = Start a capturing group
	     (?:  = Start a non-capturing group
	         [^)(]  = Match anything that isn't a parentheses
	         |  = OR
	         \(  = Match a start parentheses
	             (?:  = Start another non-capturing groups
	                 [^)(]+  = Match anything that isn't a parentheses
	                 |  = OR
	                 \(  = Match a start parentheses
	                     [^)(]*  = Match anything that isn't a parentheses
	                 \)  = Match a end parentheses
	             )  = End Group
              *\) = Match anything and then a close parens
          )  = Close non-capturing group
          *  = Match anything
       )  = Close capturing group
	 \)  = Match a close parens

	 /gi  = Get all matches, not the first.  Be case insensitive.
	 */
	var fixedCss = css.replace(/url\s*\(((?:[^)(]|\((?:[^)(]+|\([^)(]*\))*\))*)\)/gi, function(fullMatch, origUrl) {
		// strip quotes (if they exist)
		var unquotedOrigUrl = origUrl
			.trim()
			.replace(/^"(.*)"$/, function(o, $1){ return $1; })
			.replace(/^'(.*)'$/, function(o, $1){ return $1; });

		// already a full url? no change
		if (/^(#|data:|http:\/\/|https:\/\/|file:\/\/\/)/i.test(unquotedOrigUrl)) {
		  return fullMatch;
		}

		// convert the url to a full url
		var newUrl;

		if (unquotedOrigUrl.indexOf("//") === 0) {
		  	//TODO: should we add protocol?
			newUrl = unquotedOrigUrl;
		} else if (unquotedOrigUrl.indexOf("/") === 0) {
			// path should be relative to the base url
			newUrl = baseUrl + unquotedOrigUrl; // already starts with '/'
		} else {
			// path should be relative to current directory
			newUrl = currentDir + unquotedOrigUrl.replace(/^\.\//, ""); // Strip leading './'
		}

		// send back the fixed url(...)
		return "url(" + JSON.stringify(newUrl) + ")";
	});

	// send back the fixed css
	return fixedCss;
};


/***/ })
],[8]);