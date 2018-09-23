#!/usr/bin/env python
################################################################################
# pia/make_COLOR_VS_PIAPAGE.py
#
# This is a stand-alone program to scrape the color information for the PIA
# pages. The color information is not on the pages for individual products, but
# it is available on many of the pages that are tabulations of PIA products as
# the third dimesion of the image size (3 for color, 1 for black and white).
#
# The program checks a set of specified URLS.
#
# This program also contains a list of exception PIA values. These are pages
# that, for some reason, list the number of channels as something other than
# one or three.
#
# The output of this program is a file COLOR_VS_PIAPAGE.py. That file can be
# imported as follows:
#   from .COLOR_VS_PIAPAGE import COLOR_VS_PIAPAGE
#
# COLOR_VS_PIAPAGE is a string that can be indexed by the PIA number and returns
# '3' for a color product, '1' for a black and white product, or '0' if the
# product does not exist or its color properties are unknown.
################################################################################

from bs4 import BeautifulSoup
import requests
import re
import pickle
import numpy as np
import datetime

from piapage.MAX_PIAPAGE import MAX_PIAPAGE

# This is the list of URLs to check each time
URLS = [
    'https://photojournal.jpl.nasa.gov/target/Sun',
    'https://photojournal.jpl.nasa.gov/keywords/dp',
    'https://photojournal.jpl.nasa.gov/gallery/universe',
    'https://photojournal.jpl.nasa.gov/gallery/snt',
    'https://photojournal.jpl.nasa.gov/target/Other',
    'https://photojournal.jpl.nasa.gov/targetFamily/Mercury',
    'https://photojournal.jpl.nasa.gov/targetFamily/Venus',
    'https://photojournal.jpl.nasa.gov/targetFamily/Earth',
    'https://photojournal.jpl.nasa.gov/targetFamily/Mars',
    'https://photojournal.jpl.nasa.gov/targetFamily/Jupiter',
    'https://photojournal.jpl.nasa.gov/targetFamily/Saturn',
    'https://photojournal.jpl.nasa.gov/targetFamily/Uranus',
    'https://photojournal.jpl.nasa.gov/targetFamily/Neptune',
    'https://photojournal.jpl.nasa.gov/targetFamily/Pluto',
]

# A dictionary keyed by PIA number, which returns True if the image is in color
# or False if it is black and white.
COLOR_VS_PIAPAGE = {}

# The size is 'nxnxn' where each n is an integer or -1 if unknown
SIZE_REGEX = re.compile('(-1|[0-9])+x(-1|[0-9])+x[0-9]+')
PIA_REGEX = re.compile('PIA[0-9]{5}:')

# For each URL and each subsequent page...
for base_url in URLS:
  for start in range(0, 100000, 100):
    url = base_url + '?start=%d' % start
    print url

    req = requests.get(url)

    # Make sure we got back a good request
    if req.status_code != 200:
        raise IOError('URL not found: "%s"' % url)

    html = ''.join(c if ord(c) < 128 else ' ' for c in req.text)

    # Find all the tables on the page
    soup = BeautifulSoup(html, 'lxml')
    tables = soup.find_all('table')
    if len(tables) not in (10, 11):
        print 'Number of tables =', len(tables)
        continue

    # The third-to-last table is the one we wenat
    table = tables[-3]

    trs = table.find_all('tr')
    sizes = []
    pias = []
    for tr in trs:
        td = tr.find_all('td')[-1]
        text = td.text.strip()

        if SIZE_REGEX.match(text):
            sizes.append(text)

        if PIA_REGEX.match(text):
            pias.append(text[:8])

    if len(sizes) == 0:
        break

    if len(sizes) != len(pias):
        print 'Size and PIA mismatch!'
        continue

    # The third element in the size is "1" for black and white or "3" for color
    for (pia, size) in zip(pias, sizes):
        ipia = int(pia[3:])
        if size[-2:] == 'x1':
            is_color = False
        elif size[-2:] == 'x3':
            is_color = True
        else:
            print 'Invalid size: ', pia, size
            continue

        COLOR_VS_PIAPAGE[ipia] = is_color

# Erroneous sizes, values base on human review of the website

