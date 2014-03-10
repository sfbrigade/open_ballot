var lazy = require('lazy.js');
var controllers = angular.module('openBallotControllers');

controllers.controller('ballotController', ['$scope', 'api', '$stateParams', function($scope, api, $stateParams) {
  api.ballot_history.query().$promise.then(function(data){
    // TODO: This should be in the api service and not re-query for ballots
    $scope.ballot = lazy(data).findWhere({'ID': $stateParams.id});
  });
}]);
