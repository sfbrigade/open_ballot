var app = angular.module('open_ballot.ballots', ['ui.router', 'highcharts-ng', 'open_ballot.services']);

require('./spend');
require('./votes');

app.config(['$stateProvider', function($stateProvider) {
  $stateProvider
    .state('ballots', {
      abstract: true,
      url: '/ballots',
      templateUrl: 'partials/ballots/index.tpl.html'
    })
    .state('ballots.index', {
      url: '/:ballot_id',
      views: {
        'ballots.numbers': {
          templateUrl: 'partials/ballots/numbers.tpl.html',
          controller: 'numbersController'
        },
        'ballots.votes': {
          templateUrl: 'partials/ballots/votes.tpl.html',
          controller: 'votesController'
        },
        'ballots.spend': {
          templateUrl: 'partials/ballots/spend.tpl.html',
          controller: 'spendController'
        }
      },
      resolve: {
        ballot: ['$stateParams', 'api', function ($stateParams, api) {
          return api.ballots.get({ballot_id: $stateParams.ballot_id});
        }]
      }
    });
}]);

app.controller('numbersController', ['$rootScope', '$scope', 'animateNumber', 'ballot', function ($rootScope, $scope, animateNumber, ballot) {
  $scope.ballot = ballot;
  ballot.$promise.then(function (ballot) {
    ballot.animations = ballot.animations || {};
    ballot.animations.num_yes = animateNumber(ballot.num_yes);
    $rootScope.title = "Prop " + ballot.prop_id + ": " + ballot.name;
  });
}]);
