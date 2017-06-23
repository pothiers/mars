casper = require('casper').create()


casper.start("localhost:8000/natica/search", function(){
  this.echo(this.getTitle());
  });

casper.run();
