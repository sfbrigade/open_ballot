var app = angular.module('open_ballot.ballots', ['ui.router', 'highcharts-ng', 'openBallotServices']);

require('./spend');
require('../controllers/ballot');

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
        '': {
          templateUrl: 'partials/ballot_view/main.tpl.html',
          controller: 'ballot.controller'
        },
        'ballot.votes': {
          templateUrl: 'partials/ballot.tpl.html',
          controller: 'ballotController'
        },
        'ballot.spent': {
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

app.controller('ballot.controller', ['$rootScope', '$scope', 'animateNumber', 'ballot', function ($rootScope, $scope, animateNumber, ballot) {
  $scope.ballot = ballot;
  ballot.$promise.then(function (ballot) {
    ballot.animations = ballot.animations || {};
    ballot.animations.num_yes = animateNumber(ballot.num_yes);
    $rootScope.title = "Prop " + ballot.prop_id + ": " + ballot.name;
  });
}]);
