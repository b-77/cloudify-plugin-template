# coding=UTF-8

"""Provides FCO API Client and decorator."""

from functools import wraps

from fcoclient.exceptions import (NonRecoverableError, RecoverableError)

import requests
import json
from requests import codes as rsc
from time import sleep


# REST Client default settings
REST_RETRY_COUNT = 5
REST_RETRY_DELAY = 30
REST_FAILURE_EXCEPTION = NonRecoverableError
REST_INTERNAL_RETRY = True

REST_API_VERSION = '5.0'
REST_HEADERS = {'content-type': 'application/json'}


# Configurable properties dict keys
PROP_CLIENT_CONFIG = 'auth'
PROP_CLIENT_TOKEN = 'token'
PROP_CLIENT_USERNAME = 'username'
PROP_CLIENT_PASSWORD = 'password'
PROP_CLIENT_API_USERNAME = 'api_uuid'
PROP_CLIENT_API_PASSWORD = 'password'
PROP_CLIENT_CUSTOMER = 'customer'
PROP_CLIENT_SERVICE_URL = 'url'
PROP_CLIENT_CA_CERT = 'ca_cert'

# Configurable kwargs keys for client
KW_PAYLOAD = 'payload'
KW_PATTERN = 'pattern'


def _rest_client_retry_and_auth(f):
    """Authenticate, log and retry requests."""
    @wraps(f)
    def wrapper(self, endpoint, data=None, **kwargs):
        # TODO: remove legacy block
        try:
            endpoint = endpoint.format(**kwargs.get('pattern', {}))
        except IndexError:
            NonRecoverableError('Unable to format endpoint, pattern: {}, '
                                'data: {}.'
                                .format(endpoint, kwargs.get(KW_PATTERN)))

        url = '{service_url}/rest/user/{api_version}/{endpoint}'.format(
            service_url=self.service_url, api_version=REST_API_VERSION,
            endpoint=endpoint)
        retry_count = self.retry_count
        payload = kwargs.get(KW_PAYLOAD)

        if data:
            payload = data

        while retry_count:
            terminate = False

            self.logger.info('Client function: %s', f.__name__)
            self.logger.info('Client URL: %s', url)
            self.logger.info('Client data: %s', data)
            r = f(self, url, payload, self.auth, self.headers,
                  self.verify)

            self.logger.debug('Client final URL: {}'.format(r.url))
            if len(r.content) > 60:
                self.logger.info('Content: {}'.format(r.content[:57] + '...'))
                self.logger.debug('Full content: {}'.format(r.content))
            else:
                self.logger.info('Content: {}'.format(r.content))
            self.logger.info('Status code: {}'.format(r.status_code))

            if r.status_code == rsc.accepted or r.status_code == rsc.ok:
                self.logger.debug('=' * 60)

                # TODO: convert everything to unicode?
                content = json.loads(r.content)

                def to_str(uni):
                    """Recursively turn unciode to str."""
                    if isinstance(uni, list):
                        gen = enumerate(uni)
                        string = [None]*len(uni)
                    elif isinstance(uni, dict):
                        gen = uni.items()
                        string = {}
                    elif isinstance(uni, basestring):
                        return str(uni)
                    else:
                        return uni
                    for k, v in gen:
                        string[to_str(k)] = to_str(v)
                    return string

                return to_str(content)

            if r.status_code == rsc.too_many_requests:
                error = 'Server busy (too many requests); waiting and ' \
                        'retrying {} more time(s).'.format(retry_count)
            elif r.status_code == rsc.bad_request:
                error = 'Server responded with bad request; will not ' \
                        'retry.'
                terminate = True
            elif r.status_code == rsc.not_implemented:
                error = 'Server responded with not implemented; will not' \
                        'retry.'
                terminate = True
            elif r.status_code == rsc.forbidden:
                error = 'Server responded with forbidden; will not retry.'
                terminate = True
            elif r.status_code == rsc.service_unavailable:
                error = 'Server responded with service unavailable; waiting ' \
                        'and retrying {} more time(s).'.format(retry_count)
            else:
                error = 'Other error; waiting and retrying {} more times(s).' \
                    .format(retry_count)

            try:
                error += ' (Message: {})'.format(
                    json.loads(r.content)['message'].strip())
            except KeyError:
                pass

            if terminate:
                self.logger.error(error)
                raise NonRecoverableError(error)
            elif self.internal_retry:
                self.logger.warn(error)
                retry_count -= 1
                sleep(self.retry_delay)
            else:
                self.logger.warn(error)
                raise RecoverableError(message=error,
                                       retry_after=self.retry_delay)

        self.logger.error('Giving up on client API request')
        REST_FAILURE_EXCEPTION('Giving up on client API request')

    return wrapper


# "Abstract" Client Classes

