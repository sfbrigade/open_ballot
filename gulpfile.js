var gulp = require('gulp')
  , stylus = require('gulp-stylus')
  , browserify = require('browserify')
  , source = require('vinyl-source-stream');


gulp.task('stylus', function() {
    gulp.src('open_ballot/stylus/*')
    .pipe(stylus({
        compress: true
    }))
    .pipe(gulp.dest('open_ballot/static/css'))
})

gulp.task('build', function() {
    browserify('./open_ballot/js/app.js')
    .bundle()
    .pipe(source('bundle.js'))
    .pipe(gulp.dest('./build/'))
  }
)

gulp.task('dev', function() {
  gulp.watch('open_ballot/stylus/**', ['stylus'])
  gulp.watch('open_ballot/js/**', ['build'])
})