#!/usr/bin/env python
################################################################################
# Class PiaPage
#
# A class that customizes the GalleryPage interface for NASA press release web
# pages from the Planetary Photojournal, https://photojournal.jpl.nasa.gov.
#
# Andrew Lin & Mark Showalter
################################################################################

from gallerypage import GalleryPage

from bs4 import BeautifulSoup, ResultSet
import requests
import os
import json
import lxml
import re

from piapage_background_strings import BACKGROUND_STRINGS
from mission_full_names    import MISSION_FULL_NAMES
from host_full_names       import HOST_FULL_NAMES
from instrument_full_names import INSTRUMENT_FULL_NAMES
from target_full_names     import TARGET_FULL_NAMES

PARSER = 'lxml'

PIA_REGEX = re.compile(r'PIA[0-9]{5}')
YMD_REGEX = re.compile(r'[12][0-9]{3}-[01][0-9]-[0-3][0-9]$')

class PiaPage(GalleryPage):

    # Class constants
    PIA_URL = "https://photojournal.jpl.nasa.gov/catalog/"
    MISSING_PAGE_TEXT = 'No images in our database met your search criteria'
    PIAROOT_ENVNAME = 'PIAPATH'
    _PIAROOT = None

    def __init__(self, src, overwrite=False):
        """ The constructor of this class. Requires a source. Contains
        attributes source, html, soup, title, credit, and caption.

        Input:
            src         The PIA source. This can be
                        1. an integer up to five digits.
                        2. 'PIA' followed by a five-digit number, using leading
                           zeros.
                        3. A local path to a file containing the HTML.
                        4. The URL of a PIA page. In this case, the HTML is
                           saved as a local file for future, quick access.

            overwrite   True to overwrite a local copy of the HTML source with
                        one pulled from the website; False to leave any local
                        copy unchanged
        """

        self.source = src

        self.id = PiaPage.get_id(self.source)
                            # Unique identifier for this product, e.g., PIA12345
        self.origin_url = PiaPage.url_from_source(self.source)

        # Read the page as HTML
        self.html = PiaPage.get_html_for_id(self.source, overwrite)

