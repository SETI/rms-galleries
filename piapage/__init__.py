################################################################################
# piapage/__init__.py
################################################################################
# Class PiaPage
#
# A class that customizes the GalleryPage interface for NASA press release web
# pages from the Planetary Photojournal, https://photojournal.jpl.nasa.gov.
#
# Andrew Lin & Mark Showalter
################################################################################

from gallerypage import GalleryPage
import storedpage

from bs4 import BeautifulSoup, ResultSet
import requests
import os
import warnings
import json
import lxml
import re
import pickle
import pycurl
from io import StringIO
from PIL import Image

from .BACKGROUND_STRINGS import BACKGROUND_STRINGS
from .GIF_PIAPAGES       import MEDIUM_GIF_PIAPAGES, \
                                SMALL_GIF_PIAPAGES, \
                                THUMBNAIL_GIF_PIAPAGES
from .COLOR_VS_PIAPAGE   import COLOR_VS_PIAPAGE
from piapage.repairs import repair_tables, repair_piapage

from piapage.MAX_PIAPAGE import MAX_PIAPAGE

PARSER = 'lxml'

PIA_REGEX = re.compile(r'PIA[0-9]{5}')
YMD_REGEX = re.compile(r'[12][0-9]{3}-[01][0-9]-[0-3][0-9]$')

# Any mission that starts with one of these is definitely planetary
MISSIONS_ALWAYS_INCLUDED = set([
    '2001 Mars Odyssey',
    'Cassini',
    'DART',
    'Dawn',
    'Deep Impact',
    'Deep Space',
    'Double Asteroid',  # DART
    'EPOXI',
    'ExoMars',
    'Galileo',
    'InSight',
    'Juno',
    'Kepler',
    'Magellan',
    'Mariner',
    'Mars ',
    'MAVEN',
    'MESSENGER',
    'NEAR',
    'NEOWISE',
    'New Horizons',
    'OSIRIS-REx',
    'Phoenix',
    'Pioneer',
    'Psyche',
    'Rosetta',
    'Stardust',
    'Surveyor',
    'Viking',
    'Voyager',
])

