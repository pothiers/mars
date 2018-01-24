"use strict";

const webpack = require('webpack');
const path = require('path');
const fs = require('fs');
const outPath = "./build/dist/";
var AssetsPlugin = require('assets-webpack-plugin');
var assetsPluginInstance = new AssetsPlugin();

/* 
  Common resources should be placed in a seperate config/import settings file
  i.e. plugins etc
  
  Use webpack-merge to facilitate merging config objects
*/
module.exports = {
  entry:{
    app: "./karma/main.js"
  },
  output: {
    path: path.resolve(outPath),
    filename: "[name].js"
  },
  resolve: {
    extensions: ['.js', '.vue', '.json'],
    alias: {
      vue: 'vue/dist/vue.js',
      jquery: 'jquery/dist/jquery.js',
      'jquery-ui': 'jquery-ui-dist/jquery-ui.js',
    }
  },
  externals: {
    "Vue":"vue",
    "VeeValidate":"vee-validate"
  },
  module: {
    /*loaders: [
      { test: require.resolve("jquery"), loader: "expose?$!expose?jQuery" },
    ],*/
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
