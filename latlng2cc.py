#!/usr/bin/env python
# -*- mode: python; coding: utf-8; fill-column: 80; -*-
#
# latlng2cc.py
# Created by Balakrishnan Chandrasekaran on 2016-05-13 03:39 -0400.
# Copyright (c) 2016 Balakrishnan Chandrasekaran <balac@cs.duke.edu>.
#

"""
latlng2cc.py
Use Google's Reverse Geocoding API to convert latitude-longitude coordinates to
ISO 2-letter country codes.
"""

__author__  = 'Balakrishnan Chandrasekaran <balac@cs.duke.edu>'
__version__ = '1.0'
__license__ = 'MIT'


import argparse
import io
import os
import requests
import sys
import time


# Default output file path and name.
CWD = u'.'
DEF_OUT_FNAME = u'latlng-cc.txt'

COMMA = u','

# Google's reverse geocoding service URL.
SRVC_URL = u'https://maps.googleapis.com/maps/api/geocode/json?'
SRVC_PARAM = lambda lat, lng: {u'latlng' : u"%f,%f" % (lat, lng)}

HTTP_OK = 200
# Time to wait (in seconds) between requests to avoid rate violations.
WAIT_TIME = 3

# Fields of interest in response.
RES_RESULTS = u'results'
RES_ADDR_COMPS = u'address_components'
RES_SHORT_NAME = u'short_name'
RES_TYPES = u'types'
RES_CCODE_TYPES = set([u'country', u'political'])

CC_UNAVAILABLE = u'N/A'


def _err(msg):
    """Write message to STDERR.
    """
    sys.stderr.write(u"#> %s\n" % msg)


def parse_ccode(doc, missing_cc, verbose):
    """Parse the country code from the Google's reverse geocoding API results.
    """
    if not RES_RESULTS in doc or not doc[RES_RESULTS]:
        if verbose:
            _err(u"parse_ccode: missing key '%s'!" % RES_RESULTS)
        return missing_cc

    cc_lst = set()
    for res in doc[RES_RESULTS]:
        if not RES_ADDR_COMPS in res or not res[RES_ADDR_COMPS]:
            continue

        addr_comps = res[RES_ADDR_COMPS]
        for comp in addr_comps:
            if not RES_SHORT_NAME in comp:
                continue

            if not RES_TYPES in comp:
                continue

            comp_types = comp[RES_TYPES]
            if not len(RES_CCODE_TYPES & set(comp_types)) == len(RES_CCODE_TYPES):
                continue

            cc_lst.add(comp[RES_SHORT_NAME])

    if not cc_lst:
        if verbose:
            _err(u"parse_ccode: no country codes found!")
        return missing_cc

    return COMMA.join(cc_lst)


def lookup_ccode(lat, lng, verbose):
    """Lookup the country code corresponding to the latitude-longitude
    coordinate.
    """
    r = requests.get(SRVC_URL, params=SRVC_PARAM(lat, lng))
    if not r.status_code == HTTP_OK:
        return CC_UNAVAILABLE
    return parse_ccode(r.json(), CC_UNAVAILABLE, verbose)


def check_path(p):
    """Checks if path exists.
    """
    d = os.path.dirname(os.path.abspath(p))
    if not (os.path.exists(d) and os.path.isdir(d)):
        raise ValueError("Path '%s' does not exist!" % d)
    return True


def check_file(p):
    """Checks if path exists and points to a file.
    """
    if not (check_path(p) and os.path.isfile(p)):
        raise ValueError("Path '%s' is not a file!" % p)
    return True


def read_coords(in_path, delim, verbose):
    """Read the latitude-longitude coordinates from file.
    """
    for line in (line.strip() for line in
                 io.open(in_path, 'r', encoding='utf-8')):
        lat, lng = [float(v.strip()) for v in line.split(delim)]
        yield (lat, lng)


def latlng_to_ccode(in_path, out_path, delim, verbose):
    """Convert latitude-longitude coordinates to country codes.
    """
    with io.open(out_path, 'w', encoding='utf-8') as f:
        for res in ((lat, lng, lookup_ccode(lat, lng, verbose))
                    for lat, lng in read_coords(in_path, delim, verbose)):
            lat, lng, cc = res
            f.write(u"%f,%f %s\n" % (lat, lng, cc))
            try:
                time.sleep(WAIT_TIME)
            except:
                _err('Interrupted!')
                sys.exit(1)


def main(args):
    # Run sanity checks.
    check_file(args.in_path)
    check_path(args.out_path)

    latlng_to_ccode(args.in_path, args.out_path, args.delim, args.verbose)


def __config_parser():
    """Return a parser for parsing command line arguments.
    """
    desc = ('Convert latitude-longitude coordinates to'
            ' ISO two-letter country codes.')
    parser = argparse.ArgumentParser(description = desc)
    parser.add_argument('--version',
                        action = 'version',
                        version = '%(prog)s ' + "%s" % (__version__))
    parser.add_argument('-v', '--verbose',
                        action = 'store_true',
                        dest = 'verbose',
                        help = 'Enable verbose output.')
    parser.add_argument('-o', '--output',
                        dest = 'out_path',
                        metavar = 'out-path',
                        default = os.path.sep.join((CWD, DEF_OUT_FNAME)),
                        help = 'Absolute or relative path of output file.')
    parser.add_argument('--delim',
                        dest = 'delim',
                        metavar = 'delimiter',
                        default = u',',
                        help = ('Delimiter for parsing the'
                                ' latitude-longitude coordinates in file..'))
    parser.add_argument('in_path',
                        metavar = 'in-path',
                        help = ('Absolute or relative path containing file'
                                ' containing latitude-longitude coordinates.'))
    return parser


if __name__ == '__main__':
    parser = __config_parser()
    main(parser.parse_args())
