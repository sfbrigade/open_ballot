from django.core.management.base import BaseCommand, CommandError
import csv, re, os
from configparser import ConfigParser
from dateutil import parser

from open_ballot.models import Donor, Committee, Donation

class Command(BaseCommand):
    args = '< filename >'
    help = """
    Input a CSV file from SFEthics.org, and optionally a .ini settings
    file.  This defines the CSV headers and maps them to attributes
    of our models.
    """

    def handle(self, filename, settings=None, *args, **kwargs):
        if not filename.endswith('.csv'):
            raise Exception('Please input a csv file.')            
        #os.getcwd() gives the current directory that this
        #script is being run from
        #This way, the file's path can be accurately determined
        csv_file_path = os.path.join(os.getcwd(), filename)

        if settings:
            if not settings.endswith('.ini'):
                raise Exception('Settings must be a .ini file.')

            settings_file = os.path.join(os.getcwd(), settings)
        else:
            settings_file = os.path.join(os.path.dirname(__file__), 'headers.ini')


        #Open config file to get the csv headers to properly
        #parse the csv file
        configparser = ConfigParser()
        configparser.read_file(open(settings_file))

        headers = {
            'amount': configparser.get('headers', 'amount'),
            'committee_name': configparser.get('headers', 'committee_name'),
            'first_name': configparser.get('headers', 'first_name'),
            'last_name': configparser.get('headers', 'last_name'),
            'transaction_date': configparser.get('headers', 'transaction_date'),
            'location': configparser.get('headers', 'location')
        }

        reader = csv.DictReader(open(csv_file_path))

        for row in reader:
            location = row[headers['location']]

            if not location:
                continue

            location = location.replace('(', '').replace(')', '').split(',')

            latitude, longitude = float(location[0]), float(location[1])
            first_name = row[headers['first_name']]
            last_name = row[headers['last_name']]

            donor = Donor.get_or_create(first_name=first_name, last_name=last_name,
                latitude=latitude, longitude=longitude)

            committee_name = row[headers['committee_name']]
            transaction_date = parser.parse(row[headers['transaction_date']]) 
            year = transaction_date.year

            committee = Committee.get_or_create(name=committee_name, year=year)

            #TODO: Figure out how to spot duplicate donations...
            Donation(
                donor=donor,
                committee=committee,
                amount=float(row[headers['amount']].replace('$', '')),
                transaction_date=transaction_date
                ).save()