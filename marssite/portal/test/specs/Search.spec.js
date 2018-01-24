import Vue from 'vue';
import Search from '../../vue/Search.vue';

var moment = require("moment");
var _ = require("lodash");

// jquery is required as it's used for the calendar widget
window.$ = window.jQuery = require('jquery');
require('jquery-ui');

window.moment = moment;
window._ = _;

require('../../../theme/js/main.js');

describe('Search component should mount', ()=>{
  it('Should mount without issue', ()=>{
    var vm = new Vue(Search).$mount();
    expect(typeof vm.getTelescopes).to.equal('function');
  }); 
});
