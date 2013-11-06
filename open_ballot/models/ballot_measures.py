from base import BaseModel
from django.db import models, connection
from dateutil.parser import parse as date_parse
import re, datetime

MIN_YEAR = 1999

class BallotMeasure(BaseModel):
    class Meta:
        app_label = 'open_ballot'

    name = models.CharField(max_length=300, null=True)
    prop_id = models.CharField(max_length=3)
    description = models.TextField(blank=True)
    num_yes = models.IntegerField(null=True)
    num_no = models.IntegerField(null=True)
    passed = models.NullBooleanField(null=True)

    ballot_type = models.ForeignKey('BallotType', null=True)
    election = models.ForeignKey('Election', null=True)
    tags = models.ManyToManyField('Tag')

    @classmethod
    def get_or_create(cls, election, prop_id):
        try:
            return cls.objects.get(election=election,
            prop_id=prop_id)
        except BallotMeasure.DoesNotExist:
            new_ballot = cls(election=election, prop_id=prop_id)
            new_ballot.save()
            return new_ballot

    def save(self):
        if self.election:
            super(BallotMeasure, self).save()

class Election(BaseModel):
    class Meta:
        app_label = 'open_ballot'

    date = models.DateField()
    
    @classmethod
    def get_or_create(self, election_date_str):
        if not election_date_str:
            return None

        election_date_time = date_parse(election_date_str)
        election_date = datetime.date(year=election_date_time.year,
            month=election_date_time.month,
            day=election_date_time.day)
        try:
            return Election.objects.get(date=election_date)
        except Election.DoesNotExist:
            election = Election(date=election_date)
            election.save()
            return election

    def is_valid(self):
        return self.date.year >= MIN_YEAR

    def save(self):
        if self.is_valid():
            super(Election, self).save()

class BallotType(BaseModel):
    class Meta:
        app_label = 'open_ballot'

    name = models.CharField(max_length=300)
    percent_required = models.DecimalField(max_digits=2, decimal_places=2)

class Tag(BaseModel):
    class Meta:
        app_label = 'open_ballot'

    name = models.CharField(max_length=300)

class Committee(BaseModel):
    class Meta:
        app_label = 'open_ballot'

    name = models.CharField(max_length=300)
    filer_id = models.CharField(max_length=10, blank=True)
    sponsor = models.CharField(max_length=300)

    election = models.ForeignKey('Election', null=True)

    @classmethod
    def format_name(cls, name):
        stance_clause = re.compile(',\W+(yes|no)\W+on\W+prop\W[a-z]+$')

    @classmethod
    def get_or_create(cls, name, election=None):
        name = name.title()

        try:
            cursor = connection.cursor()
            params = [name]
            querystring = "SELECT id FROM open_ballot_committee\n"

            if election:
                querystring += "WHERE election_id=%s\n"
                params.insert(0, election.id)
            querystring += "ORDER BY similarity(name, %s) DESC;"

            cursor.execute(querystring, params)
            most_similar_id = cursor.fetchone()[0]
        except TypeError:
            pass
        else:
            most_similar = cls.objects.get(id=most_similar_id)
            #Run db-level query to find how strong of a match the input name
            #is to the existing committee name.
            cursor.execute(
                'SELECT similarity(%s, %s);',
                [name, most_similar.name])

            fuzzy_match = cursor.fetchone()[0]
            #Arbitrarily decided threshold of .6
            #import ipdb;ipdb.set_trace()
            if fuzzy_match >= .6:
                return most_similar

        #If no committees exist or if none with a similar name exist
        new_committee = Committee(name=name, election=election)
        new_committee.save()
        return new_committee

    def __repr__(self):
        return unicode('< Committee | Name: %s >' % self.name).encode('utf-8')

    def save(self):
        self.name = self.name.title()
        super(Committee, self).save()

class Stance(BaseModel):
    class Meta:
        app_label = 'open_ballot'
        unique_together = ('committee', 'ballot_measure')

    voted_yes = models.BooleanField()

    committee = models.ForeignKey('Committee')
    ballot_measure = models.ForeignKey('BallotMeasure')

    @classmethod
    def get(cls, committee, ballot_measure):
        try:
            return cls.objects.get(committee=committee,
                ballot_measure=ballot_measure)
        except Stance.DoesNotExist:
            return None

    @classmethod
    def get_or_create(cls, committee, ballot_measure, voted_yes):
        existing = cls.get(committee, ballot_measure)
        if existing:
            return existing

        new_stance = cls(committee=committee, ballot_measure=ballot_measure,
            voted_yes=voted_yes)
        new_stance.save()
        return new_stance

