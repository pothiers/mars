###
Author: Peter Peterson
Date: 2017-06-09
Description: Serves functionality for displaying and filtering result sets
Original file: results.coffee
###

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
  template: "<tr><table-cell v-for='vis in cols' v-bind:data='row[vis.mapping]' :key='row.id'></table-cell></tr>"

Vue.component "table-body",
   props: ['data', 'visibleCols']
   template: "<tbody><table-row v-for='(item,idx) in data' v-bind:cols='visibleCols' v-bind:row='item' :key='item.id'></table-row></tbody>"


###
   App - Results Class
###
class Results
  constructor: ()->
    console.log "Results set created"
    @table = new Vue
      el: "#query-results"
      data:
        # This should be set based on some session/local storage set
        visibleColumns : JSON.parse(JSON.stringify(@defaultColumns))
        visible: false
        results: [] # loaded on page for development
      methods:
        displayForm: ()->
          window.results.table.visible = false
          window.searchForm.form.visible = true

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

results = new Results()
