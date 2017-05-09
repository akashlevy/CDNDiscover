'''Retrieve Alexa top sites'''

# Standard library imports
import hmac
import json
from hashlib import sha1
from urllib import quote_plus
from base64 import b64encode
from datetime import datetime

# Custom library imports
import requests
import xmltodict

# Get Alexa keys
AWS_ACCESS_KEY, AWS_SECRET_KEY = open("alexa_keys.txt").read().splitlines()


class AlexaTopSites(object):
    '''A class for getting Alexa top sites'''
    def __init__(self, access_key_id, secret_access_key):
        '''Initialize getter'''
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key

    def _get_url(self, start=1, count=100, country=None):
        '''Get URL to request'''
        service_host = 'ats.amazonaws.com'
        query = {
            'Action': 'TopSites',
            'AWSAccessKeyId': self.access_key_id,
            'Timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            'ResponseGroup': 'Country',
            'Start': start,
            'Count': count,
            'CountryCode': country,
            'SignatureVersion': '2',
            'SignatureMethod': 'HmacSHA1'
        }
        if country is None:
            del query['CountryCode']
        join = lambda x: '='.join([x[0], quote_plus(str(x[1]))])
        query_str = '&'.join(sorted(map(join, query.iteritems())))
        sign_str = 'GET\n%s\n/\n%s' % (service_host, query_str)
        signature = hmac.new(self.secret_access_key, sign_str, sha1).digest()
        query_str += '&Signature=' + quote_plus(b64encode(signature).strip())
        url = 'http://%s/?%s' % (service_host, query_str)
        return url

    def _get_alexa_sites(self, start=1, count=100, country=None):
        '''Make request and return top sites'''
        content = requests.get(self._get_url(start, count, country)).text
        nss = {
            'http://alexa.amazonaws.com/doc/2005-10-05/': None,
            'http://ats.amazonaws.com/doc/2005-11-21': None
        }
        res = xmltodict.parse(content, process_namespaces=True, namespaces=nss)
        res = res['TopSitesResponse']['Response']['TopSitesResult']['Alexa']
        res = res['TopSites']['Country']['Sites']['Site']
        return res

    def get_alexa_sites_global(self, start=1, count=100):
        '''Make request and return global top sites'''
        return self._get_alexa_sites(start, count)

    def get_alexa_sites_us(self, start=1, count=100):
        '''Make request and return U.S. top sites'''
        return self._get_alexa_sites(start, count, 'US')



