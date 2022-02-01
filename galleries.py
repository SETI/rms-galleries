################################################################################
# galleries.py
#
# Functions to write Jekyll pages containing arrays of thumbnail images and
# titles for browsing.
################################################################################

import os
from gallerypage import GalleryPage

MONTH_NAMES = ['', 'January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']

QUARTER_NAMES = ['', 'January-March',    '', '',
                     'April-June',       '', '',
                     'July-September',   '', '',
                     'October-December', '', '']

QUARTER_ABBREVS = ['', 'Jan-Mar', '', '', 'Apr-Jun', '', '',
                       'Jul-Sep', '', '', 'Oct-Dec', '', '']

################################################################################

def by_release_date(catalog, fileroot, url_prefix, title_prefix,
                    merge_limit=240, merge_early=True, merge_late=True):
    """Write a set of galleries based on release date and organized by month,
    quarter or year.

    Input:
        catalog         a dictionary of GalleryPage objects keyed by product_id,
                        one for each thumbnail to appear in the gallery.
        fileroot        the path to the output directory.
        url_prefix      string to put in front of each URL, e.g., 'cassini'.
        title_prefix    text to put in front of each title, e.g.,
                        'Mar Press Releases'.
        merge_limit     target number of thumbnail images per page. If an entire
                        year contains fewer images than the merge_limit, the
                        thumbnails from the entire year will be merged into a
                        single page. If several years at the beginning or end
                        of the catalog can be merged and will fall below this
                        limit, they are also merged.
        merge_early     True to merge the earliest years of possible.
        merge_late      True to merge the latest years if possible.
    """

    def _title(key):
        """A suitable title for the page, based on the dictionary key."""

        if len(key) == 4:       # one year
            return title_prefix + ' for ' + key

        if '-' in key:          # range of years
            return title_prefix + ' ' + key

        if grouping == 'month':
            month = MONTH_NAMES[int(key[5:])]
            return title_prefix + ' for ' + month + ' ' + key[:4]

        else:
            months = QUARTER_NAMES[int(key[5:])]
            return title_prefix + ' for ' + months + ' of ' + key[:4]

    def _label(key):
        """A suitable label for the page, based on the dictionary key."""

        if len(key) == 4:
            return key

        if grouping == 'month':
            return MONTH_NAMES[int(key[5:])][:3]

        else:
            return QUARTER_ABBREVS[int(key[5:])]

    # Sort chronologically
    tuples = []
    for (product_id, page) in catalog.iteritems():
        tuples.append((page.release_date, product_id))

    # Group by month
    by_month = {}
    for (release_date, product_id) in tuples:
        key = release_date[:7]
        if key not in by_month:
            by_month[key] = []

        by_month[key].append(product_id)

    yyyy_mm = by_month.keys()
    yyyy_mm.sort()

    first_year = yyyy_mm[0][:4]
    last_year = yyyy_mm[-1][:4]

    # Group by quarter
    by_quarter = {}
    for key in yyyy_mm:
        imonth = 3 * ((int(key[5:]) - 1)//3) + 1
        qkey = key[:5] + '%02d' % imonth

        if qkey not in by_quarter:
            by_quarter[qkey] = []

        by_quarter[qkey] += by_month[key]

    # Group by year
    by_year = {}
    for key in yyyy_mm:
        ykey = key[:4]
        if ykey not in by_year:
            by_year[ykey] = []

        by_year[ykey] += by_month[key]

    # Determine the maximum thumbnail count on each hypothetical page
    ycount_max = max([len(by_year[k])    for k in by_year])
    qcount_max = max([len(by_quarter[k]) for k in by_quarter])

    # Determine how to organize the page
    if len(tuples) <= merge_limit:
        grouping = 'all'
        years = list(by_year.keys())
        years.sort()
        if len(years) == 1:
            key = years[0]
        else:
            key = years[0] + '-' + years[-1]

        all_years = []
        for year in years:
            all_years += by_year[year]
        by_date= {key: all_years}
    elif ycount_max <= merge_limit:
        grouping = 'year'
        by_date = by_year
    elif qcount_max <= merge_limit:
        grouping = 'quarter'
        by_date = by_quarter
    else:
        grouping = 'month'
        by_date = by_month

    keys = list(by_date.keys())
    keys.sort()

    # Merge entire years if possible

    years_merged = []
    years_unmerged = []

    if grouping != 'all':
        year_keys = by_year.keys()
        year_keys.sort()

        if grouping == 'year':
            years_merged = [int(y) for y in year_keys]

        else:
            for year_key in year_keys:
                thumbnails = len(by_year[year_key])
                if thumbnails <= merge_limit:
                    years_merged.append(int(year_key))
                    by_date[year_key] = by_year[year_key]
                else:
                    years_unmerged.append(int(year_key))

                keys_to_delete = []
                for year in years_merged:
                    year_key = str(year)
                    for key in by_date:
                        if len(key) > 4 and key[:4] == year_key:
                            keys_to_delete.append(key)

                for key in keys_to_delete:
                    del by_date[key]

        keys = by_date.keys()
        keys.sort()

    # Merge multiple early years if possible
    early_year = None
    year_limit = min(merge_limit, max([len(v) for v in by_date.values()]) + merge_limit//4)
            # don't merge to exceed far beyond the size of the largest page

    if grouping != 'all' and years_merged and merge_early:
        y0 = years_merged[0]
        cumsum = 0
        count = 0

        if years_unmerged:
            ystop = years_unmerged[0]
        else:
            ystop = years_merged[-1] + 1

        for y1 in range(y0, ystop):
            key = str(y1)
            if key not in by_date:
                continue

            tempsum = cumsum + len(by_date[key])
            if tempsum > year_limit:
                break

            cumsum = tempsum
            count += 1

        if count > 2:       # Don't bother to merge just two years
            merged_ids = []
            for y in range(y0,y1):
                key = str(y)
                if key in by_date:
                    merged_ids += by_date[key]
                    del by_date[key]

            by_date[str(y0)] = merged_ids
            early_year = y1

    # Merge multiple late years if possible
    late_year = None
    if grouping != 'all' and years_merged and merge_late:
        y0 = years_merged[-1]
        cumsum = 0
        count = 0

        if years_unmerged:
            ystop = years_unmerged[-1]
        else:
            ystop = years_merged[0] - 1

        if early_year:
            ystop = max(ystop, early_year)

        for y1 in range(y0, ystop, -1):
            key = str(y1)
            if key not in by_year:
                continue

            tempsum = cumsum + len(by_year[key])
            if tempsum > merge_limit:
                break

            cumsum = tempsum
            count += 1

        if count > 2:       # Don't bother to merge just two years
            merged_ids = []
            for y in range(y0,y1,-1):
                key = str(y)
                if key in by_date:
                    merged_ids += by_date[key]
                    del by_date[key]

            by_date[str(y0)] = merged_ids
            late_year = y1

    # Re-sort the keys
    keys = by_date.keys()
    keys.sort()

    # Create product_ids and links
    tuples = []         # a flat list of tuples with key in first slot
    product_ids = {}

#         (key, filename, label, title)
#         (key, filename, label_if_closed, label_if_open, title)

    # Create the first tuple
    key = keys[0]
    if len(keys) == 1:
        filename = url_prefix + '.html'
        info = (key, filename, key, _title(key))
    else:
        filename = url_prefix + '_' + key + '.html'

        if early_year:
            year_range = first_year + '-' + str(early_year)
            title = _title(year_range)
            label = year_range
            info = (key, filename, label, title)
        elif len(key) == 4:
            info = (key, filename, key, _title(key))
        else:
            info = (key, filename, key[:4], key + ' ' + _label(key), _title(key))

    tuples.append(info)
    product_ids[filename] = by_date[key]

    if len(keys) > 1:
        # Loop through intermediate entries
        prev_year = key[:4]
        for key in keys[1:-1]:
            if len(key) == 4:
                filename = url_prefix + '_' + key + '.html'
                info = (key, filename, key, _title(key))
            elif key[:4] == prev_year:
                filename = url_prefix + '_' + key + '.html'
                info = (key, filename, _label(key), _title(key))
            else:
                filename = url_prefix + '_' + key[:4] + '.html'
                info = (key, filename, key[:4], key[:4] + ' ' + _label(key),
                                                                _title(key))

            tuples.append(info)
            product_ids[filename] = by_date[key]
            prev_year = key[:4]

        # Create final tuple
        key = keys[-1]
        filename = url_prefix + '.html'
        if late_year:
            year_range = str(late_year+1) + '-' + last_year
            title = _title(year_range)
            label = year_range
            info = (key, filename, label, title)
        else:
            info = (key, filename, _label(key), _title(key))

        tuples.append(info)
        product_ids[filename] = by_date[key]

    # Right now the list of tuples is flat. Create sublists where needed.

    links = []
    prev_year = ''
    for info in tuples:
        key = info[0]
        if len(info) == 5:      # if it has label_if_closed and label_if_open
            prev_year = key[:4]
            links.append([info[1:]])  # skip leading key
        elif key[:4] == prev_year:
            links[-1].append(info[1:])
        else:
            links.append(info[1:])

    _gallery(fileroot, product_ids, catalog, links,
             separators=('|','|'), linebreaks=2)

################################################################################
################################################################################

def by_target(catalog, fileroot, url_prefix, title_prefix, targets,
              page_limit=240, target_types=False, plurals=[]):
    """Write a set of target-by-target galleries.

    Input:
        catalog         a dictionary of GalleryPage objects keyed by product_id,
                        one for each thumbnail to appear in the gallery.
        fileroot        the path to the output directory.
        url_prefix      string to put in front of each URL, e.g., 'cassini'.
        title_prefix    text to put in front of each title, e.g.,
                        'Cassini Press Releases'.
        targets         an ordered list of target names in order (or a list of
                        target_types if target_types is True).
        page_limit      target number of thumbnail images per page. If all the
                        images of a target is less than or equal to this limit,
                        then they will all appear on a single page. If more
                        images exist, the images of the target will be split
                        across multiple pages, ordered by release date.
        target_types    True to create a gallery page by target type instead of
                        target.
        plurals         optional list of plurals, to use in titles in place of
                        the value in the targets list.
    """

    def _title(target, page, pages):
        """A suitable title for the page."""

        if plurals:
                k = targets.index(target)
                title = title_prefix + ' referring to ' + plurals[k]
        elif ('Ring' in target and 'Rings' not in target) or \
            'Division' in target or 'Gap' in target or 'System' in target:
                title = title_prefix + ' referring to the ' + target
        else:
                title = title_prefix + ' referring to ' + target

        if pages <= 1:
            return title

        return title + ' (p. %d of %d)' % (page, pages)

    def _label(target, page, pages):
        """A suitable label for the hyperlink to the page."""

        if pages <= 1:
            return target
        elif page == 1:
            return target + ' p.1'
        else:
            return str(page)

    # Organize by target or system
    info = {}
    for (key, page) in catalog.iteritems():

        if target_types:
            names = page.target_types
        else:
            names = page.targets

        for name in names:
            if name not in targets:
                continue

            if name not in info:
                info[name] = []

            info[name].append((page.release_date, key))

        for name in page.systems:       # optionally include system names
            sysname = name + ' System'
            if sysname not in targets:
                continue

            if sysname not in info:
                info[sysname] = []

            info[sysname].append((page.release_date, key))

    # Create the links structure
    links = []
    product_ids = {}
    for target in targets:
        if target not in info:
            continue

        tuples = info[target]
        tuples.sort()
        ids = [t[1] for t in tuples]

        filename_prefix = (url_prefix + '_' +
                           target.lower().replace(' ', '_')
                                         .replace('/','_')
                                         .replace('(','')
                                         .replace(')',''))

        if len(tuples) <= page_limit:
            filename = filename_prefix + '.html'
            links.append((filename, target, _title(target, 0, 0)))
            product_ids[filename] = ids

        else:
            pages = (len(tuples) + page_limit - 1) // page_limit
            pagesize = (len(tuples) + pages - 1) // pages

            # First page
            filename = filename_prefix + '_p01.html'
            links.append([(filename, target, _label(target, 1, pages),
                                             _title(target, 1, pages))])
            product_ids[filename] = ids[:pagesize]
            ids = ids[pagesize:]

            # Middle pages
            for k in range(2, pages):
                filename = filename_prefix + '_p%02d.html' % k
                links[-1].append((filename, _label(target, k, pages),
                                            _title(target, k, pages)))
                product_ids[filename] = ids[:pagesize]
                ids = ids[pagesize:]

            # Last page
            filename = filename_prefix + '.html'
            links[-1].append((filename, _label(target, pages, pages),
                                        _title(target, pages, pages)))
            product_ids[filename] = ids

    _gallery(fileroot, product_ids, catalog, links,
             separators=('|',''), linebreaks=0)

################################################################################
# Internal function to write a full set of browse pages
################################################################################

def _gallery(fileroot, product_ids, catalog, links,
             separators=('|','|'), linebreaks=True, bottom_nav=20):
    """Write a a complete set of Jekyll gallery pages of thumbnails with links
    between one another and to the image pages.

    Inputs:
        fileroot        the path to the output directory.
        product_ids     a dictionary, keyed by html filename, that returns an
                        ordered list of the thumbnail IDs to appear on the page.
        catalog         a dictionary, keyed by product_id, that returns the
                        associated GalleryPage object.
        links           a list structure defining the labels, titles and html
                        filenames for a thumbnail gallery. See details below.
        separators      a string or a tuple of two strings indicating the
                        separator character between hyperlinks in lists and
                        sublists.
        linebreaks      number of adjacent sublists to show, separated by line
                        breaks
        bottom_nav      number of items in the page before it adds prev/next
                        navigation to the bottom of the page. True for always;
                        False for never.

    The basic element in the links structure is a tuple
        (filename, label, title)
    where filename is the basename of an output file, label is the text to use
    for hyperlink that appears in the index section of each page, and title is
    title text to appear on this page.

    "links" is a list defining all the pages of the gallery. Each element in the
    list is either a tuple as defined above or a sublist. When the element is a
    tuple, the label appears in the index section of every page and links to the
    associated page.

    When the list element is a sublist, it defines a group of links that can
    appear on the page as either "open" or "closed". When the group is open,
    then all the hyperlinks are visible and they are grouped inside square
    brackets "[]". When the group is closed, only the first hyperlink is
    visible.

    The first tuple in a sublist has an extra element as shown:
        (filename, label_if_closed, label_if_open, title)
    Here label_if_closed is the text of the hyperlink to use if the sublist is
    closed, and label_if_open is the text to use if the sublist is open.

    "separators" is a single string or a tuple of two strings. The first string
    appears between hyperlinks in the index. Vertical bar "|" is the default.
    The second string, if present, appears between hyperlinks in a sublist.

    If "linebreaks" is 1, then an open sublist is surrounded by line breaks. If
    2 or more, then adjacent sublists are also open and surrounded by line
    breaks. If 0, then open sublists are not surrounded by line breaks.

    Example 1:
        [("images_2007.html", "2007", "Images from 2007"),
         ("images_2008.html", "2008", "Images from 2008"),
         ("images_2009.html", "2009", "Images from 2009")]
    If separators = "|", then the page index will look like this:
        2007 | 2008 | 2009

    Example 2:
        [("images_2007.html", "2007", "Images from 2007"),
         [("images_2008_01.html", "2008", "2008 Jan-Mar", "Images 2008-Q1"),
          ("images_2008_04.html",              "Apr-Jun", "Images 2008-Q2"),
          ("images_2008_07.html",              "Jul-Aug", "Images 2008-Q3"),
          ("images_2008_10.html",              "Sep-Dec", "Images 2008-Q4")],
         [("images_2009_01.html", "2009", "2009 Jan-Mar", "Images 2009-Q1"),
          ("images_2009_04.html",              "Apr-Jun", "Images 2009-Q2"),
          ("images_2009_07.html",              "Jul-Aug", "Images 2009-Q3"),
          ("images_2009_10.html",              "Sep-Dec", "Images 2009-Q4")],
         [("images_2010_01.html", "2010", "2010 Jan-Mar", "Images 2010-Q1"),
          ("images_2010_04.html",              "Apr-Jun", "Images 2010-Q2"),
          ("images_2010_07.html",              "Jul-Aug", "Images 2010-Q3"),
          ("images_2010_10.html",              "Sep-Dec", "Images 2010-Q4")],
        ("images_2011.html", "2011", "Images from 2011"),
        ("images_2012.html", "2012", "Images from 2012")]

    If separators = ("|","|") and the first item is selected, the page index
    will look like this:
        2007 | 2008 | 2009 | 2010 | 2011 | 2012

    If 2008 or any item in its sublist is selected, separators = ("|","") and
    linebreaks = 0, the page index will look like this:
      2007 | [2008 Jan-Mar Apr-Jun Jul-Aug Sep-Dec] | 2009 | 2010 | 2011 | 2012

    Same as above, but linebreaks = 1:
        2007 |
        [2008 Jan-Mar Apr-Jun Jul-Aug Sep-Dec] |
        2009 | 2010 | 2011 | 2012

    Same as above, but linebreaks = 2:
        2007 |
        [2008 Jan-Mar Apr-Jun Jul-Aug Sep-Dec] |
        [2009 Jan-Mar Apr-Jun Jul-Aug Sep-Dec] |
        2010 | 2011 | 2012

    Example 3:
        [[("saturn.html", "Saturn", "Saturn p.1", "Saturn Images (p.1)"),
          ("saturn_p2.html",               "p.2", "Saturn images (p.2)"),
          ("saturn_p3.html",               "p.3", "Saturn images (p.3)"),
         [("mimas.html", Mimas", "Mimas p.1", "Mimas Images (p.1)"),
          ("mimas_p2.html",            "p.2", "Mimas images (p.2)", )],
         ("enceladus.html", "Enceladus", "Enceladus Images")]

    If separators = (|",""), linebreaks = 0, and one of the Saturn pages is
    selected, the index will look like 
        [Saturn p.1 p.2 p.3] | Mimas | Enceladus

    If Enceladus is selected, the index will look like this:
        Saturn | Mimas | Enceladus
    """

    # Replace each element that is not a sublist by a one-element sublist
    links = list(links)
    for k in range(len(links)):
        if isinstance(links[k], tuple):
            links[k] = [links[k]]

    for sublist in links:
        for k in range(len(sublist)):
            if len(sublist[k]) == 3:
               sublist[k] = (sublist[k][0], sublist[k][1], sublist[k][1],
                                                           sublist[k][2])

    # Make sure we have two separator strings
    if isinstance(separators, str):
        separators = [separators, '']
    elif len(separators) == 1:
        separators = [separators[0], '']

    if separators[1]:
        spacer = ' '
    else:
        spacer = ''

    separators = list(separators)
    if separators[1].strip() == '':
        separators[1] = '&thinsp;'

    # Create the parent directories if necessary
    try:
        os.makedirs(fileroot)
    except OSError:
        pass

    #### Walk through the pages of the gallery indexed [j]

    nlinks = len(links)
    for j in range(nlinks):
      sublist_is_open  = nlinks * [False]
      linebreak_before = (nlinks+1) * [False]

      sublist = links[j]
      nsublinks = len(sublist)

      # Decide which sublists are open
      if nsublinks > 1:
          sublist_is_open[j] = True
          if linebreaks:
              linebreak_before[j] = True
              linebreak_before[j+1] = True

          if linebreaks > 1:
              if j > 0 and len(links[j-1]) > 1:
                  sublist_is_open[j-1] = True
                  linebreak_before[j-1] = True
              if j < nlinks-1 and len(links[j+1]) > 1:
                  sublist_is_open[j+1] = True
                  linebreak_before[j+2] = True

      linebreak_before[0] = False         # No line break before first
      linebreak_before[-1] = False        # No line break after last

      # Walk through sublist items indexed [k]

      nsubs = len(sublist)
      for k in range(nsubs):
        neighbors = 4 * [None]

        # Locate target of "<<"
        if k > 0:
            neighbors[0] = sublist[0]
        else:
            neighbors[0] = links[0][0]

        if (j,k) == (0,0):
            neighbors[0] = None

        # Locate target of "<"
        if k > 0:
            neighbors[1] = sublist[k-1]
        elif j == 0:
            neighbors[1] = None
        elif sublist_is_open[j-1]:
            neighbors[1] = links[j-1][-1]
        else:
            neighbors[1] = links[j-1][0]

        # Locate target of ">"
        if k < nsubs - 1:
            neighbors[2] = sublist[k+1]
        elif j == nlinks - 1:
            neighbors[2] = None
        else:
            neighbors[2] = links[j+1][0]

        # Locate target of ">>"
        if k < nsubs - 1:
            neighbors[3] = sublist[-1]
        elif j == nlinks - 1:
            neighbors[3] = None
        elif sublist_is_open[-1]:
            neighbors[3] = links[-1][-1]
        else:
            neighbors[3] = links[-1][0]

        # Write the Jekyll file
        (filename, _, _, title) = sublist[k]
        filepath = os.path.join(fileroot, filename)
        with open(filepath, 'w') as f:

          # Write header
          escaped = title.encode('ascii', 'xmlcharrefreplace')

          f.write('---\n')
          f.write('layout: base\n')
          f.write('layout_style: wide\n')
          f.write('format: html\n')
          f.write('title: "%s"\n' % escaped.replace('"',"'"))
          f.write('---\n\n')

          f.write('<style>\n')
          f.write('.floated_img\n')
          f.write('{\n')
          f.write('    float: left;\n')
          f.write('    padding: 3px;\n')
          f.write('}\n')
          f.write('.floated_img table {\n')
          f.write('    width: 200px;\n')
          f.write('    border: 1px solid lightgrey;\n')
          f.write('    border-collapse: collapse;\n')
          f.write('}\n')
          f.write('td.thumbnail {\n')
          f.write('    vertical-align: bottom;\n')
          f.write('    height: 100px;\n')
          f.write('    text-align: 100px;\n')
          f.write('}\n')
          f.write('td.caption {\n')
          f.write('    vertical-align: top;\n')
          f.write('    height: 66px;\n')
          f.write('    font-size: 10pt;\n')
          f.write('    max-height: 66px;\n')
          f.write('    word-wrap: break-word;\n')
          f.write('    overflow: hidden;\n')
          f.write('    text-overflow: ellipsis;\n')
          f.write('    display: -webkit-box;\n')
          f.write('    -webkit-line-clamp: 3;\n')
          f.write('    -webkit-box-orient: vertical;\n')
          f.write('}\n')
          f.write('</style>\n\n')

          f.write('<h1>%s</h1>\n\n' % escaped)
          f.write('<hr/>\n')

          # Write first/prev/next/last navigation
          if nlinks > 1:
            f.write('<p align="center">\n')

            if neighbors[0] is None:
                f.write('&lt;&lt; first |\n')
            else:
                f.write('<a href="%s">&lt;&lt; first</a> |\n' % neighbors[0][0])

            if neighbors[1] is None:
                f.write('&lt; previous |\n')
            else:
                f.write('<a href="%s">&lt; previous</a> |\n' % neighbors[1][0])

            if neighbors[2] is None:
                f.write('next &gt; |\n')
            else:
                f.write('<a href="%s">next &gt;</a> |\n' % neighbors[2][0])

            if neighbors[3] is None:
                f.write('last &gt;&gt;\n')
            else:
                f.write('<a href="%s">last &gt;&gt;</a>\n' % neighbors[3][0])

            f.write('</p>\n\n')

            # Write complete navigation
            f.write('<b>Jump to</b>:<br/>\n')

            for jj in range(nlinks):
              if jj != 0:
                f.write(separators[0] + ' ')

              if linebreak_before[jj]:
                f.write('<br/>')

              if sublist_is_open[jj]:
                (url, _, label_if_open, _) = links[jj][0]
                if filename == url:
                  f.write('[%s<b>%s</b>\n' % (spacer, label_if_open))
                else:
                  f.write('[%s<a href="%s">%s</a>\n' % (spacer, url,
                                                        label_if_open))

                for kk in range(1, len(links[jj])-1):
                  (url, _, label_if_open, _) = links[jj][kk]
                  if filename == url:
                    f.write('%s <b>%s</b>\n' % (separators[1], label_if_open))
                  else:
                    f.write('%s <a href="%s">%s</a>\n' % (separators[1], url,
                                                          label_if_open))

                (url, _, label_if_open, _) = links[jj][-1]
                if filename == url:
                  f.write('%s <b>%s</b>%s]\n' % (separators[1], label_if_open,
                                                 spacer))
                else:
                  f.write('%s <a href="%s">%s</a>%s]\n' % (separators[1], url,
                                                         label_if_open, spacer))

              else:
                (url, label_if_closed, _, _) = links[jj][0]
                if filename == url:
                  f.write('<b>%s</b>\n' % label_if_closed)
                else:
                  f.write('<a href="%s">%s</a>\n' % (url, label_if_closed))

#             f.write('<hr/>\n')
            f.write('<div align="left">\n')

          # Write the thumbnails
          for id in product_ids[filename]:
            title = catalog[id].title
            is_movie = catalog[id].is_movie
            if catalog[id].thumbnail_shape:
                (w,h) = catalog[id].thumbnail_shape
                width = int(100. * w/float(h) + 0.9999999)
            elif catalog[id].shape:
                (w,h) = catalog[id].shape
                width = int(100. * w/float(h) + 0.9999999)
            else:
                width = 100.

            width = int(max(width + 0.5, 200))

            escaped = title.encode('ascii', 'xmlcharrefreplace')
            unquoted = escaped.replace('"', '&quot;')

            f.write('  <div class="floated_img">\n')
            f.write('    <table width="%d">\n' % width)
            f.write('      <tr>\n')
            f.write('        <td class="thumbnail">\n')
            f.write('          <a href="%s">\n' %
                                 catalog[id].local_page_url)
            f.write('            <img src="%s"\n' %
                                 catalog[id].local_thumbnail_url)
            f.write('                 alt="%s: %s"\n' % (id, unquoted))
            f.write('                 align="center" height="100">\n')
            f.write('          </a>\n')
            f.write('        </td>\n')
            f.write('      </tr>\n')
            f.write('      <tr>\n')
            f.write('        <td class="caption">\n')

            if is_movie:
                f.write('          <img src="/icons-local/movie_icon.png"\n')
                f.write('               alt="Movie icon">\n')

            f.write('          <a href="%s">\n' %
                                catalog[id].local_page_url)
            f.write('              %s\n' % escaped)
            f.write('          </a>\n')
            f.write('        </td>\n')
            f.write('      </tr>\n')
            f.write('    </table>\n')
            f.write('  </div>\n\n')

          f.write('</div>\n\n')

          # Repeat first/prev/next/last navigation
          if nlinks >= 1 and (bottom_nav is True or len(product_ids[filename]) >= bottom_nav):
            f.write('<div><br clear="all" /><br/><p align="center">\n')

            if neighbors[0] is None:
                f.write('&lt;&lt; first |\n')
            else:
                f.write('<a href="%s">&lt;&lt; first</a> |\n' % neighbors[0][0])

            if neighbors[1] is None:
                f.write('&lt; previous |\n')
            else:
                f.write('<a href="%s">&lt; previous</a> |\n' % neighbors[1][0])

            if neighbors[2] is None:
                f.write('next &gt; |\n')
            else:
                f.write('<a href="%s">next &gt;</a> |\n' % neighbors[2][0])

            if neighbors[3] is None:
                f.write('last &gt;&gt;\n')
            else:
                f.write('<a href="%s">last &gt;&gt;</a>\n' % neighbors[3][0])

            f.write('</p><br/></div>\n\n')

################################################################################
