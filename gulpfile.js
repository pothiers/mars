'use strict';
var gulp = require('gulp');
var sass = require('gulp-sass');
var minifyCSS = require('gulp-csso');
//var coffee = require('gulp-coffeescript');

var sassSrc = "./marssite/**/*.scss";
var cssDest = "./marssite/sass_out";

gulp.task('sass', function(){
  return gulp.src(sassSrc)
    .pipe(sass().on('error', sass.logError))
    .pipe(gulp.dest(cssDest));
});

gulp.task('sass:watch', function(){
  gulp.watch(sassSrc, ['sass']);
});
