###
Author: Peter Peterson
Date: 2017-06-09
Description: Serves functionality for displaying and filtering result sets
Original file: results.coffee
###

import Vue from "vue"
import Shared from "./mixins.coffee"

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

  methods:
    selectRow: ()->
      this.isSelected = !this.isSelected
      console.log "Row selected"
      this.$emit("rowselected", this)

Vue.component "table-body",
   props: ['data', 'visibleCols']
   template: "<tbody v-on:rowselected='iheardthat'><table-row v-for='(item,idx) in data' v-bind:cols='visibleCols' v-bind:row='item' :key='item.id'></table-row></tbody>"
   methods:
     iheardthat: ()->
       console.log "I heard that"
       console.log arguments

###
   App - Results
###
config = Shared.config
export default {
  props: ['componentData']
  mixins: [Shared.mixin]
  data: ()->
    return {
      # This should be set based on some session/local storage set
      visibleColumns : JSON.parse(JSON.stringify(config.defaultColumns))
      visible: false
      pageNum: 1
      isLoading: false
      recordsFrom: 1
      recordsTo: 100
      results: []
      selected: []
      searchObj: JSON.parse(localStorage.getItem('search'))
      totalItems: 0
      toggle: false
      error: ""
    }
  methods:
    sayWhat: ()->
      console.log "what"
      console.dir arguments
    toggleResults: ()->
      @toggle = !@toggle
      console.log "toggle"
    displayForm: ()->
      window.location.hash = "#search_again"
      this.$emit("displayform", ["search", JSON.parse(localStorage.getItem('search'))] )
    handleError: (e)->
      console.log "There was an error", e
    pageNext: ()->
      @pageTo(@pageNum+1)
    pageBack: ()->
      @pageTo(@pageNum-1)
    pageTo: (page)->
      # TODO: Use vue routes to make urls look right
      # resend post data with new page num
      @pageNum = page
      localStorage.setItem('currentPage', page)
      this.$emit("pageto", page)
      @isLoading = true
      self = @
      @submitForm(null, "paging",  (data)->
        self.isLoading = false
        self.results = data
        self.recordsFrom = data.meta.to_here_count-data.meta.page_result_count+1
        self.recordsTo = data.meta.to_here_count
      )
  mounted:()->
    window.base.bindEvents()
    #

    if window.location.hash is "#query"
      try
        @results = JSON.parse(localStorage.getItem('results')) || []
        @totalItems = @results?.meta.total_count
        @visible = true
        @pageNum = parseInt(localStorage.getItem("currentPage"))
      catch e
        @results = []
        @totalItems = 0
        @visible = true
        @error = "There was an error parsing results from server"
        @handleError(e)
      #window.searchForm.form.search = JSON.parse(localStorage.getItem('search'))



}
