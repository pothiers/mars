<template>
    <div id="query-results">
    <transition name="fade">
        <div v-if="visible">
            <div class="container" >
                <div class="row heading">
                    <div class="col-xs-10">

                        <h2 class="text-warn">Query returned <em>{{totalItems}}</em> records</h2>
                    </div>
                    <div class="col-xs-2 text-right">
                        <button class="btn btn-primary" v-on:click="displayForm">Search Again</button>
                    </div>
                </div>
                <div class="row results-controls">
                    <div class="col-sm-5">
                        <button class="btn-link btn page-prev" v-on:click="pageBack">Prev</button>
                        <span class="page-num">{{ pageNum }}</span>
                        <button class="btn-link btn page-next" v-on:click="pageNext">Next</button>
                        <span class="records-from">{{ recordsFrom }}</span> to <span class="records-to">{{ recordsTo }}</span>
                        <span class="fa fa-spinner fa-spin fa-1x fa-fw" v-if="isLoading"></span>
                   </div>
                    <div class="col-sm-7 ">
                        <!--control button/dropdown placeholder-->
                    </div>
                </div>
                <div class="row table-filters">

                </div>
                <hr>
            </div>
            <div class="container">
                <div class="row">
                    <div class="col-xs-12 results-wrapper">
                        <div class="collapsible container fluid">

                            <div class="filters panel">
                                <div class="panel-heading section-heading clearfix">
                                    <h4 class="pull-left">Toggle visibility of columns</h4>
                                    <div class="section-toggle pull-right">
                                        <span class="icon open"></span>
                                    </div>

                                </div>
                                <div class="panel-body section-content ">
                                    <ul class="list-unstyled columns">
                                        <li v-for="column in allColumns"><label><input name="" type="checkbox" value="" v-bind:name="column.mapping" v-bind:checked="column.checked" v-on:change="toggleColumn(column)"> {{ column.name }}</label></li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                      <div class="row">
                          <div class="col-sm-3">
                            <label><input class="" name="" type="checkbox" value="" v-on:change="toggleResults"> Select all</label>
                          </div>
                      </div>
                        <table class="results" v-if="(results.resultset.length > 0)">
                            <thead>
                                <tr>
                                    <th>Selected</th>
                                <th v-for="col in visibleColumns">
                                    <span is="table-header" v-bind:name="col.name"></span>
                                </th>
                                </tr>
                            </thead>
                            <tbody is="table-body" v-bind:data="results.resultset" v-bind:visible-cols="visibleColumns">
                            </tbody>
                            <tfoot>

                            </tfoot>
                        </table>
                        <div v-else>
                          <h1 class="text-center">No results found</h1>
                          <div class="alert alert-danger text-center" v-if="error">{{ error }}</div>
                          <pre class="code">{{ searchObj }}
                          </pre>
                          <div class="text-center">
                            <h5>You might try and adjust your paramaters and search again</h5>
                            <button class="btn btn-success" v-on:click="displayForm">Adjust Paramaters</button>
                          </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </transition>
    </div>
</template>

<script>
  import results from "../js/results.coffee";

  export default results;
</script>
