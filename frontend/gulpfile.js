"use strict";
var gulp = require("gulp");

var browserify = require("browserify");
var source = require("vinyl-source-stream");
var tsify = require("tsify");

var watchify = require("watchify");
var fancy_log = require("fancy-log");
var browserifyInc = require('browserify-incremental')

// var b = browserify({
//         entries: ["src/app.ts"],
//         cache: {},
//         packageCache: {},
// });

var b = browserify(browserifyInc.args, {
        entries: ["src/app.ts"]
}).ignore('pixi.js');
b.plugin(tsify);
b.plugin(watchify, {ignoreWatch: "**/static/**", poll: true});
// in wsl you must use polling and then ignore complied files so that they won't
// cause infinite change loop

function bundle(){
    return b
        .bundle()
        .on('error', fancy_log)
        .pipe(source("bundle.js"))
        .pipe(gulp.dest("static"));
};

gulp.task("default", bundle);
b.on("update", bundle);
b.on("update", fancy_log);
b.on("log", fancy_log);
