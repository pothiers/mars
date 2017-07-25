"use strict";

const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
const CleanWebpackPlugin = require('clean-webpack-plugin');
const webpack = require('webpack');
const path = require('path');
const outPath = "../static/natica/dist";
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
    "app.bundle":"./app.coffee",
    "staging.bundle":"./staging.app.coffee",
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
    new CleanWebpackPlugin(["static/natica/dist"], cleanConfig),
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
    new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/)
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
      {
        test: /\.coffee$/,
        use: [ 'coffee-loader' ]
      },
    ]
  }
};
