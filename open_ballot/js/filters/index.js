lazy = require('lazy.js');
var app = angular.module('open_ballot');

app.filter('metric', ['$filter', function ($filter) {

  return function (value, options) {
    var metric_metrics = ['k', 'M', 'G', 'T', 'P'];
    var imperial_metrics = ['K', 'M', 'B', 'T']; // I don't know what these are really called

    options = lazy(options)
    .defaults({
      precision: 1,
      metric: false
    })
    .toObject();
    var metrics = options.metric ? metric_metrics : imperial_metrics;
    var metric = '';

    while (value >= 1000) {
      value = value / 1000;
      metric = metrics.shift() || '?';
    }

    return $filter('number')(value, options.precision) + metric;
  };
}]);
