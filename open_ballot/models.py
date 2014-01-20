# coding: utf-8
from sqlalchemy import Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.dialects.postgresql import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import (
    scoped_session, sessionmaker,
    relationship,
    backref,
    )
from zope.sqlalchemy import ZopeTransactionExtension

import datetime
from dateutil.parser import parse as date_parse

class BallotBase(object):
    id = Column(UUID, primary_key=True,
        server_default='uuid_generate_v4()')
    created = Column(DateTime(True), nullable=False,
        server_default='now()')
    updated = Column(DateTime(True), nullable=False,
        server_onupdate='now()', server_default='now()')

    @classmethod
    def get_by_id(cls, id):
        return DBSession.query(cls).filter(cls.id==id).first()


Base = declarative_base(cls=BallotBase)
metadata = Base.metadata

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

class BallotMeasure(Base):
    __tablename__ = u'ballot_measure'

    _name = Column('name', Text)
    prop_id = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    num_yes = Column(Integer)
    num_no = Column(Integer)
    passed = Column(Boolean)
    ballot_type_id = Column(ForeignKey(u'ballot_type.id'), index=True)
    election_id = Column(ForeignKey(u'election.id'), index=True)

    ballot_type = relationship(u'BallotType', backref=backref('ballotmeasures'))
    election = relationship(u'Election', backref=backref('ballotmeasures'))

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name.title()

class BallotMeasureTag(Base):
    __tablename__ = u'ballot_measure_tags'
    __table_args__ = (
        UniqueConstraint(u'ballot_measure_id', u'tag_id'),
    )

    ballot_measure_id = Column(ForeignKey(u'ballot_measure.id'), nullable=False, index=True)
    tag_id = Column(ForeignKey(u'tag.id'), nullable=False, index=True)

    ballot_measure = relationship(u'BallotMeasure', backref=backref('ballotmeasuretags'))
    tag = relationship(u'Tag', backref=backref('ballotmeasuretags'))


class BallotType(Base):
    __tablename__ = u'ballot_type'

    name = Column(Text, nullable=False)
    percent_required = Column(Numeric(2, 2), nullable=False)


class Committee(Base):
    __tablename__ = u'committee'

    name = Column(Text, nullable=False)
    filer_id = Column(Text)
    sponsor = Column(Text, nullable=False)
    election_id = Column(ForeignKey(u'election.id'), index=True)

    election = relationship(u'Election', backref=backref('committees'))


class Consultant(Base):
    __tablename__ = u'consultant'

    name = Column(Text, nullable=False)
    address = Column(Text, nullable=False)


class Contract(Base):
    __tablename__ = u'contract'

    payment = Column(Float, nullable=False)
    consultant_id = Column(ForeignKey(u'consultant.id'), nullable=False, index=True)
    service_id = Column(ForeignKey(u'service.id'), nullable=False, index=True)
    committee_id = Column(ForeignKey(u'committee.id'), nullable=False, index=True)

    committee = relationship(u'Committee', backref=backref('contracts'))
    consultant = relationship(u'Consultant', backref=backref('contracts'))
    service = relationship(u'Service', backref=backref('contracts'))


class Donation(Base):
    __tablename__ = u'donation'

    amount = Column(Float, nullable=False)
    transaction_date = Column(Date, nullable=False)
    donor_id = Column(ForeignKey(u'donor.id'), nullable=False, index=True)
    committee_id = Column(ForeignKey(u'committee.id'), nullable=False, index=True)

    committee = relationship(u'Committee', backref=backref('donations'))
    donor = relationship(u'Donor', backref=backref('donations'))


class Donor(Base):
    __tablename__ = u'donor'
    __table_args__ = (
        UniqueConstraint(u'first_name', u'last_name', u'latitude', u'longitude'),
    )

    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    address = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    employer_id = Column(ForeignKey(u'employer.id'), index=True)

    employer = relationship(u'Employer', backref=backref('donors'))


class Election(Base):
    __tablename__ = u'election'

    date = Column(Date, nullable=False)

    @classmethod
    def get_or_create(cls, election_date):
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

class Employer(Base):
    __tablename__ = u'employer'

    name = Column(Text, nullable=False)


class Service(Base):
    __tablename__ = u'service'

    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)


class Stance(Base):
    __tablename__ = u'stance'
    __table_args__ = (
        UniqueConstraint(u'committee_id', u'ballot_measure_id'),
    )

    voted_yes = Column(Boolean, nullable=False)
    committee_id = Column(ForeignKey(u'committee.id'), nullable=False, index=True)
    ballot_measure_id = Column(ForeignKey(u'ballot_measure.id'), nullable=False, index=True)

    ballot_measure = relationship(u'BallotMeasure', backref=backref('stances'))
    committee = relationship(u'Committee', backref=backref('stances'))


class Tag(Base):
    __tablename__ = u'tag'

    name = Column(Text, nullable=False)

    @classmethod
    def get_or_create(cls, name):
        tag = DBSession.query(cls).filter(cls.name==name).first()
        if not tag:
            tag = cls(name=name)
            DBSession.add(tag)
            DBSession.flush()

        return tag
