var app = angular.module('openBallotServices');

app.service('animateNumber', ['$interval', '$rootScope', function ($interval, $rootScope) {

  return function(originalValue) {
      console.log('animate ', originalValue);
      var delay = 1000;
      var update = 50;
      var turns = 1;
      var totalTurns = delay / update;
      var scope = {};

      scope.value = 0;
      var timeout = $interval(function () {
        scope.value = originalValue * (turns++) / totalTurns;
        if (turns > totalTurns) {
          $interval.cancel(timeout);
          scope.value = originalValue;
        }
      }, update);

      return scope;
  };
}]);
