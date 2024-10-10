################################################################################
# Class GalleryPage
#
# An abstract class and methods to handle the reading and interpretation of web
# pages containing press release materials and their captions.
#
# Andrew Lin & Mark Showalter
################################################################################

import os
import re
import julian
import inspect

################################################################################
# Load dictionaries used to standardize keyword values
import dicts                # used by "inspect.getfile" below
from dicts import (
    DETECTOR_FULL_NAMES,
    HOST_FROM_INSTRUMENT,
    HOST_FULL_NAMES,
    HOST_INFO,
    INSTRUMENT_FROM_DETECTOR,
    INSTRUMENT_FULL_NAMES,
    KEYWORDS,
    MISSION_FULL_NAMES,
    SYSTEM_FROM_TARGET,
    TARGET_FULL_NAMES,
)

from HTML_SYMBOLS import HTML_SYMBOLS

# Compile regular expressions for KEYWORDS
KEYWORD_USAGE = {}
compiled = {}
for (category, pairs) in KEYWORDS.items():
    KEYWORD_USAGE[category] = {}

    new_pairs = []
    for (regex, values) in pairs:
#         print(regex)
        new_pairs.append((re.compile(regex), values))
        KEYWORD_USAGE[category][regex] = []

    compiled[category] = new_pairs

KEYWORDS = compiled

def reset_usage():
    for category in KEYWORD_USAGE:
        for regex in KEYWORD_USAGE[category]:
            KEYWORD_USAGE[category][regex] = []

################################################################################

class GalleryPage(object):

    PLANET_NAMES = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus',
                    'Neptune']

    PRESS_RELEASES_SUBDIR_ = 'press_releases/'
    GALLERIES_SUBDIR_      = 'galleries/'
    DOCUMENTS_FILE_ROOT_   = '/Library/WebServer/Documents/'

    # Define the absolute path to the local Jekyll directory
    JEKYLL_ROOT_ = inspect.getfile(dicts).rpartition('dicts/')[0] + 'jekyll/'

    # Null constructor
    def __init__(self):

        # Attributes or properties required for all subclasses

        self.html = ''      # The source page as HTML
        self.soup = None    # The source page as BeautifulSoup

        self.id = ''        # Unique identifier for this product, e.g., PIA12345
        self.origin_url     # The remote URL of the source of this press release

        self.caption_soup = None
                            # The caption represented as BeautifulSoup
        self.background_soup = None
                            # The background information represented as
                            # BeautifulSoup. Background information refers to
                            # descriptions of the mission, instrument, etc. that
                            # is not unique to this page.

        self.title = ''     # Title of page with optional HTML formatting
        self.credit = ''    # Credit info with optional HTML formatting
        self.release_date = ''
                            # Release date in yyyy-mm-dd format if available
        self.acquisition_date = ''
                            # Image acquisition date in yyyy-mm-dd format if
                            # available
        self.xrefs = []     # A list of IDs of products referenced by this one
        self.is_movie = False
                            # True if this is a movie
        self.is_color = False
                            # True if this is known to be in color
        self.is_grayscale = False
                            # True if this product is known to be in black and
                            # white.
        self.is_planetary = False
                            # True if this product relates to the solar system.
        self.shape = (1,1)  # (width, height) of the full-size product.
        self.thumbnail_shape = None
                            # (width, height) of the thumbnail product if
                            # available.

        # Paths on local website
        self.local_medium_url   = ''
        self.local_small_url    = ''
        self.local_thumbnail_url= ''
        self.local_page_url     = ''

        # Source URL
        self.origin_url         = ''

        # A dictionary that returns (url, shape, size) given a key such as
        # "Full-size TIFF". shape is a tuple (w,h). size is in bytes. Both can
        # be None if unknown.
        self.remote_version_info = {}

    ############################################################################
    # Properties for which overrides by subclasses are optional. Default
    # behavior is to search a text string (typically the caption) and report all
    # occurrences of matching text.
    ############################################################################

    @staticmethod
    def soup_as_text(soup):
        text = soup.text
