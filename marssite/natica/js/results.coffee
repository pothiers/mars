###
Author: Peter Peterson
Date: 2017-06-09
Description: Serves functionality for displaying and filtering result sets
Original file: results.coffee
###

import Vue from "vue"

###
  Helper functions
###
Number.prototype.pad = (size, char='0')->
  s = String(this)
  while (s.length < (size || 2))
    s = "0" + s
  return s

###
   Vue components
###
Vue.component "table-header",
  props: ['name']
  template: "<th>{{ name }}</th>"

Vue.component "table-cell",
  props: ['data']
  template: "<td v-if='data'>{{ format }}</td><td class='empty' v-else></td>"
  computed: 
      format: ()->
        if @data is null
          return @data
        if @data.toString().match(/\d{4}-\d{2}-[0-9T:]+/) isnt null
          try
            d = new Date(@data)
            dateStr = "#{d.getFullYear()}-#{(d.getMonth()+1).pad()}-#{(d.getDate()).pad()}"
            return dateStr
          catch
            return @data
        else
          return @data

Vue.component "table-row",
  props: ['row', 'cols']
  template: "<tr v-on:click='selectRow' v-bind:class='{selected:isSelected}'><td class='select-row'><input type='checkbox' name='' v-bind:checked='isSelected' v-bind:name='row.reference'></td><table-cell v-for='vis in cols' v-bind:data='row[vis.mapping]' :key='row.id'></table-cell></tr>"
  data: ()->
    return
      isSelected: false
      
  methods:
    selectRow: ()->
      this.isSelected = !this.isSelected
      console.log "Row selected"

Vue.component "table-body",
   props: ['data', 'visibleCols']
   template: "<tbody><table-row v-for='(item,idx) in data' v-bind:cols='visibleCols' v-bind:row='item' :key='item.id'></table-row></tbody>"


###
   App - Results
###
config = {
 defaultColumns:[
    {"mapping": "dec", "name" : "Dec"},
    {"mapping": "depth", "name": "Depth"},
    {"mapping": "exposure", "name": "Exposure"},
    {"mapping": "filename", "name": "Filename"},
    {"mapping": "filesize", "name" : "File size"},
    {"mapping": "filter", "name": "Filter"},
    {"mapping": "image_type", "name": "Image Type"},
    {"mapping": "instrument", "name": "Instrument"},
    {"mapping": "md5sum", "name": "MD5 sum"},
    {"mapping": "obs_date", "name": "Observed date"},
    {"mapping": "original_filename", "name":"Original filename"},
    {"mapping": "pi", "name": "Principle Investigator"},
    {"mapping": "product", "name":"Product"},
    {"mapping": "prop_id", "name": "Program Number"},
    {"mapping": "ra", "name":"RA"},
    {"mapping": "reference", "name":"Reference"},
    {"mapping": "release_date", "name":"Release Date"},
    {"mapping": "seeing", "name":"Seeing"},
    {"mapping": "telescope", "name":"Telescope"},
    {"mapping": "survey_id", "name":"Survey Id"}
  ]
}
# TODO: Handle 0 results
export default {
  props: ['componentData']
  data: ()->
    return {
      # This should be set based on some session/local storage set
      visibleColumns : JSON.parse(JSON.stringify(config.defaultColumns))
      visible: false
      pageNum: 1
      isLoading: false
      results: []
    }
  methods:
    displayForm: ()->
      window.location.hash = ""
      this.$emit("displayform", ["search", JSON.parse(localStorage.getItem('search'))] )
    pageNext: ()->
      @pageTo(@pageNum+1)
    pageBack: ()->
      @pageTo(@pageNum-1)
    pageTo: (page)->
      # TODO: Use vue routes to make urls look right
      # resend post data with new page num
      this.$data.pageNum = page
      localStorage.setItem('currentPage', page)
      this.$emit("pageto", page)
      this.$data.isLoading = true
      self = @
      this.$emit("submitform", [null, "paging", ()->
        self.$data.isLoading = false
      ])
  mounted:()->
    window.base.bindEvents()
    #
    
    if window.location.hash is "#query"
      @results = JSON.parse(localStorage.getItem('results'))
      @visible = true
      @pageNum = parseInt(localStorage.getItem("currentPage"))
      #window.searchForm.form.search = JSON.parse(localStorage.getItem('search'))


  
}
