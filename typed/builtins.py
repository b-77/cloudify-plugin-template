# coding=UTF-8

"""Provides two basic builtin alternatives: List and Dict."""

from typed import (factory, Array, Map)


def List(item_type):
    return factory(Array, {'item_type': item_type})


def Dict(key_type, item_type):
    return factory(Map, {'key_type': key_type, 'item_type': item_type})
