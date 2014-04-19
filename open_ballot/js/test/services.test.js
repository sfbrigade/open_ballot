describe('services', function() {
  describe('api', function() {
    var api, $httpBackend;

    beforeEach(function() {
      module('open_ballot.services');
      inject(function(_api_, _$httpBackend_) {
        api = _api_;
        $httpBackend = _$httpBackend_;

        $httpBackend.whenGET(/^\/data\/ballot_history.csv/).respond("" +
          "ID,ISSUE,PROPLetter,PROPTitle,Month,Day,Year,Date,Description,PASS_FAIL,Vote_Counts,Percent_Vote,Percent_Required_To_Pass,Kind,HowPlaced,Fullimage" + "\n" +
          "1,,1,Bonds issued for acquisition of public utilities,November,5,1907,05-Nov-07,\"Setting forth a proposal relating to bonds issued for the acquisition of public utilities, the registration thereof, and the levy of taxes to provide for the interest thereon and a sinking fund, and to bonds issued for the acquisition of land and the construction or acquisition of any permanent building or buildings, improvement or improvements.\",P,\"Yes: 23,257 No: 4,637\",Yes: 83.3% No: 16.7%,50%+1,Charter Amendment,Supervisors,November5_1907"
        );
      });
    });

    describe('ballot_history', function () {
      it('exists', function () {
        expect(api).to.have.property('ballot_history');
      });

      describe('query', function() {
        var response;

        beforeEach(function() {
          response = api.ballot_history.query();
          $httpBackend.expectGET('/data/ballot_history.csv');
          $httpBackend.flush();
        });

        it('returns an array', function() {
          expect(response.length).to.equal(1);
        });

        describe('ballot', function() {
          var ballot;
          beforeEach(function() {
            ballot = response[0];
          });

          it('has commitee', function() {
            expect(ballot).to.have.property('PROPTitle');
            expect(ballot['PROPTitle']).to.equal('Bonds issued for acquisition of public utilities');
          });
        });
      });
    });
  });
});

