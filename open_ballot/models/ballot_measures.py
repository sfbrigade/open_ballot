from base import BaseModel
from django.db import models

class BallotMeasure(BaseModel):
	class Meta:
		app_label = 'open_ballot'

	name = models.CharField(max_length=200)
	prop_id = models.CharField(max_length=200)
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

	name = models.CharField(max_length=200)
	percent_required = models.DecimalField(max_digits=2, decimal_places=2)

class Tag(BaseModel):
	class Meta:
		app_label = 'open_ballot'

	name = models.CharField(max_length=200)

class Committee(BaseModel):
	class Meta:
		app_label = 'open_ballot'

	name = models.CharField(max_length=200)
	date = models.DateTimeField()
	money_raised = models.FloatField()

	stance = models.ForeignKey('Stance')

class Stance(BaseModel):
	class Meta:
		app_label = 'open_ballot'

	voted_yes = models.BooleanField()

	ballot_measure = models.ForeignKey('BallotMeasure')

class Consultant(BaseModel):
	class Meta:
		app_label = 'open_ballot'

	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	address = models.CharField(max_length=200)

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

	name = models.CharField(max_length=200)
	description = models.TextField()

class Donor(BaseModel):
	class Meta:
		app_label = 'open_ballot'

	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	address = models.CharField(max_length=200)
	latitude = models.FloatField()
	longitude = models.FloatField()

class Donation(BaseModel):
	class Meta:
		app_label = 'open_ballot'

	amount = models.FloatField()

	donor = models.ForeignKey('Donor')
	committee = models.ForeignKey('Committee')