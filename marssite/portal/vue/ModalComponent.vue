<template>
    <!-- Modal -->
    <div class="modal fade" id="modal-component" tabindex="-1" role="dialog" aria-labelledby="searchModelLabel">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" v-on:click="closeModal" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h4 class="modal-title" id="myModalLabel">{{ modalTitle }}</h4>
            </div>
            <div class="modal-body" v-html="modalBody">
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal" v-on:click="closeModal">Close</button>
            </div>
            </div>
        </div>
    </div>
</template>

<script>

module.exports = {
    data: function(){
        return {
            modalTitle: "",
            modalBody:"",
            modalComponent: null,
            backdrop: null,
            body: document.querySelector("body")
        }
    },
    created() {
        if( window.bus ){
            window.bus.$on("open-modal", this.openModal);
            window.bus.$on("close-modal", this.closeModal);
        }
    },
    mounted() {
        this.modalComponent = document.querySelector("#modal-component");
    },
    methods: {
        closeModal: function() {
            this.backdrop.remove();
            this.backdrop = null;
            this.modalComponent.style.display = 'none';
            this.modalComponent.classList.remove('in');
        },
        /*
         * Args require:
         * - title
         * - body
         */
        openModal: function(args) {
            this.modalTitle = args.title;
            this.modalBody = args.body;
            this.modalComponent.style.display = 'block';
            this.modalComponent.classList.add('in')
            this.backdrop = document.createElement('div');
            this.backdrop.setAttribute('class', 'modal-backdrop fade in');
            this.body.append(this.backdrop);
        }

    }
}

</script>