COLOR_VS_PIAPAGE[ 2146] = True
COLOR_VS_PIAPAGE[ 3035] = False
COLOR_VS_PIAPAGE[ 3997] = False
COLOR_VS_PIAPAGE[ 4423] = False
COLOR_VS_PIAPAGE[ 5031] = False
COLOR_VS_PIAPAGE[ 5032] = False
COLOR_VS_PIAPAGE[ 5045] = False
COLOR_VS_PIAPAGE[ 5050] = False
COLOR_VS_PIAPAGE[ 5051] = False
COLOR_VS_PIAPAGE[ 5052] = False
COLOR_VS_PIAPAGE[ 5068] = False
COLOR_VS_PIAPAGE[ 5088] = False
COLOR_VS_PIAPAGE[ 5089] = False
COLOR_VS_PIAPAGE[ 5090] = False
COLOR_VS_PIAPAGE[ 5099] = False
COLOR_VS_PIAPAGE[ 5110] = False
COLOR_VS_PIAPAGE[ 5166] = False
COLOR_VS_PIAPAGE[ 5211] = False
COLOR_VS_PIAPAGE[ 5213] = False
COLOR_VS_PIAPAGE[ 5214] = False
COLOR_VS_PIAPAGE[ 5215] = False
COLOR_VS_PIAPAGE[ 5267] = False
COLOR_VS_PIAPAGE[ 5268] = True
COLOR_VS_PIAPAGE[ 5308] = False
COLOR_VS_PIAPAGE[ 5323] = False
COLOR_VS_PIAPAGE[ 5343] = True
COLOR_VS_PIAPAGE[ 5344] = False
COLOR_VS_PIAPAGE[ 5345] = False
COLOR_VS_PIAPAGE[ 5384] = False
COLOR_VS_PIAPAGE[ 5522] = False
COLOR_VS_PIAPAGE[ 5553] = False
COLOR_VS_PIAPAGE[ 5556] = False
COLOR_VS_PIAPAGE[ 5565] = True
COLOR_VS_PIAPAGE[ 5637] = False
COLOR_VS_PIAPAGE[ 5685] = False
COLOR_VS_PIAPAGE[ 5724] = False
COLOR_VS_PIAPAGE[ 5754] = False
COLOR_VS_PIAPAGE[ 5942] = True
COLOR_VS_PIAPAGE[ 6065] = False
COLOR_VS_PIAPAGE[ 6076] = False
COLOR_VS_PIAPAGE[ 6080] = False
COLOR_VS_PIAPAGE[ 6082] = False
COLOR_VS_PIAPAGE[ 6083] = False
COLOR_VS_PIAPAGE[ 6084] = False
COLOR_VS_PIAPAGE[ 6105] = False
COLOR_VS_PIAPAGE[ 6106] = False
COLOR_VS_PIAPAGE[ 6115] = False
COLOR_VS_PIAPAGE[ 6119] = True
COLOR_VS_PIAPAGE[ 6124] = False
COLOR_VS_PIAPAGE[ 6137] = False
COLOR_VS_PIAPAGE[ 6267] = False
COLOR_VS_PIAPAGE[ 6268] = False
COLOR_VS_PIAPAGE[ 6340] = False
COLOR_VS_PIAPAGE[ 7138] = False
COLOR_VS_PIAPAGE[ 7139] = False
COLOR_VS_PIAPAGE[ 7140] = False
COLOR_VS_PIAPAGE[ 7448] = False
COLOR_VS_PIAPAGE[ 7620] = False
COLOR_VS_PIAPAGE[ 7710] = False
COLOR_VS_PIAPAGE[ 9114] = True
COLOR_VS_PIAPAGE[ 9170] = False
COLOR_VS_PIAPAGE[10171] = False
COLOR_VS_PIAPAGE[12134] = False
COLOR_VS_PIAPAGE[13088] = False
COLOR_VS_PIAPAGE[13134] = True

# Write the color information into COLOR_STRING.py

is_color     = [k for k in COLOR_VS_PIAPAGE if COLOR_VS_PIAPAGE[k]]
is_grayscale = [k for k in COLOR_VS_PIAPAGE if not COLOR_VS_PIAPAGE[k]]

is_color.sort()
is_grayscale.sort()

keys = COLOR_VS_PIAPAGE.keys()
max_key = max(keys)
if max_key > MAX_PIAPAGE:
    raise ValueError('MAX_PIAPAGE has been exceeded: ' +
                     'page PIA%d exists' % max_key)

channels = np.zeros(MAX_PIAPAGE, dtype='u1')

for k in is_color:
    channels[k] = 3

for k in is_grayscale:
    channels[k] = 1

now = datetime.datetime.now()
with open('COLOR_VS_PIAPAGE.py', 'w') as f:
    f.write(80*'#' + '\n')
    f.write('# File automatically generated by program make_COLOR_VS_PIA.py\n')
    f.write('#\n')
    f.write('# Last run: %s\n' % now.strftime("%Y-%m-%d %H:%M"))
    f.write(80*'#' + '\n')
    f.write('\n')
    f.write('COLOR_VS_PIAPAGE = (\n')

    for k in range(0, len(channels), 50):
        kstop = min(k+50, len(channels))
        string = ''.join([str(channels[kk]) for kk in range(k,kstop)])
        f.write('    "' + string + '"')

        if kstop < len(channels):
            f.write(' +\n')

    f.write('\n)\n\n')
    f.write(80*'#' + '\n')