#         if hasattr(soup, 'contents'):
#             text = ' '.join([GalleryPage.soup_as_text(s)
#                              for s in soup.contents])
#         elif hasattr(soup, 'text'):
#             text = soup.text
#         elif hasattr(soup, 'string'):
#             text = soup.string
#         else:
#             text = ''

        text = text.strip()
        text = text.replace('\r', ' ').replace('\n', ' ')
        text = GalleryPage._escape_html(text)

        while '  ' in text:
            text = text.replace('  ', ' ')

        text = text.replace(' .','.').replace(' ,', ',')

        return text

    @property
    def caption_text(self):
        """The caption as a single string, stripped of HTML."""

        if not hasattr(self, '_caption_text'):
            paragraphs_in_soup = list(self.caption_soup.children)
            paragraphs = [GalleryPage.soup_as_text(s)
                          for s in paragraphs_in_soup]
            paragraphs = [p for p in paragraphs if p]
            self._caption_text = '\n\n'.join(paragraphs)

        return self._caption_text

    @property
    def background_text(self):
        """The background as a single string, stripped of HTML."""

        if not hasattr(self, '_background_text'):
            paragraphs_in_soup = list(self.background_soup.children)
            paragraphs = [GalleryPage.soup_as_text(s)
                          for s in paragraphs_in_soup]
            paragraphs = [p for p in paragraphs if p]
            self._background_text = '\n\n'.join(paragraphs)

        return self._background_text

    @property
    def keywords(self):
        """A list of keywords associated with the caption."""

        # If the value is a subclass attribute, return it
        if hasattr(self, '_keywords'):
            return self._keywords

        keywords_used = set()
        keywords_used |= set(self.targets)
        keywords_used |= set(self.systems)
        keywords_used |= set(self.target_types)
        keywords_used |= set(self.missions)
        keywords_used |= set(self.hosts)
        keywords_used |= set(self.host_types)
        keywords_used |= set(self.instruments)
        keywords_used |= set(self.detectors)

        found = {k for k in self._keywords_with_suffixes if '+X' not in k}
        found = {str(k.partition('+')[0]) for k in self._keywords_with_suffixes}
        found -= keywords_used
        found = list(found)
        found.sort()
        self._keywords = found

        return found

    def _get_keywords_by_suffix(self, suffix):
        """Utility to select keywords by suffix from scraping the text."""

        # Default is to return every keyword with a identified suffix
        keywords = self._keywords_with_suffixes
        filtered = {str(k.partition('+')[0]) for k in keywords if suffix in k}
        filtered = list(filtered)
        filtered.sort()
        return filtered

    def _get_keywords_by_category(self, suffix, front_attr='', front_values=[],
                                                tail_attr=''):
        """A list of the keyword values associated with the image. The primary
        keyword is first in the returned list. If the primary key cannot be
        identified, the first item in the list is blank.

        The list is constructed as follows.
        1. If front_attr is defined and self has an attribute by this name, the
           first name on this list starts (and is primary) on the returned list.
        2. If the list is to be returned is still empty and front_values is not
           an empty list, the first item on this list becomes the first item on
           the returned list.
        3. Any remaining items associated with front_attr are appended to the
           list.
        4. Next, a list constructed by scraping keywords with the specified
           suffix (e.g., "+t" for targets) is appended.
        5. Finally, if tail_attr is defined and self has an attribute by this
           name, then it contains a list of names appended to the end of the
           list. A leading minus sign "-" instead indicates that this keyword is
           to be removed from the list if present.

        Use front_attr and front_values to define the primary.

        In the returned list, a defined primary keyword comes first. Any
        remaining keywords are in alphabeticaly order. If a primary keyword
        has not been clearly defined, the list is returned with an empty string
        as the first element.
        """

        results = []
        primary = ''

        # front_attr
        front_attr_keywords = []
        if front_attr and hasattr(self, front_attr):
            front_attr_keywords = self.__dict__[front_attr]
            results = list(front_attr_keywords) # copy

        if front_attr_keywords:
            primary = front_attr_keywords[0]

        # front_values
        if front_values:
            if not primary:
                primary = front_values[0]
                if primary and primary[0] == '?':
                    primary = ''

            results += front_values

        # Scrape the category keywords from the caption and other text
        keywords = self._keywords_with_suffixes
        keywords = {str(k.partition('+')[0]) for k in keywords if suffix in k}
        results += list(keywords)

        # tail_attr
        if tail_attr and hasattr(self, tail_attr):
            for value in self.__dict__[tail_attr]:
                if value and value[0] == '-' and value[1:] in results:
                    results.remove(value[1:])
                else:
                    results.append(value)

        # Try to identify the primary

        # Handle leading keywords that begin with question marks. One of these
        # is the primary only if the same item appears (without "?") later in
        # the list. Otherwise, omit this item and try again.

        if not primary:
            while results and results[0] and results[0][0] == '?':
                if results[0][1:] in results[1:]:
                    primary = results[0][1:]
                    results[0] = primary
                    break
                else:
                    results = results[1:]

        # At this point, remove any more result values that start with a
        # question mark
        results = [r for r in results if r and r[0] != '?']

        # If necessary, keep trying
        if not primary:
            result_set = set(results)

            if len(result_set) == 1:
                primary = results[0]

            # If there are multiple answers, see if there is exactly one in the
            # title
            elif len(result_set) > 1:
                test = self._keywords_with_suffixes_from_title
                test = {k.partition('+')[0] for k in test if suffix in k}
                test = list(test)
                if len(test) == 1:
                    primary = test[0]

                # Failing that, see if there is exactly
                else:
                    test = self._keywords_with_suffixes_from_background
                    test = {k.partition('+')[0] for k in test if suffix in k}
                    test = list(test)
                    if len(test) == 1:
                        primary = test[0]

        # Remove duplicates, sort
        results = list(set(results))
        results.sort()

        # Put the primary in front (empty string if unknown)
        if primary in results:
            results.remove(primary)

        return [primary] + results

    @property
    def missions(self):
        """A list of the names of missions associated with the image. The
        primary mission comes first. If the primary mission is unknown, the list
        begins with ''."""

        # Return saved value if present
        if hasattr(self, '_missions_filled'):
            return self._missions_filled

        if hasattr(self, '_primary_missions'):
            self._primary_missions = [GalleryPage.full_mission_name(m)
                                      for m in self._primary_missions]

        front_values = [HOST_INFO.get(key.lower(), (key,'',''))[1]
                        for key in self.hosts]
        front_values = [v for v in front_values if v]   # skip empty values

        # Save value for future requests
        self._missions_filled = self._get_keywords_by_category('+m',
                                                            '_primary_missions',
                                                            front_values,
                                                            '_missions')
        return self._missions_filled

    @property
    def host_types(self):
        """A list of the types of the hosts associated with the image. The
        type of the primary host comes first. If the primary host is unknown,
        the list begins with ''."""

        # Return saved value if present
        if hasattr(self, '_host_types_filled'):
            return self._host_types_filled

        front_values = [HOST_INFO.get(key.lower(), (key,key,''))[2]
                        for key in self.hosts]
        front_values = [v for v in front_values if v]   # skip empty values

        # Save value for future requests
        self._host_types_filled = self._get_keywords_by_category('+H',
                                                        '_primary_host_types',
                                                        front_values,
                                                        '_host_types')
        return self._host_types_filled

    @property
    def hosts(self):
        """A list of spacecraft or instrument hosts associated with the
        image. The primary host comes first. If the primary host is unknown,
        the list begins with '',"""

        # Return saved value if present
        if hasattr(self, '_hosts_filled'):
            return self._hosts_filled

        if hasattr(self, '_primary_hosts'):
            self._primary_hosts = [GalleryPage.full_host_name(h)
                                   for h in self._primary_hosts]

        # This keeps the host values in the order of the instruments
        front_values = []
        for inst in self.instruments:
            front_value = None

            key = inst.lower()
            if key in HOST_FROM_INSTRUMENT:
                front_value = HOST_FROM_INSTRUMENT[key]
            elif '(' in key:
                abbrev = key.partition('(')[2][:-1]
                abbrev = abbrev.partition(')')[0]
                if abbrev in HOST_FROM_INSTRUMENT:
                    front_value = HOST_FROM_INSTRUMENT[abbrev]

            if isinstance(front_value, str):
                if front_value in front_values:
                    continue
