
function onSearchLoaded(event){
}

casper.test.begin('Search page loads...', 3, {
    setUp: function(){
      casper.on('page.initialized', onSearchLoaded);
    },

    tearDown: function(){},

    test: function(test){
      casper.start("http://localhost:8000/natica/search", function(){
        test.assertExists("#search-form");
        formData = {
          'obs-date': '2015-05-10'
        };
        this.echo("Filling out form, and submitting");
        this.fill("#search-form form", formData, false);
        this.captureSelector("formfilled.jpg", "#search-form");
        this.click("#submit-form");
      });

      casper.waitFor(function check(){
        return this.evaluate(function(){
          return document.querySelector("#query-results").length > 0;
        });
      }, function then(){
        // nothing
      }, function timout(){
        this.echo("Timeout exceeded for submitting search query");
      }, 10000);

      casper.then(function(){

        test.assertExists("#query-results");
        test.assertEval(function(){
          return __utils__.findAll(".results tbody tr").length > 0;
                       }, "Got more than 0 results");
      });
      casper.run(function(){
        this.capture("testresultpage.jpg");
        test.done();
      });
    }
});

