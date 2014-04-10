var directives = angular.module('openBallotDirectives', []);

directives.directive('animatedNumberDirective', ['$interval', '$filter', function ($interval, $filter) {
  return {
    restrict: 'E',
    template: '<span>{{filterFn(animatedValue)}}</span>',
    scope: {
      originalValue: '=animate'
    },
    link: function (scope, elem, attrs) {
      var delay = 1200;
      var update = 50;
      var turns = 0;
      var totalTurns = delay / update;
      scope.filterFn = function (x) {return x;};

      if (attrs.filter) {
        scope.filterFn = $filter(attrs.filter);
      }

      var timeout = $interval(function () {
        scope.animatedValue = scope.originalValue * (turns++) / totalTurns;
        if (turns > totalTurns) {
          $interval.cancel(timeout);
          scope.animatedValue = scope.originalValue;
        }
      }, update);
    }
  };
}]);
