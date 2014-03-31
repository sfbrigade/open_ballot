VERSION = '/v1'
PREFIX = '/api' + VERSION

class ListUrl(object):
    LIST = ''
    ROUTE = ''

    @classmethod
    def get_list_url(cls):
        return PREFIX + cls.LIST

    @classmethod
    def get_list_route(cls):
        return 'api_v1_' + cls.ROUTE + '_list'

class ResourceUrl(object):
    RESOURCE = ''
    ROUTE = ''

    @classmethod
    def get_resource_url(cls, id):
        return PREFIX + cls.RESOURCE.replace('{id}', id)

    @classmethod
    def get_routing_url(cls):
        return PREFIX + cls.RESOURCE

    @classmethod
    def get_resource_route(cls):
        return 'api_v1_' + cls.ROUTE + '_resource'

class BallotUrl(ResourceUrl, ListUrl):
    LIST = '/ballots'
    RESOURCE = '/ballots/{id}'
    ROUTE = 'ballots'

class CommitteeUrl(ResourceUrl):
    # LIST = '/committees'
    RESOURCE = '/committees/{id}'
    ROUTE = 'committees'

class DonorUrl(ResourceUrl):
    # LIST = '/donors'
    RESOURCE = '/donors/{id}'
    ROUTE = 'donors'

class DonationUrl(ResourceUrl):
    RESOURCE = '/donations/{id}'
    ROUTE = 'donations'

class ConsultantUrl(ResourceUrl):
    # LIST = '/consultants'
    RESOURCE = '/consultants/{id}'
    ROUTE = 'consultants'

class ContractUrl(ResourceUrl):
    RESOURCE = '/contracts/{id}'
    ROUTE = 'contracts'
