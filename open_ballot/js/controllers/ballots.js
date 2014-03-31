lazy = require('lazy.js');
var controllers = angular.module('openBallotControllers');

controllers.controller('ballotsController', ['$scope', 'api', function($scope, api) {
  $scope.ballots = api.ballots.query();
  $scope.ballots.$promise.then(function (ballots) {
    lazy(ballots)
      .each(function (ballot) {
        api.committees.query({ballot_id: ballot.id}).$promise.then(function (committees) {
          ballot.committee_count = committees.length;
        });
      });
  });
}]);
