################################################################################
# storedpage.py
################################################################################
# Class StoredPage
#
# A subclass of GalleryPage that contains the minimal information needed to
# create an imge page or browse page.
################################################################################

from gallerypage import GalleryPage

import pickle

class StoredPage(GalleryPage):
    """StoredPage is a subclass of GalleryPage. It implements the complete
    GalleryPage API by storing the minimal information required. This is used
    to reduce the storage requirements of large catalogs."""

    def __init__(self, page):
        """Constructor for a StoredPage object.

        Input:
            page        A GalleryPage object whose information is to be stored.
                        Alternatively, it can be a dictionary containing all the
                        needed attributes.
        """

        # Make a copy if necessary
        if isinstance(page, dict):
            for (key, value) in page.iteritems():
                self.__dict__[key] = value

            return

        # Otherwise use the standard constructor

        self.source             = page.source
        self.id                 = page.id
        self.html               = ''      # not stored
        self.soup               = ''      # not stored
        self.caption_soup       = page.caption_soup
        self.background_soup    = page.background_soup
        self.title              = page.title
        self.credit             = page.credit
        self.release_date       = page.release_date
        self.acquisition_date   = page.acquisition_date
        self.xrefs              = page.xrefs

        self.is_movie           = page.is_movie
        self.is_color           = page.is_color
        self.is_grayscale       = page.is_grayscale
        self.shape              = page.shape
        self.thumbnail_shape    = page.thumbnail_shape

        self.is_planetary       = page.is_planetary

        self._keywords          = page.keywords
        self._missions          = page.missions
        self._host_types        = page.host_types
        self._hosts             = page.hosts
        self._instruments       = page.instruments
        self._detectors         = page.detectors
        self._targets           = page.targets
        self._target_types      = page.target_types
        self._systems           = page.systems
        self._dates             = page.dates

        self.local_medium_url   = page.local_medium_url
        self.local_small_url    = page.local_small_url
        self.local_thumbnail_url= page.local_thumbnail_url
        self.local_page_url     = page.local_page_url
        self.origin_url         = page.origin_url

        self.remote_version_info = page.remote_version_info

################################################################################
# Catalog support functions
#
# A catalog is a dictionary of StoredPage objects keyed by the product ID.
# It is saved in a pickle file.
################################################################################

def save_catalog(catalog, filepath):
    """Save a catalog. Convert pages to StoredPage objects if necessary."""

    # Convert to dictionaries
    dicts = {}
    for (key, page) in catalog.iteritems():
        if not isinstance(page, StoredPage):
            page = StoredPage(page)

        dicts[key] = page.__dict__

    # Save pickle file
    with open(filepath, 'w') as f:
        pickle.dump(dicts, f)

def load_catalog(filepath):
    """Load a dictionary of StoredPage objects from a pickle file.
    """

    with open(filepath) as f:
        dicts = pickle.load(f)

    catalog = {}
    for (key, value) in dicts.iteritems():
        catalog[key] = StoredPage(value)

    return catalog

################################################################################
