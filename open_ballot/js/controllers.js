var controllers = angular.module('openBallotControllers', ['openBallotServices']);

controllers.controller('contractsController', ['$scope', 'api', function($scope, api) {
  $scope.contracts = api.contracts.query();
  $scope.text = 'hello world';
}]);
