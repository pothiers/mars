<template>
    <div id="query-results">
    <transition name="fade">
        <div v-if="visible">
            <div class="container" >
               <div class="row breadcrumb-wrapper">
                    <div class="category-history" v-if="categoryHistory.length > 0">
                        <ol class="breadcrumb">
                            <li><button class="btn btn-link" @click="clearCategory">Original Results</button></li>
                            <li v-for="hist in categoryHistory"><button class="btn btn-link">{{ hist.category ? hist.category.toString() :  "Uncategorized" }}</button></li>
                        </ol>
                    </div>
               </div>
               <div class="row heading">
                    <div class="col-xs-10">

                        <h2 class="text-warn">Query returned <em>{{totalItems}}</em> records</h2>
                         <ul class="list-inline category-filter-controls">
                             <li>
                                 <button class="btn btn-default" @click="toggleCategories"><span class="fa fa-bars"></span> Toggle Categories</button>
                             </li>
                            <li>
                               <div class="form-inline">
                                    <div class="form-group">
                                        <input class="form-control" name="" type="text" value="" placeholder="Filter">
                                    </div>
                               </div>
                            </li>
                         </ul>

                    </div>
                    <div class="col-xs-2 text-right">
                        <button class="btn btn-primary" @click="displayForm">Search Again</button>
                    </div>

                </div><!-- /heading -->
                <div class="row">
                    <div class="col-xs-12 results-categories" v-if="categorizeFirst">
                        <h3>Results by Category:</h3>
                        <div class="alert alert-info text-center" v-if="categorizeFirst">
                            There are too many results to effectively display here. Consider refining results further by categorizing.
                            <br>
                            <button class="btn btn-primary btn-sm" @click="toggleCategories">Show Categories</button>
                        </div>
                       
                    </div>
                </div>

            </div>
            <div class="container">
                <div class="row">
                    <div class="col-md-3 col-xs-12" v-if="categoriesVisible">
                        <div class="loading-wrapper text-center" v-if="!categoriesLoaded">
                            <h4>Analyzing results. Loading categories...</h4>
                            <div class="fa fa-spin fa-spinner fa-3x fa-fw"></div>
                        </div>
                        <ul class="list-group" v-for="(cat, indx) in categories">
                            <li class="list-group-item"><h4 class="text-primary" >{{ indx.replace("_"," ") }}</h4>
                               <ul class="category-sublist" >
                                   <li class="checkbox" v-for="item in cat" >
                                       <label>
                                           <!-- Send setCategory key, value  -->
                                           <input type="radio" @click="setCategory(indx,item.name)" name="category_selection"> {{ item.name || "Uncategorized" }} <span class="badge alert-info">{{ item.total }}</span>
                                       </label>
                                   </li>
                               </ul>
                           </li>
                       </ul>
                    </div>    

                    <!-- Begin main results table -->
                    <div class="col-xs-12 results-wrapper" v-bind:class="{'col-md-9':categoriesVisible}"  >
                        <div class="collapsible">

                            <div class="column-toggle panel panel-default">
                                <div class="panel-heading section-heading clearfix">
                                    <strong class="">Toggle visibility of columns
                                    </strong>

                                    <div class="section-toggle">
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
                            <div class="row results-controls">
                                <div class="col-sm-5">
                                    <button class="btn-link btn page-prev" @click="pageBack">Prev</button>
                                    <span class="page-num">{{ pageNum }}</span>
                                    <button class="btn-link btn page-next" @click="pageNext">Next</button>
                                    <span class="records-from">{{ recordsFrom }}</span> to <span class="records-to">{{ recordsTo }}</span>
                                    <span class="fa fa-spinner fa-spin fa-1x fa-fw" v-if="isLoading"></span>
                            </div>
                                <div class="col-sm-7 ">
                                    <!--control button/dropdown placeholder-->
                                </div>
                            </div>

                        </div>
                    <div class="row">
                        <div class="col-sm-3">
                            <label><input class="" name="" type="checkbox" value="" v-on:change="toggleResults"> Select all visible</label>
                        </div>
                        <div class="col-sm-9 text-right">

                            <button class="btn btn-default" v-bind:disabled="selected.length == 0" @click="stageSelected">Stage selected files</button>
                            <button class="btn btn-default" v-bind:class="{ 'btn-danger' : stageAllConfirm }" @click="confirmStage">{{ stageButtonText }}</button>
                        <div class="text-small help-block" v-if="stageAllConfirm" >
                            <span class="text-danger">You are about to stage <strong>ALL</strong> results. <strong>Click again to confirm</strong> </span>
                            <span class="label label-primary" v-if="stageAllConfirm">{{ results.meta.total_count }} files</span> | <button class="btn btn-default btn-small" @click="cancelStageAll">Cancel</button>
                        </div>
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
                            <button class="btn btn-success" @click="displayForm">Adjust Paramaters</button>
                        </div>
                        </div>
                    </div>
                    <!-- end results table -->

                    <!-- Category view -->


                </div>
            </div>
        </div>
    </transition>
    <!-- Modal Component -->
    <modal-component></modal-component>
    </div>      
</template>

<script>
  import Results from "../js/results.js";
  export default Results;
</script>
