describe('app', function() {
  beforeEach(function() {
    module('openBallotApp');
  });

  describe('scope', function() {
    var scope, controller;

    beforeEach(function() {
      scope = {};
      inject(function($controller) {
        // Initialize the controller
        $controller('helloworldController', {
          $scope: scope
        });
      });
    });

    it('says hello world', function() {
      expect(scope.text).to.equal('hello world');
    });
  });
});
