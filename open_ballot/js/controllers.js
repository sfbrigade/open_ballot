var controllers = angular.module('openBallotControllers', []);

controllers.controller('helloworldController', ['$scope', function($scope) {
  $scope.text = 'hello world';
}]);
