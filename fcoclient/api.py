"""Abstraction of FCO API."""

import fcoclient.rest.enums as enums
import fcoclient.rest.cobjects as cobjects
import fcoclient.rest.endpoints as endpoints
import fcoclient.clients as clients
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

    def query(self, endpoint, parameters=None, data=None, validate=False, **kwargs):
        endpoint = endpoint[0].capitalize() + endpoint[1:]
        # TODO: more precise check of exception
        # try:
            # TODO: use instantiated endpoint for ease?
            # endpoint = getattr(endpoints, endpoint)
        endpoint = getattr(endpoints, endpoint)(parameters, data, **kwargs)
        # print endpoint
        # except:
        #    raise AttributeError('API does not support requested endpoint')
        # type, url = endpoint.get_endpoint(parameters, data)
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

        # print('ayy lmao api: ' + str(payload))

        # print('api call ' + str(fn))
        # print('api payload ' + str(payload))

        rv = fn(url, payload)

        # print('api result: ' + str(rv))

        if validate:
            return rv, endpoint.validate_return(rv)
        else:
            return endpoint.RETURNS.items()[0][1](rv)
