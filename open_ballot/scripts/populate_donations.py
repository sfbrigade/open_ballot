from open_ballot.models import Donor, Committee, Donation, Employer, Election, DBSession
import transaction
from model_patches import (election_get_or_create, consultant_get_or_create,
    committee_get_or_create, ballot_measure_get_or_create,
    donor_get_or_create, employer_get_or_create)
import csv, re, os
from configparser import ConfigParser
from dateutil import parser

Election.get_or_create = election_get_or_create
Employer.get_or_create = employer_get_or_create
Committee.get_or_create = committee_get_or_create
Donor.get_or_create = donor_get_or_create

def populate_donations(input_file):
    if type(input_file) in [str, unicode]:
        input_file = open(input_file)

    reader = csv.DictReader(input_file)
    settings_file = os.path.join(os.path.dirname(__file__), 'headers.ini')

    #Open config file to get the csv headers to properly
    #parse the csv file
    configparser = ConfigParser()
    configparser.read_file(open(settings_file))

    headers = {
        'amount': configparser.get('donations', 'amount'),
        'committee_name': configparser.get('donations', 'committee_name'),
        'first_name': configparser.get('donations', 'first_name'),
        'last_name': configparser.get('donations', 'last_name'),
        'transaction_date': configparser.get('donations', 'transaction_date'),
        'employer': configparser.get('donations', 'employer'),
        'election_date': configparser.get('donations', 'election_date'),
        'filer_id': configparser.get('donations', 'filer_id'),
        'location': configparser.get('donations', 'location')
    }

    DBSession.autoflush = False
    for row in reader:
        location = row[headers['location']]

        if not location:
            continue

        try:
            election = Election.get_or_create(row[headers['election_date']])
        except ValueError:
            #Some idiot put in some years as 57815.  I ain't dealing with that shit.
            continue

        location = location.replace('(', '').replace(')', '').split(',')

        latitude, longitude = float(location[0]), float(location[1])
        first_name = row[headers['first_name']]
        last_name = row[headers['last_name']]

        donor = Donor.get_or_create(first_name=first_name, last_name=last_name,
            latitude=latitude, longitude=longitude)

        employer_name = row[headers['employer']]

        if employer_name and not donor.employer:
            employer = Employer.get_or_create(name=employer_name)
            donor.employer = employer

        committee_name = row[headers['committee_name']]
        transaction_date = parser.parse(row[headers['transaction_date']]) 

        filer_id = row[headers['filer_id']]

        committee = Committee.get_or_create(name=committee_name,
            election=election)

        committee.filer_id = filer_id

        DBSession.add(Donation(
            donor=donor,
            committee=committee,
            amount=float(row[headers['amount']].replace('$', '')),
            transaction_date=transaction_date
            ))

        transaction.commit()
    DBSession.autoflush = True
