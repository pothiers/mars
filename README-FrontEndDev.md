## Setup

First do `yarn install`

Next set your environment, `source ../dev.env`

## Tools

Using webpack, gulp, Vue to generate pages and assets. 
Webpack will bundle vendor libraries and app code seperately with hashed names to utilize browser caching as much as possible.

Because the names of the files change on build, it will also generate a manifest `webpack-assets.json` containing the names of the files generated so they can be dynamically injected onto the main html page render.


