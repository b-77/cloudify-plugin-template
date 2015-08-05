# coding=UTF-8

"""Provides common utility functions for REST types."""

from enum import Enum
from typed import Typed
from datetime import datetime, timedelta

from cloudify import ctx

__author__ = 'alen'


def to_str(uni_):
    """Recursively turn unciode to str."""
    if isinstance(uni_, list):
        gen = enumerate(uni_)
        str_ = [None]*len(uni_)
    elif isinstance(uni_, dict):
        gen = uni_.items()
        str_ = {}
    elif isinstance(uni_, basestring):
        return str(uni_)
    else:
        return uni_
    for k, v in gen:
        str_[to_str(k)] = to_str(v)
    return str_


def rat_check(given_dict, all_, required, types, noneable,
              fail_additional=True):
    """Check for required stuff, additional stuff and types of stuff."""
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
    """Check whether given instance is suitable for a cobject of type type_."""
    if inst is None and noneable:
        pass
    elif issubclass(type_, Typed):
        if not isinstance(inst, type_) and \
                not type_.is_acceptable(inst):
            return False
    elif issubclass(type_, Enum):
        if not isinstance(inst, type_) and \
                not hasattr(type_, inst):
            return False
    elif issubclass(type_, datetime):
        try:
            datetime.strptime(inst[:-5], '%Y-%m-%dT%H:%M:%S')
            timedelta(hours=int(inst[-4:-2]), minutes=int(inst[-2:]))
        except ValueError:
            return False
    elif not isinstance(inst, type_):
        ctx.logger.info('{} {} {}'.format(inst, type(inst), type_))
        return False
    return True


def construct_data(inst, type_, noneable):
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
