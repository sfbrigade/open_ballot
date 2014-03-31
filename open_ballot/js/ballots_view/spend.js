var lazy = require('lazy.js');
var app = angular.module('open_ballot.ballots');

app.controller('ballotContributionsController', ['$scope', 'api', '$stateParams', function($scope, api, $stateParams) {
  var committieeData, stanceData, colors, committees, color;
  colors = Highcharts.getOptions().colors;

  function _color(stance) {
    return {
      "Supports": "#2f7ed8",
      "Against": "#910000"
    }[stance] || "#8bbc21";
  }

  function updateChart(committees) {
    stanceCommitteePairs = lazy(committees)
      .groupBy('stance')
      .pairs()
      .sortBy(function(pair) {
        return pair[0]; // stance
      }).toArray();

    stanceData = lazy(stanceCommitteePairs)
      .map(function (pair) {
        var committees = pair[1],
            stance = pair[0];
        return {
          name: stance,
          y: lazy(committees)
            .sum(function (committee) {
              return committee.y;
            }),
          color: _color(stance)
        };
      }).toArray();

    committieeData = lazy(stanceCommitteePairs)
      .map(function (pair) {
        return pair[1]; // committees
      }).flatten()
      .toArray();

    $scope.contributions.series.push({
      name: 'Stance',
      data: stanceData,
      size: '60%'
    });
    $scope.contributions.series.push({
      name: 'Committees',
      data: committieeData,
      size: '80%',
      innerSize: '60%'
    });
    $scope.contributions.title = {text: 'Contributions'};
    $scope.contributions.loading = false;
  }

  $scope.total_spend = 0;
  $scope.committees = [];
  $scope.contributions = {
    options: {
      chart: {type: 'pie'}
    },
    series: [],
    title: {text: 'Contributions'},
    loading: false
  };

  api.committees.query({ballot_id: $stateParams.ballot_id}).$promise.then(function(data){
    data.forEach(function (committee) {
      var stance = committee.stance.voted_yes ? "Supports" : "Against";
      $scope.committees.push({
        name: committee.name,
        stance: stance,
        y: committee.total_spend,
        color: _color(stance)
      });
      $scope.total_spend += committee.total_spend;
    });
    updateChart($scope.committees);
  });
}]);
