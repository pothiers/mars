webpackJsonp([2],{

/***/ 21:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__vue_Staging_vue__ = __webpack_require__(22);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__vue_Staging_vue___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0__vue_Staging_vue__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_vue__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_vue___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_vue__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__styles_search_scss__ = __webpack_require__(5);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__styles_search_scss___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_2__styles_search_scss__);
var App;







App = (function() {
  function App() {
    new __WEBPACK_IMPORTED_MODULE_1_vue___default.a({
      el: "#content",
      template: "<component compdata='componentData' v-bind:is='currentView' v-on:displayform='switchComponent' />",
      methods: {
        switchComponent: function(data) {
          return this.currentView = data[0];
        }
      },
      data: {
        currentView: "staging",
        componentData: []
      },
      components: {
        staging: __WEBPACK_IMPORTED_MODULE_0__vue_Staging_vue___default.a
      }
    });
  }

  return App;

})();

new App();


/***/ }),

/***/ 22:
/***/ (function(module, exports, __webpack_require__) {

var disposed = false
var Component = __webpack_require__(1)(
  /* script */
  __webpack_require__(23),
  /* template */
  __webpack_require__(25),
  /* styles */
  null,
  /* scopeId */
  null,
  /* moduleIdentifier (server only) */
  null
)
Component.options.__file = "/Users/peter/Workspace/NOAO/dev-docker-mars/mars/marssite/natica/vue/Staging.vue"
if (Component.esModule && Object.keys(Component.esModule).some(function (key) {return key !== "default" && key.substr(0, 2) !== "__"})) {console.error("named exports are not supported in *.vue files.")}
if (Component.options.functional) {console.error("[vue-loader] Staging.vue: functional components are not supported with templates, they should use render functions.")}

/* hot reload */
if (false) {(function () {
  var hotAPI = require("vue-hot-reload-api")
  hotAPI.install(require("vue"), false)
  if (!hotAPI.compatible) return
  module.hot.accept()
  if (!module.hot.data) {
    hotAPI.createRecord("data-v-f63f9152", Component.options)
  } else {
    hotAPI.reload("data-v-f63f9152", Component.options)
  }
  module.hot.dispose(function (data) {
    disposed = true
  })
})()}

module.exports = Component.exports


/***/ }),

/***/ 23:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__js_staging_coffee__ = __webpack_require__(24);
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//



/* harmony default export */ __webpack_exports__["default"] = (__WEBPACK_IMPORTED_MODULE_0__js_staging_coffee__["a" /* default */]);

/***/ }),

/***/ 24:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_vue__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_vue___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_vue__);

/*
Author: Peter Peterson
Date: 2017-07-24
Description: Code for interactions with the staging page
Original file: staging.coffee
 */
var generateResultsSet, stagingComponent;



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
  created: function() {
    window.staging = this;
    return console.log("Staging created");
  },
  mounted: function() {
    console.log("Component mounted");
    return this.results = generateResultsSet();
  },
  methods: {
    toggleSelected: function() {
      return console.dir(arguments);
    }
  },
  data: function() {
    return {
      results: [],
      selected: []
    };
  }
};

/* harmony default export */ __webpack_exports__["a"] = (stagingComponent);


/***/ }),

/***/ 25:
/***/ (function(module, exports, __webpack_require__) {

module.exports={render:function (){var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;
  return _c('div', {
    staticClass: "container"
  }, [_vm._m(0), _vm._v(" "), _c('div', {
    staticClass: "row"
  }, [_c('div', {
    staticClass: "col-xs-12"
  }, [_c('table', [_vm._m(1), _vm._v(" "), _c('tbody', _vm._l((_vm.results), function(result) {
    return _c('tr', {
      on: {
        "click": function($event) {
          _vm.toggleSelected(result)
        }
      }
    }, [_c('td', [_c('input', {
      attrs: {
        "type": "checkbox",
        "name": "selected[]",
        "value": ""
      },
      domProps: {
        "value": result.filename
      }
    })]), _vm._v(" "), _c('td', [_vm._v(_vm._s(result.filename))])])
  })), _vm._v(" "), _c('tfoot')], 1)])])])
},staticRenderFns: [function (){var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;
  return _c('div', {
    staticClass: "row"
  }, [_c('div', {
    staticClass: "col-xs-12"
  }, [_c('h2', [_vm._v("Staging Area")])])])
},function (){var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;
  return _c('thead', [_c('tr', [_c('th', [_vm._v("Selected")]), _vm._v(" "), _c('th', [_vm._v("File name")])])])
}]}
module.exports.render._withStripped = true
if (false) {
  module.hot.accept()
  if (module.hot.data) {
     require("vue-hot-reload-api").rerender("data-v-f63f9152", module.exports)
  }
}

/***/ })

},[21]);