class APIClient(object):

    """FCO API Client."""

    REQUIRED_AUTH = [None]

    def __init__(self, auth, retry_count=REST_RETRY_COUNT,
                 retry_delay=REST_RETRY_DELAY, rest_headers=REST_HEADERS,
                 logger=None, internal_retry=REST_INTERNAL_RETRY):
        """Initialise FCO API Client."""
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.headers = rest_headers
        self.logger = logger
        self.internal_retry = internal_retry
        self.auth2 = auth

    @classmethod
    def can_handle(cls, auth):
        """Determine if a class is suitable to handle authentication type."""
        return all([auth.get(k) is not None for k in cls.REQUIRED_AUTH])


class RESTClient(APIClient):

    """FCO REST API Client."""

    REQUIRED_AUTH = [None]

    def __init__(self, *args, **kwargs):
        """Initialise FCO REST API Client."""
        super(RESTClient, self).__init__(*args, **kwargs)
        self.auth = ('', '')
        self.service_url = None
        self.verify = self.auth2.get(PROP_CLIENT_CA_CERT, True)

    @_rest_client_retry_and_auth
    def post(self, url, data, auth, headers, verify):
        """Make POST request to FCO API."""
        return requests.post(url, data, auth=auth, headers=headers,
                             verify=verify)

    @_rest_client_retry_and_auth
    def get(self, url, data, auth, headers, verify):
        """Make GET request to FCO API."""
        return requests.get(url, params=data, auth=auth, headers=headers,
                            verify=verify)

    @_rest_client_retry_and_auth
    def put(self, url, data, auth, headers, verify):
        """Make PUT request to FCO API."""
        return requests.put(url, data, auth=auth, headers=headers,
                            verify=verify)

    @_rest_client_retry_and_auth
    def delete(self, url, data, auth, headers, verify):
        """Make DELETE request to FCO API."""
        return requests.delete(url, params=data, auth=auth, headers=headers,
                               verify=verify)


# "Usable" Client Classes

class UserPassRESTClient(RESTClient):

    """Username and password based authentication REST client."""

    REQUIRED_AUTH = [PROP_CLIENT_USERNAME, PROP_CLIENT_PASSWORD,
                     PROP_CLIENT_CUSTOMER, PROP_CLIENT_SERVICE_URL]

    def __init__(self, *args, **kwargs):
        """Initialise UserPassRESTClient."""
        super(UserPassRESTClient, self).__init__(*args, **kwargs)
        try:
            self.auth = ('{}/{}'.format(self.auth2[PROP_CLIENT_USERNAME],
                                        self.auth2[PROP_CLIENT_CUSTOMER]),
                         self.auth2[PROP_CLIENT_PASSWORD])
            self.service_url = self.auth2[PROP_CLIENT_SERVICE_URL]
        except:
            raise NonRecoverableError('Invalid auth to create REST client: {}'
                                      .format(str(self.auth2)))


class APIUserPassRESTClient(RESTClient):

    """API user based authentication REST client."""

    REQUIRED_AUTH = [PROP_CLIENT_API_USERNAME, PROP_CLIENT_API_PASSWORD,
                     PROP_CLIENT_CUSTOMER, PROP_CLIENT_SERVICE_URL]

    def __init__(self, *args, **kwargs):
        """Initialise APIUserPassRESTClient."""
        super(APIUserPassRESTClient, self).__init__(*args, **kwargs)
        try:
            self.auth = ('{}/{}'.format(self.auth2[PROP_CLIENT_API_USERNAME],
                                        self.auth2[PROP_CLIENT_CUSTOMER]),
                         self.auth2[PROP_CLIENT_API_PASSWORD])
            self.service_url = self.auth2[PROP_CLIENT_SERVICE_URL]
        except:
            raise NonRecoverableError('Invalid auth to create REST client: {}'
                                      .format(str(self.auth2)))


class APITokenRESTClient(RESTClient):

    """API token based authentication REST client."""

    REQUIRED_AUTH = [PROP_CLIENT_TOKEN, PROP_CLIENT_SERVICE_URL]

    def __init__(self, *args, **kwargs):
        """Initialise APIUserPassRESTClient."""
        super(APITokenRESTClient, self).__init__(*args, **kwargs)
        try:
            self.auth = (self.auth2[PROP_CLIENT_TOKEN], '')
            self.service_url = self.auth2[PROP_CLIENT_SERVICE_URL]
        except:
            raise NonRecoverableError('Invalid auth to create REST client: {}'
                                      .format(str(self.auth2)))


# Client functions

def get_client(auth, logger):
    """Get an instance of the appropriate API Client."""
    for cls in UserPassRESTClient, APIUserPassRESTClient, APITokenRESTClient:
        if cls.can_handle(auth):
            logger.info('Using client: {}'.format(cls.__name__))
            return cls(auth, logger=logger)
    raise NonRecoverableError('Failed to determine FCO Client class based on '
                              'the following authentication arguments: {}'
                              .format(str(auth)))
