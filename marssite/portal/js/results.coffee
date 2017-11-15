###
Author: Peter Peterson
Date: 2017-06-09
Description: Serves functionality for displaying and filtering result sets
Original file: results.coffee
###

import Vue from "vue"
import Shared from "./mixins.coffee"
import "./components.coffee"

###
  Helper functions
###
Number.prototype.pad = (size, char='0')->
  s = String(this)
  while (s.length < (size || 2))
    s = "0" + s
  return s

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
      filtersVisible: false
      allColumns: config.allColumns
      stageAllConfirm: false
      stageButtonText: "Stage ALL results"
      visible: false
      pageNum: 1
      isLoading: false
      recordsFrom: 1
      recordsTo: 100
      results: []
      selected: []
      lastSelected: null
      searchObj: JSON.parse(localStorage.getItem('search'))
      totalItems: 0
      toggle: false
      error: ""
    }
  methods:
    toggleFilters: ()->
      @filtersVisible = !@filtersVisible
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

    stageSelected: ()->
      localStorage.setItem("stage", "selectedFiles")
      localStorage.setItem("selectedFiles", JSON.stringify(@selected))
      # send this list to backed to create symlinks in this step
      form = document.createElement("form")
      form.setAttribute("method", "POST")
      form.setAttribute("action", "/portal/staging/?stage=selected")
      data = document.createElement("input")
      data.setAttribute("type", "hidden")
      data.setAttribute("value", localStorage.getItem("selectedFiles"))
      data.setAttribute("name", "selectedFiles")
      form.appendChild(data)
      document.querySelector("body").appendChild(form)
      form.submit()

    cancelStageAll:()->
      @stageButtonText = 'Stage ALL results'
      @stageAllConfirm = false

    confirmStage: ()->
      if @stageAllConfirm is true
        # this is second click, stage all files
        console.log "second confirm is true"
        localStorage.setItem("stage", "all")
        form = document.createElement("form")
        form.setAttribute("method", "POST")
        form.setAttribute("action", config.stagingUrl+ "?stage=all")
        data = document.createElement("input")
        data.setAttribute("type", "hidden")
        searchObj = localStorage.getItem("searchData")
        data.setAttribute("value", searchObj)
        data.setAttribute("name", "searchData")
        form.appendChild(data)
        document.querySelector("body").appendChild(form)
        form.submit()
        #window.location.href=config.stagingUrl+"?stage=all"

      else
        # first click, ask for confirmation
        @stageButtonText = "OK, continue"
        @stageAllConfirm = true

    toggleResults: ()->
      @toggle = !@toggle
      console.log "toggle"
      bus.$emit("toggleselected", @toggle)
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
  updated:()->
    window.base.bindEvents()
  mounted:()->
    window.results = @
    console.log "Results mounted"
    q = localStorage.getItem("search")
    new Ajax
      url: window.location.origin+"/dal/get-filters"
      data: JSON.parse(q)
      method: "post"
      accept: "json"
      success: (data)->
        console.log "got this for filters", data


    # listen to bus toggle selected notifications
    bus.$on "toggleselected", (onoff)=>
      if onoff
        @selected = [].concat(@results.resultset)
      else
        @selected = []
    # listen to bus selected row notifications
    bus.$on "rowselected", (data)=>
      # if checked, push on the selected queue
      if data.isSelected
        @selected.push(data.row)
        if data.event.shiftKey
          prevIdx = null
          curIdx = null
          for obj,idx in @results.resultset
            if obj == data.row
              curIdx = idx
              break
          for obj, idx in @results.resultset
            if obj == @lastSelected
              prevIdx = idx
              break

          for idx in [prevIdx..curIdx]
            row = @results.resultset[idx]
            alreadySelected = false
            for sel in @selected
              if row.reference is sel.reference
                alreadySelected = true
                break

            if alreadySelected is false
              bus.$emit("selectrow",row )
              @selected.push(row)

        @lastSelected = data.row
      else
      # else find & remove from selected queue
        index = _.indexOf(@selected, data.row)
        @selected.splice(index, 1)

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
    console.log document.querySelectorAll(".collapsible")
}
