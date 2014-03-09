require('./controllers');
require('./services');

var app = angular.module('openBallotApp', [
  'ngRoute',
  'ngResource',
  'openBallotControllers',
  'openBallotServices'
]);

app.config(['$routeProvider', function($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: 'partials/helloworld.html',
      controller: 'helloworldController'
    });
}]);
