################################################################################
# galleries.py
#
# Functions to write Jekyll pages containing arrays of thumbnail images and
# titles for browsing.
################################################################################

import os
import yaml
import itertools
import inspect
import dicts                # used by "inspect.getfile" below
import urllib.request

MONTH_NAMES = ['', 'January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']

QUARTER_NAMES = ['', 'January-March',    '', '',
                     'April-June',       '', '',
                     'July-September',   '', '',
                     'October-December', '', '']

QUARTER_ABBREVS = ['', 'Jan-Mar', '', '', 'Apr-Jun', '', '',
                       'Jul-Sep', '', '', 'Oct-Dec', '', '']

GALLERIES_SUBDIR_      = 'galleries/'
# Define the absolute path to the local Jekyll directory
JEKYLL_ROOT_ = inspect.getfile(dicts).rpartition('dicts/')[0] + 'jekyll/'
PHOTOJOURNAL_URL_      = 'https://photojournal.jpl.nasa.gov/catalog/'
PDS_PHOTOJOURNAL_URL = '//pds-rings.seti.org/press_releases/pages/'

################################################################################

class FixIndent(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)

def get_final_NASA_url(url):
    """ Since NASA is now redirecting all the original photojournal links,
        this will (hopefully) get the redirected links for the updated galleries

    Input:
        url     Original photojournal URL w/PIA embedded, example:
                https://photojournal.jpl.nasa.gov/catalog/PIA24615
    """

    # Only allow http/https schemes
    if not url.startswith(('http://', 'https://')):
        return url

    try:
        opener = urllib.request.build_opener()
        request = urllib.request.Request(url)
        with opener.open(request) as response:
            ret = response.geturl() # geturl() returns the final URL after redirects
            print(f'orig url: {url}, response: {ret}')
            return ret
    except urllib.error.URLError:
        # fall back to the original URL so generated hrefs stay valid
        return url

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
    for (product_id, page) in catalog.items():
        tuples.append((page.release_date, product_id))

    # Group by month
    by_month = {}
    for (release_date, product_id) in tuples:
        key = release_date[:7]
        if key not in by_month:
            by_month[key] = []

        by_month[key].append(product_id)

    yyyy_mm = list(by_month.keys())
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
        year_keys = list(by_year.keys())
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

        keys = list(by_date.keys())
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
    keys = list(by_date.keys())
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

    _gallery(fileroot, product_ids, catalog, links)

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
    for (key, page) in catalog.items():

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

    _gallery(fileroot, product_ids, catalog, links)

################################################################################
# Internal function to write a full set of browse pages
################################################################################

