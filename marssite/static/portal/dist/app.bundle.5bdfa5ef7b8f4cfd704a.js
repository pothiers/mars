webpackJsonp([1],[
/* 0 */,
/* 1 */,
/* 2 */,
/* 3 */,
/* 4 */,
/* 5 */,
/* 6 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__vue_Search_vue__ = __webpack_require__(9);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__vue_Search_vue___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0__vue_Search_vue__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__vue_Results_vue__ = __webpack_require__(13);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__vue_Results_vue___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1__vue_Results_vue__);
var Vue = __webpack_require__(0);
var moment = __webpack_require__(3);




var AppStyles = __webpack_require__(5);

//import Main from "../vue/Main.vue";

class App {
  constructor(){
    window.moment = moment;
    new Vue({
      el: "#content",
      template: "<component compdata='componentData' v-bind:is='currentView' v-on:displayform='switchComponent' />",
      methods: {
        switchComponent(data){
          this.componentData = data[1];
          this.currentView = data[0];
          window.base.bindEvents();
        }
      },
      data: {
        currentView: "search",
        componentData: []
      },
      components: {
        search: __WEBPACK_IMPORTED_MODULE_0__vue_Search_vue___default.a,
        results: __WEBPACK_IMPORTED_MODULE_1__vue_Results_vue___default.a
      }
    });
  }
}

new App();


/***/ }),
/* 7 */,
/* 8 */,
/* 9 */
/***/ (function(module, exports, __webpack_require__) {

var disposed = false
var Component = __webpack_require__(1)(
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
Component.options.__file = "/Users/ppeterson/Workspace/portal/mars/marssite/portal/vue/Search.vue"
if (Component.esModule && Object.keys(Component.esModule).some(function (key) {return key !== "default" && key.substr(0, 2) !== "__"})) {console.error("named exports are not supported in *.vue files.")}
if (Component.options.functional) {console.error("[vue-loader] Search.vue: functional components are not supported with templates, they should use render functions.")}

/* hot reload */
if (false) {(function () {
  var hotAPI = require("vue-hot-reload-api")
  hotAPI.install(require("vue"), false)
  if (!hotAPI.compatible) return
  module.hot.accept()
  if (!module.hot.data) {
    hotAPI.createRecord("data-v-b46fd354", Component.options)
  } else {
    hotAPI.reload("data-v-b46fd354", Component.options)
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
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__js_search_js__ = __webpack_require__(11);
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//


/* harmony default export */ __webpack_exports__["default"] = (__WEBPACK_IMPORTED_MODULE_0__js_search_js__["a" /* default */]);
///module.exports = search;

/***/ }),
/* 11 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_vue__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_vue___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_vue__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_vee_validate__ = __webpack_require__(4);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__mixins_js__ = __webpack_require__(2);
/*
Author: Peter Peterson
Date: 2017-06-09
Description: Serves functionality for submitting and displaying archive query forms/results
*/

//import Vue from 'vue';




const validateDependsOn = {
  getMessage(field, params, data){
    const id = params[0].replace("#", "");
    const dependsOn = document.querySelector(`label[for=${id}]`).innerText;
    return (data && data.message) || `This field depends on ${dependsOn}`;
  },
  validate(value, args){
    return (document.querySelector(args[0]).value !== "");
  }
};

var config = __WEBPACK_IMPORTED_MODULE_2__mixins_js__["a" /* default */].config;

(function(){
  // This gets called after the component has been mounted
  window.addEventListener('searchLoaded', function(e){
    console.log("Search loaded", e);
    // re-bind since the template will render after the page is loaded.
    return window.base.bindEvents();
  });
  __WEBPACK_IMPORTED_MODULE_1_vee_validate__["Validator"].extend('dependson', validateDependsOn);
  const validation = new __WEBPACK_IMPORTED_MODULE_1_vee_validate__["Validator"]({dependant:"dependson"});
  // Use vee-validate, and assign before component is loaded
  __WEBPACK_IMPORTED_MODULE_0_vue___default.a.use(__WEBPACK_IMPORTED_MODULE_1_vee_validate__["default"], config.validatorConfig); // validation plugin
})();

const dateLookup = {
      "obs-date": {
        "field" : "obs_date",
        "index" : 0
      },
      "obs-date-max": {
        "field" : 'obs_date',
        "index" : 1
      },
      "release-date": {
        "field": "release_date",
        "index": 0
      },
      "release-date-max":{
        "field": "release_date",
        "index": 1
      },
      "parent":{
        "obj": this
      }
};

const scrollingWatcher = function(){
  if (document.querySelector("[rel=form-submit]") === null) {
    return;
  }

  const doc = document.documentElement;
  const top = (window.pageYOffset || doc.scrollTop)  - (doc.clientTop || 0);
  const element = document.querySelector("[rel=form-submit]");
  const elementTop = element.offsetTop;

  // check offset
  if (top > elementTop) {
    element.classList.add("scroll");
  } else {
    element.classList.remove("scroll");
  }
};

var Search;
/* harmony default export */ __webpack_exports__["a"] = (Search = {
  mixins: [__WEBPACK_IMPORTED_MODULE_2__mixins_js__["a" /* default */].mixin],
  created(){
    this.getTelescopes();
  },
  mounted(){
    // check if this is a new search
    if (window.location.hash.indexOf("search_again") > -1) {
      const oldSearch = JSON.parse(localStorage.getItem("searchData"));
      this.search = oldSearch;
    } else if (window.location.hash.indexOf("query") > -1) {
      this.$emit("displayform", ["results", []]);
    }
    window.base.bindEvents();

    document.onscroll = scrollingWatcher;

    $("input.date").datepicker({
            changeMonth: true,
            changeYear: true,
            onSelect: (dateText, datePicker)=> {
              const fieldName = datePicker.input[0].name;
              const field = this.search[dateLookup[fieldName].field];
              field[dateLookup[fieldName].index] = dateText;
              const e = new CustomEvent("datechanged", {'detail':{'date':dateText} });
              document.dispatchEvent(e);
              // this value is updated to force the computed values to refresh
              // for the code sample view
              return this.code = new Date().getTime();
            }
              //nothing = this.code
      });
    $("input.date").datepicker("option", "dateFormat", "yy-mm-dd");

    // for debugging/testing in the browser
    window.searchVue = this;

    // Datepicker doesn't trigger change in the model data, so...
    // bind to datepicker changes
    document.addEventListener("datechanged", ()=> console.log("update code view"));
  },

  computed: {
    code: {
      get(){
        this.codeView = JSON.stringify({search:this.stripData()}, null, 2);
        return this.codeView;
      },
      set(update){
        // for some reason, the code view won't update unless we go through this mess
        this.codeUpdate = update;
        this.codeView = JSON.stringify({search:this.stripData()}, null, 2);
        return null;
      }
    }
  },
  data(){
    return {
      url: config.apiUrl,
      visible: true,
      loading: false,
      codeUpdate: 0,
      codeView: "",
      modalTitle: "",
      modalBody: "",
      loadingMessage: "Sweeping up star dust...",
      search: JSON.parse(JSON.stringify(config.formData)), // deep copy
      showExposureMax: false,
      showObsDateMax: false,
      showReleaseDateMax: false,
      showBothExposureFields: false,
      showBothObsDateFields: false,
      showBothReleaseDateFields: false,
      telescopes: [],
      relatedSplitFieldFlags : {
        "exposure_time":
          {"fieldFlag":'showExposureMax', "bothFieldFlag":"showBothExposureFields"},
        "obs_date":
          {"fieldFlag":"showObsDateMax", "bothFieldFlag":"showBothObsDateFields"},
        "release_date":
          {"fieldFlag":"showReleaseDateMax","bothFieldFlag":"showBothReleaseDateFields"}
      },
      option:{
        format: 'YYYY-MM-DD'
      }
    };
  },

  methods: {
    closeModal(){
      ToggleModal("#search-modal");
    },
    newSearch(){
      // clear current search and storage
      this.search = JSON.parse(JSON.stringify(this.config.formData));
      localStorage.setItem("searchData", JSON.stringify(this.search));
    },
    getTelescopes(){
      // check if we have a cached set to use
      let telescopes = JSON.parse(localStorage.getItem("telescopes")||"0");
      const self = this;
      const now = moment();
      if (telescopes && (moment(telescopes != null ? telescopes.expires : undefined) > now)) {
        self.telescopes = telescopes.telescopes;
      } else {
        new Ajax({
          url: window.location.origin+"/dal/ti-pairs",
          method: "get",
          accept: "json",
          success(data){
            self.telescopes = data;
            telescopes = {
              expires: moment().add(7,'days'),
              telescopes: data
            };
            localStorage.setItem("telescopes", JSON.stringify(telescopes));
          }
        });
      }
    },

    splitSelection(val){
      // for toggling conditional form inputs, one and sometimes both
      const fieldFlag = this.relatedSplitFieldFlags[val]['fieldFlag'];
      const bothFlag = this.relatedSplitFieldFlags[val]['bothFieldFlag'];

      if ((this.search[val][2] === "(]") || (this.search[val][2] === "[]")) {
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

});


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
      "id": "submit-form",
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
  })])]), _vm._v(" "), _c('div', {
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
  })])])])])])])]), _vm._v(" "), _c('div', {
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
  }, [_vm._v("Program Number (Prop ID)")]), _vm._v(" "), _c('input', {
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
      "placeholder": "Program Number (Prop ID)",
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
        _vm.$set(_vm.search.obs_date, 2, $event.target.multiple ? $$selectedVal : $$selectedVal[0])
      }, function($event) {
        _vm.splitSelection('obs_date')
      }]
    }
  }, [_c('option', {
    attrs: {
      "value": "="
    }
  }, [_vm._v("On Date")]), _vm._v(" "), _c('option', {
    attrs: {
      "value": "(]"
    }
  }, [_vm._v("Before Date")]), _vm._v(" "), _c('option', {
    attrs: {
      "value": "[)"
    }
  }, [_vm._v("After Date")]), _vm._v(" "), _c('option', {
    staticClass: "toggle-option",
    attrs: {
      "value": "[]"
    }
  }, [_vm._v("Between")])]), _vm._v(" "), (_vm.search.obs_date[2] !== '(]') ? _c('input', {
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
        _vm.$set(_vm.search.obs_date, 0, $event.target.value)
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
        _vm.$set(_vm.search.obs_date, 1, $event.target.value)
      }
    }
  })])]), _vm._v(" "), _c('div', {
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
        _vm.$set(_vm.search.exposure_time, 2, $event.target.multiple ? $$selectedVal : $$selectedVal[0])
      }, function($event) {
        _vm.splitSelection('exposure_time')
      }]
    }
  }, [_c('option', {
    attrs: {
      "value": "="
    }
  }, [_vm._v("Exactly")]), _vm._v(" "), _c('option', {
    attrs: {
      "value": "(]"
    }
  }, [_vm._v("Less Than")]), _vm._v(" "), _c('option', {
    attrs: {
      "value": "[)"
    }
  }, [_vm._v("Greater Than")]), _vm._v(" "), _c('option', {
    staticClass: "toggle-option",
    attrs: {
      "value": "[]"
    }
  }, [_vm._v("Between")])]), _vm._v(" "), (_vm.search.exposure_time[2] !== '(]') ? _c('input', {
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
        _vm.$set(_vm.search.exposure_time, 0, $event.target.value)
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
        _vm.$set(_vm.search.exposure_time, 1, $event.target.value)
      }
    }
  })])])])])])])]), _vm._v(" "), _c('div', {
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
        _vm.$set(_vm.search.release_date, 2, $event.target.multiple ? $$selectedVal : $$selectedVal[0])
      }, function($event) {
        _vm.splitSelection('release_date')
      }]
    }
  }, [_c('option', {
    attrs: {
      "value": "="
    }
  }, [_vm._v("On Date")]), _vm._v(" "), _c('option', {
    attrs: {
      "value": "(]"
    }
  }, [_vm._v("Before Date")]), _vm._v(" "), _c('option', {
    attrs: {
      "value": "[)"
    }
  }, [_vm._v("After Date")]), _vm._v(" "), _c('option', {
    staticClass: "toggle-option",
    attrs: {
      "value": "[]"
    }
  }, [_vm._v("Between")])]), _vm._v(" "), (_vm.search.release_date[2] !== '(]') ? _c('input', {
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
        _vm.$set(_vm.search.release_date, 0, $event.target.value)
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
      "data-polyfill": "all",
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
        _vm.$set(_vm.search.release_date, 1, $event.target.value)
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
  }, [_vm._v("Sky Subtracted (Newfirm)")])]), _vm._v(" "), _c('p', {
    staticClass: "help-block"
  }, [_vm._v("\n                                        * "), _c('em', [_vm._v("Calibrated, Reprojected, Stacked, Master calibration, Image Tiles")]), _vm._v(" are for "), _c('strong', [_vm._v("Mosiac, NEWFIRM and DECam")]), _vm._v(".\n                                    ")])])])]), _vm._v(" "), _c('div', {
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
      "name": "telescope[]",
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
        "value": tel[0] + ',' + tel[1]
      }
    }, [_vm._v(_vm._s(tel[0]) + " + " + _vm._s(tel[1]))])
  }))])])])])])])])]) : _vm._e()]), _vm._v(" "), _c('div', {
    staticClass: "code-view"
  }, [_c('pre', {
    staticClass: "code"
  }, [_vm._v(_vm._s(_vm.code))])]), _vm._v(" "), _c('div', {
    staticClass: "modal fade",
    attrs: {
      "id": "search-modal",
      "tabindex": "-1",
      "role": "dialog",
      "aria-labelledby": "searchModelLabel"
    }
  }, [_c('div', {
    staticClass: "modal-dialog",
    attrs: {
      "role": "document"
    }
  }, [_c('div', {
    staticClass: "modal-content"
  }, [_c('div', {
    staticClass: "modal-header"
  }, [_c('button', {
    staticClass: "close",
    attrs: {
      "type": "button",
      "data-dismiss": "modal",
      "aria-label": "Close"
    },
    on: {
      "click": _vm.closeModal
    }
  }, [_c('span', {
    attrs: {
      "aria-hidden": "true"
    }
  }, [_vm._v("×")])]), _vm._v(" "), _c('h4', {
    staticClass: "modal-title",
    attrs: {
      "id": "myModalLabel"
    }
  }, [_vm._v(_vm._s(_vm.modalTitle))])]), _vm._v(" "), _c('div', {
    staticClass: "modal-body",
    domProps: {
      "innerHTML": _vm._s(_vm.modalBody)
    }
  }), _vm._v(" "), _c('div', {
    staticClass: "modal-footer"
  }, [_c('button', {
    staticClass: "btn btn-default",
    attrs: {
      "type": "button",
      "data-dismiss": "modal"
    },
    on: {
      "click": _vm.closeModal
    }
  }, [_vm._v("Close")])])])])])], 1)
},staticRenderFns: []}
module.exports.render._withStripped = true
if (false) {
  module.hot.accept()
  if (module.hot.data) {
     require("vue-hot-reload-api").rerender("data-v-b46fd354", module.exports)
  }
}

