webpackJsonp([2],[
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
var Vue = __webpack_require__(0);
var moment = __webpack_require__(1);


//var Results = require("../vue/Results.vue");
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
        //stuff: Main,
        search: __WEBPACK_IMPORTED_MODULE_0__vue_Search_vue___default.a,
        //results: Results
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
var Component = __webpack_require__(2)(
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
Component.options.__file = "/home/peter/Workspace/NOAO/portal/mars/marssite/portal/vue/Search.vue"
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
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_vee_validate__ = __webpack_require__(3);
/*
Author: Peter Peterson
Date: 2017-06-09
Description: Serves functionality for submitting and displaying archive query forms/results
*/

//import Vue from 'vue';



var shared = __webpack_require__(4);

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

var config = shared.default.config;

(function(){
  // This gets called after the component has been mounted
  window.addEventListener('searchLoaded', function(e){
    console.log("Search loaded", e);
    // re-bind since the template will render after the page is loaded.
    return window.base.bindEvents();
  });
//  Validator.extend('dependson', validateDependsOn);
//  const validation = new Validator({dependant:"dependson"});
  // Use vee-validate, and assign before component is loaded
//  Vue.use(VeeValidate, config.validatorConfig); // validation plugin
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

/* harmony default export */ __webpack_exports__["a"] = ({
  mixins: [shared.default.mixin],
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

/***/ })
],[6]);