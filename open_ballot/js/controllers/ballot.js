var lazy = require('lazy.js');
var controllers = angular.module('openBallotControllers');

controllers.controller('ballotController', ['$scope', 'api', '$stateParams', function($scope, api, $stateParams) {
  api.ballot_history.query().$promise.then(function(data){
    // TODO: This should be in the api service and not re-query for ballots
    $scope.ballot = lazy(data).findWhere({'ID': $stateParams.id});
    $scope.ballot_config.series[0].data.push(['Yes votes', parseInt($scope.ballot.Vote_Counts_Yes)], ['No votes', parseInt($scope.ballot.Vote_Counts_No)]);
    console.log($scope.ballot);
  });

  $scope.ballot_config =
  {
    options: {
          plotOptions: {
            pie: {
                startAngle: -90,
                endAngle: 90
            }
        },

      chart: {
        type: 'pie'}
    },

      series: [{
            type: 'pie',
            name: 'to come',
            innerSize: '50%',
            data: []
        }],
    
    title: {text: 'Vote count'},
    loading: false
  };


}]);


    
