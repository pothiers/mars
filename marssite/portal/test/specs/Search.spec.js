import Vue from 'vue';
import Search from '../../vue/Search.vue';

Vue.config.productionTip = false;

var moment = require("moment");
var _ = require("lodash");

// jquery is required as it's used for the calendar widget
window.$ = window.jQuery = require('jquery');
require('jquery-ui');

window.moment = moment;
window._ = _;

// this is necessary to have ajax calls go to the right place
window.testing = true;

require('../../../theme/js/main.js');

describe('Search component should mount', ()=>{
  var vm = new Vue(Search).$mount();
  it('Should mount without issue', ()=>{
    expect(typeof vm.getTelescopes).to.equal('function');
  });

  it('Should have an $el element', ()=>{
    assert.property(vm, '$el');
  });

  it('Should have a list of the telescopes', ()=>{
    var noCache = true;
    vm.getTelescopes(noCache).then((data)=>{
      console.log("got this from the server", data);
      expect(vm.telescopes.length).to.be.above(1);
    }).catch(err =>{
      console.error("Didn't get telescopes");
      console.log(err);
      expect(err.status).to.be(200);
    });
  });

  it('Should be able to resolve an object', ()=>{
    // set the search in the field and simulate button click
    vm.objectName = "orion";
    var e = new MouseEvent("click");
    vm.resolveObject(e).then(data => {
      console.log("got some data", data);
    }).catch(err =>{
      expect(err.status).to.be(200);
    });

  });
  // test codeView, resolvingObject, datepicker, submitForm, submitQuery, clear

});
