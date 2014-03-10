describe('services', function() {
  describe('api', function() {
    var api, $httpBackend;

    beforeEach(function() {
      module('openBallotServices');
      inject(function(_api_, _$httpBackend_) {
        api = _api_;
        $httpBackend = _$httpBackend_;

        $httpBackend.whenGET(/^\/data\/contracts.csv/).respond("" +
          "Ballot Measure Committee,Stance,Election,Ballot Measure,Consulting Firm,Services,Payment Received" + "\n" +
          "\"Committee to Save Laguna Honda Hospital, Yes on Prop A\",Yes,11/02/99,A,Robert Barnes & Associates,Campaign consulting focusing on outreach; campaign management,$0.00"
        );
      });
    });

    describe('contracts', function () {
      it('exists', function () {
        expect(api).to.have.property('contracts');
      });

      describe('query', function() {
        var response;

        beforeEach(function() {
          response = api.contracts.query();
          $httpBackend.expectGET('/data/contracts.csv');
          $httpBackend.flush();
        });

        it('returns an array', function() {
          expect(response.length).to.equal(1);
        });

        describe('contract', function() {
          var contract;
          beforeEach(function() {
            contract = response[0];
          });

          it('has commitee', function() {
            expect(contract).to.have.property('Ballot Measure Committee');
            expect(contract['Ballot Measure Committee']).to.equal('Committee to Save Laguna Honda Hospital, Yes on Prop A');
          });
        });
      });
    });
  });
});

