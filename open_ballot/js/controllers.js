var controllers = angular.module('openBallotControllers', ['openBallotServices']);

controllers.controller('contractsController', ['$scope', 'api', function($scope, api) {
  $scope.contracts = api.contracts.query();
  $scope.text = 'hello world';
}]);

controllers.controller('ballotsController', ['$scope', 'api', function($scope, api) {
  $scope.ballots = api.ballot_history.query();
  $scope.text = 'hello ballots';
}]);

controllers.controller('ballotController', ['$scope', 'api', '$stateParams', function($scope, api, $stateParams) {
  api.ballot_history.query().$promise.then(function(data){
    $scope.ballot = lazy(data).findWhere({'ID': $stateParams.id});
  });
}]);