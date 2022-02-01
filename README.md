# pds-galleries

## Quick notes from Mark 1/30/2022

* This is the version used to create the current galleries.

* Everything is still in Python 2, although a conversion to 3 would probably be straightforward.

* The highest-numbered press release checked is PIA25121.

* The code could stand a good bit of cleanup but this currently meets our needs.

## GalleryPage

- The superclass of all gallery pages is __GalleryPage__, defined in ``gallerypage.py``. 
    - This class defines a number of properties and methods that ought to be useful
      across multiple families of gallery pages.
    - These properties include ``is_planetary``, ``targets``, ``target_types``,
      ``missions``, ``hosts``, ``keywords``, ``caption_html``, etc.
    - There should be a single __GalleryPage__ object associated with each HTML page
      online in the ``press_releases/pages`` subdirectory.
- Subclass __PiaPage__ handles Photojournal gallery pages at ``https://photojournal.jpl.nasa.gov/``.
    - This class is defined in ``piapage/__init__.py``. Use "``import piapage``".
    - Various other files in the ``piapage`` directory support this class.
- Subclass __HubblePage__ handles planetary web pages at ``https://hubblesite.org/``.
    - This work was not completed.
- The idea is that each subclass of GalleryPage handles the nuts and bolts of
   getting press release product info from a particular source, and then reorganizes
   that info a standardized format.
    - Presumably, we would want an additional subclass for APOD (``https://apod.nasa.gov/apod/astropix.html``).
    - Also, note that the Photojournal has almsot nothing from the New Horizons Arrokoth flyby.
      That's all at ``http://pluto.jhuapl.edu/``.

- The __GalleryPage__ superclass includes methods to support the scraping of information out of
  online captions and organizing that info as needed.
    - The ``dicts`` subdirectory contains carefully curated dictionaries that define some of
      the info that is extracted from the captions and extracted values are normalized.

## Galleries

- A "gallery" is the name for a index page that points to a bunch of online GalleryPages.
- The file ``galleries.py`` defines two useful functions for creating these galleries.
    - ``by_release_date`` takes a dictionary of GalleryPage objects, a bunch of additional information,
      and creates index pages that organize the selected pages by date.
    - ``by_target``takes a dictionary of GalleryPage objects, a bunch of additional information,
      and creates index pages that organize the selected pages by target name or target type.

## PiaPage

- The __PiaPage__ constructor takes the ID of a Photojournal page as a string (e.g., "``PIA12345``")
  or as an integer (e.g., ``12345``) and creates a __PiaPage__ for that product.
- It maintains a local cache of pages from the Photojournal, so that a request for a given product
  is only retrieved from the website if there isn't a local copy.
- The local cache is maintained in our shared dropbox inside ``PDS-Galleries/PIAxxxxx``.
    - All local copies are organized by the first two digits, then all five, so the retrieved HTML for
      product ``PIA12345`` is in ``PDS-Galleries/PIAxxxxx/PIA12xxx/PIA12345.html``.
    - I have found numerous HTML errors in the Photojournal pages, so some of these pages have
      been edited locally compared to what you would get by going back to the Photojournal and
      retrieving them anew. It follows that you should not overwrite the locally cached copies blindly.
    - Your local environment variable ``PIAPATH`` defines the root location of the cache, meaning
      the directory that contains a subdirectory called ``PIAxxxx``.
- The file ``piapage/repairs.py`` contains a bunch of specialized instructions for how to fix
  the metadata extracted from individual product pages. Things are automated to the extent possible,
  but there is so much variation among Photojournal pages that, in the end, I had to build a big
  dictionary listing keywords to add, keywords to remove, values to replace, etc.
    - This source code is NOT pretty.
    - You will find customized metadata repairs for about 10% of all the pages retrieved.
- We try to separate each caption into two parts--the part with useful information relevant to the
  product vs. the annoying extra information about who manages what and who build what. That latter
  information gets repeated way too often and is rarely useful to
  the reader. This latter information is tagged as "backgound text" and is separated from
  the caption when displayed online.
    - The file ``piapage/BACKGROUND_STRING.py`` contains strings that are used to distinguish
      background text from caption text. It needs to be actively maintained.
    - Here is an example of background text:

The Cassini-Huygens mission is a cooperative project of NASA, the European Space Agency and
the Italian Space Agency. The Jet Propulsion Laboratory, a division of the California Institute
of Technology in Pasadena, manages the mission....

- We try to indicate whether each product is color or black and white using attributes
  ``is_color`` and ``is_grayscale``. This information is hard to obtain from the Photojournal,
  but a separate procedure works reasonably well.
    - Program ``piapage/make_COLOR_VS_PIAPAGE.py`` is a stand-alone program that scrapes the
      Photojournal site for information about which images are color and which are grayscale.
    - It writes the file ``piapage/COLOR_VS_PIAPAGE.py``, containing its results.
    - The __PiaPage__ constructor checks this cache of information to assign the values of
      ``is_color`` and ``is_grayscale`` to each object.
    - At reasonable intervals, as new products are added to the Photojournal, one should re-run
      ``make_COLOR_VS_PIAPAGE.py`` to keep this index up to date.
- We download the thumbnail, small, and medium display products from the Photojournal site and
  host them locally.
    - This happens automatically when you create a __PiaPage__ object and it determines that
      the local files are not available.
    - Image files are saved directly into the ``/Library/WebServer/Documents/press_releases``
      directory tree, although you can modify this behavior by editing the value of class
      constant ``DOCUMENTS_FILE_ROOT_`` inside ``gallerypage.py``.
- On rare occasions, the thumbnail, small, and medium display products are GIFs instead of
  JPGs. There's no easy way to know this, so the slightly clunky current approach is to
  maintain the list of GIF products manually, in ``piapage/GIF_PIAPAGES.py``.
    - You can run the program ``check_for_missing_or_unneeded_previews.py`` manually before
      a deploy to identify any missing image files.
    - ``random-scripts/getgif.sh`` might be useful for downloading missing images.
- You can ignore anything in the ``piapage/training`` subdirectory. We're not using it now.

### Gallery Deployment Procedure

1. Make sure your ``PIAPATH`` environment variable points to a local copy of the shared Dropbox
   directory ``PDS-Galleries/PIAxxxxx``. I strongly recommend that you work on a local copy, and
   then rsync it back to Dropbox when you are done. This avoids any chance of clobbering the copy
   on Dropbox.
2. Be sure that the file ``PDS-Galleries/PIAxxxxx/PIAPAGE_CATALOG.pickle`` has been copied from
   Dropbox. If it is not present, this will necessarily be a full update rather than an incremental deploy.
3. If you don't want to write any newly retrieved JPEG files into ``/Library/Webserver/Documents``,
   edit ``DOCUMENTS_FILE_ROOT_`` inside ``gallerypage.py``. For example, if you are deploying to
   the "8080" version of the website first, ``DOCUMENTS_FILE_ROOT_`` should point to
   ``/Library/Webserver/Documents_8080`` instead. (This could be set up using an environment
   variable.)
4. Right now, we are only tracking Photojournal pages up to 25999. If we have started to
   see pages above 25900 or so, edit ``piapage/MAX_PIAPAGE.py`` to specify a higher limit.
5. ``cd`` to the ``pds-galleries`` repo directory.
6. In an ipython2 session...

        import piapage

7. For an incremental update:

        catalog = piapage.build_catalog()
        piapage.save_catalog(catalog)

8. Alternatively, for a full update:

        catalog = piapage.build_catalog(incremental=False)
        piapage.save_catalog(catalog)

At this point,
- the local catalog file ``PDS-Galleries/PIAxxxxx/PIAPAGE_CATALOG.pickle`` has been updated;
- any Photojournal product pages that were not previously cached locally have been copied
  into ``PDS-Galleries/PIAxxxxx``;
- for any new Photojournal product pages, the thumbnail, small, and medium JPEGs have been
  copied into ``/Library/WebServer/Documents/press_releases``;
- the Jekyll files for individual products have been written into the ``jekyll/press_releases/pages``
  subdirectory of this repo.

9. To generate the new galleries, run this program at the command line (not inside ipython):

        python2 piapage/piapage_galleries.py

At this point, the Jekyll galleries have been written to the ``jekyll/galleries``
subdirectory of this repo.

10. Before you can process the Jekyll files and push the HTML to the local website, you need to create
    links inside your local copy of the ``SETI/pds-website`` repo:

        cd <path to pds-website repo>

        mkdir website_galleries
        ln -s website/_config.production.yml website_galleries/_config.yml
        ln -s website/_config.yml  website_galleries/_config.yml
        ln -s website/_data     website_galleries/_data
        ln -s website/_includes website_galleries/_includes
        ln -s website/_layouts  website_galleries/_layouts
        ln -s website/_posts    website_galleries/_posts
        ln -s website/_sass     website_galleries/_sass

        ln -s <path to this repo>/jekyll/galleries      website_galleries/galleries
        ln -s <path to this repo>/jekyll/press_releases website_galleries/press_releases

11. To deploy to your local copy of the website:

        cd <path to pds-website repo>/deploy
        fab deploy localhost_galleries

12. Alternatively, to deploy to the local "8080" version of the website:

        cd <path to pds-website repo>/deploy
        fab deploy localhost_8080_galleries

13. Review the local website. Visit:

        https://localhost/galleries.html

        https://localhost/galleries/mercury.html
        https://localhost/galleries/venus.html
        https://localhost/galleries/moon.html
        https://localhost/galleries/mars.html
        https://localhost/galleries/jupiter.html
        https://localhost/galleries/saturn.html
        https://localhost/galleries/uranus.html
        https://localhost/galleries/neptune.html
        https://localhost/galleries/pluto.html

        https://localhost/galleries/asteroids.html
        https://localhost/galleries/comets.html
        https://localhost/galleries/kbos.html
        https://localhost/galleries/exoplanets.html

        https://localhost/galleries/target_mars.html
        https://localhost/galleries/target_jupiter.html
        https://localhost/galleries/target_saturn.html
        https://localhost/galleries/target_uranus.html
        https://localhost/galleries/target_neptune.html
        https://localhost/galleries/target_pluto.html
        https://localhost/galleries/asteroid_1_ceres.html
        https://localhost/galleries/comet_1p_halley.html
        https://localhost/galleries/kbo_pluto.html
        https://localhost/galleries/exoplanet_55_cancri.html

        https://localhost/galleries/cassini.html
        https://localhost/galleries/voyager.html
        https://localhost/galleries/juno.html
        https://localhost/galleries/new_horizons.html
        https://localhost/galleries/messenger.html
        https://localhost/galleries/dawn.html
        https://localhost/galleries/rosetta.html

        https://localhost/galleries/cassini_jupiter.html
        https://localhost/galleries/cassini_saturn.html
        https://localhost/galleries/voyager_jupiter.html
        https://localhost/galleries/voyager_saturn.html
        https://localhost/galleries/voyager_uranus.html
        https://localhost/galleries/voyager_neptune.html

14. If history is any guide, about 10% of the new images will have metadata that needs
to be repaired. The simplest way to handle a small number of repairs is to itemize
the changes inside the ``REMOVALS`` dictionary inside ``repairs.py``. Just create a new
dictionary entry keyed by the PIA code of the image. You can list extraneous keyword
values to remove, or specify new values to insert for the target, target type,
mission, etc.

15. Once you are satisfied with the results, deploy to the public servers. Note
    that this command only works from a server that has a current, up to date
    copy of the galleries and press releases.

        cd <path to pds-website repo>/deploy
        fab deploy server1_galleries
        fab deploy server2_galleries

16. Copy the new JPEGs to the servers by rsyncing the contents of these
    directories (although we should really fix this):

        /Library/WebServer/Documents/press_releases/thumbnails
        /Library/WebServer/Documents/press_releases/small
        /Library/WebServer/Documents/press_releases/medium

17. Rsync your local copy of the ``PDS-Galleries/PIAxxxxx`` directory back to Dropbox.

18. Commit your changes back to the repo on GitHub.
