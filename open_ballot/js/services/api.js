var csv = require('csv-string'),
    lazy = require('lazy.js');

var services = angular.module('openBallotServices');

services.service('api', ['$resource', function($resource) {
  var simpleDataResourceFactory = function(url) {
    url = url + ".csv";
    return $resource(url, null, {
      query: {
        method: 'GET',
        isArray: true,
        transformResponse: function (data) {
          parsed = csv.parse(data);
          headers = parsed.shift();
          return lazy(parsed).map(function(rowData) {
            var row = {};
            headers.forEach(function(key, idx) {
              row[key] = rowData[idx];
            });

            return row;
          }).toArray();
        }
      }
    });
  };

  var indexedDataResourceFactory = function (url) {
    return $resource(url, null, {
      query: {
        method: 'GET',
        isArray: true,
        transformResponse: function (data) {
          return lazy(angular.fromJson(data))
            .values()
            .toArray();
        }
      }
    });
  };

  return {
    ballots: indexedDataResourceFactory('/api/v1/ballots/:ballot_id', {ballot_id: '@ballot_id'}),
    ballot_history: simpleDataResourceFactory('/data/ballot_history'),
    contracts: simpleDataResourceFactory('/data/contracts'),
    committees: indexedDataResourceFactory('/api/v1/committees/:id', {id: '@id'}),
    donations: simpleDataResourceFactory('/data/donations')
  };

}]);