#                 print('WARNING: host "%s" inferred from instrument "%s"' %
#                       (front_value, inst))
                front_values.append(front_value)

            elif isinstance(front_value, (list, tuple)):
                for value in front_value:
                    if value in front_values:
                        continue
                    front_values.append('?' + value)
                        # "?" means use this value at this location in the list
                        # only if it can be confirmed that the host is also
                        # elsewhere in the list.

        # Save value for future requests
        self._hosts_filled = self._get_keywords_by_category('+h',
                                                            '_primary_hosts',
                                                            front_values,
                                                            '_hosts')
        return self._hosts_filled

    @property
    def instruments(self):
        """A list of the instruments associated with the image. The primary
        instrument comes first. If the primary instrument is unknown, the list
        begins with ''."""

        # Return saved value if present
        if hasattr(self, '_instruments_filled'):
            return self._instruments_filled

        if hasattr(self, '_primary_instruments'):
            self._primary_instruments = [GalleryPage.full_instrument_name(i)
                                         for i in self._primary_instruments]

        # This keeps the instrument values in the order of the detectors
        front_values = []
        for det in self.detectors:
            front_value = None

            key = det.lower()
            if key in INSTRUMENT_FROM_DETECTOR:
                front_value = INSTRUMENT_FROM_DETECTOR[key]
            elif '(' in key:
                abbrev = key.partition('(')[2][:-1]
                abbrev = abbrev.partition(')')[0]
                if abbrev in INSTRUMENT_FROM_DETECTOR:
                    front_value = INSTRUMENT_FROM_DETECTOR[abbrev]

            if isinstance(front_value, str):
                if front_value in front_values: continue
                front_values.append(front_value)

            elif isinstance(front_value, (list, tuple)):
                for value in front_value:
                    if value in front_values: continue
                    front_values.append('?' + value)
                        # "?" means use this value at this location in the list
                        # only if it can be confirmed that the host is also
                        # elsewhere in the list.

        # Save value for future requests
        self._instruments_filled = self._get_keywords_by_category('+i',
                                                        '_primary_instruments',
                                                        front_values,
                                                        '_instruments')
        return self._instruments_filled

    @property
    def detectors(self):
        """A list of the detectors associated with the image. The primary
        detector comes first. If the primary detector is unknown or not
        applicable to the instrument, the list begins with ''."""

        # Return saved value if present
        if hasattr(self, '_detectors_filled'):
            return self._detectors_filled

        if hasattr(self, '_primary_detectors'):
            self._primary_detectors = [GalleryPage.full_detector_name(d)
                                       for d in self._primary_detectors]

        # Save value for future requests
        self._detectors_filled = self._get_keywords_by_category('+d',
                                                        '_primary_detectors',
                                                        [],
                                                        '_detectors')
        return self._detectors_filled

    @property
    def targets(self):
        """A list of the target bodies associated with the image. The primary
        target comes first. If the primary target is unknown, the list begins
        with ''."""

        # Return saved value if present
        if hasattr(self, '_targets_filled'):
            return self._targets_filled

        if hasattr(self, '_primary_targets'):
            self._primary_targets = [GalleryPage.full_target_name(t)
                                     for t in self._primary_targets]

        # Save value for future requests
        self._targets_filled = self._get_keywords_by_category('+t',
                                                             '_primary_targets',
                                                             [],
                                                             '_targets')
        return self._targets_filled

    @property
    def target_types(self):
        """A list of the target types, e.g. comet, asteroid, satellite, planet,
        etc. associated with the image. The type of the primary target comes
        first. If unknown, then the list begins with ''."""

        # Return saved value if present
        if hasattr(self, '_target_types_filled'):
            return self._target_types_filled

        front_values = [SYSTEM_FROM_TARGET.get(key.lower(), ('',''))[1]
                        for key in self.targets]
        front_values = [v for v in front_values if v]   # skip empty values

        # Save value for future requests
        self._target_types_filled = self._get_keywords_by_category('+T',
                                                        '_primary_target_types',
                                                        front_values,
                                                        '_target_types')
        # Check for an asteroid or comet ID
        if self._target_types_filled == ['']:
            if self.targets[0]:
                target = self.targets[0]
            elif len(self.targets) > 1:
                target = self.targets[1]
            else:
                target = ''

            if '/' in target:
                self._target_types_filled = ['Comet']

            parts = target.split(' ')
            if len(parts) > 1:
                first = parts[0].strip()
                if first.startswith('('):
                    first = first[1:-1]
                try:
                    k = int(first)
                    self._target_types_filled = ['Asteroid']
                except ValueError:
                    pass

        return self._target_types_filled

    @property
    def systems(self):
        """A list of the names of the planetary systems associated with any
        targets. The primary system comes first. If unknown or not applicable,
        then the list begins with ''. """

        # Return saved value if present
        if hasattr(self, '_systems_filled'):
            return self._systems_filled

        front_values = [SYSTEM_FROM_TARGET.get(key.lower(), ('',''))[0]
                        for key in self.targets]

        # Save value for future requests
        self._systems_filled = self._get_keywords_by_category('+s',
                                                             '_primary_systems',
                                                              front_values,
                                                              '_systems')
        return self._systems_filled

    @property
    def dates(self):
        """A list of dates associated with the caption, in 'yyyy-mm-dd' format.
        The primary date comes first. If the primary date is unknown, the list
        begins with ''."""

        # Return saved value if present
        if hasattr(self, '_dates_filled'):
            return self._dates_filled

        # If the value is a subclass attribute, return it
        if hasattr(self, '_dates'):
            return self._dates

        # Cache the result the first time this is called
        self._dates = find_dates(self._date_search_text)

        # Take a guess that the earliest date is the primary date, so we leave
        # the returned dates in sort order.

        # If the primary date has been defined by the subclass, use it
        if hasattr(self, '_primary_date'):
            primary_date = self._primary_date

            if primary_date is self._dates:
                self._dates.remove(primary_date)

            self._dates = [primary_date] + self._dates

        if len(self._dates) == 0:
            self._dates = ['']

        # Save value for future requests
        self._dates_filled = self._dates
        return self._dates_filled

    ############################################################################
    # Internal properties; overrides by subclasses are generally unnecessary
    ############################################################################

    @property
    def _keyword_search_text(self):
        """Retrieve the text that is to be searched for keywords. If not already
        defined, this defaults to the title, caption and background text.
        Subclasses may wish to override this behavior."""

        # If the search text was not already defined, fill in the default
        if not hasattr(self, '_keyword_search_text_defined'):
            title = self.title.replace('Moon', 'moon')
                    # Avoid being fooled by capitalization of title!
            self._keyword_search_text_defined = (title + '\n\n' +
                                                 self.caption_text + '\n\n' +
                                                 self.background_text)

        return self._keyword_search_text_defined

    @_keyword_search_text.setter
    def _keyword_search_text(self, text):
        """Define the text that is to be searched for keywords."""

        self._keyword_search_text_defined = text

    @property
    def _keywords_with_suffixes(self):
        """A list of keywords associated with the caption, including any
        suffixes that indicate the type of the keyword."""

        # Cache the result the first time this is called
        if not hasattr(self, '_keywords_with_suffixes_found'):
            self._keywords_with_suffixes_found = \
                                find_keywords(self._keyword_search_text, self)

        return self._keywords_with_suffixes_found

    @property
    def _keywords_with_suffixes_from_background(self):
        """A list of keywords associated with the background info, including any
        suffixes that indicate the type of the keyword."""

        # Cache the result the first time this is called
        if not hasattr(self, '_keywords_with_suffixes_from_background_found'):
            self._keywords_with_suffixes_from_background_found = \
                                find_keywords(self.background_text, self)

        return self._keywords_with_suffixes_from_background_found

    @property
    def _keywords_with_suffixes_from_title(self):
        """A list of keywords associated with the title, including any suffixes
        that indicate the type of the keyword."""

        # Cache the result the first time this is called
        if not hasattr(self, '_keywords_with_suffixes_from_title_found'):
            title = self.title.replace('Moon', 'moon')
                # Avoid being fooled by capitalization of title!
            self._keywords_with_suffixes_from_title_found = \
                                find_keywords(title, self)

        return self._keywords_with_suffixes_from_title_found

    @property
    def _date_search_text(self):
        """Retrieve the text that is to be searched for dates. If not already
        defined, this defaults to the caption. Subclasses may wish to override
        this behavior."""

        # If the search text was not already defined, fill in the default
        if not hasattr(self, '_date_search_text_defined'):
            self._date_search_text = self.caption_text

        return self._date_search_text_defined

    @_date_search_text.setter
    def _date_search_text(self, text):
        """Define the text that is to be searched for dates."""

        self._date_search_text_defined = text

    ############################################################################
    # Tools to standardize keyword values
    ############################################################################

    @staticmethod
    def full_detector_name(name):

        key = name.lower()
        if key in DETECTOR_FULL_NAMES:
            return DETECTOR_FULL_NAMES[key]

        if '(' in key:
            abbrev = key.partition('(')[2]
            abbrev = abbrev.partition(')')[0]
            if abbrev in DETECTOR_FULL_NAMES:
                return DETECTOR_FULL_NAMES[abbrev]

        return ''   # no detector specified

    @staticmethod
    def full_instrument_name(name):

        key = name.lower()
        if key in INSTRUMENT_FULL_NAMES:
            return INSTRUMENT_FULL_NAMES[key]

        if '(' in key:
            abbrev = key.partition('(')[2]
            abbrev = abbrev.partition(')')[0]
            if abbrev in INSTRUMENT_FULL_NAMES:
                return INSTRUMENT_FULL_NAMES[abbrev]

        return name

    @staticmethod
    def full_host_name(name):

        key = name.lower()
        if key in HOST_FULL_NAMES:
            return HOST_FULL_NAMES[key]

        key = name.lower()
        if key in HOST_INFO:
            return HOST_INFO[key][0]

        return name

    @staticmethod
    def full_mission_name(name):

        key = name.lower()
        if key in MISSION_FULL_NAMES:
            return MISSION_FULL_NAMES[key]

        return name

    @staticmethod
    def full_target_name(name):

        key = name.lower()
        if key in TARGET_FULL_NAMES:
            return TARGET_FULL_NAMES[key][0]

        parts = name.split()        # remove digits in front and try again
        if len(parts) > 1:
            try:
                test = int(parts[0])
            except ValueError:
                pass
            else:
                key = ' '.join(parts[1:])
                if key in TARGET_FULL_NAMES:
                    return TARGET_FULL_NAMES[key][0]

        return name

    ############################################################################
    # Tools to associated keyword values
    ############################################################################

    @staticmethod
    def _select_by_suffix(keywords, suffix):

        assert suffix[0] == '+' and len(suffix) == 2

        # sometimes a plus is just a plus!
        selected = set()
        for keyword in keywords:
            parts = keyword.split('+')
            if not suffix[1:] in parts:
                continue

            for k in range(len(parts)-1, -1, -1):
                if len(parts[k]) != 1:
                    break

            keyword = ''.join(parts[:k+1])
            selected.add(keyword)

        return selected

    @staticmethod
    def hosts_from_mission(mission):

        hosts = {h[0] for h in HOST_INFO.values() if h[1] == mission}

        mission = GalleryPage.full_mission_name(mission)
        hosts |= {h[0] for h in HOST_INFO.values() if h[1] == mission}

        for category in KEYWORDS:
            keywords = _find_keywords1(category, ' ' + mission + ' ')
            hosts |= GalleryPage._select_by_suffix(keywords, '+h')

        return hosts

    @staticmethod
    def host_from_mission(mission):

        hosts = GalleryPage.hosts_from_mission(mission)
        if len(hosts) == 1:
            return hosts.pop()

        return ''

    @staticmethod
    def missions_from_host(host):

        missions = {h[1] for h in HOST_INFO.values() if h[0] == host}

        host = GalleryPage.full_host_name(host)
        missions |= {h[1] for h in HOST_INFO.values() if h[0] == host}

        for category in KEYWORDS:
            keywords = _find_keywords1(category, ' ' + host + ' ')
            missions |= GalleryPage._select_by_suffix(keywords, '+m')

        return missions

    @staticmethod
    def mission_from_host(host):

        missions = GalleryPage.missions_from_host(host)
        if len(missions) == 1:
           missions.pop()

        return ''

    @staticmethod
    def host_types_from_host(host):

        host_types = {h[2] for h in HOST_INFO.values() if h[0] == host}

        host = GalleryPage.full_host_name(host)
        host_types |= {h[2] for h in HOST_INFO.values() if h[0] == host}

        keywords = set()
        for category in KEYWORDS:
            keywords |= _find_keywords1(category, ' ' + host + ' ')
            host_types |= GalleryPage._select_by_suffix(keywords, '+H')

        return host_types

    @staticmethod
    def host_type_from_host(host):

        host_types = GalleryPage.host_types_from_host(host)
        if len(host_types) == 1:
            return host_types.pop()

        return ''

    @staticmethod
    def hosts_from_instrument(instrument):

        instrument = GalleryPage.full_instrument_name(instrument)
        keywords = _find_keywords1('General', ' ' + instrument + ' ')
        hosts = GalleryPage._select_by_suffix(keywords, '+h')
        if hosts:
            return hosts

        for category in KEYWORDS:
            keywords = _find_keywords1(category, ' ' + instrument + ' ')
            hosts |= GalleryPage._select_by_suffix(keywords, '+h')

        return hosts

    @staticmethod
    def host_from_instrument(instrument):

        hosts = GalleryPage.hosts_from_instrument(instrument)
        if len(hosts) == 1:
            return hosts.pop()

        return ''

    @staticmethod
    def target_types_from_target(target):

        target = GalleryPage.full_target_name(target)
        pairs = {t[1:] for t in TARGET_FULL_NAMES.values() if t[0] == target}

        target_types = {p[0] for p in pairs}
        systems = {p[1] for p in pairs}

        categories = {'General'} | target_types | systems
        for category in categories:
            keywords = _find_keywords1(category, ' ' + target + ' ')
            target_types |= GalleryPage._select_by_suffix(keywords, '+T')

        if target_types:
            return target_types

        for category in KEYWORDS:
            if category not in categories:
                keywords = _find_keywords1(category, ' ' + target + ' ')
                target_types |= GalleryPage._select_by_suffix(keywords, '+T')

        return target_types

    @staticmethod
    def target_type_from_target(target):

        target_types = GalleryPage.target_types_from_target(target)
        if len(target_types) == 1:
            return target_types.pop()

        return ''

    @staticmethod
    def systems_from_target(target):

        target = GalleryPage.full_target_name(target)
        pairs = {t[1:] for t in TARGET_FULL_NAMES.values() if t[0] == target}

        target_types = {p[0] for p in pairs}
        systems = {p[1] for p in pairs if p[1]} # there might not be a system

        categories = {'General'} | target_types | systems
        for category in categories:
            keywords = _find_keywords1(category, ' ' + target + ' ')
            systems |= GalleryPage._select_by_suffix(keywords, '+s')

        if systems:
            return systems

        for category in KEYWORDS:
            if category not in categories:
                keywords = _find_keywords1(category, ' ' + target + ' ')
                systems |= GalleryPage._select_by_suffix(keywords, '+s')

        return systems

    @staticmethod
    def system_from_target(target):

        systems = GalleryPage.systems_from_target(target)
        if len(systems) == 1:
            return systems.pop()

        return ''

    ############################################################################
    # Jekyll output
    ############################################################################

    _HTML_NUMERIC_SYMBOL = re.compile(r'(&#\d+;)')

    def _escape_html(text):
        """Escape the given text for HTML; replace numeric symbols if possible.

        It is assumed that any occurrences of "<" and ">" are HTML tags embedded
        in the text, so these are not escaped.
        """

        text = text.encode('ascii', 'xmlcharrefreplace').decode()
        # text = text.replace('>', '&lt;').replace('<', '&gt;')

        # Replace numeric HTML symbols by their standard values if possible
        parts = GalleryPage._HTML_NUMERIC_SYMBOL.split(text)
        for k, part in enumerate(parts):
            if k%2 == 0:
                continue
            parts[k] = HTML_SYMBOLS.get(part, part)

        return ''.join(parts)

    def _write_jekyll(self, filepath, remote_keys, replacements,
                            neighbors=None):
        """Write Jekyll file.

        remote_keys is a list of keys identifying links to remote versions.

        replacements is a list of tuples (pattern, replacement) which are
        applied to the text prior to writing. Pattern is a regular expression
        and replacement is the associated replacement string."""

        parent = os.path.split(os.path.abspath(filepath))[0]
        if not os.path.exists(parent):
            os.makedirs(parent)

        with open(filepath, 'w') as f:

            # Write Jekyll header
            escaped = GalleryPage._escape_html(self.title)
            escaped_unquoted = escaped.replace('"', '&quot;')

            f.write('---\n')
            f.write('layout: base\n')
            f.write('layout_style: default\n')
            f.write('title: "%s: %s"\n' % (self.id, escaped_unquoted))
            f.write('---\n\n')

            f.write('<style>\n')
            f.write('#noborder {\n')
            f.write('    border: 0;\n')
            f.write('}\n')
            f.write('img {\n')
            f.write('    margin: auto;\n')
            f.write('    width: auto;\n')
            f.write('    height: auto;\n')
            f.write('    max-width: 1200px;\n')
            f.write('    max-height: 800px;\n')
            f.write('}\n')
            f.write('</style>\n\n')

            # Neighbor navigation mainly for debugging
            written = False
            if neighbors and neighbors[0]:
                f.write('[prev](%s)\n' % neighbors[0])
                written = True

            if neighbors and neighbors[1]:
                f.write('[next](%s)\n' % neighbors[1])
                written = True

            if written:
                f.write('\n\n')

            # Include small image with a link to a larger one
            f.write('<table width="840px">\n')
            f.write('<tr id="noborder">\n')
            f.write('<td id="noborder" style="text-align:center;">\n')
            f.write('<a href="%s">\n' % self.local_medium_url)
            f.write('  <img src="%s"\n' % self.local_small_url)
            f.write('       alt="%s: %s" />\n' % (self.id, escaped_unquoted))
            f.write('</a>\n\n')
            f.write('</td>\n')
            f.write('</tr>\n')
            f.write('</table>\n\n')

            f.write('<br clear="left" />\n\n')

            # Write title
            f.write('# %s\n\n' % escaped)

            # Include external links to more versions
            f.write(' * Click the [image above](%s) for a larger view\n' %
                    self.local_medium_url)

            for key in remote_keys:
                if 'movie' in key.lower():
                    icon = '<img src="/icons-local/movie_icon.png" /> '
                else:
                    icon = ''

                try:
                    (url, shape, size) = self.remote_version_info[key]
                except KeyError:
                    continue

                f.write(' * %s[%s](%s) ' % (icon, key, url))
                if shape:
                    f.write('(%d x %d) ' % shape)
                if size:
                    if size >= 1.e6:
                        f.write('(%.1f MB)' % (size/1.e6))
                    else:
                        f.write('(%.1f kB)' % (size/1000.))

                f.write('\n')

            f.write('\n')

            # Write caption
            f.write('<h3>Caption:</h3>\n\n')

            text = GalleryPage._escape_html(self.caption_soup.prettify())
            for (pattern, repl) in replacements:
                text = pattern.sub(repl, text)

            f.write(text)
            f.write('\n\n')

            # Write background info if available
            if self.background_text:

                f.write('<h3>Background Info:</h3>\n\n')

                text = GalleryPage._escape_html(self.background_soup.prettify())
                for (pattern, repl) in replacements:
                    text = pattern.sub(repl, text)

                f.write(text)
                f.write('\n\n')

            # Write a table of keywords
            f.write('<h3>Cataloging Keywords:</h3>\n\n')

            f.write("""<table>
                          <tr>
                            <th>Name</th>
                            <th>Value</th>
                            <th>Additional Values</th>
                          </tr>
                    """)

            names = ['Target',
                     'System',
                     'Target Type',
                     'Mission',
                     'Instrument Host',
                     'Host Type',
                     'Instrument',
                     'Detector',
                     'Extra Keywords',
                     'Acquisition Date',
                     'Release Date',
                     'Date in Caption',
                     'Image Credit',
                     'Source',
                     'Identifier'
            ]

            if self.dates:
                date = self.dates[0]
                other_dates = self.dates[1:]
            else:
                date = ''
                other_dates = []

            keywords = self.keywords

            if self.is_movie:
                keywords.append('Movie')
            if self.is_color:
                keywords.append('Color')
            if self.is_grayscale:
                keywords.append('Grayscale')

            keywords.sort()

            if '//' in self.origin_url:
                display_url = self.origin_url.split('//')[1]
            else:
                display_url = self.origin_url

            values = [[self.targets[0],      ', '.join(self.targets[1:])],
                      [self.systems[0],      ', '.join(self.systems[1:])],
                      [self.target_types[0], ', '.join(self.target_types[1:])],
                      [self.missions[0],     ', '.join(self.missions[1:])],
                      [self.hosts[0],        ', '.join(self.hosts[1:])],
                      [self.host_types[0],   ', '.join(self.host_types[1:])],
                      [self.instruments[0],  ', '.join(self.instruments[1:])],
                      [self.detectors[0],    ', '.join(self.detectors[1:])],
                      ', '.join(keywords),
                      self.acquisition_date,
                      self.release_date,
                      [date,                 ', '.join(other_dates)],
                      self.credit,
                      '<a href="%s" target="_blank">%s</a>' % (self.origin_url,
                                                               display_url),
                      self.id,
            ]

            for (name, value) in zip(names, values):
                if isinstance(value, str):
                    f.write("""<tr>
                                 <td style="text-align:right">%s</td>
                                 <td style="text-align:left" colspan="2">%s</td>
                               </tr>
                            """ % (name, GalleryPage._escape_html(value))
                           )
                else:
                    f.write("""<tr>
                                 <td style="text-align:right">%s</td>
                                 <td style="text-align:left">%s</td>
                                 <td style="text-align:left">%s</td>
                               </tr>
                            """ % (name,
                                   GalleryPage._escape_html(value[0]),
                                   GalleryPage._escape_html(value[1]))
                           )

            f.write('</table>\n')
            f.write('<br>\n')


