# coding=UTF-8

"""Provides utilities to scrape and generate Complex Objects."""

from .common import (line, wrap, set_wrap, write, source_type)
from enum import Enum
try:
    from functools import reduce
except:
    pass


def create_relationships_rec(t):
    """Recursive part of create_relationships, searches through cobjects."""
    if type(t) is tuple:
        if t[0] == 'co':
            return {t[1]}
        elif t[0] is dict:
            return create_relationships_rec(t[1]) | \
                create_relationships_rec(t[2])
        elif t[0] is list:
            return create_relationships_rec(t[1])
        elif t[0] is Enum:
            return set()
    else:
        return set()


def create_relationships(co_dict):
    """Creates a mapping of every cobject to the set of its dependencies."""
    d = {}
    for co in co_dict:
        d[co] = set()
        for a, r in co_dict[co]['attribs'].items():
            t = r['type']
            d[co] = d[co] | create_relationships_rec(t)
    return d


def topological_sort(data):
    """Topologically sorts the network of related cobjects into layers."""
    data = data.copy()
    # Find undefined elements
    undefined = reduce(set.union, data.values()) - set(data.keys())
    # Give them empty definitions
    data.update({k: set() for k in undefined})
    # While we have data, construct layers, construct layers
    layers = []
    while data:
        layer = set(item for item, dep in data.items() if not dep)
        if not layer:
            break
        layers.append(layer)
        data = {item: (dep - layer) for item, dep in data.items()
                if item not in layer}
    return layers, undefined, data


def gen_single(co_name, co, out=[]):
    """Generate single cobject definition."""
    line(out, 'class {}(ComplexObject):', co_name)
    line(out)
    line(out, '    """FCO REST API {} complex object.', co_name)
    line(out)

    # Format docstring to include a full stop
    ds = co['docstring']
    ds = (ds + '.') if ds[-1] != '.' else ds
    wrap(out, ds, 4)
    line(out)

    # Docstring attributes header
    line(out, '    Attributes (type name (required): description:')

    # Print docstring definitions
    for n, a in co['attribs'].items():
        text = '{} {} ({}):'.format(source_type(a['type'], cobjects_prefix=''),
                                    n, 'T' if a['required'] else 'F')
        wrap(out, text, 8, 4)
        wrap(out, a['desc'], 12, 0)

    # End docstring
    line(out, '    """')
    line(out)

    # Print definitions
    attribs = set(str(n) for n in co['attribs'])
    required = {str(n) for n in attribs if co['attribs'][n]['required']}
    optional = attribs - required
    types = {str(n): source_type(co['attribs'][n]['type'], cobjects_prefix='')
             for n in attribs}

    set_wrap(out, 'ALL_ATTRIBS = ' + str(attribs), 4, 15, False)
    set_wrap(out, 'REQUIRED_ATTRIBS = ' + str(required), 4, 20, False)
    set_wrap(out, 'OPTIONAL_ATTRIBS = ' + str(optional), 4, 20, False)
    set_wrap(out, 'TYPES = ' + str(types), 4, 9, False)

    # Final empty line
    line(out)


def gen(enums, handler, out=[], line_wrapper=str):
    """Generate and write all cobject definitions."""
    layers, undefined, cyclic = topological_sort(create_relationships(enums))

    for name in undefined:
        co = {
            'docstring': 'Undefined Complex Object {}.'.format(name),
            'desc': '',
            'attribs': {}
        }
        gen_single(name, co, out)
        line(out)

    for layer in layers:
        for name in layer:
            if name not in undefined:
                gen_single(name, enums[name], out)
                line(out)

    if cyclic:
        line(out, 'CYCLIC FIX: {}', cyclic)
    else:
        out.pop()

    out = map(line_wrapper, out)
    write(out, handler)

    return out
