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
var el = document.createElement("div");
el.setAttribute("id", "mount");
document.body.appendChild(el);
describe('Search component should mount', ()=>{
  var vm = new Vue({
    template:"<div><h1>Testing...</h1><search></search></div>",
    components: {'search':Search}
  }).$mount("#mount");
  it('Should mount without issue', ()=>{
    expect(typeof vm.$children[0].getTelescopes).to.equal('function');
  });

  it('Should have an $el element', ()=>{
    assert.property(vm, '$el');
  });


  // test codeView, resolvingObject, datepicker, submitForm, submitQuery, clear

});
