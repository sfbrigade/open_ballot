var lazy = require('lazy.js');
var app = angular.module('open_ballot.ballots');

app.controller('ballotContributionsController', ['$scope', '$q', 'api', 'animateNumber', 'ballot', '$stateParams', function($scope, $q, api, animateNumber, ballot, $stateParams) {
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
      })
      .reverse()
      .toArray();

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
      size: '60%',
      dataLabels: {
        color: 'white',
        distance: -40
      }
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

  $scope.committees = [];
  $scope.contributions = {
    options: {
      chart: {type: 'pie'}
    },
    series: [],
    title: {text: 'Contributions'},
    loading: false
  };


  committees = [];
  ballot.$promise.then(function (ballot) {
    ballot.animations = ballot.animations || {};
    ballot.total_spent = 0;
    ballot.donation_total = 0;

    committees = lazy(ballot.committees)
      .map(function (committee) {
        return api.committees.get({id: committee.id}).$promise;
      })
      .toArray();

    $q.all(committees).then(function (data) {
      data.forEach(function (committee) {
        var stance = lazy(committee.ballot_measures)
        .find(function (ballot_measure) {
          return ballot_measure.id === ballot.id;
        }).stance.voted_yes ? "Supports" : "Against";

        ballot.total_spent += committee.total_spent;
        ballot.donation_total += committee.donation_total;
        $scope.committees.push({
          name: committee.name,
          stance: stance,
          y: committee.total_spent,
          color: Highcharts.Color(_color(stance)).brighten(0.2).get()
        });
      });

      // Big numbers
      ballot.animations.donation_total = animateNumber(ballot.donation_total);
      ballot.animations.total_spent = animateNumber(ballot.total_spent);

      updateChart($scope.committees);
    });
  });
}]);
