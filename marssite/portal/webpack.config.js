"use strict";

const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
const CleanWebpackPlugin = require('clean-webpack-plugin');
const WebpackOnBuildPlugin = require('on-build-webpack');
const webpack = require('webpack');
const path = require('path');
const fs = require('fs');
const outPath = "../static/portal/dist";
var AssetsPlugin = require('assets-webpack-plugin');
var assetsPluginInstance = new AssetsPlugin();



let cleanConfig = {
  root: path.resolve("../"),
  exclude:  [],
  verbose:  true,
  dry:      false
};

module.exports = {
  entry:{
    "app.bundle":"./app_scripts/app.js",
    "staging.bundle":"./app_scripts/staging.app.js",
    "vue":['vue', 'vee-validate'],
    "vendor":['moment']
  },
  output: {
    path: path.resolve(outPath),
    filename: "[name].[chunkhash].js"
  },
  resolve: {
    alias: {
      vue: 'vue/dist/vue.js'
    }
  },
  externals: {
    "Vue":"vue",
    "VeeValidate":"vee-validate",
  },
  plugins: [
    assetsPluginInstance,
    new CleanWebpackPlugin(["static/portal/dist"], cleanConfig),
    /*
    new BundleAnalyzerPlugin({
      analyzerMode: 'static'
    }),
    */
    // splitting can be done implicitly
    // https://webpack.js.org/guides/code-splitting-libraries/
    new webpack.optimize.CommonsChunkPlugin({
      names: ['vendor', 'vue', 'manifest'] // Specify the common bundle's name.
    }),
    new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/),
    new WebpackOnBuildPlugin(function (stats) {
      // clean up built resource files after build during development/watch
      const newlyCreatedAssets = stats.compilation.assets;

      const unlinked = [];
      fs.readdir(path.resolve(outPath), (err, files) => {
        files.forEach(file => {
          if (!newlyCreatedAssets[file]) {
            fs.unlink(path.resolve(outPath +'/'+ file));
            unlinked.push(file);
          }
        });
        if (unlinked.length > 0) {
          console.log('Removed old assets: ', unlinked);
      }
      });
    })
  ],
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [{
          loader: "style-loader" // creates style nodes from JS strings
        }, {
          loader: "css-loader" // translates CSS into CommonJS
        }, {
          loader: "sass-loader" // compiles Sass to CSS
        }]
      },
      {
        test: /\.vue$/,
        use: ['vue-loader']
      },
    ]
  }
};