################################################################################
# Date identification support
################################################################################

# Regular expressions to match just about any reasonable format of date

MONTHNAME = (r'Jan(|\.|uary)|JAN(|\.|UARY)|' +
             r'Feb(|\.|ruary)|FEB(|\.|RUARY)|' +
             r'Mar(|\.|ch)|MAR(|\.|CH)|' +
             r'Apr(|\.|il)|APR(|\.|IL)|' +
             r'May|MAY|'
             r'Jun(|\.|e)|JUN(|\.|E)|' +
             r'Jul(|\.|y)|JUL(|\.|Y)|' +
             r'Aug(|\.|ust)|AUG(|\.|UST)|' +
             r'Sep(|\.|tember)|SEP(|\.|TEMBER)|' +
             r'Oct(|\.|ober)|OCT(|\.|OBER)|' +
             r'Nov(|\.|ember)|NOV(|\.|EMBER)|' +
             r'Dec(|\.|ember)|DEC(|\.|EMBER)')

MONTHNO = r'0[1-9]|[1-9]|1[0-2]'

YEAR = r'19[5-9][0-9]|20[0-4][0-9]'

DATE1 = r'[1-9]'
DATE2 = r'0[1-9]|[12][0-9]|3[01]'

MDY_DATE = ('((' + MONTHNAME + r')(\s+|-)' +
             '(' + DATE2 + '|' + DATE1 + r')(|,\s*|-)' +
             '(' + YEAR + '))')