class PiaPage(GalleryPage):
    """PiaPage is a subclass of GalleryPage. It implements the complete
    GalleryPage API for the specific case of a page on the PDS Photojournal
    website, https://photojournal.jpl.nasa.gov."""

    # Class constants
    PHOTOJOURNAL_DOMAIN = "photojournal.jpl.nasa.gov"
    PHOTOJOURNAL_URL = "https://" + PHOTOJOURNAL_DOMAIN

    MISSING_PAGE_TEXT = 'No images in our database met your search criteria'
    BACK_TO_HOME_TEXT = 's.channel="Home"'

    root = os.environ['PIAPATH']
    CACHE_ROOT_ = root.rstrip('/') + '/'        # where to store cached HTML
    CATALOG = CACHE_ROOT_ + 'PIAPAGE_CATALOG.pickle'

    def __init__(self, src, recache=False, download=False, images=False,
                            jekyll=False, replace=False, validate=False,
                            _dict=None):
        """Constructor for a PiaPage object.

        Input:
            src         The PIA source. This can be
                        1. an integer up to five digits.
                        2. 'PIA' followed by a five-digit number, using leading
                           zeros.
                        3. A local path to a file containing the HTML.
                        4. The URL of a PIA page. In this case, the HTML is
                           saved as a local file for future, quick access.

            recache     True to overwrite a local cached copy of the HTML source
                        with one pulled from the website; False to leave any
                        local copy unchanged.

            download    True to download the page if it exists remotely but we
                        do not have a locally cached copy.

            images      'all' to download all images associated with downloaded
                        pages; 'planetary' to download images only if they are
                        planetary; None or False to skip the downloading of
                        images. A warning is raised if one or more of the images
                        cannot be downloaded.

            jekyll      'all' to create a Jekyll source file for every page;
                        'planetary' to create one for planetary images only;
                        'new-all' to create a Jekyll page only if it does not
                        already exist; 'new-planetary' to create a Jekyll page
                        for any planetary page that does not already exist.
                        None or False to prevent the creation of a Jekyll page.

            validate    'all' to validate the existence of associated images
                        for all pages; 'planetary' to validate associated images
                        if they are planetary; None or False to skip validation.

            _dict       if not None, this is a dictionary used to fill in all
                        the object's attributes. Other input parameters are
                        ignored. Used to make copies of PiaPage objects or to
                        convert from StoredPages.
        """

        # Make a copy if necessary
        if _dict:
            for (key, value) in _dict.iteritems():
                self.__dict__[key] = value

            return

        # Otherwise use the standard constructor

        # Check the input arguments
        if images:
            if images not in ('all', 'planetary'):
                raise ValueError('Invalid images arg: ' + str(images))

        if validate:
            if validate not in ('all', 'planetary'):
                raise ValueError('Invalid validate arg: ' + str(validate))

        if jekyll:
            if jekyll not in ('all', 'planetary', 'new-all', 'new-planetary'):
                raise ValueError('Invalid jekyll arg: ' + str(jekyll))

        # Otherwise use the standard constructor
        self.source = src

        self.id = PiaPage.get_id(self.source)
                            # Unique identifier for this product, e.g., PIA12345
        self.origin_url = PiaPage.url_from_source(self.source)

        # Read the page as HTML
        self.html = PiaPage.get_html_for_id(self.source, recache, download)

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
        self.acquisition_date = ''      # Not generally available for PIA pages
        self.xrefs = self.find_xrefs()

        self.is_movie = self.get_is_movie()
        self.is_color = self.get_is_color()
        self.is_grayscale = self.get_is_grayscale()

        # Get key information from the PIA page's table
        self.get_pia_tables()
        missions    = self.pia_table.get('Mission', [''])
        hosts       = self.pia_table.get('Spacecraft', [''])
        instruments = self.pia_table.get('Instrument', [''])
        targets     = self.pia_table.get('Target Name', [''])
        systems     = self.pia_table.get('Is a satellite of', [''])

        # Fix known errors and weirdness in tables
        (missions, hosts, instruments,
         targets, systems) = repair_tables(missions, hosts, instruments,
                                           targets, systems)

        # Replace tabulated names with their full or corrected names
        # Identify primary values

        targets = [GalleryPage.full_target_name(t) for t in targets]
        targets = [str(t) for t in targets]
        self._primary_targets = targets             # assume targets are
                                                    # in primary order

        systems = [GalleryPage.full_target_name(s) for s in systems]
        systems = [str(s) for s in systems]
        self._primary_systems = systems

        self._primary_target_types = [GalleryPage.target_type_from_target(t)
                                      for t in targets]

        instruments = [GalleryPage.full_instrument_name(i)
                       for i in instruments]
        instruments = [str(i) for i in instruments] # needed?
        self._primary_instruments = instruments     # assume instruments are
                                                    # in primary order

        hosts = [GalleryPage.full_host_name(h) for h in hosts]
        hosts = [str(h) for h in hosts]
        self._primary_hosts = hosts

        missions = [GalleryPage.full_mission_name(m) for m in missions]
        missions = [str(m) for m in missions]
        self._primary_missions = missions

        # Scrape the text for more keyword values
        _ = self.keywords
        _ = self.targets
        _ = self.target_types
        _ = self.systems
        _ = self.missions
        _ = self.hosts
        _ = self.instruments
        _ = self.detectors

        # Apply known corrections
        repair_piapage(self)

        # Earth and Sun images are only treated as planetary if they include a
        # planetary target or come from a planetary mission
        target_types_filtered = set(self.target_types)
        target_types_filtered.discard('')
        target_types_filtered.discard('Sun')
        target_types_filtered.discard('Earth')
        self.is_planetary = len(target_types_filtered) > 0

        for pattern in MISSIONS_ALWAYS_INCLUDED:
            for mission in self.missions:
                if mission.startswith(pattern):
                    self.is_planetary = True
                    break

        if not self.might_be_planetary:
            self.is_planetary = False

        # Locate remote resources and relevant info
        self.remote_version_info = {}

        if 'Product Size' in self.pia_table:
            text = self.pia_table['Product Size'][0]
            w_x_h = text.partition(' pixels')[0]
            parts = w_x_h.split(' x ')
            width  = int(parts[0])
            height = int(parts[1])
            self.shape = (width, height)
        else:
            self.shape = None

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
                except KeyboardInterrupt:
                    sys.exit(1)
                except Exception:
                    pass            # If anything goes wrong, size = 0

            size = int(size + 0.5)  # round to int
            self.remote_version_info[key] = (PiaPage.PHOTOJOURNAL_URL + href,
                                             self.shape, size)

        for img in self.soup.find_all('img'):
            if 'browse' in img.attrs['src']:
                self.remote_version_info['Browse Image'] = (
                        PiaPage.PHOTOJOURNAL_URL + str(img.attrs['src']), (), 0)
                break

        for a in self.soup.find_all('a'):
            if 'jpegMod' in a.attrs['href']:
                self.remote_version_info['Medium Image'] = (
                        PiaPage.PHOTOJOURNAL_URL + str(a.attrs['href']), (), 0)
                break

        # If it's a movie
        if self.is_movie:
            self.remote_version_info['Movie Download Options'] = \
                    (PiaPage.PHOTOJOURNAL_URL + '/animation/' + self.id, (), 0)

        self.local_page_url      = PiaPage.local_page_url_for_id(self.id)
        self.local_thumbnail_url = PiaPage.local_thumbnail_url_for_id(self.id)
        self.local_small_url     = PiaPage.local_small_url_for_id(self.id)
        self.local_medium_url    = PiaPage.local_medium_url_for_id(self.id)

        # Download images or validate if necessary
        TEST = [('all', True), ('all', False), ('planetary', True)]
        if (images, self.is_planetary) in TEST:
            PiaPage.download_images_for_id(self.id, replace=False,
                                                    verbose=True, warn=True)

        elif (validate, self.is_planetary) in TEST:
            path = PiaPage.thumbnail_filepath_for_id(self.id)
            if not os.path.exists(path):
                raise IOError('Missing thumbnail for %s: %s' % (self.id, path))

            path = PiaPage.small_filepath_for_id(self.id)
            if not os.path.exists(path):
                raise IOError('Missing small image for %s: %s' % (self.id,
                                                                  path))

            path = PiaPage.medium_filepath_for_id(self.id)
            if not os.path.exists(path):
                raise IOError('Missing medium image for %s: %s' % (self.id,
                                                                   path))

        # Create the Jekyll file if necessary
        if jekyll:
            new_only = jekyll.startswith('new')
            if new_only:
                jekyll = jekyll[4:]

            if (jekyll, self.is_planetary) in TEST:
                self.write_jekyll(replace=(not new_only), verbose=new_only)

        # Fill in the thumbnail shape if possible
        path = PiaPage.thumbnail_filepath_for_id(self.id)
        if os.path.exists(path):
            im = Image.open(path)
            self.thumbnail_shape = im.size
            im.close()
        else:
            self.thumbnail_shape = None

    ############################################################################
    # Procedures to locate URLs and files
    ############################################################################

    @staticmethod
    def remote_page_url_for_id(id):

        id = PiaPage.get_id(id)
        return PiaPage.PHOTOJOURNAL_URL + '/catalog/' + id

    @staticmethod
    def remote_thumbnail_url_for_id(id):

        id = PiaPage.get_id(id)

        ipia = int(id[3:])
        if ipia in THUMBNAIL_GIF_PIAPAGES:
            return PiaPage.PHOTOJOURNAL_URL + '/thumb/' + id + '.gif'
        else:
            return PiaPage.PHOTOJOURNAL_URL + '/thumb/' + id + '.jpg'

    @staticmethod
    def remote_small_url_for_id(id):

        id = PiaPage.get_id(id)

        ipia = int(id[3:])
        if ipia in SMALL_GIF_PIAPAGES:
            return PiaPage.PHOTOJOURNAL_URL + '/browse/' + id + '.gif'
        else:
            return PiaPage.PHOTOJOURNAL_URL + '/jpeg/' + id + '.jpg'

    @staticmethod
    def remote_medium_url_for_id(id, is_movie):

        id = PiaPage.get_id(id)

        ipia = int(id[3:])
        if ipia in MEDIUM_GIF_PIAPAGES:
            suffix = 'gif'
        elif is_movie:
            return PiaPage.PHOTOJOURNAL_URL + '/animation/' + id + '.gif'
        else:
            suffix = 'jpg'

        return PiaPage.PHOTOJOURNAL_URL + '/jpegMod/' + id + '_modest.jpg'

    @staticmethod
    def local_page_url_for_id(id):

        id = PiaPage.get_id(id)
        return '/' + GalleryPage.PRESS_RELEASES_SUBDIR_ + \
                        'pages/%sxxx/%s.html' % (id[:5], id)

    @staticmethod
    def local_thumbnail_url_for_id(id):

        id = PiaPage.get_id(id)

        ipia = int(id[3:])
        if ipia in THUMBNAIL_GIF_PIAPAGES:
            suffix = 'gif'
        else:
            suffix = 'jpg'

        return '/' + GalleryPage.PRESS_RELEASES_SUBDIR_ + \
                        'thumbnails/%sxxx/%s_thumb.%s' % (id[:5], id, suffix)

    @staticmethod
    def local_small_url_for_id(id):

        id = PiaPage.get_id(id)

        ipia = int(id[3:])
        if ipia in SMALL_GIF_PIAPAGES:
            suffix = 'gif'
        else:
            suffix = 'jpg'

        return '/' + GalleryPage.PRESS_RELEASES_SUBDIR_ + \
                        'small/%sxxx/%s_small.%s' % (id[:5], id, suffix)

    @staticmethod
    def local_medium_url_for_id(id):

        id = PiaPage.get_id(id)
        ipia = int(id[3:])

        if ipia in MEDIUM_GIF_PIAPAGES:
            suffix = 'gif'
        else:
            suffix = 'jpg'

        return '/' + GalleryPage.PRESS_RELEASES_SUBDIR_ + \
                        'medium/%sxxx/%s_med.%s' % (id[:5], id, suffix)

    @staticmethod
    def page_filepath_for_id(id):

        return GalleryPage.DOCUMENTS_FILE_ROOT_[:-1] + \
               PiaPage.local_page_url_for_id(id)

    @staticmethod
    def thumbnail_filepath_for_id(id):

        return GalleryPage.DOCUMENTS_FILE_ROOT_[:-1] + \
               PiaPage.local_thumbnail_url_for_id(id)

    @staticmethod
    def small_filepath_for_id(id):

        return GalleryPage.DOCUMENTS_FILE_ROOT_[:-1] + \
               PiaPage.local_small_url_for_id(id)

    @staticmethod
    def medium_filepath_for_id(id):

        return GalleryPage.DOCUMENTS_FILE_ROOT_[:-1] + \
               PiaPage.local_medium_url_for_id(id)

    @staticmethod
    def cache_filepath_for_id(id):

        id = PiaPage.get_id(id)
        return PiaPage.CACHE_ROOT_ + '%sxxx/%s.txt' % (id[:5], id)

    ############################################################################
    # Main routine to retrieve HTML from either a local or remote site, and to
    # cache a local copy if requested.
    ############################################################################

    @staticmethod
    def get_html_for_id(source, recache=False, download=True):
        """Obtain the html from a PIA number or string"""

        # Convert the PIA code from a string if necessary
        if isinstance(source, int):
            source = PiaPage.get_id(source)

        # If this is not a URL, read a local file if possible
        if not PiaPage.is_url(source) and not recache:
            if os.path.exists(source):
                filepath = source
            else:
                filepath = PiaPage.filepath_from_source(source)

            try:
                with open(filepath, 'r') as file:
                    html = file.read()
