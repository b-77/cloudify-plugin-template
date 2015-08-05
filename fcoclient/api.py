# coding=UTF-8

"""Abstraction of FCO API in the form of a Python wrapper."""

import fcoclient.clients as clients
import rest_types.enums as enums
import rest_types.cobjects as cobjects
import rest_types.endpoints as endpoints

import json
import inspect


class REST(object):

    """FCO REST API Interface."""

    def __init__(self, auth, logger):
        """Initialise FCP API Interface."""
        self.client = clients.get_client(auth, logger=logger)
        self.logger = logger

    def __getattr__(self, item):
        """Get relevant Endpoint object when accessed."""
        # back to wrapper for clarity?
        class Endpoint(object):
            def __call__(eself, *args, **kwargs):
                return self.query(item, *args, **kwargs)

        return Endpoint()

    def query(self, endpoint, parameters=None, data=None, validate=False,
              **kwargs):
        endpoint = endpoint[0].capitalize() + endpoint[1:]
        # TODO: exception handling
        endpoint = getattr(endpoints, endpoint)(parameters, data, **kwargs)
        type, url = endpoint.endpoint
        if type is endpoints.Verbs.PUT:
            fn = self.client.put
        elif type is endpoints.Verbs.GET:
            fn = self.client.get
        elif type is endpoints.Verbs.POST:
            fn = self.client.post
        elif type is endpoints.Verbs.DELETE:
            fn = self.client.delete
        else:
            raise TypeError('unsupported verb')

        payload = endpoint.untype()

        if not len(payload):
            payload = None
        else:
            payload = json.JSONEncoder().encode(payload)

        rv = fn(url, payload)

        if validate:
            return rv, endpoint.validate_return(rv)
        else:
            return endpoint.RETURNS.items()[0][1](rv)