#       The default parser cannot handle some PIA pages. lxml does.
#       self.soup = BeautifulSoup(self.html, 'html.parser')
        self.soup = BeautifulSoup(self.html, PARSER)

        # Validate the PIA page
        if len(self.soup.find_all('dt')) != 3:
            raise IOError("PIA page does not contain three description tags")

        text = self.soup.find_all('dt')[0].text.strip()
        if 'Caption' not in text:
            raise IOError("No caption found in PIA page")

        text = self.soup.find_all('dt')[1].text.strip()
        if not text.startswith("Image Credit:"):
            raise IOError("No image credit found in PIA page")

        text = self.soup.find_all('dt')[2].text.strip()
        if not text.startswith("Image Addition Date:"):
            raise IOError("No image addition date found in PIA page")

        text = self.soup.find_all('b')[0].text.lstrip()
        if text[:8] != self.id:
            raise IOError("Invalid title in PIA page: " + text)

        # Extract the caption and separate it from the background info
        (self.caption_soup,
         self.background_soup) = self.get_caption_and_background()

        self.title = self.get_title()
        self.credit = self.get_credit()
        self.release_date = self.get_release_date()
        self.xrefs = self.find_xrefs()

        # Get key information from the PIA page's table
        self.pia_table = self.load_pia_table()
        missions    = self.pia_table.get('Mission', [])
        hosts       = self.pia_table.get('Spacecraft', [])
        instruments = self.pia_table.get('Instrument', [])
        targets     = self.pia_table.get('Target Name', [])

        if targets and 'Sol' in targets[0]:
            targets[0] = 'Sun'

        # Commone error in pages
        if 'Comet' in targets and 'Rosetta' in missions:
            targets[targets.index('Comet')] = '67P/Churyumov-Gerasimenko'

        # Take the first entry as primary
        if missions:
            missions = [MISSION_FULL_NAMES.get(m, m) for m in missions]
            missions = [str(m) for m in missions]
            self._mission = missions[0]

        if hosts:
            hosts = [HOST_FULL_NAMES.get(h.lower(), h) for h in hosts]
            hosts = [str(h) for h in hosts]
            self._host = hosts[0]

        if instruments:
            instruments = [INSTRUMENT_FULL_NAMES.get(i.lower(), i)
                           for i in instruments]
            instruments = [str(i) for i in instruments]
            self._instrument = instruments[0]

        if targets:
            targets = [TARGET_FULL_NAMES.get(t.lower(), t) for t in targets]
            targets = [str(t) for t in targets]
            self._target = targets[0]

        planets = self.pia_table.get('Is a satellite of', [])
        if planets and 'Sol' in planets[0]:
            planets = self.pia_table.get('Target Name', [])
            planets = [str(p) for p in planets]
            planets = [p for p in planets if p in GalleryPage.PLANET_NAMES]

            if planets:
                self._planet = planets[0]

        # Make sure the list attributes are complete
        if missions:
            self._missions = list(set(self.missions + missions))
            self._missions.sort()

        if hosts:
            self._hosts = list(set(self.hosts + hosts))
            self._hosts.sort()

            # Use the mission as the host if necessary
            if missions and self._missions and not self._hosts:
                self._hosts = self._missions

        if instruments:
            self._instruments = list(set(self.instruments + instruments))
            self._instruments.sort()

        if targets:
            self._targets = list(set(self.targets + targets))
            self._targets.sort()

        if planets:
            self._planets = list(set(self.planets + planets))
            self._planets.sort()

    ############################################################################
    # piaroot() returns the path to the root directory for PIA text files. It
    # is filled in internally the first time it is used.
    # 
    # The path to the local copy of a particular PIA text file is
    #   piaroot/PIAnnxxx/PIAnnnnn.txt
    # where 'nnnnn' is replaced by the pia number. The directory name uses the
    # first two digits of the pia number followed by literal 'xxx'. This
    # prevents directories from growing to more than 1000 files.
    ############################################################################

    @staticmethod
    def piaroot():
        """Return the root directory for PIA text files. Search via an
        environment variable if it is undefined."""

        if not PiaPage._PIAROOT:
            try:
                PiaPage._PIAROOT = os.environ[PiaPage.PIAROOT_ENVNAME]
            except KeyError:
                ## Failing that, we will use the current working directory
                PiaPage._PIAROOT = ''

        return PiaPage._PIAROOT

    @staticmethod
    def set_piaroot(root):
        """Set the root directory for PIA text files. Generally, this should
        be called before a constructor. It is unnecessary if the environment
        variable PIAPATH is defined.

        The path to the local copy of a particular PIA text file is
            piaroot/PIAnnxxx/PIAnnnnn.txt
        where 'nnnnn' is replaced by the pia number. The directory name uses
        the first two digits of the pia number followed by literal 'xxx'. This
        prevents directories from growing to more than 1000 files.
        """

        PiaPage._PIAROOT = root

    ############################################################################
    # Main routine to retrieve HTML from either a local or remote site, and to
    # cache a local copy if requested.
    ############################################################################

    @staticmethod
    def get_html_for_id(source, overwrite=False):
        """Obtain the html from a PIA number or string"""

        # Convert the PIA code from a string if necessary
        if isinstance(source, int):
            source = PiaPage.get_id(source)

        # If this is not a URL, read a local file if possible
        if not PiaPage.is_url(source) and not overwrite:
            if os.path.exists(source):
                filepath = source
            else:
                filepath = PiaPage.filepath_from_source(source)

            try:
                with open(filepath, 'r') as file:
                    html = file.read()
                return str(html)

            # If local file not found
            except IOError:
                pass

        # Otherwise, get the online version
        if PiaPage.is_url(source):
            url = source
        else:
            url = PiaPage.url_from_source(source)

        req = requests.get(url)

        # Make sure we got back a good request
        if req.status_code != 200 or PiaPage.MISSING_PAGE_TEXT in req.text:
            raise IOError('URL not found: "%s"' % url)

        # Replace non-ASCII characters that normally breaks HTML
        cleaned = ''.join(c if ord(c) < 128 else ' ' for c in req.text)

        # Save the file so we don't need to retrieve it next time
        filepath = PiaPage.filepath_from_source(source)
        if overwrite or not os.path.exists(filepath):
            with open(filepath, 'w') as file:
                file.write(cleaned)

        return cleaned

    ############################################################################
    # Utilities
    ############################################################################

    @staticmethod
    def is_url(source):
        """Check if the source is a URL"""

        return source.startswith('http://') or source.startswith('https://')

    @staticmethod
    def get_id(source):
        """Return a string 'PIA' + five digits from a source, which could be an
        integer, a PIA string, a filepath or a full URL."""

        if type(source) == int:
            source = 'PIA%05d' % source

        source = source.upper()
        k = source.upper().rindex('PIA')    # find the rightmost 'PIA'
        id = source[k:k+8]

        return str(id)

    @staticmethod
    def filepath_from_source(source):
        """Return the local file path based on the source."""

        id = PiaPage.get_id(source)
        filepath = '%sxxx/%s.txt' % (id[:5], id)

        return os.path.join(PiaPage.piaroot(), filepath)

    @staticmethod
    def url_from_source(source):
        """Return the URL based on the source."""

        id = PiaPage.get_id(source)
        return PiaPage.PIA_URL + id

    ############################################################################
    # Methods to extract info from the soup
    ############################################################################

    def get_title(self):
        """Return the title of the page. Example: Artemis Corona"""

        title = GalleryPage.soup_as_text(self.soup.find('b'))
        if title[:8] == self.id and title[8] == ':':
            title = title[9:].strip()

        return title

    def get_credit(self):
        """Return the Image Credit. Example: NASA/JPL"""

        return GalleryPage.soup_as_text(self.soup.find_all('dd')[1])

    def get_release_date(self):
        """Return the release date in yyyy-mm-dd format."""

        date = GalleryPage.soup_as_text(self.soup.find_all('dd')[2])
        date = str(date.strip())
        date = date.replace('\\r','').replace('\\n','') # Fix HTML glitch
        if not YMD_REGEX.match(date):
            raise ValueError('No valid release date: ' + date)

        return date

    def get_caption_and_background(self):
        """Return the caption and any identified background information as two
        soups."""

        # Get the caption as soup
        paragraphs_in_soup = list(self.soup.find('dd').children)

        # Convert to strings and strip out empty strings 
        paragraphs = [GalleryPage.soup_as_text(s) for s in paragraphs_in_soup]

        filtered_paragraphs_in_soup = []
        filtered_paragraphs = []
        for k in range(len(paragraphs)):
            if not paragraphs[k]: continue

            filtered_paragraphs_in_soup.append(paragraphs_in_soup[k])
            filtered_paragraphs.append(paragraphs[k])

        background_indices = []

        # Test the last four paragraphs for background info
        for k in range(-3,0):

            # The first paragraph is never background info
            if len(filtered_paragraphs) <= -k: continue

            # Stop each paragraph search if any background substring is found
            for test_str in BACKGROUND_STRINGS:
                if test_str in filtered_paragraphs[k]:
                    background_indices.append(k)
                    break

        self.background_indices = background_indices    # save for debugging

        # Split up the paragraphs as caption and background; create new
        # BeautifulSoup objects
        caption_as_soup    = BeautifulSoup('', PARSER)
        background_as_soup = BeautifulSoup('', PARSER)
        for k in range(-len(filtered_paragraphs), 0):

            if k in background_indices:
                background_as_soup.append(filtered_paragraphs_in_soup[k])
            else:
                caption_as_soup.append(filtered_paragraphs_in_soup[k])

        return (caption_as_soup, background_as_soup)

    def load_pia_table(self):
        """Gets all the information inside the table."""

        table = {}

        # The table row are best recognized by the unique bgcolor
        rows = self.soup.find_all('tr', attrs={'bgcolor':"#eeeeee"})
        for row in rows:
            columns = row.find_all('td')

            pair = []
            for column in columns:

              # Clean up Unicode
              text = str(''.join([c if ord(c) < 128 else ' '
                         for c in column.text]))
              text = text.strip()

              text = text.replace('\r', '\n')
              items = text.split('\n')

              for k in range(len(items)):
                item = items[k]
                item = item.strip()
                item = item.replace('\\r','').replace('\\n','') # Fix HTML
                item = item.strip()
                items[k] = item

              items = [i for i in items if i]
              pair.append(items)

            key = pair[0][0].replace(':','')
            table[key] = pair[1]

        return table

    def find_xrefs(self):
        """This will find any cross references to different PIA"""

        xrefs = PIA_REGEX.findall(self.html)

        # Return unique values in numeric order
        xrefs = list(set(xrefs))
        xrefs.remove(self.id)
        xrefs.sort()
        return xrefs