#                 return str(html.encode('ascii', 'xmlcharrefreplace'))
                return html

            # If local file not found
            except IOError:
                pass

        # Otherwise, get the online version
        if not download:
            raise IOError('Local copy of page "%s" not found' % source)

        if PiaPage.is_url(source):
            url = source
        else:
            url = PiaPage.url_from_source(source)

        req = requests.get(url)

        # Make sure we got back a good request
        if (req.status_code != 200 or
            PiaPage.MISSING_PAGE_TEXT in req.text or
            PiaPage.BACK_TO_HOME_TEXT in req.text):
                raise IOError('URL not found: "%s"' % url)

        print('Downloaded ' + url)

        # Replace non-ASCII characters that normally break HTML
#         cleaned = ''.join(c if ord(c) < 128 else ' ' for c in req.text)
        cleaned = req.text

        # Save the file so we don't need to retrieve it next time
        filepath = PiaPage.filepath_from_source(source)
        if recache or not os.path.exists(filepath):
            parent = os.path.split(filepath)[0]
            if not os.path.exists(parent):
                os.mkdir(parent)

            with open(filepath, 'w') as file:
                file.write(cleaned)

        return cleaned

    @staticmethod
    def download_images_for_id(id, is_movie=False, replace=False,
                                                   verbose=False, warn=True):
        """Download local copies of the thumbnail, small and medium images."""

        path = PiaPage.thumbnail_filepath_for_id(id)
        if replace or not os.path.exists(path):
            url = PiaPage.remote_thumbnail_url_for_id(id)

            try:
                buffer = StringIO()
                c = pycurl.Curl()
                c.setopt(c.URL, url)
                c.setopt(c.WRITEDATA, buffer)
                c.perform()
                c.close()

                parent = os.path.split(path)[0]
                try:
                    os.makedirs(parent)
                except OSError:
                    pass

                with open(path, 'w') as f:
                    f.write(buffer.getvalue())

            except KeyboardInterrupt:
                sys.exit(1)

            except Exception:
                if warn:
                    warnings.warn('Unable to download thumbnail for ' + id)
                else:
                    raise

            if verbose:
                print('Thumbnail downloaded for ' + id)

        path = PiaPage.small_filepath_for_id(id)
        if replace or not os.path.exists(path):
            url = PiaPage.remote_small_url_for_id(id)

            try:
                buffer = StringIO()
                c = pycurl.Curl()
                c.setopt(c.URL, url)
                c.setopt(c.WRITEDATA, buffer)
                c.perform()
                c.close()

                parent = os.path.split(path)[0]
                try:
                    os.makedirs(parent)
                except OSError:
                    pass

                with open(path, 'w') as f:
                    f.write(buffer.getvalue())

            except KeyboardInterrupt:
                sys.exit(1)

            except Exception:
                if warn:
                    warnings.warn('Unable to download small image for ' + id)
                else:
                    raise

            if verbose:
                print('Small image downloaded for ' + id)

        path = PiaPage.medium_filepath_for_id(id)
        if replace or not os.path.exists(path):
            url = PiaPage.remote_medium_url_for_id(id, is_movie)

            try:
                buffer = StringIO()
                c = pycurl.Curl()
                c.setopt(c.URL, url)
                c.setopt(c.WRITEDATA, buffer)
                c.perform()
                c.close()

                parent = os.path.split(path)[0]
                try:
                    os.makedirs(parent)
                except OSError:
                    pass

                with open(path, 'w') as f:
                    f.write(buffer.getvalue())

            except KeyboardInterrupt:
                sys.exit(1)

            except Exception:
                if warn:
                    warnings.warn('Unable to download medium image for ' + id)
                else:
                    raise

            if verbose:
                print('Medium image downloaded for ' + id)

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
        return PiaPage.cache_filepath_for_id(id)

    @staticmethod
    def url_from_source(source):
        """Return the URL based on the source."""

        id = PiaPage.get_id(source)
        return PiaPage.remote_page_url_for_id(id)

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

    def get_acquisition_date(self):
        return ''

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
            return COLOR_VS_PIAPAGE[ipia] == '3'
        except IndexError:
            return False

    def get_is_grayscale(self):
        """Return True if this is black and white; False if it is a in color or
        unknown."""

        ipia = int(self.id[3:])
        try:
            return COLOR_VS_PIAPAGE[ipia] == '1'
        except IndexError:
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

        # Test the last eight paragraphs for background info
        for k in range(1,len(filtered_paragraphs)):

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
        background_found = False
        for k in range(len(filtered_paragraphs)):

            if k in background_indices:
                background_found = True
                background_as_soup.append(filtered_paragraphs_in_soup[k])
            else:
