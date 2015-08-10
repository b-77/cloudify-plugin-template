# coding=UTF-8

"""Abstraction of FCO API in the form of a Python wrapper."""

import fcoclient.clients as clients
import fcoclient.exceptions as exceptions
import resttypes.endpoints as endpoints

import json


class REST(object):

    """FCO REST API Interface."""

    def __init__(self, auth, logger):
        """Initialise FCP API Interface."""
        self.client = clients.get_client(auth, logger=logger)
        self.logger = logger

    def __getattr__(self, item):
        """Get relevant Endpoint object when accessed."""
        class Endpoint(object):
            def __call__(eself, *args, **kwargs):
                self.logger.debug('API endpoint {} requested'.format(item))
                return self.query(item, *args, **kwargs)

        return Endpoint()

    def query(self, endpoint, parameters=None, data=None, validate=False,
              **kwargs):
        endpoint = endpoint[0].capitalize() + endpoint[1:]
        endpoint = getattr(endpoints, endpoint)(parameters, data, **kwargs)
        type, url = endpoint.endpoint

        payload = endpoint.untype()
        if not len(payload):
            payload = None

        if type is endpoints.Verbs.PUT:
            fn = self.client.put
        elif type is endpoints.Verbs.GET:
            fn = self.client.get
        elif type is endpoints.Verbs.POST:
            fn = self.client.post
            if payload:
                payload = json.JSONEncoder().encode(payload)
        elif type is endpoints.Verbs.DELETE:
            fn = self.client.delete
        else:
            raise exceptions.NonRecoverableError('unsupported API verb')

        rv = fn(url, payload)

        if validate:
            return rv, endpoint.validate_return(rv)
        else:
            return endpoint.RETURNS.items()[0][1](rv)
