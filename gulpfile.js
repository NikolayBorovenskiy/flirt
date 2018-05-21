"use strict";

let gulp = require('gulp');
let uglify = require('gulp-uglify');
let es = require('event-stream');
let concat = require('gulp-concat');
let notify = require('gulp-notify');
let plumber = require('gulp-plumber');
let cssmin = require('gulp-cssmin');
let imagemin = require('gulp-imagemin');
let rename = require("gulp-rename");
let sass = require('gulp-sass');
let postcss = require('gulp-postcss');
let autoprefixer = require('autoprefixer');
let path = require('path');
let browserSync = require('browser-sync').create();
// let webpack_stream = require('webpack-stream');
// let webpackConfig = require('./webpack.config.js');
let _ = require('lodash');
let fs = require('fs');

let spawn = require('child_process').spawn;
let argv = require('yargs')
    .default('host', '127.0.0.1')
    .default('port', 3001)
    .default('bsync-port', 8001)
    .argv;

let scripts = require('./app.scripts.json');

let djangoAddress = argv.host + ":" + argv.port;
let config = {
    sass: {
        src: './assets/sass/index.scss',
        watch: './assets/sass/**/*.scss',
        dest: './src/dating/static/build/',
        destDevFileName: 'bundle.css',
        destProdFileName: 'bundle.min.css',
        sassOptions: {
            includePaths: ['node_modules']
        }
    },
    js: {
        src: './assets/js/*.js',
        entry: {
            'bundle': './assets/js/index.js'
        },
        watch: './assets/js/**/*.jsx?',
        dest: './src/dating/static/build/'
    },
    img: {
        src: './assets/img/**/*',
        dest: './src/dating/static/img/'
    }
};

//gulp.task('js:dev', function () {
//    let cfg = Object.assign({}, webpackConfig.development, {entry:
// config.js.entry});  return gulp.src(config.js.src)
// .pipe(webpack_stream(cfg)) .on('error', function (error) {
// console.log(error.message); this.emit('end'); })
// .pipe(gulp.dest(config.js.dest)) });

gulp.task('js:dev', function() {
    return es.merge(gulp.src(config.js.src))
        .pipe(concat('app.js'))
        .pipe(gulp.dest(config.js.dest));
});

gulp.task('js:prod', function() {
    return es.merge(gulp.src(config.js.src))
        .pipe(uglify())
        .pipe(concat('app.js'))
        .pipe(gulp.dest(config.js.dest));
});

gulp.task('img:compress', function() {
        gulp.src(config.img.src)
            .pipe(imagemin({
                optimizationLevel: 3,
                progressive: true,
                interlaced: true
            }))
            .pipe(gulp.dest(config.img.dest))
    }
);

//gulp.task('js:prod', function () {
//    let cfg = Object.assign({}, webpackConfig.production, {entry:
// config.js.entry}); return gulp.src(config.js.src) .pipe(webpack_stream(cfg))
// .pipe(gulp.dest(config.js.dest)); });

gulp.task('sass:dev', function() {
    return gulp.src(config.sass.src)
        .pipe(plumber())
        .pipe(sass(config.sass.sassOptions).on('error', sass.logError))
        .pipe(postcss([autoprefixer({browsers: ['>1%']})]))
        .pipe(rename(config.sass.destDevFileName))
        .pipe(gulp.dest(config.sass.dest))
        .pipe(browserSync.stream())
});


gulp.task('sass:prod', function() {
    return gulp.src(config.sass.src)
        .pipe(sass(config.sass.sassOptions))
        .pipe(postcss([autoprefixer({browsers: ['>1%']})]))
        .pipe(rename(config.sass.destProdFileName))
        .pipe(cssmin())
        .pipe(gulp.dest(config.sass.dest))
});

gulp.task('vendor', function() {
    _.forIn(scripts.chunks, function(chunkScripts, chunkName) {
        var paths = [];
        chunkScripts.forEach(function(script) {
            var scriptFileName = scripts.paths[script];
            if (!fs.existsSync(__dirname + '/' + scriptFileName)) {

                throw console.error('Required path doesn\'t exist: ' + __dirname + '/' + scriptFileName, script)
            }
            paths.push(scriptFileName);
        });
        gulp.src(paths)
            .pipe(uglify())
            .pipe(concat(chunkName + '.js'))
            //.on('error', swallowError)
            .pipe(gulp.dest(config.js.dest))
    })

});

gulp.task('django-runserver', function() {
    if (!process.env['VIRTUAL_ENV']) {
        console.warn("WARNING: To run django you should activate virtual environment")
    } else {
        let args = ["src/manage.py", "runserver", djangoAddress];
        let python = process.env['VIRTUAL_ENV'] + '/bin/python';
        let runserver = spawn(python, args, {stdio: "inherit"});
        runserver.on('close', function(code) {
            if (code !== 0) {
                console.error('Django runserver exited with error code: ' + code);
            } else {
                console.log('Django runserver exited normally.');
            }
        });
    }
});


gulp.task('browsersync', ['django-runserver'], function() {
    browserSync.init({
        proxy: djangoAddress,
        port: argv['bsync-port']
    });
});


gulp.task('watch', function() {
    gulp.watch(config.sass.watch, ['sass:dev']);
    gulp.watch(config.js.src, ['js:dev']);
});


// Run in development
gulp.task('default', ['img:compress', 'sass:dev', 'js:dev', 'django-runserver', 'browsersync', 'watch', 'vendor']);


// Run before deploy to production
gulp.task('bundle', ['img:compress', 'sass:prod', 'js:prod', 'vendor']);
