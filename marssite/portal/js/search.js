/*
Author: Peter Peterson
Date: 2017-06-09
Description: Serves functionality for submitting and displaying archive query forms/results
*/

//import Vue from 'vue';
import Vue from "vue";
import VeeValidate, {Validator} from "vee-validate";
import Shared from "./mixins.js";

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

var config = Shared.config;

(function(){
  // This gets called after the component has been mounted
  window.addEventListener('searchLoaded', function(e){
    console.log("Search loaded", e);
    // re-bind since the template will render after the page is loaded.
    return window.base.bindEvents();
  });
  Validator.extend('dependson', validateDependsOn);
  const validation = new Validator({dependant:"dependson"});
  // Use vee-validate, and assign before component is loaded
  Vue.use(VeeValidate, config.validatorConfig); // validation plugin
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

export default {
  mixins: [Shared.mixin],
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

};
