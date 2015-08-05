# coding=UTF-8

"""Provides utilities to scrape and generate Enums."""

from .common import (line, wrap, write)


def gen_single(enum_name, enum, out=[]):
    """Generate single enum definition."""
    line(out, 'class {}(Enum):', enum_name)
    line(out)
    line(out, '    """FCO REST API {} enum.', enum_name)
    line(out)

    # Format docstring to include a full stop
    ds = enum['docstring']
    ds = (ds + '.') if ds[-1] != '.' else ds
    wrap(out, ds, 4)
    line(out)

    # Nicely align value descriptions
    in_ = (len(max(enum['values'].keys(), key=len)) + 2)
    for v, d in enum['values'].items():
        wrap(out, '{}:{}{}'.format(v, ' '*(in_ - len(v) - 1), d), 4, in_)

    # End docstring
    line(out, '    """')
    line(out)

    # Assign values their own value
    for v in enum['values']:
        line(out, '    {} = \'{}\'', v, v)

    # Final empty line
    line(out)

    return out


def gen(enums, handler, out=[], line_wrapper=str):
    """Generate and write all enum definitions."""
    for enum_name, enum in enums.items():
        gen_single(enum_name, enum, out)
        line(out)
    out.pop()

    out = map(line_wrapper, out)
    write(out, handler)

    return out
