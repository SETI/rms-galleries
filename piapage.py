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
from piapage_gifs import PIAPAGE_MEDIUM_GIFS, PIAPAGE_SMALL_GIFS, \
                         PIAPAGE_THUMBNAIL_GIFS
from piapage_color_string import PIAPAGE_COLOR_STRING

PARSER = 'lxml'

PIA_REGEX = re.compile(r'PIA[0-9]{5}')
YMD_REGEX = re.compile(r'[12][0-9]{3}-[01][0-9]-[0-3][0-9]$')

REQUIRED_MISSIONS = set([
    'Cassini-Huygens',
    'Dawn',
    'Deep Impact',
    'Galileo',
    'Kepler',
    'Juno',
    'Magellan',
    'Mariner',
    'MESSENGER',
    'NEAR Shoemaker',
    'New Horizons',
    'Phoenix',
    'Viking',
    'Voyager',
])

EXCLUDED_MISSIONS = set([
    'Aqua',
    'Aura',
    'FINESSE',
    'Galaxy Evolution Explorer (GALEX)',
    'GALEX Orbiter',
    'NuSTAR',
    'UAVSAR'
])

class PiaPage(GalleryPage):

    # Class constants
    ROOT_URL = "https://photojournal.jpl.nasa.gov"
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
#         self.local_url  = PiaPage.local_url(self.id)

        # Read the page as HTML
        self.html = PiaPage.get_html_for_id(self.source, overwrite)

