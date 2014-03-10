var controllers = angular.module('openBallotControllers');

controllers.controller('ballotsController', ['$scope', 'api', function($scope, api) {
  $scope.ballots = api.ballot_history.query();
  $scope.text = 'hello ballots';
}]);
