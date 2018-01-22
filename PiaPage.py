#make sure to have object if python 2.7
from bs4 import BeautifulSoup
import requests
import os
import json
class PiaPage:
    def __init__(self, src):
        """ The constructor of this class. Requires a source. Contains attributes source, html, soup, title, credit,
        and caption.
        """
        # information type (url or file)

        self.source = src
        self.HTML = self.get_HTMLfromPIACode()
        self.SOUP = self.get_Soup()
        self.TITLE = self.get_Title()
        self.CREDIT = self.get_Credit()
        self.CAPTION = self.get_Caption()
        self.information = self.get_Information()


    @staticmethod
    def isUrl(source):
        """Check if the source is a URL"""
        if "https://photojournal.jpl.nasa.gov/" in source and len(source) <= 50:
            return True
    @staticmethod
    def isFile(source):
        """Check if the source is a file or not"""
        if not os.path.exists("htmls/" + source[5:]):
            return True
        else:
            return False
    @staticmethod
    def get_HTMLfromURL(source):
        """Gets the response from the request to the source"""
        req = requests.get(source)
        return req.text

    def get_Soup(self):
        """Returns the soup from HTML"""
        return BeautifulSoup(self.HTML, 'html.parser')

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
            print(' '.join(left.text.replace(":", "").split()))
        for right in table_found.find('tr').find_all('td', align="left"):
            rightside.append(' '.join(right.text.split()))

        # i is used to find the element by index when adding the left side to the right side.
        i = 0
        for left_text in leftside:
            tr_dict.update(json.loads("{\"" + left_text + "\" : \"" + rightside[i] + "\"}"))
        return tr_dict


    def get_HTMLfromPIACode(self):
        """Obtain the html from a PIA"""
        the_source = self.source
        try:
            # turns sources with types like ints to a useable string.

            src = self.convert_other_type(the_source)
        except ValueError:

            # if failed to convert, then return a not working.

            return "Not working type"
        if self.check_is_pia(the_source):
            if self.isUrl(the_source):

                # return the html from a url

                return self.get_HTMLfromURL(self.source)
            elif self.isFile(the_source):

                # return html from a file

                return self.get_HTMLfromFile(self.filepath_from_source(src))



    @staticmethod
    def filepath_from_source(source):

        # finds the path to the source.

        return "htmls/" + source

    @staticmethod
    def get_HTMLfromFile(filepath):

        # read and return the contents of a file.

        with open(filepath, 'r') as file:
            html = file.read()
        return str(html)


    def check_is_pia(self, source):
        """Checking if a PIA is valid or not. (If the source is less than 5 digits then it is not)"""

        if self.isFile(self.source):
            pia = source.replace(".txt", "")
            if len(pia[3:]) < 5:
                return "PIA code does not contain 5 digits"
            else:
                return True
        elif self.isUrl(self.source):
            if len(source.replace("https://photojournal.jpl.nasa.gov/catalog/PIA", "")) < 5:
                return "PIA code does not contain 5 digits"
            else:
                return True

    @staticmethod
    def get_source_type(source):
        # find the type of the source
        return type(source)

    @staticmethod
    def isOtherType(source):

        # check if the source is another type

        if type(source) is str:
            return False
        else:
            return True

    def convert_other_type(self, source):
        """If the source is another type, this function will attempt to convert the source into a useable type where
        the other functions are able to use."""

        if self.isOtherType(source):
            if self.get_source_type(source) == int:
                return "PIA" + str(source)
            elif self.get_source_type(source) == str:
                return source
            else:
                try:
                    return str(source)
                except TypeError:
                    return "bad type"




