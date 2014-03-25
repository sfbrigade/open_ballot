var lazy = require('lazy.js');
var controllers = angular.module('openBallotControllers');

controllers.controller('ballotContributionsController', ['$scope', 'api', '$stateParams', function($scope, api, $stateParams) {
  var committieeData, stanceData, colors, committees, color;
  colors = Highcharts.getOptions().colors;

  function _stance(stance) {
    if (stance === "Yes") {
      return "Supports";
    } else if (stance === "No") {
      return "Against";
    } else {
      return "Unknown";
    }
  }

  function _payment(payment) {
    var p, m;
    m = payment.replace(/[^\d]/g, '');
    p = parseInt(m);
    return Number.isNaN(p) ? 0 : p;
  }

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

  $scope.committees = [];
  $scope.contributions = {
    options: {
      chart: {type: 'pie'}
    },
    series: [],
    title: {text: 'Contributions'},
    loading: false
  };

  //TODO: only fetch the contracts we need
  api.contracts.query().$promise.then(function(data){
    var committee = null;
    for (var i = 0; i < data.length; i++) {
      var contract = data[i];
      if (committee === null ||
        (contract["Ballot Measure"] !== null && contract["Ballot Measure"] != committee["Ballot Measure"])) {

        // Next committee
        committee = {
          name: contract["Ballot Measure Committee"],
          stance: _stance(contract["Stance"]),
          y: _payment(contract["Payment Received"]),
          color: _color(_stance(contract["Stance"]))
        };
        $scope.committees.push(committee);
      } else {
        committee.y += _payment(contract["Payment Received"]); // Add the contribution
      }
    }

    updateChart($scope.committees);
  });
}]);
