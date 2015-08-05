# coding=UTF-8

"""Provides common utilities."""

from cloudify import context
from cloudify.exceptions import (NonRecoverableError, RecoverableError)

from functools import wraps

from fcoclient.clients import (get_client, RESTClient, PROP_CLIENT_CONFIG)
from fcoclient.api import REST as RESTApi
import fcoclient.exceptions as fco_exceptions
import rest_types.cobjects as cobjects


def _find_instanceof_in_kwargs(cls, kw):
    """Find a single instance of a class in a dict.

    Courtesy of the Cloudify Openstack Plugin.
    """
    ret = [v for v in kw.values() if isinstance(v, cls)]
    if not ret:
        return None
    if len(ret) > 1:
        raise NonRecoverableError(
            "Expected to find exactly one instance of {0} in "
            "kwargs but found {1}".format(cls, len(ret)))
    return ret[0]


def _get_ctx(kwargs):
    """Get Cloudify ctx from kwargs."""
    if isinstance(kwargs.get('ctx'), context.CloudifyContext):
        return kwargs.get('ctx')
    return _find_instanceof_in_kwargs(context.CloudifyContext, kwargs)


def _put_client_in_kwargs(client_name, kwargs):
    """Consolidate authentication information and insert client into kwargs."""
    if client_name in kwargs and not isinstance(kwargs[client_name],
                                                RESTClient):
        raise NonRecoverableError('Incorrect client class exists.')

    ctx = _get_ctx(kwargs)
    auth = None

    if ctx.type == context.NODE_INSTANCE:
        auth = ctx.node.properties.get(PROP_CLIENT_CONFIG)
    elif ctx.type == context.RELATIONSHIP_INSTANCE:
        auth = ctx.source.node.properties.get(PROP_CLIENT_CONFIG)
        if not auth:
            auth = ctx.target.node.properties.get(PROP_CLIENT_CONFIG)
    if PROP_CLIENT_CONFIG in kwargs:
        try:
            auth = auth.copy()
            auth.update(kwargs[PROP_CLIENT_CONFIG])
        except AttributeError:
            auth = kwargs[PROP_CLIENT_CONFIG]

    kwargs[client_name] = get_client(auth, logger=ctx.logger.info)


def _put_api_in_kwargs(api_name, kwargs):
    if api_name in kwargs and not isinstance(kwargs[api_name], RESTApi):
        raise NonRecoverableError('Incorrect API class exists.')

    ctx = _get_ctx(kwargs)
    auth = None

    if ctx.type == context.NODE_INSTANCE:
        auth = ctx.node.properties.get(PROP_CLIENT_CONFIG)
    elif ctx.type == context.RELATIONSHIP_INSTANCE:
        auth = ctx.source.node.properties.get(PROP_CLIENT_CONFIG)
        if not auth:
            auth = ctx.target.node.properties.get(PROP_CLIENT_CONFIG)
    if PROP_CLIENT_CONFIG in kwargs:
        try:
            auth = auth.copy()
            auth.update(kwargs[PROP_CLIENT_CONFIG])
        except AttributeError:
            auth = kwargs[PROP_CLIENT_CONFIG]

    kwargs[api_name] = RESTApi(auth, logger=ctx.logger)


def with_fco_client(f):
    """Wrapper to add FCO API client."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        _put_client_in_kwargs('fco_client', kwargs)

        try:
            return f(*args, **kwargs)
        except fco_exceptions.NonRecoverableError as e:
            raise NonRecoverableError(str(e))
        except fco_exceptions.RecoverableError as e:
            raise RecoverableError(str(e), retry_after=e.retry_after)
        except Exception as e:
            raise NonRecoverableError(str(e))

    return wrapper


def with_fco_api(f):
    """Wrapper to add FCO API client."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        _put_client_in_kwargs('fco_api', kwargs)

        try:
            return f(*args, **kwargs)
        except fco_exceptions.NonRecoverableError as e:
            raise NonRecoverableError(str(e))
        except fco_exceptions.RecoverableError as e:
            raise RecoverableError(str(e), retry_after=e.retry_after)
        except Exception as e:
            raise NonRecoverableError(str(e))

    return wrapper


def cfy_id(ctx, type_):

    if not isinstance(type_, type):
        type_ = type(type_).__name__
    else:
        type_ = type_.__name__

    return "{0}_{1}_{2}".format(type_, ctx.deployment.id, ctx.instance.id)


def co_from_properties(co, properties):
    co = getattr(cobjects, co)
    data = {}
    parameters = {}

    attribs = {v.replace('_', '').lower(): v for v in co.ALL_ATTRIBS}
    params = {v.replace('_', '').lower(): v for v in co.ALL_PARAMS}

    for p in properties:
        if p.replace('_', '').lower() in attribs:
            data[attribs[p]] = properties[p]
        if p.replace('_', '').lower() in params:
            parameters[params[p]] = properties[p]

    return co(parameters, data)