#       The default parser cannot handle some PIA pages. lxml does.
#       self.soup = BeautifulSoup(self.html, 'html.parser')
        self.soup = BeautifulSoup(self.html, PARSER)

        # Validate the PIA page
        if len(self.soup.find_all('dt')) != 3:
            raise ValueError(self.id + " page does not contain three " +
                                       "description tags")

        text = self.soup.find_all('dt')[0].text.strip()
        if 'Caption' not in text:
            raise ValueError(self.id + " page contains no caption")

        text = self.soup.find_all('dt')[1].text.strip()
        if not text.startswith("Image Credit:"):
            raise ValueError(self.id + " page contains no image credit")

        text = self.soup.find_all('dt')[2].text.strip()
        if not text.startswith("Image Addition Date:"):
            raise ValueError(self.id + " page contains no image date")

        text = self.soup.find_all('b')[0].text.lstrip()
        if text[:8] != self.id:
            raise ValueError(self.id + " page has invalid title: " + text)

        # Extract the caption and separate it from the background info
        (self.caption_soup,
         self.background_soup) = self.get_caption_and_background()

        self.title = self.get_title()
        self.credit = self.get_credit()
        self.release_date = self.get_release_date()
        self.xrefs = self.find_xrefs()

        self.is_movie = self.get_is_movie()
        self.is_color = self.get_is_color()
        self.is_grayscale = self.get_is_grayscale()

        # Get key information from the PIA page's table
        self.get_pia_tables()
        missions    = self.pia_table.get('Mission', [])
        hosts       = self.pia_table.get('Spacecraft', [])
        instruments = self.pia_table.get('Instrument', [])
        targets     = self.pia_table.get('Target Name', [])

        if targets and 'Sol' in targets[0]:
            targets[0] = 'Sun'

        # Known errors in pages
        if 'Comet' in targets and 'Rosetta' in missions:
            targets[targets.index('Comet')] = '67P/Churyumov-Gerasimenko'

        if 'Dawn' in missions and 'Field Experiment' in hosts:
            hosts = ['Dawn']

        if 'Mars Pathfinder (MPF)' in missions and 'Field Experiment' in hosts:
            hosts.remove('Field Experiment')

        if 'Hubble Space Telescope' in instruments:
            instruments.remove('Hubble Space Telescope')
            hosts += ['Hubble Space Telescope (HST)']

        if 'MESSENGER' in missions and \
           'Gamma-ray Spectrometer (GRS)' in instruments:
                k = instruments.index('Gamma-ray Spectrometer (GRS)')
                instruments[k] = 'Gamma-Ray and Neutron Spectrometer (GRNS)'

        if self.id == 'PIA15485':
            hosts.append('-Deep Impact')
            missions.append('-Deep Impact')

        if 'Mars Volcanic Emission Life Scout (MARVEL)' in instruments:
            instruments.remove('Mars Volcanic Emission Life Scout (MARVEL)')

        if 'VIRTIS' in instruments and 'Venus Express' in hosts:
            hosts.remove('Venus Express')
            self._primary_hosts = ['Venus Express']
            hosts = ['Venus Express'] + hosts

        if 'Cassini-Huygens' in missions and \
           'Infrared Spectrometer' in instruments:
                k = instruments.index('Infrared Spectrometer')
                instruments[k] = 'Composite Infrared Spectrometer (CIRS)'

        if 'Cassini-Huygens' in missions and \
           'Infrared Spectrometer (IRS)' in instruments:
                k = instruments.index('Infrared Spectrometer (IRS)')
                instruments[k] = 'Composite Infrared Spectrometer (CIRS)'

        if 'Visible Light' in instruments:
            instruments.remove('Visible Light')

        if 'Ultraviolet Light' in instruments:
            instruments.remove('Ultraviolet Light')

        # Order might matter here because certain properties depend on others

        if instruments:
            instruments = [GalleryPage.full_instrument_name(i)
                           for i in instruments]
            instruments = [str(i) for i in instruments]
            self._primary_instruments = instruments     # assume instruments are
                                                        # in primary order

            # If any of these refer to known detectors, add them to the detector
            # list
            self._primary_detectors = []
            for inst in instruments:
                detector = GalleryPage.full_detector_name(inst)
                if detector:
                    self._primary_detectors.append(detector)

        if hosts:
            hosts = [GalleryPage.full_host_name(h) for h in hosts]
            hosts = [str(h) for h in hosts]
            if not self.instruments or not self.instruments[0]:
                self._primary_hosts = hosts
            self._hosts = hosts

        if missions:
            missions = [GalleryPage.full_mission_name(m) for m in missions]
            missions = [str(m) for m in missions]
            if not self.hosts or not self.hosts[0]:
                self._primary_missions = missions
            self._missions = missions

        if targets:
            targets = [GalleryPage.full_target_name(t) for t in targets]
            targets = [str(t) for t in targets]
            self._primary_targets = targets         # assume targets are
                                                    # in primary order

        systems = self.pia_table.get('Is a satellite of', [])
        if systems and 'Sol' in systems[0]:
            systems = self.pia_table.get('Target Name', [])
            systems = [str(s) for s in systems]
            systems = [s for s in systems if s in
                        ['Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus',
                         'Neptune', 'Pluto']]

            if not systems:
                systems = ['']

            if len(systems) == 1 and not targets:
                self._primary_systems = [systems[0]]
            self._systems = systems

        # Determine if this is a planetary press release
        target_types_filtered = set(self.target_types)
        target_types_filtered.discard('')
        target_types_filtered.discard('Sun')
        target_types_filtered.discard('Earth')

        self.is_planetary = len(target_types_filtered) != 0

        for mission in self.missions:
            if mission in REQUIRED_MISSIONS or 'Mars' in mission:
                self.is_planetary = True
                break

        for mission in self.missions:
            if mission in EXCLUDED_MISSIONS:
                self.is_planetary = False
                break

        # Locate remote resources and relevant info
        self.remote_version_info = {}

        if 'Product Size' in self.pia_table:
            text = self.pia_table['Product Size'][0]
            w_x_h = text.partition(' pixels')[0]
            parts = w_x_h.split(' x ')
            width  = int(parts[0])
            height = int(parts[1])
            shape = (width, height)
        else:
            shape = ()

        # Find the images and sizes in bytes
        for (key,value) in self.pia_soup_table.items():
            try:
                href = value.a.attrs['href']
            except (KeyError, AttributeError):
                continue

            if 'PIA' not in href: continue

            info = self.pia_table[key][0].partition('(')[2].strip()
            size = 0
            if info:
                try:
                    size_str = info.partition(')')[0]
                    parts = size_str.split(' ')
                    size = float(parts[0])
                    units = parts[1].strip()
                    if units == 'MB':
                        size *= 1.e6
                    elif units == 'kB':
                        size *= 1000.
                except Exception:
                    pass            # If anything goes wrong, size = 0

            size = int(size + 0.5)  # round to int
            self.remote_version_info[key] = (PiaPage.ROOT_URL + href,
                                             shape, size)

        for img in self.soup.find_all('img'):
            if 'browse' in img.attrs['src']:
                self.remote_version_info['Browse Image'] = (
                                PiaPage.ROOT_URL + str(img.attrs['src']), (), 0)
                break

        for a in self.soup.find_all('a'):
            if 'jpegMod' in a.attrs['href']:
                self.remote_version_info['Medium Image'] = (
                                PiaPage.ROOT_URL + str(a.attrs['href']), (), 0)
                break

        # If it's a movie
        if self.is_movie:
            self.remote_version_info['Movie Download Options'] = \
                            (PiaPage.ROOT_URL + '/animation/' + self.id, (), 0)

        self.local_html_url      = PiaPage.local_html_url_for_id(self.id)
        self.local_thumbnail_url = PiaPage.local_thumbnail_url_for_id(self.id)
        self.local_small_url     = PiaPage.local_small_url_for_id(self.id)
        self.local_medium_url    = PiaPage.local_medium_url_for_id(self.id,
                                                                  self.is_movie)

    ############################################################################
    # Procedures to locate URLs
    ############################################################################

    @staticmethod
    def local_html_url_for_id(id):

        return GalleryPage.LOCAL_ROOT_ + 'pages/%sxxx/%s.html' % (id[:5], id)

    @staticmethod
    def local_thumbnail_url_for_id(id):

        ipia = int(id[3:])
        if ipia in PIAPAGE_THUMBNAIL_GIFS:
            suffix = 'gif'
        else:
            suffix = 'jpg'

        return GalleryPage.LOCAL_ROOT_ + \
                        'thumbnails/%sxxx/%s_thumb.%s' % (id[:5], id, suffix)

    @staticmethod
    def local_small_url_for_id(id):

        ipia = int(id[3:])
        if ipia in PIAPAGE_SMALL_GIFS:
            suffix = 'gif'
        else:
            suffix = 'jpg'

        return GalleryPage.LOCAL_ROOT_ + \
                        'small/%sxxx/%s_small.%s' % (id[:5], id, suffix)

    @staticmethod
    def local_medium_url_for_id(id, is_movie):

        ipia = int(id[3:])
        if ipia in PIAPAGE_MEDIUM_GIFS:
            suffix = 'gif'
        elif is_movie:
            return PiaPage.ROOT_URL + '/animation/' + id
        else:
            suffix = 'jpg'

        return GalleryPage.LOCAL_ROOT_ + \
                        'medium/%sxxx/%s_med.%s' % (id[:5], id, suffix)

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

    def get_is_movie(self):
        """Return True if this is a movie; False if it is a still."""

        test = self.soup.find('td', attrs={'bgcolor': '#cccccc'})
        if not test: return False

        return 'movie' in test.text

    def get_is_color(self):
        """Return True if this is in color; False if it is a grayscale or
        unknown."""

        ipia = int(self.id[3:])
        try:
            return PIAPAGE_COLOR_STRING[ipia] == '3'
        except:
            return False

    def get_is_grayscale(self):
        """Return True if this is black and white; False if it is a in color or
        unknown."""

        ipia = int(self.id[3:])
        try:
            return PIAPAGE_COLOR_STRING[ipia] == '1'
        except:
            return False

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

    def get_pia_tables(self):
        """Gets all the information inside the table."""

        table = {}
        soup_table = {}

        # The table row are best recognized by the unique bgcolor
        rows = self.soup.find_all('tr', attrs={'bgcolor':"#eeeeee"})
        for row in rows:
            columns = row.find_all('td')
            soup_value = columns[1]

            pair = []
            for column in columns:

              # Clean up Unicode
              text = str(''.join([c if ord(c) < 128 else ' '
                         for c in column.text]))
              text = text.strip()

              text = text.replace('\r', '\n')
              items = text.split('\n')

              new_items = []
              for k in range(len(items)):
                item = items[k]
                item = item.strip()
                item = item.replace('\\r','').replace('\\n','') # Fix HTML
                item = item.strip()
                if not item: continue

                parts = item.split(',')
                for part in parts:
                    new_items.append(part.strip())

              pair.append(new_items)

            key = pair[0][0].replace(':','')
            table[key] = pair[1]
            soup_table[key] = soup_value

        self.pia_table = table
        self.pia_soup_table = soup_table

    def find_xrefs(self):
        """This will find any cross references to different PIAs"""

        xrefs = PIA_REGEX.findall(self.html)

        # Return unique values in numeric order
        xrefs = list(set(xrefs))
        xrefs.remove(self.id)
        xrefs.sort()
        return xrefs

    pattern = '"https{0,1}://photojournal.jpl.nasa.gov/catalog/(PIA..)(...)"'
    BEFORE = re.compile(pattern)
    AFTER  = r'"%spages/\1xxx/\1\2.html"' % GalleryPage.LOCAL_ROOT_

    def write_jekyll(self, filepath):
        """Uses super() but fills in the default arguments."""

        remote_keys = ['Movie Download Options',
                      'Full-Res JPEG', 'Full-Res TIFF']
        self._write_jekyll(filepath, remote_keys,
                                     [(PiaPage.BEFORE, PiaPage.AFTER)])

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
