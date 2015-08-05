# coding=UTF-8

"""Provides common utilities to scrape and generate API elements."""

import os
import textwrap
from enum import Enum


NEWLINE = os.linesep
MAX_WIDTH = 79
FLOWING_MAX_WIDTH = 72

MAGIC_CHARACTER = 'ž'
TYPED_LIST = 'List'
TYPED_DICT = 'Dict'


class Named(object):

    """Returns a source-friendly representation of an object."""

    def __init__(self, type_):
        self.type_ = type_

    def __str__(self):
        try:
            return self.type_.__name__
        except AttributeError:
            return self.type_

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()


def source_type(type_, cobjects_prefix='cobjects.', enums_prefix='enums.'):
    """Get a source-friendly representation, adding necessary prefixes."""
    if type(type_) is tuple:
        if type_[0] is Enum:
            return Named(enums_prefix + type_[1])
        elif type_[0] == 'co':
            return Named(cobjects_prefix + type_[1])
        elif type_[0] is dict:
            return Named('{}({},{}{})'.format(TYPED_DICT,
                                              source_type(type_[1],
                                                          cobjects_prefix),
                                              MAGIC_CHARACTER,
                                              source_type(type_[2],
                                                          cobjects_prefix)))
        elif type_[0] is list:
            return Named('{}({})'.format(TYPED_LIST, source_type(type_[1],
                         cobjects_prefix)))
        else:
            raise TypeError('unknown type to name')
    else:
        return Named(type_)


def line(obj, content='', *args):
    """Add a line to a string or list."""
    content = content.format(*args)
    if isinstance(obj, basestring):
        obj += content + NEWLINE
    elif isinstance(obj, list):
        obj.append(content + NEWLINE)

    return obj


def lines(obj, content):
    """Add multiple lines to a string or list."""
    if isinstance(obj, basestring):
        obj += NEWLINE.join(content) + NEWLINE
    elif isinstance(obj, list):
        obj.extend(map(lambda l: l + NEWLINE, content))

    return obj


def wrap(obj, text, initial=0, subsequent=0, flowing=True):
    """Add a block of text wrapped to fit guidelines."""
    lines(obj, textwrap.wrap(text, initial_indent=' '*initial,
          subsequent_indent=' '*(initial+subsequent),
          width=(FLOWING_MAX_WIDTH if flowing else MAX_WIDTH)))

    return obj


def set_wrap(out, text, *args, **kwargs):
    """Fixes Python2.7 set printing style - set([...])."""
    text = text.replace('set([])', 'set()')
    text = text.replace('set([', '{')
    text = text.replace('])', '}')
    wrap(out, text, *args, **kwargs)


def write(obj, handler):
    """Writes object using handler, or writes to file if handler is string."""
    if isinstance(handler, basestring):
        with open(handler, 'w') as f:
            if isinstance(obj, basestring):
                f.write((obj))
            elif isinstance(obj, list):
                f.writelines(obj)
    else:
        if isinstance(obj, basestring):
            handler(obj)
        elif isinstance(obj, list):
            map(handler, obj)
