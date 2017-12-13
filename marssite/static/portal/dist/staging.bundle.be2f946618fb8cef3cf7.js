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
/**
 * @fileOverview
 * @name staging.app.js
 * @author
 * @license
 */






class App {
  constructor(){
    new __WEBPACK_IMPORTED_MODULE_1_vue___default.a({
      el: "#content",
      template: "<component compdata='componentData' v-bind:is='currentView' v-on:displayform='switchComponent' />",
      methods: {
        switchComponent(data){
          this.currentView = data[0];
          return "nothing";
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
}
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
Component.options.__file = "/Users/ppeterson/Workspace/portal/mars/marssite/portal/vue/Staging.vue"
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
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__js_staging_js__ = __webpack_require__(25);
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//


/* harmony default export */ __webpack_exports__["default"] = (__WEBPACK_IMPORTED_MODULE_0__js_staging_js__["a" /* default */]);

/***/ }),

/***/ 25:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__mixins_js__ = __webpack_require__(2);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_vue__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_vue___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_vue__);
/*
Author: Peter Peterson
Date: 2017-07-24
Description: Code for interactions with the staging page
*/




const generateResultsSet = function(){
  const results = [];
  for (let x = 1; x <= 100; x++) {
    results.push({count:x, filename: Math.random().toString(36).substring(7)});
  }

  return results;
};

const stagingComponent = {
  mixins:[__WEBPACK_IMPORTED_MODULE_0__mixins_js__["a" /* default */].mixin],
  data(){
      return {
        stagingAllFiles: false,
        loading: false,
        selectAll: false,
        results: [],
        selected: [],
        totalfiles: 0,
        missingfiles:0
      };
    },
  created(){
    window.staging = this;
    console.log("Staging created");
  },
  mounted(){
    console.log("Component mounted");
    window.base.bindEvents();
    if (localStorage.getItem("stage") === "selectedFiles") {
      // Files array is generated by the staging django template
      const files = JSON.parse(localStorage.getItem("selectedFiles"));
      Array.from(files).map((file) =>
        this.results.push({'selected':false, 'file':file}));
    } else {
      // show a loading screen
      this.stagingAllFiles = true;
      this.loading = true;
      const querydata = localStorage.getItem("search");


      new Ajax({
        url: "/portal/stageall/",
        method: "post",
        accept: "json",
        data: JSON.parse(querydata),
        success: data=> {
          this.totalfiles = data.total_files;
          this.missingfiles = data.missing_files;
          this.loading = false;
        },
        fail(statusMsg, status, xhr){
          console.log("ajax failed");
          console.info("TODO: Add a fail message and option to try again/or stage less files");
        }
      });
    }
  },


      // call api to start staging process...

  methods: {
    toggleAll(){
      this.selectAll = !this.selectAll;
      if (this.selectAll) {
        return (() => {
          const result = [];
          for (let file of Array.from(this.results)) {
            file.selected = true;
            result.push(this.selected.push(file));
          }
          return result;
        })();
      } else {
        for (let file of Array.from(this.results)) {
          file.selected = false;
        }
        return this.selected = [];
      }
    },

    downloadSingleFile(file, event){
      // identify which file...
      event.stopPropagation();
      window.open(`/portal/downloadsinglefile/?f=${file.reference}`, "_blank");
      return false;
    }, // prevent bubbling up

    _confirmDownloadSelected(){
      const { selected } = this; // scope resolution
      const query = {"files":selected.slice(0, 10)};
      const form = document.createElement("form");
      form.setAttribute("method", "post");
      //form.setAttribute("target", "_blank")
      form.setAttribute("action", "/portal/downloadselected");
      const data = document.createElement("input");
      data.setAttribute("type", "hidden");
      data.setAttribute("name", "selected");
      data.setAttribute("value", JSON.stringify(selected.slice(0,10)));
      form.appendChild(data);
      document.querySelector("body").appendChild(form);
      return form.submit();
      /*
      new Ajax
        url: "/portal/downloadselected"
        method: "post"
        accept: "json"
        data: query
        success: (data)=>
          console.log "Got this from the server"
          console.log data
        fail: (statusmsg, status, xhr)->
          console.log "request failed"
      */
    },


    downloadSelected(){
      console.log("downloading selected");
      const self = this;
      if (this.selected.length > 10) {
        BootstrapDialog.confirm("Only ten files can be downloaded at one time. See download instructions for downloading more at one time",
        function(goAhead){
           if (goAhead) {
            self._confirmDownloadSelected();
          }
        });
      } else {
        self._confirmDownloadSelected();
      }
    },


    toggleSelected(item){
      item.selected = !item.selected;
      if (item.selected) {
        this.selected.push(item);
      } else {
        const indx = _.indexOf(this.selected, item);
        this.selected.splice(indx, 1);
      }
    }
  }

};


/* harmony default export */ __webpack_exports__["a"] = (stagingComponent);
//module.exports(stagingComponent);


/***/ }),

