# coding=UTF-8

"""A not-so-nice way to degenerate the FCO API."""

from __future__ import print_function
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from enum import Enum


BASE = 'http://docs.flexiant.com'


def bs(s):
    """Force use of html parser."""
    return BeautifulSoup(s, "html.parser")


def get_type(s, d_types, u_types, o=None):
    """Determine type, including complex type. MUST REFACTOR."""
    builtins = {
        'boolean value, either true or false': bool,
        'date string in the format "yyyy-MM-dd\'T\'HH:mm:ssZ", for example "20'
        '13-12-11T10:09:08+0000"': datetime,
        'floating point number': float,
        'string of characters': str,
        'whole number': int,
        'byte value': bytes,
        'enum': Enum
    }

    try:
        d_types.update({a.text: a['href'] for a in s.select('a')})
        s = s.text
    except AttributeError:
        pass

    if not o:
        o = s

    if any([s.startswith(p) for p in ['Map of ', 'map of ']]):
        s = s[7:].split(' to ', 1)
        return dict, get_type(s[0], d_types, u_types, o), get_type(s[1],
                                                                   d_types,
                                                                   u_types, o)
    if any([s.startswith(p) for p in ['A ', 'a ', 'An ', 'an ']]):
        s = s.split(' ', 1)[1]
        if s.endswith(' array'):
            return list, get_type('a ' + str(s[:-6]), d_types, u_types, o)
        elif s.endswith(' object'):
            return 'co', s[:-7]
        elif s.endswith(' enum'):
            return Enum, s.rsplit(' ', 2)[1]
        else:
            try:
                return builtins[s]
            except:
                u_types.add(s)
                return s
    else:
        u_types.add(s)
        return s


def indexer(url):
    """Get first table in a page."""
    for tr in bs(requests.get(BASE + url).text)\
            .select('.wiki-content .table-wrap')[0].select('tr')[1:]:
        a = tr.find('td').find('a')
        yield a.text, a['href']


def parsed_page(url, d_types, u_types):
    """Get name-indexed dict of tables on a page."""
    page = bs(requests.get(BASE + url).text)
    table = {}
    for h1 in page.select('.wiki-content h1'):
        key = h1.text.lower()
        value = h1.findNext()
        if key == 'definition':
            temp = value.text.split(', ')
            temp2 = []
            value = []
            for v in temp:
                temp2.extend(v.split('\nor\n'))
            for v in temp2:
                value.append(tuple(v.split()))
        elif key == 'example':
            value = value.text.split('\n')
        elif key == 'remarks':
            value = value.text
        elif key == 'values':
            temp = {}
            for tr in value.select('tr')[1:]:
                td = tr.select('td')
                temp[td[0].text] = td[1].text
            value = temp
        elif key == 'returns':
            temp = {}
            for tr in value.select('tr')[1:]:
                td = tr.select('td')
                temp[td[0].text] = {
                    'desc': td[1].text,
                    'type': get_type(td[2], d_types, u_types),
                }
            value = temp
        elif key in ['parameters', 'data']:
            temp = {}
            for tr in value.select('tr')[1:]:
                td = tr.select('td')
                temp[td[0].text] = {
                    'desc': td[1].text,
                    'type': get_type(td[2], d_types, u_types),
                    'required': td[3].text == 'Yes'
                }
            value = temp
        else:
            value = value.text
        table[key] = value
        table['docstring'] = page.select('p')[0].text

    return table


def api(url='/display/DOCS/REST+User+API+Methods'):
    """Scrape API spec."""
    print('==> API', end='')

    degenerated = {}
    u_types = set()
    d_types = {}

    for name, href in indexer(url):
        print('.', end='')
        degenerated[name] = parsed_page(href, d_types, u_types)

    print()
    return degenerated, d_types, u_types


def enums(url='/display/DOCS/REST+Enum+Values'):
    """Scrape Enum spec."""
    print('==> Enums', end='')

    degenerated = {}
    u_types = set()
    d_types = {}

    for name, href in indexer(url):
        print('.', end='')
        degenerated[name] = parsed_page(href, d_types, u_types)

    print()
    return degenerated, d_types, u_types


def cobjects(url='/display/DOCS/REST+Complex+Objects', detailed=False):
    """Scrape Cobjects spec."""
    print('==> Cobjects', end=('\n' if detailed else ''))

    degenerated = {}
    u_types = set()
    d_types = {}

    for name, href in indexer(url):
        print('.', end='')

        page = bs(requests.get(BASE + href).text).select('.table-wrap')[0]

        info = {
            'docstring': page.select('p')[0].text,
            'attribs': {}
        }

        for tr in page.select('tr')[1:]:
            td = tr.select('td')
            info['attribs'][td[0].text] = {
                'desc': td[2].text,
                'type': get_type(td[1], d_types, u_types),
                'required': td[3].text == 'Yes'
            }

        degenerated[name] = info

    return degenerated, d_types, u_types


def print_api(endpoints):
    """"Nicely" listed endpoints."""
    for name in endpoints:
        print(name + ': ' + endpoints[name]['docstring'])
        print('  ' + str(endpoints[name]['definition']))


def print_enums(enums):
    """"Nicely" listed enums."""
    for name in enums:
        print(name + ': ' + enums[name]['docstring'])
        for value in enums[name]['values']:
            print('  ' + value + ': ' + enums[name]['values'][value])