def _gallery(fileroot, product_ids, catalog, links, resolve_urls=False):
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
        resolve_urls    if True, resolve NASA URLs to their final redirected
                        location (time-consuming operation).

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

    """

    def create_yaml_header(title):
        data = {}
        data['layout'] = 'base'
        data['layout_style'] = 'wide'
        data['title'] = title.encode('ascii', 'xmlcharrefreplace').decode('ascii')

        return data

    def create_previous_next_menu(isSublist, previous_link):
        page_menu_data = {}

        if url != all_links[0][0]:
            page_menu_data['first_link'] = all_links[0][0]

        if url != all_links[-1][0]:
            page_menu_data['last_link'] = all_links[-1][0]

        # handle the sublist next/previous differently
        if isSublist:
            if subindex + 1 < len(item):
                page_menu_data['next_link'] = item[subindex + 1][0]

            elif index + 1 < len(main_links):
                page_menu_data['next_link'] = main_links[index + 1][0]

        else:
            if index + 1 < len(main_links):
                page_menu_data['next_link'] = main_links[index + 1][0]

        if previous_link is not None:
            page_menu_data['previous_link'] = previous_link

        return page_menu_data


    def create_menu_item(title, url, alt):
        return {
            'menu_item': {
                'title': title,
                'url': url,
                'alt': alt
            }
        }

    def create_jump_to_links(link_list, sublist = None):
        jump_to_links = []

        for element in link_list:
            if isinstance(element, tuple):
                if len(element) > 3:
                    (url, title, _, alt) = element
                else:
                    (url, title, alt) = element

                jump_to_links.append(create_menu_item(title, url, alt))

            else:
                if sublist == element:
                    for subelement in sublist:
                        if len(subelement) > 3:
                            (url, _, title, alt) = subelement
                        else:
                            (url, title, alt) = subelement

                        jump_to_links.append(create_menu_item(title, url, alt))
                else:
                    subelement = element[0]
                    if len(subelement) > 3:
                        (url, title, _, alt) = subelement
                    else:
                        (url, title, alt) = subelement

                    jump_to_links.append(create_menu_item(title, url, alt))


        return jump_to_links

    def create_floated_img_blocks(filename):
        floated_img_blocks = []
        for id in product_ids[filename]:
            title = catalog[id].title.encode('ascii', 'xmlcharrefreplace').decode('ascii')
            alt = id + ':' + title.replace('"', '&quot;')

            href = PDS_PHOTOJOURNAL_URL + id[:5] + 'xxx/' + id + '.html'

            """
            # NOTE: the NASA photojournal should NOT be usedfor now,
            # keeping the PDS links as a temporary solution until NASA photojournal
            # completes some of their implementation modifications.
            """
            if resolve_urls is True:
                NASA_href = PHOTOJOURNAL_URL_ + id
                href = get_final_NASA_url(NASA_href)

            row_data = {
                'row': '',
                'href': href,
                'src': catalog[id].local_thumbnail_url,
                'alt': alt,
                'title': title
            }
            if catalog[id].is_movie:
                row_data['movie'] = True

            floated_img_blocks.append({k: v for k, v in row_data.items() if v is not None})

        return floated_img_blocks

    def write_yaml_file(filename, yaml_data):
        yaml_output = yaml.dump(yaml_data, Dumper=FixIndent, default_flow_style=False, sort_keys=False)

        # Adding '---' at the beginning and end of the YAML
        yaml_output = f"---\n{yaml_output}---\n"
        yaml_output += "\n# {{ page.title }}\n\n---\n\n{% include gallery.html %}\n"

        # Write YAML data to file
        filepath = os.path.join(fileroot, filename)
        os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(yaml_output)

    # flatten the array of arrays to make it easier to create the next and previous links
    all_links = list(itertools.chain.from_iterable(
        item if isinstance(item, list) else [item] for item in links
    ))

    main_links = []
    for element in links:
        if isinstance(element, tuple):
            main_links.append(element)
        elif isinstance(element, list):
            main_links.append(element[0])

    previous_link = None
    for index, item in enumerate(links):
        if isinstance(item, tuple):
            (url, _, alt,) = item

            yaml_data = create_yaml_header(alt)

            # don't create addition menus when it is a flat structure
            if len(all_links) > 1:
                yaml_data['page_menu'] = create_previous_next_menu(False, previous_link)
                previous_link = url

                # jump to navigation
                yaml_data['jump_to'] = create_jump_to_links(links)

            # image blocks
            yaml_data['image_table'] = create_floated_img_blocks(url)

            write_yaml_file(url, yaml_data)

        else:
            for subindex, subitem in enumerate(item):
                if len(subitem) > 3:
                    (url, _, _, alt,) = subitem
                else:
                    (url, _, alt,) = subitem

                yaml_data = create_yaml_header(alt)

                yaml_data['page_menu'] = create_previous_next_menu(True, previous_link)
                previous_link = url

                # jump to navigation
                yaml_data['jump_to'] = create_jump_to_links(links, sublist = item)

                # image blocks
                yaml_data['image_table'] = create_floated_img_blocks(url)

                write_yaml_file(url, yaml_data)

################################################################################
