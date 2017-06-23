
function onSearchLoaded(event){
}

casper.test.begin('Search page loads...', 2, {
    setUp: function(){
        casper.on('page.initialized', onSearchLoaded);
    },

    tearDown: function(){},

    test: function(test){
        casper.start("http://localhost:8000/natica/search", function(){
            test.assertEvalEquals(function(){return typeof(window.searchForm);},"object");
            test.assertExists("#search-form");
        });
        casper.run(function(){
            test.done();
        });
    }
});

