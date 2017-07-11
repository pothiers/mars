_config =
  apiUrl: "/dal/search/"
  rangeInputs: ["obs_date", "exposure_time", "release_date"]

  validatorConfig:
    delay: 800
    events: "input|blur"
    inject: true
    dependsOn: "dependson"

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
        newFormData = if @search then JSON.parse(JSON.stringify(@search)) else JSON.parse(localStorage.getItem("search"))
        search = newFormData
        localStorage.setItem('search', JSON.stringify(search))

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
              localStorage.setItem('results', JSON.stringify(data))
              self.$emit("displayform", ["results", data])
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
          .send()

}
