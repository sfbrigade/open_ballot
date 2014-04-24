lazy = require('lazy.js');
var app = angular.module('open_ballot.ballot_list', ['open_ballot.services']);

app.controller('ballotsController', ['$scope', 'api', function($scope, api) {
  $scope.ballots = api.ballots.query();
}]);
