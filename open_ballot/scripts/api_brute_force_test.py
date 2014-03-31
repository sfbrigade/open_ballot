if __name__ == '__main__':
    import requests
    from open_ballot.models import (DBSession, Donation, Donor, Consultant,
        Contract, BallotMeasure, Committee)
    from open_ballot import api_urls
    from paste.deploy.loadwsgi import appconfig
    from sqlalchemy import engine_from_config
    import os

    current_directory = os.path.dirname(os.path.realpath(__file__))
    settings = appconfig('config:' + os.path.join(current_directory, '../../development.ini'))

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    host = 'http://localhost:6543'

    try:
        for ListClass in api_urls.ListUrl.__subclasses__():
            response = requests.get(host+ListClass.get_list_url())
            response.json()

        url_reference = {
            Donation: api_urls.DonationUrl,
            Donor: api_urls.DonorUrl,
            Consultant: api_urls.ConsultantUrl,
            Contract: api_urls.ContractUrl,
            Committee: api_urls.CommitteeUrl
        }

        for model, url_class in url_reference.iteritems():
            for obj in model.all():
                response = requests.get(host+url_class.get_resource_url(obj.id))
                response.json()
    except ValueError:
        import ipdb;ipdb.set_trace()
        raise
