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
  created: ()->
    console.log 'created'
    bus.$on "toggleSelected", (onoff)=>
      console.log "Gettin' toggled", onoff
      this.isSelected = onoff
  methods:
    selectRow: ()->
      this.isSelected = !this.isSelected
      console.log "Row selected"
      bus.$emit("rowselected", {stuff:'hi', thing:this.row})
      this.$emit("rowselected", this)

Vue.component "table-body",
   props: ['data', 'visibleCols']
   template: "<tbody ><table-row v-for='(item,idx) in data' v-bind:cols='visibleCols' v-bind:row='item' :key='item.id'></table-row></tbody>"
   methods:
     iheardthat: ()->
       console.log "I heard that"
       console.log arguments

###
   App - Results
###
config = Shared.config
window.bus = new Vue()
export default {
  props: ['componentData']
  mixins: [Shared.mixin]
  data: ()->
    return {
      # This should be set based on some session/local storage set
      visibleColumns : []
      allColumns: config.allColumns
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
    toggleColumn: (column)->

      if column.checked
        for col, n in @visibleColumns
          if _.isEqual(col, column)
            @visibleColumns.splice(n,1)
      else
        found = false
        for col,n in @visibleColumns
          if column.num < col.num
            first = @visibleColumns.slice(0,n)
            last = @visibleColumns.slice(n)
            @visibleColumns = first.concat(column, last)
            found = true
            break
        if found isnt true
          # if we got here, then column is indexed greater than what is visible, just append
          @visibleColumns.push(column)
      column.checked = !column.checked

    toggleResults: ()->
      @toggle = !@toggle
      console.log "toggle"
      bus.$emit("toggleSelected", @toggle)
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
  created:()->
    for col in @allColumns
      if col.checked
        @visibleColumns.push(col)
  mounted:()->
    window.base.bindEvents()
    window.results = @

    # listen to bus selected row notifications
    bus.$on "rowselected", (data)->
      console.dir data
      console.log "bus called"

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
