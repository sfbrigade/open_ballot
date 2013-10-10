from base import BaseModel
from django.db import models

class BallotMeasure(BaseModel):
    class Meta:
        app_label = 'open_ballot'

    name = models.CharField(max_length=300)
    prop_id = models.CharField(max_length=300)
    description = models.TextField()
    election_date = models.DateTimeField()
    num_yes = models.IntegerField()
    num_no = models.IntegerField()
    passed = models.BooleanField()

    ballot_type = models.ForeignKey('BallotType')
    tags = models.ManyToManyField('Tag')

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
    filer_id = models.CharField(max_length=10)

    @classmethod
    def get_or_create(cls, name, filer_id):
        try:
            return Committee.objects.get(name=name, filer_id=filer_id)
        except Committee.DoesNotExist:
            new_committee = Committee(name=name, filer_id=filer_id)
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

class Consultant(BaseModel):
    class Meta:
        app_label = 'open_ballot'

    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    address = models.CharField(max_length=300, blank=True)

class Contract(BaseModel):
    class Meta:
        app_label = 'open_ballot'

    payment = models.FloatField()

    consultant = models.ForeignKey('Consultant')
    service = models.OneToOneField('Service')
    committee = models.ForeignKey('Committee')

class Service(BaseModel):
    class Meta:
        app_label = 'open_ballot'

    name = models.CharField(max_length=300)
    description = models.TextField()

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