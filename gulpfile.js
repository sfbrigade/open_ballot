var gulp = require('gulp')
  , stylus = require('gulp-stylus')

gulp.task('stylus', function() {
    gulp.src('open_ballot/stylus/*')
    .pipe(stylus({
        compress: true
    }))
    .pipe(gulp.dest('open_ballot/static/css'))
})

gulp.task('dev', function(){
  gulp.watch('open_ballot/stylus/**', ['stylus'])
})