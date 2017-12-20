var Vue = require("vue");

/*
   Vue components
   For rendering results table
*/
Vue.component("table-header", {
  props: ['name'],
  template: "<span>{{ name }}</span>"
}
);

Vue.component("table-cell", {
  props: ['data', 'field'],
  template: "<td v-if='data' v-bind:rel='field'>{{ format }}</td><td class='empty' v-else></td>",
  computed: {
      format(){
        if (this.data === null) {
          return this.data;
        }
        if ((this.field === 'obs_date') || (this.field === 'release_date')) {
          try {
            const d = moment(this.data);
            const dateStr = d.format("YYYY-MM-DD");
            return dateStr;
          } catch (error) {
            return this.data;
          }
        } else {
          return this.data;
        }
      }
    }
}
);

Vue.component("table-row", {
  props: ['row', 'cols'],
  template: "<tr v-on:click='selectRow' v-bind:class='{selected:isSelected}'><td class='select-row'><input type='checkbox' name='' v-bind:checked='isSelected' v-bind:name='row.reference'></td><table-cell v-for='vis in cols' v-bind:data='row[vis.mapping]' v-bind:field='vis.mapping' :key='row.id'></table-cell></tr>",
  data(){
    return {
      isSelected: false
    };
  },
  created(){
    bus.$on("selectrow", _row=> {
      if (_row.reference === this.row.reference) {
        this.isSelected = true;
      }
    });
    return bus.$on("toggleselected", onoff=> {
      this.isSelected = onoff;
    });
  },
  methods: {
    selectRow(event){
      this.isSelected = !this.isSelected;
      bus.$emit("rowselected", {isSelected:this.isSelected, row:this.row, vueobject:this, event});
    }
  }
}
);

Vue.component("table-body", {
   props: ['data', 'visibleCols'],
   template: "<tbody ><table-row v-for='(item,idx) in data' v-bind:cols='visibleCols' v-bind:row='item' :key='item.id'></table-row></tbody>",
   methods: {
   }
 }
);
