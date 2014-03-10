require('./controllers');
require('./services');

var app = angular.module('openBallotApp', [
  'ngResource',
  'ui.router',

  'openBallotControllers',
  'openBallotServices'
]);

app.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {

  $urlRouterProvider.otherwise("/contracts");
  $stateProvider
    .state('contracts', {
      url: '/contracts',
      templateUrl: 'partials/contracts.tpl.html',
      controller: 'contractsController'
    })
    .state('ballots', {
      url: '/ballots',
      templateUrl: 'partials/ballots.tpl.html',
      controller: 'ballotsController'
    });
}]);
