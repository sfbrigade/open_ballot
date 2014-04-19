lazy = require('lazy.js');
var app = angular.module('open_ballot.ballot_list', ['open_ballot.services']);

app.controller('ballotsController', ['$scope', 'api', function($scope, api) {
  $scope.ballots = api.ballots.query();
  $scope.ballots.$promise.then(function (ballots) {
    lazy(ballots)
      .each(function (ballot) {
        api.ballots.get({ballot_id: ballot.id}).$promise.then(function (b) {
          ballot.committees = b.committees;
        });
      });
  });
}]);