/***/ 26:
/***/ (function(module, exports, __webpack_require__) {

module.exports={render:function (){var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;
  return _c('div', [_vm._m(0), _vm._v(" "), (_vm.stagingAllFiles) ? _c('div', {
    staticClass: "container"
  }, [(_vm.loading) ? _c('div', {
    staticClass: "row"
  }, [_vm._m(1)]) : _vm._e(), _vm._v(" "), (!_vm.loading) ? _c('div', {
    staticClass: "row"
  }, [_c('div', {
    staticClass: "col-xs-12"
  }, [_c('h2', [_vm._v("Done Staging Files")]), _vm._v(" "), _c('h5', [_vm._v("Please see downloading instructions for accessing your files.")]), _vm._v(" "), _c('div', {
    staticClass: " col-xs-12 col-md-6 "
  }, [_c('div', {
    staticClass: "panel panel-primary "
  }, [_vm._m(2), _vm._v(" "), _c('div', {
    staticClass: "panel-body"
  }, [_c('ul', {
    staticClass: "list-unstyled"
  }, [_c('li', [_vm._v("Total files staged: "), _c('span', [_vm._v(_vm._s(_vm.totalfiles))])]), _vm._v(" "), _c('li', [_vm._v("Missing files: "), _c('span', [_vm._v(_vm._s(_vm.missingfiles.length))])]), _vm._v(" "), _vm._l((_vm.missingfiles), function(file) {
    return (_vm.missingfiles.length > 0) ? _c('ol', [_vm._v("\n                                    " + _vm._s(file) + "\n                                ")]) : _vm._e()
  })], 2)])])])])]) : _vm._e()]) : _vm._e(), _vm._v(" "), (!_vm.stagingAllFiles) ? _c('div', {
    staticClass: "container"
  }, [_c('div', {
    staticClass: "row"
  }, [_c('div', {
    staticClass: "col-xs-12"
  }, [_c('h2', [_vm._v("Staging Area\n                    | "), _c('small', [_c('strong', [_vm._v(_vm._s(_vm.results.length))]), _vm._v(" files staged")])])])]), _vm._v(" "), _c('div', {
    staticClass: "row"
  }, [_c('div', {
    staticClass: "col-xs-6"
  }, [_c('label', [_c('input', {
    attrs: {
      "type": "checkbox",
      "name": "",
      "value": ""
    },
    domProps: {
      "checked": _vm.selectAll
    },
    on: {
      "change": _vm.toggleAll
    }
  }), _vm._v("\n                    Select all\n                ")])]), _vm._v(" "), _c('div', {
    staticClass: "text-right col-xs-6"
  }, [_c('button', {
    staticClass: "btn btn-default",
    attrs: {
      "disabled": _vm.selected.length == 0
    },
    on: {
      "click": _vm.downloadSelected
    }
  }, [_vm._v("Download Selected")]), _vm._v(" "), _c('p', {
    staticClass: "help-block hint"
  }, [_vm._v("\n                  Up to 10 files may be downloaded at a time\n              ")])])]), _vm._v(" "), _c('div', {
    staticClass: "row"
  }, [_c('div', {
    staticClass: "col-xs-12"
  }, [_c('table', [_vm._m(3), _vm._v(" "), _c('tbody', _vm._l((_vm.results), function(result) {
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
        "checked": result.selected,
        "value": result.file.reference
      }
    })]), _vm._v(" "), _c('td', [_vm._v(_vm._s(result.file.reference) + " "), _c('a', {
      attrs: {
        "title": "download single file",
        "href": "#",
        "href": '#download_' + result.file.reference
      },
      on: {
        "click": function($event) {
          _vm.downloadSingleFile(result.file, $event)
        }
      }
    }, [_c('span', {
      staticClass: "fa fa-download"
    })])]), _vm._v(" "), _c('td', [_vm._v(_vm._s(result.file.filesize / 1000) + " KB")]), _vm._v(" "), _c('td', [_vm._v(_vm._s(result.file.md5sum))])])
  })), _vm._v(" "), _c('tfoot')])])])]) : _vm._e()])
},staticRenderFns: [function (){var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;
  return _c('div', {
    staticClass: "container"
  }, [_c('div', {
    staticClass: "row"
  }, [_c('div', {
    staticClass: "col-xs-12"
  }, [_c('div', {
    staticClass: "panel collapsible panel-default"
  }, [_c('div', {
    staticClass: "panel-heading section-heading"
  }, [_vm._v("\n                        Downloading instructions\n                        "), _c('div', {
    staticClass: "section-toggle"
  }, [_c('span', {
    staticClass: "icon open"
  })])]), _vm._v(" "), _c('div', {
    staticClass: "panel-body section-content"
  }, [_c('div', {
    staticClass: "row"
  }, [_c('div', {
    staticClass: "col-md-6"
  }, [_c('h4', [_vm._v("Command line LFTP")]), _vm._v(" "), _c('strong', [_vm._v("Unix/Linux/Mac:")]), _vm._v(" fast parallel transfer using lftp\n\n                                "), _c('ol', {
    staticClass: "default"
  }, [_c('li', [_vm._v("\n                                        If necessary, install lftp [available from most standard software repositories]\n                                    ")]), _vm._v(" "), _c('li', [_vm._v("\n                                        Download this lftp configuration file and save it as ~/.lftprc\n                                    ")])]), _vm._v(" "), _c('strong', [_vm._v("\n                                    For authenticated users retrieving proprietary data:\n                                ")]), _vm._v(" "), _c('ol', {
    staticClass: "default",
    attrs: {
      "start": "3"
    }
  }, [_c('li', [_vm._v("\n                                        lftp -u USERNAME,PASSWORD archive.noao.edu   [see Retrieval information above]\n                                    ")]), _vm._v(" "), _c('li', [_vm._v("\n                                        mirror -L .   [include the dot (\" . \")]\n                                    ")])]), _vm._v(" "), _c('strong', [_vm._v(" For anonymous (public search) users:")]), _vm._v(" "), _c('ol', {
    staticClass: "default",
    attrs: {
      "start": "3"
    }
  }, [_c('li', [_vm._v("\n                                        lftp -u anonymous,lftp archive.noao.edu\n                                    ")]), _vm._v(" "), _c('li', [_vm._v("\n                                        cd user_NNNN   [see Retrieval information above]\n                                    ")]), _vm._v(" "), _c('li', [_vm._v("\n                                        mirror -L .   [include the dot (\" . \")]\n                                    ")])])]), _vm._v(" "), _c('div', {
    staticClass: "col-md-6"
  }, [_c('h4', [_vm._v("Commandline FTP")]), _vm._v(" "), _c('strong', [_vm._v("Important tips for standard transfer with ftp:")]), _vm._v(" "), _c('ul', {
    staticClass: "default"
  }, [_c('li', [_vm._v("\n                                        You must use ftp instead of sftp\n                                    ")]), _vm._v(" "), _c('li', [_vm._v("\n                                        Be sure to select binary file transfer\n                                    ")])]), _vm._v(" "), _c('h4', [_vm._v("Other transfer tools (e.g. for Windows, Mac etc)")]), _vm._v(" "), _c('ul', {
    staticClass: "default"
  }, [_c('li', [_vm._v("Unix/Linux: "), _c('strong', [_vm._v("gftp")])]), _vm._v(" "), _c('li', [_vm._v("Mac: "), _c('strong', [_vm._v("fetch")])]), _vm._v(" "), _c('li', [_vm._v("Windows: "), _c('strong', [_vm._v("wsftp")])]), _vm._v(" "), _c('li', [_vm._v("Windows & Mac: "), _c('strong', [_vm._v("Cyber Duck FTP client")])])])])])])])])])])
},function (){var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;
  return _c('div', {
    staticClass: "col-xs-12 text-center"
  }, [_c('h2', [_vm._v("Staging files ..."), _c('span', {
    staticClass: "fa fa-spinner fa-spin fa-fw"
  })]), _vm._v(" "), _c('div', {
    staticClass: "spinner"
  })])
},function (){var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;
  return _c('div', {
    staticClass: "panel-heading"
  }, [_c('div', {
    staticClass: "panel-title"
  }, [_vm._v("File statistics")])])
},function (){var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;
  return _c('thead', [_c('tr', [_c('th', [_vm._v("Selected")]), _vm._v(" "), _c('th', [_vm._v("File name")]), _vm._v(" "), _c('th', [_vm._v("File size")]), _vm._v(" "), _c('td', [_vm._v("MD5 sum")])])])
}]}
module.exports.render._withStripped = true
if (false) {
  module.hot.accept()
  if (module.hot.data) {
     require("vue-hot-reload-api").rerender("data-v-378065fd", module.exports)
  }
}

/***/ })

},[22]);