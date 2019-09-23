'use strict';

// require( 'jquery' );
// require( 'popper.js' );
// require( '@fortawesome/fontawesome-free' );
// require( 'bootstrap' );

let gulp = require( 'gulp' );
let sass = require( 'gulp-sass' );
let sourcemaps = require('gulp-sourcemaps');

gulp.task('compile', function(done) {
	gulp.src( './scss/inventor.scss' )
        .pipe( sourcemaps.init() )
		.pipe( sass() )
        .pipe( sourcemaps.write( './' ) )
		.pipe( gulp.dest( './css/' ) );
    done();
});

gulp.task('watch', function() {
	gulp.watch( './scss/inventor.scss', gulp.series('compile') );
	gulp.watch( './scss/abstracts/*.scss', gulp.series('compile') );
	gulp.watch( './scss/layout/*.scss', gulp.series('compile') );
});