#                 if background_found:
#                     print('WARNING, interleaved caption: ' + str(k) + ' ' + str(self.id))
                caption_as_soup.append(filtered_paragraphs_in_soup[k])

        return (caption_as_soup, background_as_soup)

    def get_pia_tables(self):
        """Gets all the information inside the table."""

        table = {}
        soup_table = {}

        # The table rows are best recognized by the unique bgcolor
        rows = self.soup.find_all('tr', attrs={'bgcolor':"#eeeeee"})
        for row in rows:
            columns = row.find_all('td')
            soup_value = columns[1]

            pair = []
            for column in columns:

              # Clean up Unicode
              text = column.text
              text = str(''.join([c if ord(c) < 128 else ' ' for c in text]))
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
            if pair[1]:
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

################################################################################
# Jekyll routines
################################################################################

    @staticmethod
    def jekyll_filepath_for_id(id):

        id = PiaPage.get_id(id)
        return PiaPage.JEKYLL_ROOT_ + GalleryPage.PRESS_RELEASES_SUBDIR_ + \
                    'pages/%sxxx/%s.html' % (id[:5], id)

    pattern = '"https?://' + PHOTOJOURNAL_DOMAIN + '/catalog/(PIA..)(...)"'
    XREF_BEFORE = re.compile(pattern)
    XREF_AFTER  = r'"/%spages/\1xxx/\1\2.html"' % \
                                    GalleryPage.PRESS_RELEASES_SUBDIR_

    TABLE0_BEFORE = re.compile('<table')
    TABLE0_AFTER  = (r'\n<table width="840px">' +
                     r'<tr id="noborder">' +
                     r'<td id="noborder">\n' +
                     r'<table style="margin-left:auto;margin-right:auto;"')

    TABLE1_BEFORE = re.compile('</table>')
    TABLE1_AFTER  = (r'</table>\n' +
                     r'</td></tr></table>\n')

    def write_jekyll(self, neighbors=None, replace=False, verbose=False):
        """Uses the default method in _GalleryPage but fills in the default
        arguments."""

        path = PiaPage.jekyll_filepath_for_id(self.id)
        parent = os.path.split(path)[0]
        try:
            os.makedirs(parent)
        except OSError:
            pass

        if replace or not os.path.exists(path):
            remote_keys = ['Movie Download Options',
                           'Full-Res JPEG', 'Full-Res TIFF']

            self._write_jekyll(path, remote_keys,
                               [(PiaPage.XREF_BEFORE, PiaPage.XREF_AFTER),
                                (PiaPage.TABLE0_BEFORE, PiaPage.TABLE0_AFTER),
                                (PiaPage.TABLE1_BEFORE, PiaPage.TABLE1_AFTER)],
                                neighbors=neighbors)

            if verbose:
                print('Jekyll file written: ' + path)

