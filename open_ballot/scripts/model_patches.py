#These are methods used to monkey patch our models when parsing through csvs
#They are being placed here instead of in the model definition because
#these methods should not be used in any way in the application.
from dateutil.parser import parse as date_parse
from open_ballot.models import DBSession
import datetime

@classmethod
def election_get_or_create(cls, election_date):
    if type(election_date) in [str, unicode]:
        election_date = date_parse(election_date)

    if type(election_date) == datetime.datetime:
        election_date = datetime.date(year=election_date.year,
            month=election_date.month,
            day=election_date.day)

    election = DBSession.query(cls).filter(cls.date==election_date).first()

    if not election:
        election = cls(date=election_date)
        DBSession.add(election)

    return election

@classmethod
def tag_get_or_create(cls, name):
	tag = DBSession.query(cls).filter(cls.name==name).first()
	if not tag:
	    tag = cls(name=name)
	    DBSession.add(tag)
	    DBSession.flush()

	return tag

@classmethod
def consultant_get_or_create(cls, name):
	consultant = DBSession.query(cls).filter(cls.name==name).first()
	if not consultant:
	    consultant = cls(name=name)
	    DBSession.add(consultant)
	    DBSession.flush()

	return consultant

@classmethod
def employer_get_or_create(cls, name):
	employer = DBSession.query(cls).filter(cls.name==name).first()
	if not employer:
	    employer = cls(name=name)
	    DBSession.add(employer)
	    DBSession.flush()

	return employer

@classmethod
def committee_get_or_create(cls, name, election):
	committee = DBSession.query(cls).filter(
		cls.name==name.title(),
		cls.election==election
		).first()

	if not committee:
		committee = cls(name=name.title(), election=election)
		DBSession.add(committee)
		DBSession.flush()

	return committee

@classmethod
def ballot_measure_get_or_create(cls, prop_id, election):
	ballot_measure = DBSession.query(cls).filter(
		cls.prop_id==prop_id,
		cls.election==election
		).first()

	if not ballot_measure:
		ballot_measure = cls(prop_id=prop_id,
			election=election)
		DBSession.add(ballot_measure)
		DBSession.flush()

	return ballot_measure

@classmethod
def donor_get_or_create(cls, first_name, last_name, latitude, longitude):
	donor = DBSession.query(cls).filter(
		cls.first_name==first_name, cls.last_name==last_name,
		cls.latitude==latitude, cls.longitude==longitude
		).first()

	if not donor:
		donor = cls(first_name=first_name, last_name=last_name,
            latitude=latitude, longitude=longitude)
		DBSession.add(donor)
		DBSession.flush()

	return donor