################################################################################
# Unit tests
################################################################################

import unittest

# class Test_PiaPage(unittest.TestCase):
# 
#     def runTest(self):
# 
#         # Tests of get_id
#         self.assertEqual(PiaPage.get_id(1), 'PIA00001')
#         self.assertEqual(PiaPage.get_id(12345), 'PIA12345')
#         self.assertEqual(PiaPage.get_id('PIA12345'), 'PIA12345')
#         self.assertEqual(PiaPage.get_id('PIA12xxx/PIA12345.txt'),
#                                              'PIA12345')
#         self.assertEqual(PiaPage.get_id(PiaPage.PIA_URL +
#                                              'PIA12345'), 'PIA12345')
# 
#         # Tests of filepath_from_source (regardless of piaroot)
#         self.assertTrue(PiaPage.filepath_from_source(1).endswith(
#                                 'PIA00xxx/PIA00001.txt'))
#         self.assertTrue(PiaPage.filepath_from_source(12345).endswith(
#                                 'PIA12xxx/PIA12345.txt'))
#         self.assertTrue(PiaPage.filepath_from_source('PIA12345').endswith(
#                                 'PIA12xxx/PIA12345.txt'))
#         self.assertTrue(PiaPage.filepath_from_source('PIA12xxx/PIA12345.whatever').endswith(
#                                 'PIA12xxx/PIA12345.txt'))
#         self.assertTrue(PiaPage.filepath_from_source(PiaPage.PIA_URL +
#                                 'PIA12345').endswith(
#                                 'PIA12xxx/PIA12345.txt'))
# 
#         # Tests of filepath_from_source (with specified piaroot)
#         self.assertEqual(PiaPage.filepath_from_source(1, '/root'),
#                                 '/root/PIA00xxx/PIA00001.txt')
#         self.assertEqual(PiaPage.filepath_from_source(12345, '/root'),
#                                 '/root/PIA12xxx/PIA12345.txt')
#         self.assertEqual(PiaPage.filepath_from_source('PIA12345', '/root'),
#                                 '/root/PIA12xxx/PIA12345.txt')
#         self.assertEqual(PiaPage.filepath_from_source(
#                                 'PIA12xxx/PIA12345.whatever', '/root'),
#                                 '/root/PIA12xxx/PIA12345.txt')
#         self.assertEqual(PiaPage.filepath_from_source(PiaPage.PIA_URL +
#                                              'PIA12345', '/root'),
#                                 '/root/PIA12xxx/PIA12345.txt')
# 
#         self.assertEqual(PiaPage.filepath_from_source(1, ''),
#                                 'PIA00xxx/PIA00001.txt')
#         self.assertEqual(PiaPage.filepath_from_source(12345, ''),
#                                 'PIA12xxx/PIA12345.txt')
#         self.assertEqual(PiaPage.filepath_from_source('PIA12345', ''),
#                                 'PIA12xxx/PIA12345.txt')
#         self.assertEqual(PiaPage.filepath_from_source(
#                                 'PIA12xxx/PIA12345.whatever', ''),
#                                 'PIA12xxx/PIA12345.txt')
#         self.assertEqual(PiaPage.filepath_from_source(PiaPage.PIA_URL +
#                                              'PIA12345', ''),
#                                 'PIA12xxx/PIA12345.txt')
# 
#         # Tests of url_from_source
#         self.assertEqual(PiaPage.url_from_source(1),
#                                         PiaPage.PIA_URL + 'PIA00001')
#         self.assertEqual(PiaPage.url_from_source(12345),
#                                         PiaPage.PIA_URL + 'PIA12345')
#         self.assertEqual(PiaPage.url_from_source('PIA12345'),
#                                         PiaPage.PIA_URL + 'PIA12345')
#         self.assertEqual(PiaPage.url_from_source('PIA12345'),
#                                         PiaPage.PIA_URL + 'PIA12345')
#         self.assertEqual(PiaPage.url_from_source(PiaPage.PIA_URL + 'PIA12345'),
#                                         PiaPage.PIA_URL + 'PIA12345')
# 
#         self.assertRaises(ValueError, PiaPage.url_from_source,
#                                         'https://pds-rings.seti.org')
# 
#         # Some of these will only work if PIAPATH is defined in the environment
#         self.assertIn('PIAPATH', os.environ)
# 
#         html_from_file = PiaPage(1).html
#         html_from_url = PiaPage(PiaPage.url_from_source(1), overwrite=True).html
# 
#         self.assertEqual(html_from_file, html_from_url)

################################################################################

# Run unit tests if you invoke the program from the command line

if __name__ == '__main__':
    unittest.main(verbosity=2)

################################################################################
