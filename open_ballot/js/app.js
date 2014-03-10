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
      templateUrl: 'partials/contracts.tpl.html',
      controller: 'contractsController'
    })
    .when('/ballots', {
      templateUrl: 'partials/ballots.tpl.html',
      controller: 'ballotsController'
    });
}]);
