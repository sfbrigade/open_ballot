var app = angular.module('open_ballot.contracts', ['open_ballot.services']);

app.controller('contractsController', ['$scope', 'api', function($scope, api) {
  $scope.contracts = api.contracts.query();
  $scope.text = 'hello world';
}]);
