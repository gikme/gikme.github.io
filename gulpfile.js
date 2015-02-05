var gulp = require('gulp');
var stylus = require('gulp-stylus');
var prefix = require('gulp-autoprefixer');

var srcDir = './site/themes/gikme-light/src/stylus/';
var destDir = './site/themes/gikme-light/static/css'
var src = srcDir + 'main.styl';

function build(options) {
	gulp.src(src)
    	.pipe(stylus(options))
    	.pipe(prefix())
    	.pipe(gulp.dest(destDir));
}

gulp.task('compress', function () {
	build({compress: true});
});

gulp.task('watch', function () {
	gulp.watch(srcDir + '**/*.styl', function () {
		build({compress: false});
	});
});

gulp.task('default', ['watch']);