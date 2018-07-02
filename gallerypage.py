################################################################################
# Class GalleryPage
#
# An abstract class and methods to handle the reading and interpretation of web
# pages containing press release materials and their captions.
#
# Andrew Lin & Mark Showalter
################################################################################

import re
import julian

from planet_from_target import PLANET_FROM_TARGET

class GalleryPage(object):

    PLANET_NAMES = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter',
                    'Saturn', 'Uranus', 'Neptune', 'Pluto']

    # Null constructor
    def __init__(self):

        # Attributes or properties required for all subclasses

        self.html = ''      # The source page as HTML
        self.soup = None    # The source page as BeautifulSoup

        self.id = ''        # Unique identifier for this product, e.g., PIA12345
        self.origin_url     # The remote URL of the source of this press release

        self.title = ''     # Title of page with optional HTML formatting
        self.credit = ''    # Credit info with optional HTML formatting
        self.release_date = ''
                            # Release date in yyyy-mm-dd format if available
        self.xrefs = []     # A list of IDs of products referenced by this one
        self.caption_soup = None
                            # The caption represented as BeautifulSoup
        self.background_soup = None
                            # The background information represented as
                            # BeautifulSoup. Background information refers to
                            # descriptions of the mission, instrument, etc. that
                            # is not unique to this page.

        self.local_viewables
                            # The local path to the image files. These can be
                            # stored in multiple sizes and the optimal one will
                            # be seleced for resizing when it's time to display.


    ############################################################################
    # Properties for which overrides by subclasses are optional. Default
    # behavior is to search a text string (typically the caption) and report all
    # occurrences of matching text.
    ############################################################################

    @staticmethod
    def soup_as_text(soup):
        if hasattr(soup, 'contents'):
            return ''.join([GalleryPage.soup_as_text(s) for s in soup.contents])

        if hasattr(soup, 'text'):
            text = soup.text
        elif hasattr(soup, 'string'):
            text = soup.string
        else:
            text = ''

        text = text.strip()
        text = text.replace('\r', ' ').replace('\n', ' ').replace('  ', ' ')
        return text

    @property
    def caption_text(self):
        """The caption as a single string, stripped of HTML."""

        if not hasattr(self, '_caption_text'):
            paragraphs_in_soup = list(self.caption_soup.children)
            paragraphs = [GalleryPage.soup_as_text(s)
                          for s in paragraphs_in_soup]
            paragraphs = [p for p in paragraphs if p]
            self._caption_text = '\r\r'.join(paragraphs)

        return self._caption_text

    @property
    def background_text(self):
        """The background as a single string, stripped of HTML."""

        if not hasattr(self, '_background_text'):
            paragraphs_in_soup = list(self.background_soup.children)
            paragraphs = [GalleryPage.soup_as_text(s)
                          for s in paragraphs_in_soup]
            paragraphs = [p for p in paragraphs if p]
            self._background_text = '\r\r'.join(paragraphs)

        return self._background_text

    @property
    def keywords(self):
        """A list of keywords associated with the caption."""

        # If the value is a subclass attribute, return it
        if hasattr(self, '_keywords'):
            return self._keywords

        found = {str(k.partition('+')[0]) for k in self._keywords_with_suffixes}
        found = list(found)
        found.sort()
        return found

    def _get_keywords_by_suffix(self, suffix, attr):
        """Utility to select keywords by suffix."""

        # If the value is a subclass attribute, return it
        if hasattr(self, attr):
            return self.__dict__[attr]

        # Default is to return every keyword with a identified suffix
        keywords = self._keywords_with_suffixes
        filtered = {str(k.partition('+')[0]) for k in keywords if suffix in k}
        filtered = list(filtered)
        filtered.sort()
        return filtered

    def _get_primary_keyword_by_suffix(self, suffix, attr, keywords):
        """The name of the primary keyword value associated with the image."""

        # If the value is a subclass attribute, return it
        if hasattr(self, attr):
            return self.__dict__[attr]

        # If there is only one host keyword, return it
        if len(keywords) == 1:
            return keywords[0]

        # If there are multiple answers, see if there is exactly one in the
        # title
        if len(keywords) > 1:
            keywords = self._keywords_with_suffixes_from_title
            filtered = {k.partition('+')[0] for k in keywords if suffix in k}
            filtered = list(filtered)
            if len(filtered) == 1:
                return filtered[0]

        # Failing that, see if there is exactly one in the background text
        if len(keywords) > 1:
            keywords = self._keywords_with_suffixes_from_background
            filtered = {k.partition('+')[0] for k in keywords if suffix in k}
            filtered = list(filtered)
            if len(filtered) == 1:
                return filtered[0]

        # Otherwise give up
        return ''

    @property
    def missions(self):
        """A list of the names of missions associated with the image."""

        return self._get_keywords_by_suffix('+m', '_missions')

    @property
    def mission(self):
        """A list of the names of missions associated with the image."""

        return self._get_primary_keyword_by_suffix('+m', '_mission',
                                                   self.missions)

    @property
    def hosts(self):
        """A list of spacecraft or instrument hosts associated with the
        image."""

        return self._get_keywords_by_suffix('+h', '_hosts')

    @property
    def host(self):
        """The name of the primary spacecraft or instrument hosts associated
        with the image."""

        return self._get_primary_keyword_by_suffix('+h', '_host',
                                                   self.hosts)


    @property
    def instruments(self):
        """A list of the instruments associated with the image."""

        return self._get_keywords_by_suffix('+i', '_instruments')

    @property
    def instrument(self):
        """The name of the primary instrument associated with the image."""

        return self._get_primary_keyword_by_suffix('+i', '_instrument',
                                                   self.instruments)

    @property
    def targets(self):
        """A list of the target bodies associated with the image."""

        return self._get_keywords_by_suffix('+t', '_targets')

    @property
    def target(self):
        """The name of the primary target body associated with the image."""

        return self._get_primary_keyword_by_suffix('+t', '_target',
                                                   self.targets)

    @property
    def target_types(self):
        """A list of the target types, e.g. comet, asteroid, satellite, planet,
        etc. associated with the image."""

        return self._get_keywords_by_suffix('+T', '_target_types')

    @property
    def target_type(self):
        """The type of the primary target body associated with the image."""

        if hasattr(self, '_target_type'):
            return self._target_type

        # Return the target type for this target
        target = self.target
        if not target: return ''

        if target == 'Sun':
            return 'Sun'

        if target in GalleryPage.PLANET_NAMES:
            return 'Planet'

        target_lc = target.lower()
        if target in PLANET_FROM_TARGET:
            return PLANET_FROM_TARGET[target_lc][1]

        # Try some string matches
        if ' ring' in target_lc:
            return 'Ring'

        if ' gap' in target_lc or ' division' in target_lc:
            return 'Gap'

        if ' arc' in target_lc:
            return 'Arc'

        # If there is only one target type, return it
        if len(self.target_types) == 1:
            return self.target_types[0]

    @property
    def planets(self):
        """A list of the names of the central planets associated with any
        targets."""

        return self._get_keywords_by_suffix('+p', '_planets')

    @property
    def planet(self):
        """The primary central planet associated with the image."""

        if hasattr(self, '_planet'):
            return self._planet

        # Return the planet for this target, if any
        target_lc = self.target.lower()
        if target_lc in PLANET_FROM_TARGET:
            return PLANET_FROM_TARGET[target_lc][0]

        # If there is only one planet, return it
        if len(self.planets) == 1:
            return self.planets[0]

        return ''

    @property
    def dates(self):
        """A list of dates associated with the caption, in 'yyyy-mm-dd' format.
        """

        # If the value is a subclass attribute, return it
        if hasattr(self, '_dates'):
            return self._dates

        # Cache the result the first time this is called
        if not hasattr(self, '_dates'):
            self._dates = find_dates(self._date_search_text)

        return self._dates

    @property
    def acquisition_date(self):
        """The date the image was acquired, in 'yyyy-mm-dd' format; an empty
        string if unknown."""

        # If the value is a subclass attribute, return it
        if hasattr(self, '_acquisition_date'):
            return self._acquisition_date

        # It is just a guess that the acquisition date is the earliest date that
        # appears in the caption
        if self.dates:
            return self.dates[0]
        else:
            return ''

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
            self._keyword_search_text_defined = (self.title + '\r\r' +
                                                 self.caption_text + '\r\r' +
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
                                        find_keywords(self._keyword_search_text)

        return self._keywords_with_suffixes_found

    @property
    def _keywords_with_suffixes_from_background(self):
        """A list of keywords associated with the background info, including any
        suffixes that indicate the type of the keyword."""

        # Cache the result the first time this is called
        if not hasattr(self, '_keywords_with_suffixes_from_background_found'):
            self._keywords_with_suffixes_from_background_found = \
                                        find_keywords(self.background_text)

        return self._keywords_with_suffixes_from_background_found

    @property
    def _keywords_with_suffixes_from_title(self):
        """A list of keywords associated with the title, including any suffixes
        that indicate the type of the keyword."""

        # Cache the result the first time this is called
        if not hasattr(self, '_keywords_with_suffixes_from_title_found'):
            self._keywords_with_suffixes_from_title_found = \
                                        find_keywords(self.title)

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
ANY_DATE = re.compile('(?<!\w)(' + MDY_DATE + '|' + DMY_DATE + '|' +
                               DASH_DATE + '|' + SLASH_DATE + ')(?!\w)')

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
# Load keywords and compile regular expressions

from keywords import KEYWORDS

compiled = {}
for (category, pairs) in KEYWORDS.iteritems():
    new_pairs = []

    for (regex, values) in pairs:
        new_pairs.append((re.compile(regex), values))

    compiled[category] = new_pairs

KEYWORDS = compiled

########################################

def find_keywords(text):
    """Return an alphabetical list of all the keywords found in the given
    text."""

    # Returns all the keywords found in the text, based on the key to a
    # sub-dictionary of the KEYWORDS dictionary
    def find_keywords1(key):
        found = set()

        # Try each regex
        # For this purpose, partition off any suffix starting with "+"
        for (regex, values) in KEYWORDS[key.partition('+')[0]]:
            matches = regex.findall(text)
            if not matches: continue

            # Add the new keywords without substitution to the set
            nosubs = [v for v in values if '$' not in v]
            found |= set(nosubs)

            # For each value that requires a substitution...
            for v in values:
                if '$' not in v: continue

                # ...and for each match...
                for match in matches:

                    # ... perform the substitution and add it to the set
                    found.add(v.replace('$', str(match)))

        # Return the complete set
        return found

    # Start with the "General" list of keyword patterns
    keywords_found = find_keywords1('General')

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
            if groupname in keywords_followed: continue
            keywords_followed.add(groupname)

            # If it does not define a subgroup, skip it
            if groupname not in KEYWORDS: continue

            # Augment the list of additional keywords
            found_in_subgroups |= find_keywords1(groupname)

        # Merge the two keyword lists
        keywords_found |= found_in_subgroups

        # If the list has not expanded on this iteration, we're done
        if len(keywords_found) == nfound:
            return keywords_found

################################################################################
# Jekyll output
################################################################################

#     def write_jekyll_header(file, title)
#         """Write the header of the Jekyll file. The file is assumed to already
#         be open for write."""
# 
#         file.write('---\r')
#         file.write('layout: base\r')
#         file.write('layout_style: default\r')
#         file.write('title: "%s"\r' % self.title)
#         file.write('---\r\r')
#         file.write('# %s\r\r' % self.title)
# 
#     def write_jekyll_caption(file, caption)
#         """Write the caption into the Jekyll file. The file is assumed to be
#         open for write already."""
# 
#         file.write('**Caption:**\r\r')
#         file.write(self.caption_soup.prettify())
# 
#     def write_jekyll_background(file, background)
#         """Write the background information of the Jekyll file. The file is
#         assumed to be open for write already."""
# 
#         if se
#         file.write('**Background Info:**\r\r')
#         file.write(self.caption_soup.prettify())



################################################################################
