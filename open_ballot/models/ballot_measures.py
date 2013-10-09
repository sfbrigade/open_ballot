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
        unique_together = ('name', 'year')

    name = models.CharField(max_length=300)
    year = models.IntegerField()
    money_raised = models.FloatField(null=True)

    stance = models.ForeignKey('Stance', null=True)

    @classmethod
    def get_or_create(cls, name, year):
        try:
            return Committee.objects.get(name=name, year=year)
        except Committee.DoesNotExist:
            new_committee = Committee(name=name, year=year)
            new_committee.save()
            return new_committee

class Stance(BaseModel):
    class Meta:
        app_label = 'open_ballot'

    voted_yes = models.BooleanField()

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

class Donation(BaseModel):
    class Meta:
        app_label = 'open_ballot'

    amount = models.FloatField()
    transaction_date = models.DateField()

    donor = models.ForeignKey('Donor')
    committee = models.ForeignKey('Committee')