DMY_DATE = ('((' + DATE2 + '|' + DATE1 + r')\s+' +
             '(' + MONTHNAME + r'),{0,1}\s*' +
             '(' + YEAR + '))')
DASH_DATE = ('((' + YEAR + r')-' +
              '(' + MONTHNAME + '|' + MONTHNO + r')-' +
              '(' + DATE2 + '))')
SLASH_DATE = ('((' + MONTHNO + r')/(' + DATE2 + ')/(' + YEAR + '))')

# A matching string cannot have \w characters immediately before or after
ANY_DATE = re.compile(r'(?<!\w)(' + MDY_DATE + '|' + DMY_DATE + '|' +
                                   DASH_DATE + '|' + SLASH_DATE + r')(?!\w)')

def find_date_substrings(text):
    """Return a list of all the date-like substrings in the given text."""

    matches = ANY_DATE.findall(text)
    return [match[0] for match in matches]

def find_dates(text):
    """Return a list of iso-formatted dates, one for each valid date substring
    in the given text, sorted and with duplicates removed."""

    substrings = find_date_substrings(text)

    days = set()
    for datestring in substrings:
        try:
            day = julian.day_from_string(datestring)
        except Exception:       # arises if the string found is not really a
                                # valid date. Ignore these cases.
            continue

        days.add(day)

    ymd_list = [julian.ymd_format_from_day(d) for d in days]
    ymd_list.sort()

    return ymd_list

