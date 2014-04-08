var lazy = require('lazy.js');
var controllers = angular.module('openBallotControllers');

controllers.controller('ballotController', ['$scope', 'api', '$stateParams', function($scope, api, $stateParams) {
  api.ballot_history.query().$promise.then(function(data){
    // TODO: This should be in the api service and not re-query for ballots
    $scope.ballot = lazy(data).findWhere({'ID': $stateParams.id});
    $scope.ballot_config.series[0].data.push(['Vote_Counts_Yes', parseInt($scope.ballot.Vote_Counts_Yes)], ['Vote_Counts_No', parseInt($scope.ballot.Vote_Counts_No)]);
    console.log($scope.ballot);
  });

  $scope.ballot_config = {
    options: {
      chart: {type: 'pie'}
    },
      series: [{
            type: 'pie',
            name: 'Browser share',
            innerSize: '50%',
            data: []
        }],
    

    title: {text: 'Contributions'},
    loading: false
  };


}]);


    
