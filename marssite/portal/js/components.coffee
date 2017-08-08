import Vue from "vue"
###
   Vue components
   For rendering results table
###
Vue.component "table-header",
  props: ['name']
  template: "<span>{{ name }}</span>"

Vue.component "table-cell",
  props: ['data', 'field']
  template: "<td v-if='data' v-bind:rel='field'>{{ format }}</td><td class='empty' v-else></td>"
  computed:
      format: ()->
        if @data is null
          return @data
        if @field is 'obs_date' or @field is 'release_date'
          try
            d = moment(@data)
            dateStr = d.format("YYYY-MM-DD")
            return dateStr
          catch
            return @data
        else
          return @data

Vue.component "table-row",
  props: ['row', 'cols']
  template: "<tr v-on:click='selectRow' v-bind:class='{selected:isSelected}'><td class='select-row'><input type='checkbox' name='' v-bind:checked='isSelected' v-bind:name='row.reference'></td><table-cell v-for='vis in cols' v-bind:data='row[vis.mapping]' v-bind:field='vis.mapping' :key='row.id'></table-cell></tr>"
  data: ()->
    return
      isSelected: false
  created: ()->
    bus.$on "toggleselected", (onoff)=>
      this.isSelected = onoff
  methods:
    selectRow: ()->
      this.isSelected = !this.isSelected
      bus.$emit("rowselected", {isSelected:this.isSelected, row:this.row, vueobject:this})

Vue.component "table-body",
   props: ['data', 'visibleCols']
   template: "<tbody ><table-row v-for='(item,idx) in data' v-bind:cols='visibleCols' v-bind:row='item' :key='item.id'></table-row></tbody>"
   methods:
     iheardthat: ()->
       console.log "I heard that"
       console.log arguments
