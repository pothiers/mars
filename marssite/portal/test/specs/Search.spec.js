import Vue from 'vue';
import Search from '../../vue/Search.vue';

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
  it('Should have a children element', ()=>{
    assert.property(vm, '$children');

  });
  it('Should have a list of the telescopes', ()=>{
    //debugger
    expect(vm.telescopes.length).to.be.above(1);
  });
});
