webpackJsonp([2],{

/***/ 22:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__vue_Staging_vue__ = __webpack_require__(23);
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

/***/ 23:
/***/ (function(module, exports, __webpack_require__) {

var disposed = false
var Component = __webpack_require__(1)(
  /* script */
  __webpack_require__(24),
  /* template */
  __webpack_require__(26),
  /* styles */
  null,
  /* scopeId */
  null,
  /* moduleIdentifier (server only) */
  null
)
Component.options.__file = "/home/peter/Workspace/web/mars/marssite/portal/vue/Staging.vue"
if (Component.esModule && Object.keys(Component.esModule).some(function (key) {return key !== "default" && key.substr(0, 2) !== "__"})) {console.error("named exports are not supported in *.vue files.")}
if (Component.options.functional) {console.error("[vue-loader] Staging.vue: functional components are not supported with templates, they should use render functions.")}

/* hot reload */
if (false) {(function () {
  var hotAPI = require("vue-hot-reload-api")
  hotAPI.install(require("vue"), false)
  if (!hotAPI.compatible) return
  module.hot.accept()
  if (!module.hot.data) {
    hotAPI.createRecord("data-v-378065fd", Component.options)
  } else {
    hotAPI.reload("data-v-378065fd", Component.options)
  }
  module.hot.dispose(function (data) {
    disposed = true
  })
})()}

module.exports = Component.exports


/***/ }),

/***/ 24:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__js_staging_coffee__ = __webpack_require__(25);
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
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

/***/ 25:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__mixins_coffee__ = __webpack_require__(2);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_vue__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_vue___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_vue__);

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
  mixins: [__WEBPACK_IMPORTED_MODULE_0__mixins_coffee__["a" /* default */].mixin],
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
    downloadSinglefile: function() {
      debugger;
    },
    downloadSelected: function() {
      var query;
      console.log("downloading selected");
      query = {
        "files": this.selected
      };
      return new Ajax({
        url: "/portal/stagefiles",
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

/* harmony default export */ __webpack_exports__["a"] = (stagingComponent);


/***/ }),

/***/ 26:
/***/ (function(module, exports, __webpack_require__) {

module.exports={render:function(){},staticRenderFns:[]}
if (false) {
  module.hot.accept()
  if (module.hot.data) {
     require("vue-hot-reload-api").rerender("data-v-378065fd", module.exports)
  }
}

/***/ })

},[22]);