#!/usr/bin/env python
################################################################################
# Class PiaPage
#
# A class and methods to handle the reading and interpretation of web pages at
# the Planetary Photojournal, https://photojournal.jpl.nasa.gov.
#
# Andrew Lin & Mark Showalter
################################################################################

### It's usually a good idea to have a header at the top of any file.
### The first line is needed if we want to run unit tests from the command line.

from bs4 import BeautifulSoup
import requests
import os
import json

### Adding blank lines between methods, classes and other large sections of code
### is recommended. Headers are useful to separate large chunks of code; see an
### example below.

class PiaPage(object):  ### always derive classes from object

### Best to define constants like this at the top. If the URL every changes
### you only need to change one line and you don't need to go looking for it.

    PIA_URL = "https://photojournal.jpl.nasa.gov/catalog/"
    MISSING_PAGE_TEXT = 'No images in our database met your search criteria'
    PIAROOT_ENVNAME = 'PIAPATH'

### Note I added a way to pass the root directory of the HTML source tree into
### the constructor. You don't need it if you are getting the HTML over the web
### but will need it for finding a local copy.

    def __init__(self, src, piaroot=None, overwrite=False):
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

            piaroot     The root directory of the PIA file tree. The file path
                        is piaroot/PIAnnxxx/PIAnnnnn.txt. Here 'nnnnn' is
                        replaced by the pia number, whereas the directory name
                        uses the first two digits of the pia number followed by
                        literal 'xxx'. This prevents directories from growing
                        to more than 1000 files.

            overwrite   True to overwrite a local copy of the HTML source with
                        one pulled from the website; False to leave any local
                        copy unchanged
        """

### It's a PEP recommendation and also just good practice to wrap lines at 80
### characters or less. Sometimes there are exceptions.

        self.source = src
        self.piaroot = PiaPage.get_piaroot(piaroot)
        self.HTML = PiaPage.get_HTMLfromPIACode(src, self.piaroot, overwrite)   ### Changed to a static function
        self.SOUP = BeautifulSoup(self.HTML, 'html.parser')     ### Changed to a direct call

### General comment. If something _can_ be a static function, then it should be
### a static function. Static functions are easier to test because they can
### stand by themselves--you don't need to create an object in order to test the
### function.

        self.TITLE = self.get_Title()
        self.CREDIT = self.get_Credit()
        self.CAPTION = self.get_Caption()
        self.information = self.get_Information()

    @staticmethod
    def get_piaroot(piaroot=None):
        """Return the root directory for PIA text files. Search via an
        environment variable if it is None."""

        if piaroot is None:
            try:
                piaroot = os.environ[PiaPage.PIAROOT_ENVNAME]
            except KeyError:
                ## Failing that, we will use the current working directory
                piaroot = ''

        return piaroot

### get_HTMLfromPIACode will be easier to test if it is a staticmethod. The only
### inputs are source and optional piaroot, and it always returns HTML or raises
### an error.

    @staticmethod
    def get_HTMLfromPIACode(source, piaroot, overwrite=False):
        """Obtain the html from a PIA number or string"""

### Here I swapped your code around so it is easier to see the logic.

        # Convert the PIA code from a string if necessary
        if type(source) == int:
            source = PiaPage.get_piacode(source)

        # If this is not a URL, read a local file if possible
        if not PiaPage.isUrl(source) and not overwrite:
            try:
                filepath = PiaPage.filepath_from_source(source, piaroot)
                if os.path.exists(filepath):
                    with open(filepath, 'r') as file:
                        html = file.read()
                    return str(html)

            # If local file not found
            except IOError:
                pass

        # Otherwise, get the online version
        if PiaPage.isUrl(source):
            url = source
        else:
            url = PiaPage.url_from_source(source)

        req = requests.get(url)

        # Make sure we got back a good request
        if req.status_code != 200 or PiaPage.MISSING_PAGE_TEXT in req.text:
            raise IOError('URL not found: "%"' % url)

        # Save the file so we don't need to retrieve it next time
        filepath = PiaPage.filepath_from_source(source, piaroot)
        if overwrite or not os.path.exists(filepath):
            with open(filepath, 'w') as file:
                file.write(req.text)

        return req.text

### Now here we add the smaller functions used by get_HTMLfromPIACode

    @staticmethod
    def isUrl(source):
        """Check if the source is a URL"""

### Using "in" is fine in this line, but str.startswith() is better:
###        if "https://photojournal.jpl.nasa.gov/" in source and len(source) <= 50:
###            return True
### Note also that there is no "else: return False"
### This is simple and short and doesn't make any unnecessary assumptions:

        return source.startswith('http://') or source.startswith('https://')

### You can see that we no longer need this function
#     @staticmethod
#     def isFile(source):
#         """Check if the source is a file or not"""
#         if not os.path.exists("htmls/" + source[5:]):
#             return True
#         else:
#             return False


### This function is so short that I copied it into get_HTMLfromPIACode. Also
### not that I added the check to make sure it found a PIA page.
#     @staticmethod
#     def get_HTMLfromURL(source):
#         """Gets the response from the request to the source"""
#         req = requests.get(source)
#         return req.text

    @staticmethod
    def get_piacode(source):
        """Return a string 'PIA' + five digits from a source, which could be an
        integer, a PIA string, a filepath or a full URL."""

        if type(source) == int:
            source = 'PIA%05d' % source

        source = source.upper()
        k = source.upper().rindex('PIA')   # find the rightmost 'PIA'
        piacode = source[k:k+8]

        return piacode

### I modified this function because it does a lot more now.
### Note the use of an environment variable to indicate where to find the PIA
### directory tree if it is not provided in the function input.

    @staticmethod
    def filepath_from_source(source, piaroot=None):
        """Return the local file path based on the source."""

        piacode = PiaPage.get_piacode(source)
        filepath = '%sxxx/%s.txt' % (piacode[:5], piacode)

        piaroot = PiaPage.get_piaroot(piaroot)
        return os.path.join(piaroot, filepath)

    @staticmethod
    def url_from_source(source):
        """Return the URL based on the source."""

        piacode = PiaPage.get_piacode(source)
        return PiaPage.PIA_URL + piacode

    ############################################################################
    # Methods to extract info from the soup
    ############################################################################

    def get_Title(self):
        """Return the title of the page example: Artemis Corona"""
        return self.SOUP.find_all('b')[0].text

    def get_Credit(self):
        """Return the Image Credit. Example: NASA/JPL"""
        return self.SOUP.find_all('dd')[1].text

    def get_Caption(self):
        """Returns the caption of the page"""
        return self.SOUP.find_all('p')[2].text

    def get_Information(self):
        """Gets all the information inside the table. Takes the left side of the table first and loops through that side
        then takes the right side and maps both sides into a {left  : right} kind of structure."""

        # the table found from the soup

        table_found = self.SOUP.find_all('table')[0]

        # all of the sides, tr_dict is what is being returned.

        leftside = []
        rightside = []
        tr_dict = {}

        # for some reason, the page says left as right and right as left so it becomes confusing

        # loop through the left side and add that to the leftside list. the left side can be found using the align attr
        # the other way around for the right side but similar concept.
        for left in table_found.find('tr').find_all('td', align="right"):
            leftside.append(' '.join(left.text.replace(":", "").split()))
#             print(' '.join(left.text.replace(":", "").split()))
        for right in table_found.find('tr').find_all('td', align="left"):
            rightside.append(' '.join(right.text.split()))

        # i is used to find the element by index when adding the left side to the right side.
        i = 0
        for left_text in leftside:
            tr_dict.update(json.loads("{\"" + left_text + "\" : \"" + rightside[i] + "\"}"))
        return tr_dict

################################################################################
# Unit tests
################################################################################

import unittest

class Test_PiaPage(unittest.TestCase):

    def runTest(self):

        # Tests of get_piacode
        self.assertEqual(PiaPage.get_piacode(1), 'PIA00001')
        self.assertEqual(PiaPage.get_piacode(12345), 'PIA12345')
        self.assertEqual(PiaPage.get_piacode('PIA12345'), 'PIA12345')
        self.assertEqual(PiaPage.get_piacode('PIA12xxx/PIA12345.txt'),
                                             'PIA12345')
        self.assertEqual(PiaPage.get_piacode(PiaPage.PIA_URL +
                                             'PIA12345'), 'PIA12345')

        # Tests of filepath_from_source (regardless of piaroot)
        self.assertTrue(PiaPage.filepath_from_source(1).endswith(
                                'PIA00xxx/PIA00001.txt'))
        self.assertTrue(PiaPage.filepath_from_source(12345).endswith(
                                'PIA12xxx/PIA12345.txt'))
        self.assertTrue(PiaPage.filepath_from_source('PIA12345').endswith(
                                'PIA12xxx/PIA12345.txt'))
        self.assertTrue(PiaPage.filepath_from_source('PIA12xxx/PIA12345.whatever').endswith(
                                'PIA12xxx/PIA12345.txt'))
        self.assertTrue(PiaPage.filepath_from_source(PiaPage.PIA_URL +
                                'PIA12345').endswith(
                                'PIA12xxx/PIA12345.txt'))

        # Tests of filepath_from_source (with specified piaroot)
        self.assertEqual(PiaPage.filepath_from_source(1, '/root'),
                                '/root/PIA00xxx/PIA00001.txt')
        self.assertEqual(PiaPage.filepath_from_source(12345, '/root'),
                                '/root/PIA12xxx/PIA12345.txt')
        self.assertEqual(PiaPage.filepath_from_source('PIA12345', '/root'),
                                '/root/PIA12xxx/PIA12345.txt')
        self.assertEqual(PiaPage.filepath_from_source(
                                'PIA12xxx/PIA12345.whatever', '/root'),
                                '/root/PIA12xxx/PIA12345.txt')
        self.assertEqual(PiaPage.filepath_from_source(PiaPage.PIA_URL +
                                             'PIA12345', '/root'),
                                '/root/PIA12xxx/PIA12345.txt')

        self.assertEqual(PiaPage.filepath_from_source(1, ''),
                                'PIA00xxx/PIA00001.txt')
        self.assertEqual(PiaPage.filepath_from_source(12345, ''),
                                'PIA12xxx/PIA12345.txt')
        self.assertEqual(PiaPage.filepath_from_source('PIA12345', ''),
                                'PIA12xxx/PIA12345.txt')
        self.assertEqual(PiaPage.filepath_from_source(
                                'PIA12xxx/PIA12345.whatever', ''),
                                'PIA12xxx/PIA12345.txt')
        self.assertEqual(PiaPage.filepath_from_source(PiaPage.PIA_URL +
                                             'PIA12345', ''),
                                'PIA12xxx/PIA12345.txt')

        # Tests of url_from_source
        self.assertEqual(PiaPage.url_from_source(1),
                                        PiaPage.PIA_URL + 'PIA00001')
        self.assertEqual(PiaPage.url_from_source(12345),
                                        PiaPage.PIA_URL + 'PIA12345')
        self.assertEqual(PiaPage.url_from_source('PIA12345'),
                                        PiaPage.PIA_URL + 'PIA12345')
        self.assertEqual(PiaPage.url_from_source('PIA12345'),
                                        PiaPage.PIA_URL + 'PIA12345')
        self.assertEqual(PiaPage.url_from_source(PiaPage.PIA_URL + 'PIA12345'),
                                        PiaPage.PIA_URL + 'PIA12345')

        self.assertRaises(ValueError, PiaPage.url_from_source,
                                      'https://pds-rings.seti.org')

        # Some of these will only work if PIAPATH is defined in the environment
        self.assertIn('PIAPATH', os.environ)

        html_from_file = PiaPage(1).HTML
        html_from_url = PiaPage(PiaPage.url_from_source(1), overwrite=True).HTML

        self.assertEqual(html_from_file, html_from_url)

################################################################################

# Run unit tests if you invoke the program from the command line

if __name__ == '__main__':
    unittest.main(verbosity=2)

################################################################################
