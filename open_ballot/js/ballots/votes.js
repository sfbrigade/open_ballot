var lazy = require('lazy.js');
var app = angular.module('open_ballot.ballots');

app.controller('votesController', ['$scope', 'api', '$stateParams', 'ballot', function($scope, api, $stateParams, ballot) {
  ballot.$promise.then(function (ballot) {
    $scope.ballot = ballot;
    $scope.ballot_config.series.push({
        type: 'pie',
        name: 'to come',
        innerSize: '50%',
        data: [['Yes votes', parseInt($scope.ballot.num_yes)], ['No votes', parseInt($scope.ballot.num_no)]]
    });
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
      chart: {type: 'pie'}
    },
    series: [],
    title: {text: 'Vote count'},
    loading: false
  };
}]);
