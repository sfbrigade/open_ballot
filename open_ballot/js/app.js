require('./controllers');

var app = angular.module('openBallotApp', [
      'ngRoute',
      'openBallotControllers'
    ]);

app.config(['$routeProvider', function($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: 'partials/helloworld.html',
      controller: 'helloworldController'
    });
}]);
