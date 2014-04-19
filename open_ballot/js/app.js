var app = angular.module('open_ballot', [
  'ui.router',
  'highcharts-ng',

  'open_ballot.directives',
  'open_ballot.services',
  'open_ballot.ballot_list',
  'open_ballot.ballots',
  'open_ballot.contracts'
]);

require('highcharts-ng');
require('./directives');
require('./services');
require('./filters');
require('./ballot_list');
require('./ballots');
require('./contracts');

app.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {

  $urlRouterProvider.otherwise("/");
  $stateProvider
    .state('home', {
      url: '/',
      templateUrl: 'partials/index.tpl.html'
    })
    .state('contracts', {
      url: '/contracts',
      templateUrl: 'partials/contracts.tpl.html',
      controller: 'contractsController'
    })
    .state('ballot_list', {
      url: '/ballots',
      templateUrl: 'partials/ballot_list/index.tpl.html',
      controller: 'ballotsController'
    });
}]);
