var app = angular.module('open_ballot.ballots', ['ui.router', 'highcharts-ng', 'openBallotServices']);

require('./spend');

app.config(['$stateProvider', function($stateProvider) {
  $stateProvider
    .state('ballots_view', {
      abstract: true,
      url: '/ballots_view',
      templateUrl: 'partials/ballots_view.tpl.html'
    })
    .state('ballots_view.index', {
      url: '/:ballot_id',
      views: {
        '': {controller: 'ballot.controller'},
        'ballot.votes': {template: '<h3>Vote counts</h3>'},
        'ballot.spend': {
          templateUrl: 'partials/ballot_contributions.tpl.html',
          controller: 'ballotContributionsController'
        }
      },
      resolve: {
        ballot: ['$stateParams', 'api', function ($stateParams, api) {
          return api.ballots.get({ballot_id: $stateParams.ballot_id});
        }]
      }
    });
}]);

app.controller('ballot.controller', ['$rootScope', 'ballot', function ($rootScope, ballot) {
  ballot.$promise.then(function (ballot) {
    $rootScope.title = "Prop " + ballot.prop_id + ": " + ballot.description;
  });
}]);