################################################################################
# Keyword identification support
################################################################################

def find_keywords(text, page=None):
    """Return the set of all the keywords found in the given text."""

    # Start with the "General" list of keyword patterns
    keywords_found = _find_keywords1('General', text, page)

    # Augment the set of keywords by iteration until done
    keywords_followed = set()
    while (True):

        # Count the unique keywords so far
        nfound = len(keywords_found)

        # Search for more keywords in unchecked subgroups
        found_in_subgroups = set()

        # For each keyword found so far...
        for groupname in keywords_found:

            # If we have already checked it, don't try again
            if groupname in keywords_followed:
                continue
            keywords_followed.add(groupname)

            # If it does not define a subgroup, skip it
            key = groupname.partition('+')[0]
            if key in keywords_followed:
                continue
            if key not in KEYWORDS:
                continue
            keywords_followed.add(key)

            # Augment the list of additional keywords
            found_in_subgroups |= _find_keywords1(groupname, text, page)

        # Merge the two keyword lists
        keywords_found |= found_in_subgroups

        # If the list has not expanded on this iteration, we're done
        if len(keywords_found) == nfound:
            return keywords_found

# Returns the set of keywords found in the text, based on the key to a
# sub-dictionary of the KEYWORDS dictionary
def _find_keywords1(key, text, page=None):
    found = set()

    # Try each regex
    # For this purpose, partition off any suffix starting with "+"
    key = key.partition('+')[0]
    if key not in KEYWORDS:
        return set()

    for (regex, values) in KEYWORDS[key]:
        matches = regex.findall(text)
        if not matches:
            continue

        if page:
            if not hasattr(page, '_rules_applied'):
                page._rules_applied = []

            page._rules_applied.append((regex,values))

        # Add the new keywords without substitution to the set
        nosubs = [v for v in values if '\\' not in v]
        found |= set(nosubs)

        # For each value that requires a substitution...
        for v in values:
            if '\\' not in v:
                continue

            # ...and for each match...
            for match in matches:
                if isinstance(match, str):
                    match = [match]

                for k in range(len(match)):
                    try:
                        v = v.replace('\\' + str(k+1), match[k])
                    except IndexError:
                        break

                # ... perform the substitution and add it to the set
                found.add(v)

    # Return the complete set
    return found

################################################################################
