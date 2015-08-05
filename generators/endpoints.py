# coding=UTF-8

"""Provides utilities to scrape and generate Endpoints."""

from .common import (line, wrap, set_wrap, write, source_type)


def gen_single(endpoint_name, endpoint, out=[]):
    """Generate single endpoint definition."""
    line(out, 'class {}{}(Endpoint):', endpoint_name[0].upper(),
         endpoint_name[1:])
    line(out)
    line(out, '    """FCO REST API {} endpoint.', endpoint_name)
    line(out)

    # Format docstring to include a full stop
    ds = endpoint['docstring']
    ds = (ds + '.') if ds[-1] != '.' else ds
    wrap(out, ds, 4)
    line(out)

    # Include remarks, if included
    if 'remarks' in endpoint:
        line(out, '    Remarks:')
        wrap(out, endpoint['remarks'], 4)
        line(out)

    # Nicely print parameters
    if 'parameters' in endpoint:
        line(out, '    Parameters (type name (required): description):')
        for name, parameter in endpoint['parameters'].items():
            text = '{} {} ({}):'.format(source_type(parameter['type']), name,
                                        'T' if parameter['required'] else 'F')
            wrap(out, text, 8, 4)
            wrap(out, parameter['desc'], 12, 0)

    # Nicely print data
    if 'data' in endpoint:
        if 'parameters' in endpoint:
            line(out)
        line(out, '    Data (type name (required): description):')
        for name, data in endpoint['data'].items():
            text = '{} {} ({}):'.format(source_type(data['type']), name,
                                        'T' if data['required'] else 'F')
            wrap(out, text, 8, 4)
            wrap(out, data['desc'], 12, 0)

    # Nicely print return
    if 'returns' in endpoint:
        if 'parameters' in endpoint or 'data' in endpoint:
            line(out)
        line(out, '    Returns (type name: description):')
        for name, data in endpoint['returns'].items():
            text = '{} {}:'.format(source_type(data['type']), name)
            wrap(out, text, 8, 4)
            wrap(out, data['desc'], 12, 0)

    # End docstring
    line(out, '    """')
    line(out)

    # Print endpoint
    text = 'ENDPOINTS = [' + ', '.join(['(Verbs.{}, \'{}\')'
                                        .format(d[0], d[1]) for d in
                                        endpoint['definition']]) + ']'
    wrap(out, text, 4, 13, False)
    line(out)

    # Parameters' values
    if 'parameters' in endpoint:
        params = set(str(n) for n in endpoint['parameters'])
        r_params = {str(n) for n, v in endpoint['parameters'].items() if
                    v['required']}
        o_params = params - r_params
        t_params = {str(n): source_type(endpoint['parameters'][n]['type']) for
                    n in params}

        set_wrap(out, 'ALL_PARAMS = ' + str(params), 4, 14, False)
        set_wrap(out, 'REQUIRED_PARAMS = ' + str(r_params), 4, 19, False)
        set_wrap(out, 'OPTIONAL_PARAMS = ' + str(o_params), 4, 19, False)
        set_wrap(out, 'PARAMS_TYPES = ' + str(t_params), 4, 16, False)

    # Data values
    if 'data' in endpoint:
        if 'parameters' in endpoint:
            line(out)
        data = set(str(n) for n in endpoint['data'])
        r_data = {str(n) for n, v in endpoint['data'].items() if v['required']}
        o_data = data - r_data
        t_data = {str(n): source_type(endpoint['data'][n]['type']) for n in
                  data}

        set_wrap(out, 'ALL_DATA = ' + str(data), 4, 12, False)
        set_wrap(out, 'REQUIRED_DATA = ' + str(r_data), 4, 17, False)
        set_wrap(out, 'OPTIONAL_DATA = ' + str(o_data), 4, 17, False)
        set_wrap(out, 'DATA_TYPES = ' + str(t_data), 4, 14, False)

    # Return values
    if 'returns' in endpoint:
        if 'parameters' in endpoint or 'data' in endpoint:
            line(out)
        returns = {str(n): source_type(endpoint['returns'][n]['type']) for n in
                   endpoint['returns']}

        set_wrap(out, 'RETURNS = ' + str(returns), 4, 12, False)

    # Final empty line
    line(out)


def gen(enpoints, handler, out=[], line_wrapper=str):
    """Generate and write all endpoint definitions."""
    for endpoint_name, endpoint in enpoints.items():
        gen_single(endpoint_name, endpoint, out)
        line(out)
    out.pop()

    out = map(line_wrapper, out)
    write(out, handler)

    return out
