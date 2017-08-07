_config =
  apiUrl: "/dal/search/"
  rangeInputs: ["obs_date", "exposure_time", "release_date"]

  validatorConfig:
    delay: 800
    events: "input|blur"
    inject: true
    dependsOn: "dependson"

  # default columns are checked
  allColumns:[
    {"checked":true, "mapping": "prop_id", "name": "Program Number", "num":1},
    {"checked":true, "mapping": "obs_date", "name": "Observed date", "num":2},
    {"checked":false, "mapping": "pi", "name": "Principle Investigator", "num":3},
    {"checked":false, "mapping": "ra", "name":"RA", "num":4},
    {"checked":false, "mapping": "dec", "name" : "Dec", "num":5},
    {"checked":false, "mapping": "product", "name":"Product", "num":6},
    {"checked":false, "mapping": "depth", "name": "Depth", "num":7},
    {"checked":true, "mapping": "exposure", "name": "Exposure", "num":8},
    {"checked":true, "mapping": "filter", "name": "Filter","num":9},
    {"checked":true, "mapping": "telescope", "name":"Telescope", "num": 10},
    {"checked":true, "mapping": "instrument", "name": "Instrument", "num":11},
    {"checked":false, "mapping": "image_type", "name": "Image Type", "num":12},
    {"checked":false, "mapping": "filename", "name": "Filename", "num":13},
    {"checked":false, "mapping": "md5sum", "name": "MD5 sum", "num":14},
    {"checked":false, "mapping": "filesize", "name" : "File size", "num":15},
    {"checked":false, "mapping": "original_filename", "name":"Original filename", "num":16},
    {"checked":false, "mapping": "reference", "name":"Reference", "num":17},
    {"checked":true, "mapping": "survey_id", "name":"Survey Id", "num":18}
    {"checked":false, "mapping": "release_date", "name":"Release Date", "num":19},
    {"checked":false, "mapping": "seeing", "name":"Seeing", "num": 20},
  ]


  formData:
    coordinates:
      ra: ""
      dec: ""
    pi: null
    search_box_min: null
    prop_id: null
    obs_date:['','', "="]
    filename: null
    original_filename: null
    telescope_instrument:[]
    exposure_time:['', '', "="]
    release_date:['', '', "="]
    image_filter:[]

  loadingMessages:[
    "Searching the cosmos..."
    "Deploying deep space probes..."
    "Is that you Dave?..."
    "There's so much S P A C E!"
  ]

export default {
  config: _config
  mixin:
    data: ()->
      return
        config: _config



    methods:
      stripData: ()->
        # strip out anything that wasn't modified
        newFormData = if @search isnt undefined then JSON.parse(JSON.stringify(@search)) else JSON.parse(localStorage.getItem("searchData"))
        console.dir newFormData
        console.log @search
        for key of newFormData
          if _.isEqual(newFormData[key], @config.formData[key])
            delete(newFormData[key])
          else
            if @config.rangeInputs.indexOf(key) >= 0
              # flatten value if it is for direct match
              if newFormData[key][2] is "="
                newFormData[key] = newFormData[key][0]
        if newFormData.telescope_instrument
          newFormData.telescope_instrument = _.map(newFormData.telescope_instrument, (item)=> return item.split(","))
        if newFormData.coordinates?.ra
          newFormData.coordinates.ra = parseFloat(newFormData.coordinates.ra)
          newFormData.coordinates.dec = parseFloat(newFormData.coordinates.dec)
        return newFormData
      submitForm: (event, paging=null, cb=null)->
          event?.preventDefault()
          unless paging
            @loading = true
            @url = @config.apiUrl
            window.location.hash = ""
            this.$emit('setpagenum', 1)
            page = 1
            localStorage.setItem("currentPage", 1)
            localStorage.setItem("searchData", JSON.stringify(@search))
          else
            page = localStorage.getItem("currentPage")

          newFormData = @stripData()
          msgs = @config.loadingMessages
          message = Math.floor(Math.random()*msgs.length)
          @loadingMessage = msgs[message]
          self = @
          url = @config.apiUrl+"?page=#{page}"
          new Ajax
            url: url
            method: "post"
            accept: "json"
            data:
              search: newFormData
            success: (data)->
              window.location.hash = "#query"
              self.loading = false
              saveData =  if typeof(data) is "object" then JSON.stringify(data) else data

              localStorage.setItem('results', saveData )
              self.$emit("displayform", ["results", saveData])
              if cb
                cb(data)
            fail: (statusMsg, status, xhr)->
              console.log "Request failed, got this"
              message = "#{statusMsg}"
              if xhr.response
                message += ":  #{xhr.response.errorMessage}"
              self.loading = false
              self.modalTitle = "Request Error"
              self.modalBody = "<div class='alert alert-danger'>There was an error with your request.<br> <strong>#{message}</strong></div>"
              ToggleModal("#search-modal")
              console.dir arguments

}