################################################################################
# Catalog support functions
#
# A catalog is a dictionary of GalleryPage objects keyed by the product ID.
# These are saved in pickle files.
################################################################################

def build_catalog(incremental=True, verbose=True, download=False, path=None,
                  page_range=None, more_verbose=False):
    """Update or replace a catalog of the PiaPage objects.

    Input:
        incremental if True, the existing catalog is loaded and missing pages
                    are added to it; otherwise, an entirely new catalog is
                    written. Default is True for an incremental build.
        verbose     True to report progress.
        download    True to download pages not locally cached.
    """

    if not path:
        path = PiaPage.CATALOG

    if incremental:
        try:
            with open(path) as f:
                piapages = pickle.load(f)

            if verbose:
                print('catalog loaded')

            updating = True
        except:
            piapages = {}
            if verbose:
                print('starting new catalog')

            updating = False
    else:
        updating = False
        piapages = {}

    if not page_range:
        page_range = (1, MAX_PIAPAGE)

    for pia in range(*page_range):

        # Skip pages already in catalog if appropriate
        if updating and pia in piapages:
            continue

        # If not updating, print every 100th number
        if more_verbose:
            print(pia)
        elif verbose and not updating:
            if pia % 100 == 0:
                print(pia)   # Otherwise, print(every 100th

        # Try to read the PiaPage
        try:
            p = PiaPage(pia, download=download,
                             images='planetary' if download else False,
                             jekyll='planetary' if download else False)
        except IOError:
            continue
        except ValueError as e:
            print('**** Error in PIA%05d' % pia, e)
            continue

        # Always skip non-planetary
        if not p.is_planetary:
            continue

        if verbose and updating:
            print(pia)     # If updating, print every new ID

        piapages[p.id] = p

    return piapages

def save_catalog(catalog, path=None):
    """Save a catalog. Pages are converted to StoredPage objects to reduce
    the size of the file."""

    if not path:
        path = PiaPage.CATALOG

    storedpage.save_catalog(catalog, path)

def load_catalog(path=None):
    """Load a dictionary of PiaPage objects as stored in a pickle file.

    Note that they are converted back from StoredPage objects so some attributes
    will be missing. However, all the required attributes are present.
    """

    if not path:
        path = PiaPage.CATALOG

    catalog = storedpage.load_catalog(path)

    piapages = {}
    for (key, value) in catalog.iteritems():
        piapages[key] = PiaPage(value.id, _dict=value.__dict__)

    return piapages

################################################################################
