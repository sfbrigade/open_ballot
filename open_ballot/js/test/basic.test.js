describe('app', function() {
  beforeEach(function() {
    module('open_ballot');
  });

  describe('scope', function() {
    var scope, controller;

    beforeEach(function() {
      scope = {};
      inject(function($controller) {
        // Initialize the controller
        $controller('contractsController', {
          $scope: scope
        });
      });
    });

    it('says hello world', function() {
      expect(scope.text).to.equal('hello world');
    });
  });
});
