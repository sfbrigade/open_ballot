var csv = require('csv-string'),
    lazy = require('lazy.js');

var services = angular.module('openBallotServices');

services.service('api', ['$resource', function($resource) {
  simpleDataResourceFactory = function(url) {
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

  return {
    ballot_history: simpleDataResourceFactory('/data/ballot_history'),
    contracts: simpleDataResourceFactory('/data/contracts'),
    committees: $resource('/ajax/ballots/:ballot_id/committees'),
    donations: simpleDataResourceFactory('/data/donations')
  };

}]);
