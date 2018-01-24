
import Vue from 'vue';
import ModalComponent from '../../vue/ModalComponent.vue';
import MainComponent from '../../vue/Main.vue';


function mountModalComponent(component){
  var vm = new Vue(component).$mount();
  return vm;
}



function createBus(){
  window.bus = new Vue();
}

describe('MainComponent', ()=>{
  it("Should render correctly", ()=>{
    const constructor = Vue.extend( MainComponent );
    const vm = new constructor().$mount();
    expect(vm.$el.querySelector('#stuff h1').textContent).to.equal('hello');
  });
});

describe('ModalComponent', ()=>{
  it('Should render', ()=>{
    var vm = new Vue({
      template: '<div><test></test></div>',
      components: {
        'test': ModalComponent
      }
    }).$mount();
    expect(vm.$el.querySelectorAll('#modal-component').length).to.equal(1);
  });
});

describe('ModalComponent Data', ()=>{
  createBus();
  var vm = mountModalComponent(ModalComponent);
  window.bus.$emit('open-modal', {title:'MyTitle', body:'BodyContent'});

  it('Should have a title', ()=>{
    expect(vm.modalTitle).to.equal('MyTitle');
  });
  it('Should have a body', ()=>{
    expect(vm.modalBody).to.equal('BodyContent');
  });
});
