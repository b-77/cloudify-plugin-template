# coding=UTF-8

"""Abstraction of FCO API in the form of a Python wrapper."""

import fcoclient.clients as clients
import fcoclient.exceptions as exceptions
import resttypes.endpoints as endpoints

import json


class REST(object):

    """FCO REST API Interface."""

    def __init__(self, auth, logger):
        """
        Initialise FCP API Interface.

        :param auth: dictionary containing auth details
        :param logger: reference to a logger
        :return:
        """
        self.client = clients.get_client(auth, logger=logger)
        self.logger = logger
        self.logger.debug('REST API initialised with auth: %s', auth)

    def __getattr__(self, item):
        """
        Get relevant Endpoint object when accessed.

        :item: name of the endpoint
        :return: function representing the Endpoint
        """
        self.logger.debug('REST API endpoint request: %s', item)
        def wrapper(*args, **kwargs):
            return self.query(item, *args, **kwargs)
        return wrapper

    def query(self, endpoint, parameters=None, data=None, validate=False,
              **kwargs):
        """
        Perform an API query to the given endpoint.

        :param endpoint: name of the endpoint
        :param parameters: parameters for the endpoint
        :param data: data for the endpoint
        :param validate: validate return data?
        :param kwargs: alternative method for supplying parameters or data
        :return: validated, data if validate true, otherwise only data
        """
        endpoint = endpoint[0].capitalize() + endpoint[1:]
        endpoint = getattr(endpoints, endpoint)(parameters, data, **kwargs)
        type_, url = endpoint.endpoint
        payload = endpoint.untype()

        self.logger.debug('%s', payload)

        if not len(payload):
            payload = None

        self.logger.debug('REST API generated endpoint:\nTYPE: %s\nURL: %s\n'
                          'DATA: %s', type_, url, payload)

        if type_ is endpoints.Verbs.PUT:
            fn = self.client.put
        elif type_ is endpoints.Verbs.GET:
            fn = self.client.get
        elif type_ is endpoints.Verbs.POST:
            fn = self.client.post
            # POST payload needs to be JSON-encoded
            if payload:
                payload = json.JSONEncoder().encode(payload)
        elif type_ is endpoints.Verbs.DELETE:
            fn = self.client.delete
        else:
            raise exceptions.NonRecoverableError('unsupported API verb')

        rv = fn(url, payload)
        self.logger.debug('REST API return value: %s', rv)

        if validate:
            return rv, endpoint.validate_return(rv)
        else:
            return endpoint.RETURNS.items()[0][1](rv)