/***/ }),
/* 13 */
/***/ (function(module, exports, __webpack_require__) {

var disposed = false
var Component = __webpack_require__(1)(
  /* script */
  __webpack_require__(14),
  /* template */
  __webpack_require__(17),
  /* styles */
  null,
  /* scopeId */
  null,
  /* moduleIdentifier (server only) */
  null
)
Component.options.__file = "/Users/ppeterson/Workspace/portal/mars/marssite/portal/vue/Results.vue"
if (Component.esModule && Object.keys(Component.esModule).some(function (key) {return key !== "default" && key.substr(0, 2) !== "__"})) {console.error("named exports are not supported in *.vue files.")}
if (Component.options.functional) {console.error("[vue-loader] Results.vue: functional components are not supported with templates, they should use render functions.")}

/* hot reload */
if (false) {(function () {
  var hotAPI = require("vue-hot-reload-api")
  hotAPI.install(require("vue"), false)
  if (!hotAPI.compatible) return
  module.hot.accept()
  if (!module.hot.data) {
    hotAPI.createRecord("data-v-17073438", Component.options)
  } else {
    hotAPI.reload("data-v-17073438", Component.options)
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
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__js_results_js__ = __webpack_require__(15);
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//


/* harmony default export */ __webpack_exports__["default"] = (__WEBPACK_IMPORTED_MODULE_0__js_results_js__["a" /* default */]);

/***/ }),
/* 15 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_vue__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_vue___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_vue__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__components_js__ = __webpack_require__(16);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__components_js___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1__components_js__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__mixins_js__ = __webpack_require__(2);





/*
  Helper functions
 */
var config;

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
  App - Results
 */

config = __WEBPACK_IMPORTED_MODULE_2__mixins_js__["a" /* default */].config;

window.bus = new __WEBPACK_IMPORTED_MODULE_0_vue___default.a();

var Results;

/* harmony default export */ __webpack_exports__["a"] = (Results = {
  props: ['componentData'],
  mixins: [__WEBPACK_IMPORTED_MODULE_2__mixins_js__["a" /* default */].mixin],
  data: function() {
    return {
      visibleColumns: [],
      categoriesVisible: false,
      categories: {},
      activeTab: 'main',
      allColumns: config.allColumns,
      stageAllConfirm: false,
      stageButtonText: "Stage ALL results",
      visible: false,
      pageNum: 1,
      isLoading: false,
      recordsFrom: 1,
      recordsTo: 100,
      results: [],
      selected: [],
      lastSelected: null,
      searchObj: JSON.parse(localStorage.getItem('search')),
      totalItems: 0,
      toggle: false,
      error: ""
    };
  },
  methods: {
    setCategory: function (category_key, category_value) {
      console.log("category_key:", category_key, "cat_value", category_value);
      //split instrument/telescope
      var key = category_key;
      var value = category_value;

      if( key == "telescope_instrument"){
        value = [value.split(",")]
      }
      // set the category in the original search query
      var query = localStorage.getItem("search");
      query = JSON.parse(query);
      query[key] = value;
      // save this new query for future (paging etc)
      localStorage.setItem("category_"+key, JSON.stringify(query));

      // get the category results from the server...
      this.submitQuery(config.apiUrl, query, key, (data)=>{
        console.log("got this category resultset", data);
        // create a new tab and place results there
        this.results = data;
      });
    },

    getCategory: function(query){
      var self = this;
      var localCats = null;
      if ( (localCats = localStorage.getItem("categories")) !== null){
        self.categories = JSON.parse(localCats);
      }else{
        new Ajax({
          url: window.location.origin + "/dal/get-categories",
          data: JSON.parse(query),
          method: "post",
          accept: "json",
          success: function(data) {

            if (data.status == "success"){
              var cats = {};
              /*
                categories: {
                  'name': [
                    {'name':'value'}
                    ...
                    n{'name':'value'}
                  ]
                }
              */
              for(var item in data.categories){
                for(var val in data.categories[item]){
                  if(data.categories[item][val][item] !== null &&data.categories[item][val][item] !== ""){
                    if(cats[item] == undefined){ cats[item] = []}
                    cats[item].push(data.categories[item][val][item]);
                  }
                }
              }
              console.log("formated categories", cats);
              localStorage.setItem("categories", JSON.stringify(cats));
              self.categories = cats;
            }
          }
        });
      }
    },

    toggleCategories: function() {
      this.categoriesVisible = !this.categoriesVisible;
    },

    toggleColumn: function(column) {
      var col, first, found, i, j, last, len, len1, n, ref, ref1;
      if (column.checked) {
        ref = this.visibleColumns;
        for (n = i = 0, len = ref.length; i < len; n = ++i) {
          col = ref[n];
          if (_.isEqual(col, column)) {
            this.visibleColumns.splice(n, 1);
          }
        }
      } else {
        found = false;
        ref1 = this.visibleColumns;
        for (n = j = 0, len1 = ref1.length; j < len1; n = ++j) {
          col = ref1[n];
          if (column.num < col.num) {
            first = this.visibleColumns.slice(0, n);
            last = this.visibleColumns.slice(n);
            this.visibleColumns = first.concat(column, last);
            found = true;
            break;
          }
        }
        if (found !== true) {
          this.visibleColumns.push(column);
        }
      }
      column.checked = !column.checked;
    },

    stageSelected: function() {
      var data, form;
      localStorage.setItem("stage", "selectedFiles");
      localStorage.setItem("selectedFiles", JSON.stringify(this.selected));
      form = document.createElement("form");
      form.setAttribute("method", "POST");
      form.setAttribute("action", "/portal/staging/?stage=selected");
      data = document.createElement("input");
      data.setAttribute("type", "hidden");
      data.setAttribute("value", localStorage.getItem("selectedFiles"));
      data.setAttribute("name", "selectedFiles");
      form.appendChild(data);
      document.querySelector("body").appendChild(form);
      form.submit();
    },

    cancelStageAll: function() {
      this.stageButtonText = 'Stage ALL results';
      this.stageAllConfirm = false;
    },

    confirmStage: function() {
      var data, form, searchObj;
      if (this.stageAllConfirm === true) {
        console.log("second confirm is true");
        localStorage.setItem("stage", "all");
        form = document.createElement("form");
        form.setAttribute("method", "POST");
        form.setAttribute("action", config.stagingUrl + "?stage=all");
        data = document.createElement("input");
        data.setAttribute("type", "hidden");
        searchObj = localStorage.getItem("searchData");
        data.setAttribute("value", searchObj);
        data.setAttribute("name", "searchData");
        form.appendChild(data);
        document.querySelector("body").appendChild(form);
        form.submit();
      } else {
        this.stageButtonText = "OK, continue";
        this.stageAllConfirm = true;
      }
    },

    toggleResults: function() {
      this.toggle = !this.toggle;
      console.log("toggle");
      rebus.$emit("toggleselected", this.toggle);
    },

    displayForm: function() {
      window.location.hash = "#search_again";
      this.$emit("displayform", ["search", JSON.parse(localStorage.getItem('search'))]);
    },

    handleError: function(e) {
      console.log("There was an error", e);
    },

    pageNext: function() {
      this.pageTo(this.pageNum + 1);
    },

    pageBack: function() {
      this.pageTo(this.pageNum - 1);
    },

    pageTo: function(page) {
      var self;
      this.pageNum = page;
      localStorage.setItem('currentPage', page);
      this.$emit("pageto", page);
      this.isLoading = true;
      self = this;
      this.submitForm(null, "paging", function(data) {
        self.isLoading = false;
        self.results = data;
        self.recordsFrom = data.meta.to_here_count - data.meta.page_result_count + 1;
        self.recordsTo = data.meta.to_here_count;
      });
    }
  },

  created: function() {
    var col, i, len, ref, results;
    ref = this.allColumns;
    results = [];
    for (i = 0, len = ref.length; i < len; i++) {
      col = ref[i];
      if (col.checked) {
        results.push(this.visibleColumns.push(col));
      } else {
        results.push(void 0);
      }
    }
    return results;
  },

  updated: function() {
    window.base.bindEvents();
  },

  mounted: function() {
    var e, q, ref;
    window.results = this;
    console.log("Results mounted");
    q = localStorage.getItem("search");

    // get categories for this query
    this.getCategory(q);

    bus.$on("toggleselected", (function(_this) {
      return function(onoff) {
        if (onoff) {
          _this.selected = [].concat(_this.results.resultset);
        } else {
          _this.selected = [];
        }
      };
    })(this));
    bus.$on("rowselected", (function(_this) {
      return function(data) {
        var alreadySelected, curIdx, i, idx, index, j, k, l, len, len1, len2, obj, prevIdx, ref, ref1, ref2, ref3, ref4, row, sel;
        if (data.isSelected) {
          _this.selected.push(data.row);
          if (data.event.shiftKey) {
            prevIdx = null;
            curIdx = null;
            ref = _this.results.resultset;
            for (idx = i = 0, len = ref.length; i < len; idx = ++i) {
              obj = ref[idx];
              if (obj === data.row) {
                curIdx = idx;
                break;
              }
            }
            ref1 = _this.results.resultset;
            for (idx = j = 0, len1 = ref1.length; j < len1; idx = ++j) {
              obj = ref1[idx];
              if (obj === _this.lastSelected) {
                prevIdx = idx;
                break;
              }
            }
            for (idx = k = ref2 = prevIdx, ref3 = curIdx; ref2 <= ref3 ? k <= ref3 : k >= ref3; idx = ref2 <= ref3 ? ++k : --k) {
              row = _this.results.resultset[idx];
              alreadySelected = false;
              ref4 = _this.selected;
              for (l = 0, len2 = ref4.length; l < len2; l++) {
                sel = ref4[l];
                if (row.reference === sel.reference) {
                  alreadySelected = true;
                  break;
                }
              }
              if (alreadySelected === false) {
                bus.$emit("selectrow", row);
                _this.selected.push(row);
              }
            }
          }
          _this.lastSelected = data.row;
        } else {
          index = _.indexOf(_this.selected, data.row);
          _this.selected.splice(index, 1);
        }
      };
    })(this));
    if (window.location.hash === "#query") {
      try {
        this.results = JSON.parse(localStorage.getItem('results')) || [];
        this.totalItems = (ref = this.results) != null ? ref.meta.total_count : void 0;
        this.visible = true;
        this.pageNum = parseInt(localStorage.getItem("currentPage"));
      } catch (_error) {
        e = _error;
        this.results = [];
        this.totalItems = 0;
        this.visible = true;
        this.error = "There was an error parsing results from server";
        this.handleError(e);
      }
    }
  }
});


/***/ }),
/* 16 */
/***/ (function(module, exports, __webpack_require__) {

var Vue = __webpack_require__(0);

/*
   Vue components
   For rendering results table
*/
Vue.component("table-header", {
  props: ['name'],
  template: "<span>{{ name }}</span>"
}
);

Vue.component("table-cell", {
  props: ['data', 'field'],
  template: "<td v-if='data' v-bind:rel='field'>{{ format }}</td><td class='empty' v-else></td>",
  computed: {
      format(){
        if (this.data === null) {
          return this.data;
        }
        if ((this.field === 'obs_date') || (this.field === 'release_date')) {
          try {
            const d = moment(this.data);
            const dateStr = d.format("YYYY-MM-DD");
            return dateStr;
          } catch (error) {
            return this.data;
          }
        } else {
          return this.data;
        }
      }
    }
}
);

Vue.component("table-row", {
  props: ['row', 'cols'],
  template: "<tr v-on:click='selectRow' v-bind:class='{selected:isSelected}'><td class='select-row'><input type='checkbox' name='' v-bind:checked='isSelected' v-bind:name='row.reference'></td><table-cell v-for='vis in cols' v-bind:data='row[vis.mapping]' v-bind:field='vis.mapping' :key='row.id'></table-cell></tr>",
  data(){
    return {
      isSelected: false
    };
  },
  created(){
    bus.$on("selectrow", _row=> {
      if (_row.reference === this.row.reference) {
        this.isSelected = true;
      }
    });
    return bus.$on("toggleselected", onoff=> {
      this.isSelected = onoff;
    });
  },
  methods: {
    selectRow(event){
      this.isSelected = !this.isSelected;
      bus.$emit("rowselected", {isSelected:this.isSelected, row:this.row, vueobject:this, event});
    }
  }
}
);

Vue.component("table-body", {
   props: ['data', 'visibleCols'],
   template: "<tbody ><table-row v-for='(item,idx) in data' v-bind:cols='visibleCols' v-bind:row='item' :key='item.id'></table-row></tbody>",
   methods: {
     iheardthat(){
       console.log("I heard that");
     }
   }
 }
);


/***/ }),
/* 17 */
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
  }, [_vm._v("Query returned "), _c('em', [_vm._v(_vm._s(_vm.totalItems))]), _vm._v(" records")]), _vm._v(" "), _c('ul', {
    staticClass: "list-inline"
  }, [_c('li', [_c('button', {
    staticClass: "btn btn-default",
    on: {
      "click": _vm.toggleCategories
    }
  }, [_c('span', {
    staticClass: "fa fa-bars"
  }), _vm._v(" Toggle Categories")])]), _vm._v(" "), _c('li', [_c('div', {
    staticClass: "form-inline"
  }, [_c('div', {
    staticClass: "form-group"
  }, [_c('input', {
    staticClass: "form-control",
    attrs: {
      "name": "",
      "type": "text",
      "value": "",
      "placeholder": "Filter"
    }
  })])])])])]), _vm._v(" "), _c('div', {
    staticClass: "col-xs-2 text-right"
  }, [_c('button', {
    staticClass: "btn btn-primary",
    on: {
      "click": _vm.displayForm
    }
  }, [_vm._v("Search Again")])])])]), _vm._v(" "), _c('div', {
    staticClass: "container"
  }, [_c('div', {
    staticClass: "row"
  }, [(_vm.categoriesVisible) ? _c('div', {
    staticClass: "col-md-3 col-xs-12 results-categories"
  }, [_c('h3', [_vm._v("Category results by:")]), _vm._v(" "), _vm._l((_vm.categories), function(cat, indx) {
    return _c('ul', {
      staticClass: "list-group"
    }, [_c('li', {
      staticClass: "list-group-item"
    }, [_c('h4', {
      staticClass: "text-primary"
    }, [_vm._v(_vm._s(indx.replace("_", " ")))]), _vm._v(" "), _c('ul', {
      staticClass: "category-sublist"
    }, _vm._l((cat), function(item) {
      return _c('li', {
        staticClass: "checkbox"
      }, [_c('label', [_c('input', {
        attrs: {
          "type": "radio",
          "name": 'category_' + indx
        },
        on: {
          "click": function($event) {
            _vm.setCategory(indx, item)
          }
        }
      }), _vm._v(" " + _vm._s(item) + "\n                                   ")])])
    }))])])
  })], 2) : _vm._e(), _vm._v(" "), _c('div', {
    staticClass: "col-xs-12 results-wrapper",
    class: {
      'col-md-9': _vm.categoriesVisible
    }
  }, [_c('div', {
    staticClass: "collapsible"
  }, [_c('div', {
    staticClass: "column-toggle panel panel-default"
  }, [_c('div', {
    staticClass: "panel-heading section-heading clearfix"
  }, [_c('strong', {}, [_vm._v("Toggle visibility of columns\n                                ")]), _vm._v(" "), _c('div', {
    staticClass: "section-toggle"
  }, [_c('span', {
    staticClass: "icon open"
  })])]), _vm._v(" "), _c('div', {
    staticClass: "panel-body section-content "
  }, [_c('ul', {
    staticClass: "list-unstyled columns"
  }, _vm._l((_vm.allColumns), function(column) {
    return _c('li', [_c('label', [_c('input', {
      attrs: {
        "name": "",
        "type": "checkbox",
        "value": "",
        "name": column.mapping
      },
      domProps: {
        "checked": column.checked
      },
      on: {
        "change": function($event) {
          _vm.toggleColumn(column)
        }
      }
    }), _vm._v(" " + _vm._s(column.name))])])
  }))])])]), _vm._v(" "), _c('div', {
    staticClass: "row"
  }, [_c('div', {
    staticClass: "row results-controls"
  }, [_c('div', {
    staticClass: "col-sm-5"
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
  }, [_vm._v("Next")]), _vm._v(" "), _c('span', {
    staticClass: "records-from"
  }, [_vm._v(_vm._s(_vm.recordsFrom))]), _vm._v(" to "), _c('span', {
    staticClass: "records-to"
  }, [_vm._v(_vm._s(_vm.recordsTo))]), _vm._v(" "), (_vm.isLoading) ? _c('span', {
    staticClass: "fa fa-spinner fa-spin fa-1x fa-fw"
  }) : _vm._e()]), _vm._v(" "), _c('div', {
    staticClass: "col-sm-7 "
  })])]), _vm._v(" "), _c('div', {
    staticClass: "row"
  }, [_c('div', {
    staticClass: "col-sm-3"
  }, [_c('label', [_c('input', {
    attrs: {
      "name": "",
      "type": "checkbox",
      "value": ""
    },
    on: {
      "change": _vm.toggleResults
    }
  }), _vm._v(" Select all visible")])]), _vm._v(" "), _c('div', {
    staticClass: "col-sm-9 text-right"
  }, [_c('button', {
    staticClass: "btn btn-default",
    attrs: {
      "disabled": _vm.selected.length == 0
    },
    on: {
      "click": _vm.stageSelected
    }
  }, [_vm._v("Stage selected files")]), _vm._v(" "), _c('button', {
    staticClass: "btn btn-default",
    class: {
      'btn-danger': _vm.stageAllConfirm
    },
    on: {
      "click": _vm.confirmStage
    }
  }, [_vm._v(_vm._s(_vm.stageButtonText))]), _vm._v(" "), (_vm.stageAllConfirm) ? _c('div', {
    staticClass: "text-small help-block"
  }, [_c('span', {
    staticClass: "text-danger"
  }, [_vm._v("You are about to stage "), _c('strong', [_vm._v("ALL")]), _vm._v(" results. "), _c('strong', [_vm._v("Click again to confirm")])]), _vm._v(" "), (_vm.stageAllConfirm) ? _c('span', {
    staticClass: "label label-primary"
  }, [_vm._v(_vm._s(_vm.results.meta.total_count) + " files")]) : _vm._e(), _vm._v(" | "), _c('button', {
    staticClass: "btn btn-default btn-small",
    on: {
      "click": _vm.cancelStageAll
    }
  }, [_vm._v("Cancel")])]) : _vm._e()])]), _vm._v(" "), ((_vm.results.resultset.length > 0)) ? _c('table', {
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
  }), _vm._v(" "), _c('tfoot')]) : _c('div', [_c('h1', {
    staticClass: "text-center"
  }, [_vm._v("No results found")]), _vm._v(" "), (_vm.error) ? _c('div', {
    staticClass: "alert alert-danger text-center"
  }, [_vm._v(_vm._s(_vm.error))]) : _vm._e(), _vm._v(" "), _c('pre', {
    staticClass: "code"
  }, [_vm._v(_vm._s(_vm.searchObj) + "\n                    ")]), _vm._v(" "), _c('div', {
    staticClass: "text-center"
  }, [_c('h5', [_vm._v("You might try and adjust your paramaters and search again")]), _vm._v(" "), _c('button', {
    staticClass: "btn btn-success",
    on: {
      "click": _vm.displayForm
    }
  }, [_vm._v("Adjust Paramaters")])])])])])])]) : _vm._e()])], 1)
},staticRenderFns: []}
module.exports.render._withStripped = true
if (false) {
  module.hot.accept()
  if (module.hot.data) {
     require("vue-hot-reload-api").rerender("data-v-17073438", module.exports)
  }
}

/***/ })
],[6]);