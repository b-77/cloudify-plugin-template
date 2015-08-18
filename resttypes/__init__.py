# coding=UTF-8

"""Provides common utility functions for REST types."""

from enum import Enum
from typed import Typed
from datetime import datetime, timedelta

# from cloudify import ctx

__author__ = 'alen'


def to_str(uni_):
    """
    Recursively turn an object with unicode into an object with strings.

    :param uni_: object with unicode elements
    :return: object with string elements
    """
    if isinstance(uni_, list):
        str_ = [None]*len(uni_)
        for k, v in enumerate(uni_):
            str_[k] = to_str(v)
    elif isinstance(uni_, dict):
        str_ = {}
        for k, v in uni_.items():
            str_[to_str(k)] = to_str(v)
    elif isinstance(uni_, basestring):
        str_ = uni_.encode('ascii','replace')
    else:
        str_ = uni_
    return str_


def rat_check(given_dict, all_, required, types, noneable,
              fail_additional=True):
    """
    Check for required, additional and the type of given data.

    :param given_dict: the data given
    :param all_: all the possible data
    :param required: all the required data
    :param types:  all the data types
    :param noneable: can a value be None
    :param fail_additional: fail the check if additional data is given
    :return: True or False depending on whether the check passed
    """
    try:
        given = set(given_dict)
    except TypeError:
        given = set()

    missing = required - given
    additional = given - all_
    type_check = {}

    for k in (given & all_):
        v = given_dict[k]
        if v is None and noneable:
            continue
        elif issubclass(types[k], Typed):
            if not isinstance(v, types[k]) and \
                    not types[k].is_acceptable(v):
                type_check[k] = (type(v).__name__, types[k].__name__)
        elif issubclass(types[k], Enum):
            if not isinstance(v, types[k]) and \
                    not hasattr(types[k], v):
                type_check[k] = (type(v).__name__, types[k].__name__)
        elif not isinstance(v, types[k]):
            type_check[k] = (type(v).__name__, types[k].__name__)
    if missing or type_check or (additional and fail_additional):
        raise TypeError('something went wrong; missing: {}, additional: {}, '
                        'types (got, expected): {}'.format(missing, additional,
                                                           type_check))

    return True


def is_acceptable(inst, type_, noneable):
    """
    Check whether given instance is suitable for a cobjet of type type_.

    :param inst: instance to be checked
    :param type_: type to check against
    :param noneable: can data be None
    :return: True or False depending on whether the check passed
    """
    if inst is None and noneable:
        pass
    elif issubclass(type_, Typed):
        if not isinstance(inst, type_) and not type_.is_acceptable(inst):
            return False
    elif issubclass(type_, Enum):
        if not isinstance(inst, type_) and not hasattr(type_, inst):
            return False
    elif issubclass(type_, datetime):
        try:
            datetime.strptime(inst[:-5], '%Y-%m-%dT%H:%M:%S')
            timedelta(hours=int(inst[-4:-2]), minutes=int(inst[-2:]))
        except ValueError:
            return False
    elif not isinstance(inst, type_):
        return False
    return True


def construct_data(inst, type_, noneable):
    """
    Construct data for a cobject of type type_.

    :param inst: data source
    :param type_: type to construct
    :param noneable: can data be None
    :return: constructed data
    """
    """Construct data for a cobject of type type_."""
    if inst is None and noneable:
        return None
    elif issubclass(type_, (Typed, Enum)):
        if not isinstance(inst, type_):
            return type_(inst)
        else:
            return inst
    elif issubclass(type_, datetime):
        if not isinstance(inst, type_):
            tzless = datetime.strptime(inst[:-5], '%Y-%m-%dT%H:%M:%S')
            gmt = tzless + timedelta(hours=int(inst[-4:-2]),
                                     minutes=int(inst[-2:]))
            return gmt
        else:
            return inst
    elif isinstance(inst, type_):
        return inst
    raise ValueError('cannot construct type {} from data {}'.format(
        type_.__name__, inst))
