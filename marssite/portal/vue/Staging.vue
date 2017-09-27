<template>
    <div>

        <div class="container">
            <div class="row">
                <div class="col-xs-12">

                    <div class="panel collapsible panel-default">
                        <div class="panel-heading section-heading">
                            Downloading instructions
                            <div class="section-toggle">
                                <span class="icon open"></span>
                            </div>

                        </div>
                        <div class="panel-body section-content" >
                            <div class="row">
                                <div class="col-md-6">
                                    <h4>Command line LFTP</h4>
                                    <strong>Unix/Linux/Mac:</strong> fast parallel transfer using lftp

                                    <ol class="default">
                                        <li>
                                            If necessary, install lftp [available from most standard software repositories]
                                        </li>
                                        <li>
                                            Download this lftp configuration file and save it as ~/.lftprc
                                        </li>
                                    </ol>
                                    <strong>
                                        For authenticated users retrieving proprietary data:
                                    </strong>
                                    <ol class="default" start="3">
                                        <li>
                                            lftp -u USERNAME,PASSWORD archive.noao.edu   [see Retrieval information above]
                                        </li>
                                        <li>
                                            mirror -L .   [include the dot (" . ")]
                                        </li>
                                    </ol>
                                    <strong> For anonymous (public search) users:</strong>
                                    <ol class="default" start="3">
                                        <li>
                                            lftp -u anonymous,lftp archive.noao.edu
                                        </li>
                                        <li>
                                            cd user_NNNN   [see Retrieval information above]
                                        </li>
                                        <li>
                                            mirror -L .   [include the dot (" . ")]
                                        </li>
                                    </ol>
                                </div>
                                <div class="col-md-6">
                                   <h4>Commandline FTP</h4>
                                    <strong>Important tips for standard transfer with ftp:</strong>
                                    <ul class="default">
                                        <li>
                                            You must use ftp instead of sftp
                                        </li>
                                        <li>
                                            Be sure to select binary file transfer
                                        </li>
                                    </ul>
                                    <h4>Other transfer tools (e.g. for Windows, Mac etc)</h4>
                                    <ul class="default">
                                        <li>Unix/Linux: <strong>gftp</strong></li>
                                        <li>Mac: <strong>fetch</strong></li>
                                        <li>Windows: <strong>wsftp</strong></li>
                                        <li>Windows &amp; Mac: <strong>Cyber Duck FTP client</strong></li>
                                    </ul>
                                </div>
                            </div>

                        </div>
                    </div>

                </div>
            </div>
        </div>
        <!-- show loading for staging all files -->
        <div class="container" v-if="stagingAllFiles">
            <div class="row" v-if="loading">
                <div class="col-xs-12 text-center">
                    <h2>Staging files ...<span class="fa fa-spinner fa-spin fa-fw"></span></h2>
                    <div class="spinner">
                    </div>
                </div>
            </div>
        </div>
        <div class="container" v-if="!stagingAllFiles">
            <div class="row">
                <div class="col-xs-12">
                    <h2>Staging Area
                        | <small><strong>{{ results.length }}</strong> files staged</small>
                    </h2>
                </div>
            </div>
            <div class="row">
                <div class="col-xs-6">
                    <label>
                        <input type="checkbox" name="" value="" v-bind:checked="selectAll" v-on:change="toggleAll"/>
                        Select all
                    </label>
                </div>
                <div class="text-right col-xs-6">
                  <button class="btn btn-default" v-on:click="downloadSelected"  v-bind:disabled="selected.length == 0">Download Selected</button> <button class="btn btn-default">Download All</button>
                </div>
            </div>

            <div class="row">
                <div class="col-xs-12">
                    <table>
                        <thead>
                            <tr>
                                <th>Selected</th>
                                <th>File name</th>
                                <th>File size</th>
                                <td>MD5 sum</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="result in results" v-on:click="toggleSelected(result)">
                                <td><input type="checkbox" name="selected[]" value="" v-bind:checked="result.selected" v-bind:value="result.file.reference"/></td>
                                <td>{{ result.file.reference }}</td>
                                <td>{{ result.file.filesize/1000 }} KB</td>
                                <td>{{ result.file.md5sum }}</td>
                            </tr>
                        </tbody>
                        <tfoot>

                        </tfoot>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import staging from "../js/staging.coffee";

    export default staging;
</script>
