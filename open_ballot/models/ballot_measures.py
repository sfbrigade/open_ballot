from base import BaseModel
from django.db import models

class BallotMeasure(BaseModel):
    class Meta:
        app_label = 'open_ballot'

    name = models.CharField(max_length=300, null=True)
    prop_id = models.CharField(max_length=3)
    description = models.TextField(blank=True)
    election_date = models.DateField()
    num_yes = models.IntegerField(null=True)
    num_no = models.IntegerField(null=True)
    passed = models.NullBooleanField(null=True)

    ballot_type = models.ForeignKey('BallotType', null=True)
    tags = models.ManyToManyField('Tag')

    @classmethod
    def get_or_create(cls, election_date, prop_id):
        try:
            return cls.objects.get(election_date=election_date,
            prop_id=prop_id)
        except BallotMeasure.DoesNotExist:
            new_ballot = cls(election_date=election_date, prop_id=prop_id)
            new_ballot.save()
            return new_ballot

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
        unique_together = ('name', 'filer_id')

    name = models.CharField(max_length=300)
    filer_id = models.CharField(max_length=10, blank=True)

    @classmethod
    def get_or_create(cls, name):
        try:
            return Committee.objects.get(name=name)
        except Committee.DoesNotExist:
            new_committee = Committee(name=name)
            new_committee.save()
            return new_committee

    def __repr__(self):
        return '< Committee | Name: %s >' % self.name

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

    #If consultant is organization, we just use last_name
    first_name = models.CharField(max_length=300, blank=True)
    last_name = models.CharField(max_length=300)
    address = models.CharField(max_length=300, blank=True)

    @classmethod
    def get_or_create(cls, first_name, last_name, address=''):
        try:
            return cls.objects.get(first_name=first_name,
                last_name=last_name, address=address)
        except Consultant.DoesNotExist:
            new_consultant = cls(first_name=first_name, last_name=last_name,
                address=address)
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

        return reprstring

class Employer(BaseModel):
    class Meta:
        app_label = 'open_ballot'

    name = models.CharField(max_length=300)

    @classmethod
    def get_or_create(cls, name):
        try:
            employer = Employer.objects.get(name=name)
        except Employer.DoesNotExist:
            employer = Employer(name=name)
            employer.save()

        return employer

    def __repr__(self):
        return '< Employer | Name: %s >' % self.name

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

        return reprstring