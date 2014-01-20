from types import NoneType
import datetime
from dateutil.parser import parse as date_parse

from open_ballot.models import (BallotMeasure, Election, Tag, BallotType)

class DummyModel(object):
    def __setattr__(self, name, value):
        current_val = getattr(self, name)

        if type(current_val) == type:
            current_type = current_val
        else:
            current_type = type(current_type)

        def convert_to_unicode(string):
            return unicode(string, 'utf-8')

        def convert_to_int(string):
            return int(string)

        def convert_to_float(string):
            return float(string)

        def convert_to_date(string):
            parsed_date = date_parse(string)
            return date(year=parsed_date.year, month=parsed_date.month,
                day=parsed_date.day)

        def convert_to_datetime(string):
            return date_parse(string)

        converters = {
            unicode: convert_to_unicode,
            int: convert_to_int,
            float: convert_to_float,
            datetime.date: convert_to_date,
            datetime.datetime: convert_to_datetime
        }

        try:
            value = converters[current_type](value)
        except KeyError:
            pass

        object.__setattr__(self, name, value)

    def to_db_prepare(self):
        keys = []
        for key, value in self.__dict__:
            if type(value) == type:
                keys.append(key)

        for key in keys:
            setattr(self, key, None)

class DummyBallot(DummyModel):
    def __init__(self):
        self.name = unicode
        self.prop_id = unicode
        self.description = unicode
        self.num_yes = float
        self.num_no = float
        self.passed = None
        self.ballot_type = None
        self.election = None
        self.tags = []

    def add_tag(self, name):
        self.tags.append(Tag.get_or_create(name))

    def to_db(self):
        self.to_db_prepare()

class DummyContract(DummyModel):
    def __init__(self):
        self.name = unicode
        self.filer_id = unicode
        self.sponsor = unicode
        self.election = None

class DummyDonation(DummyModel):
    def __init__(self):
        self.amount = None
        self.transaction_date = None
        self.donor = None
        self.committee = None
