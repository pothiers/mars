<template>
    <div class="container">
        <div class="row">
            <div class="col-xs-12">
                <h2>Staging Area</h2> 
            </div>
        </div>


        <div class="row">
            <div class="col-xs-12">
                <table>
                    <thead>
                        <tr>
                            <th>Selected</th>
                            <th>File name</th>
                        </tr> 
                    </thead>
                    <tbody>
                        <tr v-for="result in results" v-on:click="toggleSelected(result)">
                            <td><input type="checkbox" name="selected[]" value="" v-bind:value="result.filename"/></td>
                            <td>{{ result.filename }}</td>
                        </tr>
                    </tbody>
                    <tfoot>
                        
                    </tfoot>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
    import staging from "../js/staging.coffee";

    export default staging;
</script>
