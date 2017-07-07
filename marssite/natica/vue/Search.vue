<template>
  <div class="container" id="search-form" >
      <transition name="fade">
          <div class="loading" v-show="loading">
              <div class="loading-message">
                  <small>Loading...</small>
                  <div class="message" v-bind:text="loadingMessage">{{ loadingMessage }}</div>
              </div>
          </div>
      </transition>
      <transition name="fade">
          <form method="post" action="" v-if="visible">
              <div class="form-head row">
                  <div class="col-xs-12 col-md-6">
                      <h1>NOAO Science Archive</h1>
                      <p class="lead">Raw and reduced data from NOAO telescopes and instruments</p>
                  </div>
                  <div class="col-xs-12 col-md-6 text-right" rel="form-submit">
                      <div class="form-inline">
                          <label class="form-group">Search wihin collections:
                              <select class="form-control" id="search-collections" name="collections">
                                  <option value="all">All Holdings</option>
                                  <option value="my">My Collection</option>
                                  <option value="">Decam...</option>
                              </select>
                          </label>
                          <button class="btn btn-primary" id="submit-form" type="submit" v-on:click="submitForm">Search</button>
                          <div><a class="" href="#" v-on:click="newSearch">Clear Search</a></div> 
                      </div>
                  </div><!-- /form-submit -->
              </div>

              <!-- Target section -->
              <div class="row">
                  <div class="col-xs-12 form-section panel panel-default">
                      <div class="collapsible open container-fluid">
                          <div class="section-heading row">
                              <div class="col-xs-6">
                                  <h4>Target <small>Search via coordinates or by object name</small></h4>
                              </div>
                              <div class="col-xs-6">
                                  <div class="section-toggle">
                                      <span class="icon open"></span>
                                  </div>
                              </div>
                          </div><!-- /section-heading -->

                          <div class="section-content row">
                              <div class="col-md-6">
                                  <div class="form-group">
                                      <label for="object-name" class="floating">Object Name</label>
                                      <input name="object-name" type="text" value="" placeholder="Object Name" class="form-control" id="object-name">
                                  </div>
                                  <button class="btn btn-default">Resolve object</button>
                              </div>
                              <div class="col-md-6">
                                  <div class="col-md-6">
                                      <div class="form-group">
                                          <label for="ra" class="floating">Ra</label>
                                          <input class="form-control" placeholder="RA" name="ra" id="ra" type="text" value="" v-model="search.coordinates.ra" v-validate="'decimal|dependson:#dec'">
                                          <span class="error-message" v-if="errors.has('ra')">
                                              {{errors.first('ra')}}
                                          </span>
                                      </div>
                                  </div>
                                  <div class="col-md-6">
                                      <div class="form-group">
                                          <label for="dec" class="floating">Dec</label>
                                          <input class="form-control" placeholder="Dec" name="dec" id="dec" type="text" value="" v-model="search.coordinates.dec" v-validate="'decimal|dependson:#ra'">
                                          <span class="error-message" v-if="errors.has('dec')">
                                              {{errors.first('dec')}}
                                          </span>
                                      </div> 
                                  </div>
                              </div>
                          </div> <!-- /section-content -->

                      </div> <!-- /collapsible -->
                  </div>
              </div> <!-- /row -->

              <!-- Observation section -->
              <div class="row">
                  <div class="col-xs-12 form-section">
                      <div class="collapsible open container-fluid">
                          <div class="section-heading row">
                              <div class="col-xs-6">
                                  <h4>Obervation <small>Search by obervation details</small></h4>
                              </div>
                              <div class="col-xs-6">
                                  <div class="section-toggle">
                                      <div class="icon"></div>
                                  </div>
                              </div>

                          </div> <!-- /section-heading -->
                          <div class="section-content row">
                              <div class="col-md-6">
                                  <div class="form-group">
                                      <label class="floating" for="program-number">Program Number</label>
                                      <input class="form-control" name="program-number" id="program-number" placeholder="Program Number" type="text" value="" v-model="search.prop_id">
                                  </div>
                                  <div class="form-group">
                                      <label class="floating" for="principle-investigator">Principle Investigator</label> 
                                      <input class="form-control" name="principle-investigator" id="principle-investigator" placeholder="Principle Investigator" type="text" value="" v-model="search.pi">
                                  </div>
                                  <div class="form-group">
                                      <label class="floating" for="original-filename">Original Filename</label>
                                      <input class="form-control" id="original-filename" name="original-filename" type="text" value="" placeholder="Original Filename" v-model="search.original_filename">
                                  </div>
                                  <div class="form-group">
                                      <label class="floating" for="archive-filename">Archive Filename</label> 
                                      <input class="form-control" id="archive-filename" name="archive-filename" type="text" value="" placeholder="Archive Filename" v-model="search.filename">
                                  </div>
                              </div> <!-- /col -->

                              <div class="col-md-6">
                                  <div class="form-group">
                                    <div class="input-group select-group split-val" v-bind:class="{ 'display-hidden': showBothObsDateFields } ">
                                          <label class="floating" for="obs-date">Observation Date <small>(YYYY-MM-DD)</small></label>
                                          <select name="obs-date-interval" class="form-control input-group-addon" v-model="search.obs_date[2]" v-on:change="splitSelection('obs_date')">
                                              <option value="=">=</option>
                                              <option value="(]">&le;</option>
                                              <option value="[)">&ge;</option>
                                              <option value="[]" class="toggle-option">&le; &ge;</option>
                                          </select>
                                          <input id="obs-date" class="date form-control" data-polyfill="all" name="obs-date" type="text" value="" placeholder="Obervation date" v-model="search.obs_date[0]" v-if="search.obs_date[2] !== '(]'" v-validate="'date_format:YYYY-MM-DD'">
                                          <input id="obs-date-max" class="date form-control" v-bind:class="{ 'hidden-split':showBothObsDateFields }" name="obs-date-max" type="text" value="" placeholder="Max Observation Date" v-model="search.obs_date[1]" v-show="showObsDateMax" v-validate="'date_format:YYYY-MM-DD'">
                                          <span class="error-message" v-if="errors.has('obs-date')">{{ errors.first('obs-date') }}</span>
                                          <span class="error-message" v-if="errors.has('obs-date-max')">{{ errors.first('obs-date-max') }}</span>
                                      </div><!-- /input-group -->
                                  </div><!-- /form-group -->
                                  <div class="form-group">
                                      <div class="input-group select-group split-val" v-bind:class="{ 'display-hidden': showBothExposureFields }">
                                          <label class="floating" for="exposure">Exposure</label>

                                          <select class="form-control input-group-addon" id="" name="expore-interval" v-model="search.exposure_time[2]" v-on:change="splitSelection('exposure_time')">
                                              <option value="=">=</option>
                                              <option value="(]">&le;</option>
                                              <option value="[)">&ge;</option>
                                              <option value="[]" class="toggle-option">&le; &ge;</option>
                                          </select>
                                          <input id="exposure" class="form-control" name="exposure" type="text" value="" placeholder="Exposure in seconds" v-model="search.exposure_time[0]" v-if="search.exposure_time[2] !== '(]'" v-validate="'numeric'">
                                          <input id="exposure-max" class="form-control" v-bind:class="{ 'hidden-split':showBothExposureFields }" name="exposure-max" type="text" value="" placeholder="Max exposure" v-model="search.exposure_time[1]" v-show="showExposureMax" v-validate="'numeric'">
                                          <span class="error-message" v-if="errors.has('exposure')">{{ errors.first('exposure') }}</span>
                                          <span class="error-message" v-if="errors.has('exposure-max')">{{ errors.first('exposure-max') }}</span>
                                      </div><!-- /select-group -->
                                  </div><!-- /form-group --> 

                              </div>



                          </div> <!-- /secton-content -->
                      </div><!-- /collapsible -->
                  </div>
              </div>

              <!-- Telescope Section -->
              <div class="row">
                  <div class="col-xs-12 form-section panel panel-default">

                      <div class="collapsible open container-fluid">
                          <div class="section-heading row">
                              <div class="col-xs-6">
                                  <h4>Image &amp; Telescope / Instrument <small>Search a image processing and specific telelscope and instrument</small></h4>
                              </div>
                              <div class="col-xs-6">
                                  <div class="section-toggle">
                                      <span class="icon"></span>
                                  </div>
                              </div>
                          </div><!-- /section-heading  -->
                          <div class="section-content row">
                          <div class="col-sm-6">
                                  <div class="form-group">
                                      <div class="input-group select-group split-val" v-bind:class="{ 'display-hidden':showBothReleaseDateFields }">
                                          <label class="floating" for="release-date">Public Release Date <small>(YYYY-MM-DD)</small></label>
                                          <select class="form-control input-group-addon" id="" name="release-date-interval" v-model="search.release_date[2]" v-on:change="splitSelection('release_date')">
                                              <option value="=">=</option>
                                              <option value="(]">&le;</option>
                                              <option value="[)">&ge;</option>
                                              <option value="[]" class="toggle-option">&le; &ge;</option>
                                          </select>
                                          <input id="release-date" class="date form-control" data-polyfill="all" name="release-date" type="text" value="" placeholder="Release date" v-model="search.release_date[0]" v-if="search.release_date[2] !== '(]'" v-validate="'date_format:YYYY-MM-DD'">

                                          <input id="release-date-max" class="date form-control" data-polyfill="all" v-bind:class="{ 'hidden-split': showBothReleaseDateFields }" name="release-date-max" type="text" value="" placeholder="Max release date" v-model="search.release_date[1]" v-show="showReleaseDateMax" v-validate="'date_format:YYYY-MM-DD'">
                                      </div><!-- /input-group -->
                                  </div>
                              </div><!-- /col -->
                              <div class="col-sm-3">
                                  <div class="form-group">
                                      <div class="input-group">
                                          <label for="image-filter">Image Filter</label>
                                          <select multiple name="image-filter" size="10 "id="image-filter" class="form-control" v-model="search.image_filter">
                                              <option value="raw">Raw image</option>
                                              <option value="calibrated">Calibrated</option>
                                              <option value="reprojected">Reprojected</option>
                                              <option value="stacked">Stacked</option>
                                              <option value="master_calibration">Master Calibration</option>
                                              <option value="image_tiles">Image Tiles</option>
                                              <option value="sky_subtracted">Sky Subtracted</option>
                                      </select>
                                      <p class="help-block">
                                          * <em>Sky subtracted</em> is for <strong>NEWFIRM</strong> only. <em>Calibrated, Reprojected, Stacked, Master calibration, Image Tiles</em> are for <strong>Mosiac, NEWFIRM and DECam</strong>.
                                      </p>
                                      </div>
                                  </div>
                          </div><!-- /col -->
                          <div class="col-sm-3">
                                  <div class="form-group">
                                      <div class="input-group">
                                          <label for="telescope">Telescope &amp; Intrument</label>
                                          <select id="telescope" name="telescope[]" class="form-control" multiple size="10" v-model="search.telescope_instrument">
                                            <option value="" v-for="tel in telescopes" v-bind:value="tel[0]+','+tel[1]">{{ tel[0] }} + {{ tel[1] }}</option>                                            
                                          </select>
                                      </div>
                                  </div>
                              </div>
                          </div> <!-- /row section -->
                      </div><!-- /collapsible -->
                  </div>
              </div><!-- /row -->
          </form>
      </transition>
          <div class='code-view'>
            <pre class="code">{{ code }}</pre>
          </div>
  </div>
</template>
<script>
import search from "../js/search.coffee";
 
export default search;
</script>
