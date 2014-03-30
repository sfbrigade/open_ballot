require('highcharts-ng');
require('./controllers');
require('./directives');
require('./services');

var app = angular.module('openBallotApp', [
  'ngResource',
  'ui.router',
  'highcharts-ng',

  'openBallotControllers',
  'openBallotDirectives',
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
    })
    .state('ballot', {
      url: '/ballots/:id',
      templateUrl: 'partials/ballot.tpl.html',
      controller: 'ballotController'
    })
    .state('contributions', {
      url: '/ballots/:ballot_id/contributions',
      templateUrl: 'partials/ballot_contributions.tpl.html',
      controller: 'ballotContributionsController'
    });
}]);