class Consultant(BaseModel):
    class Meta:
        app_label = 'open_ballot'

    name = models.CharField(max_length=300)
    address = models.CharField(max_length=300, blank=True)

    @classmethod
    def get_or_create(cls, name):
        try:
            cursor = connection.cursor()
            querystring = """
                SELECT id FROM open_ballot_consultant
                ORDER BY similarity(name, %s) DESC;
                """

            cursor.execute(querystring, [name])
            most_similar_id = cursor.fetchone()[0]
        except TypeError:
            pass
        else:
            most_similar = cls.objects.get(id=most_similar_id)
            #Run db-level query to find how strong of a match the input name
            #is to the existing committee name.
            cursor.execute(
                'SELECT similarity(%s, %s);',
                [name, most_similar.name])

            fuzzy_match = cursor.fetchone()[0]
            #Arbitrarily decided threshold of .7
            if fuzzy_match >= .7:
                return most_similar

        new_consultant = cls(name=name)
        new_consultant.save()
        return new_consultant

class Contract(BaseModel):
    class Meta:
        app_label = 'open_ballot'

    payment = models.FloatField()

    consultant = models.ForeignKey('Consultant')
    service = models.OneToOneField('Service')
    committee = models.ForeignKey('Committee')

    @classmethod
    def get(cls, consultant, committee, service_name='', service_description=''):
        try:
            return cls.objects.get(consultant=consultant,
                service__name=service_name, committee=committee,
                service__description=service_description)
        except Contract.DoesNotExist:
            return None

    @classmethod
    def get_or_create(cls, consultant, committee, payment,
        service_name='', service_description=''):
        existing = cls.get(consultant=consultant,
                service_name=service_name, committee=committee)

        if existing:
            return existing

        new_service = Service(name=service_name,
            description=service_description)
        new_service.save()
        new_contract = cls(consultant=consultant, committee=committee,
            payment=payment, service=new_service)

        new_contract.save()

        return new_contract

class Service(BaseModel):
    class Meta:
        app_label = 'open_ballot'

    name = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)

class Donor(BaseModel):
    class Meta:
        app_label = 'open_ballot'
        unique_together = ('first_name', 'last_name', 'latitude', 'longitude')

    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    latitude = models.FloatField()
    longitude = models.FloatField()

    employer = models.ForeignKey('Employer', null=True)

    @classmethod
    def get_or_create(cls, first_name, last_name, latitude, longitude, address=''):
        try:
            return Donor.objects.get(first_name=first_name, last_name=last_name,
                latitude=latitude, longitude=longitude, address=address)
        except Donor.DoesNotExist:
            new_donor = Donor(
                first_name=first_name,
                last_name=last_name,
                latitude=latitude,
                longitude=longitude,
                address=address
                )

            new_donor.save()
            return new_donor

    def __repr__(self):
        reprstring = '< Donor '
        #this should never happen
        if not self.first_name and not self.last_name:
            return reprstring + '>'

        if self.first_name:
            reprstring += '| First Name: ' + self.first_name

        if self.last_name:
            reprstring += '| Last Name: ' + self.last_name

        reprstring += ' >'

        return unicode(reprstring).encode('utf-8')

class Employer(BaseModel):
    class Meta:
        app_label = 'open_ballot'

    name = models.CharField(max_length=300)

    @classmethod
    def get_or_create(cls, name):
        try:
            cursor = connection.cursor()
            querystring = """
                SELECT id FROM open_ballot_employer
                ORDER BY similarity(name, %s) DESC;
                """

            cursor.execute(querystring, [name])
            most_similar_id = cursor.fetchone()[0]
        except TypeError:
            pass
        else:
            most_similar = cls.objects.get(id=most_similar_id)
            #Run db-level query to find how strong of a match the input name
            #is to the existing committee name.
            cursor.execute(
                'SELECT similarity(%s, %s);',
                [name, most_similar.name])

            fuzzy_match = cursor.fetchone()[0]
            #Arbitrarily decided threshold of .7
            if fuzzy_match >= .7:
                return most_similar

        new_employer = cls(name=name)
        new_employer.save()
        return new_employer

    def __repr__(self):
        return unicode('< Employer | Name: %s >' % self.name).encode('utf-8')

class Donation(BaseModel):
    class Meta:
        app_label = 'open_ballot'

    amount = models.FloatField()
    transaction_date = models.DateField()

    donor = models.ForeignKey('Donor')
    committee = models.ForeignKey('Committee')

    def __repr__(self):
        reprstring = '< Donation | Amount: %s | Date: %s' \
            % (str(self.amount), str(self.transaction_date))

        reprstring += '| Donor: %s %s' % (self.donor.first_name,
            self.donor.last_name)

        reprstring += '| Committee: %s >' % self.committee.name

        return unicode(reprstring).encode('utf-8')