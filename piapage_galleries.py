import piapage
import pickle

def jekyll_thumbnail_gallery(filepath, title, keys, info_dict,
                             here=0, labels=[], links=[], text_lines=3):
    """Write a Jekyll page of thumbnails with links to the image pages.

    filepath is the path to the output file.
    title is the title to appear on the page.
    keys is the ordered list of PIA IDs indicating which thumbnails to include.
    info_dcit is the dictionary read from pia_dict.pickle.

    here is the index of this page into the lists of labels and links
    labels is a list of labels for the neighbor navigation links
    links is a list of the urls for the neighbor navigation links
    """

    h = 10 + 20 * text_lines

    with open(filepath, 'w') as f:

        # Write Jekyll header

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
        f.write('    padding: 4px;\n')
        f.write('}\n')
        f.write('</style>\n\n')

        f.write('<h1>%s</h1>\n\n' % escaped)

        if labels:

            f.write('<hr/>\n')

            # First/prev/next/last navigation
            f.write('<p align="center">\n')

            if here == 0:
                f.write('&lt;&lt; first |\n')
                f.write('&lt; previous |\n')
            else:
                f.write('<a href="%s">&lt;&lt; first</a> |\n' % links[0])
                f.write('<a href="%s">&lt; previous</a> |\n' % links[here-1])

            if here == len(labels) - 1:
                f.write('next &gt; |\n')
                f.write('last &gt;&gt;\n')
            else:
                f.write('<a href="%s">next &gt;</a> |\n' % links[here+1])
                f.write('<a href="%s">last &gt;&gt;</a>\n' % links[-1])

            f.write('</p>\n\n')

            # Complete navigation
            f.write('<b>Jump to</b>: \n')

            for k in range(len(labels)):
                if k == here:
                    f.write('<b>%s</b>' % labels[k])
                else:
                    f.write('<a href="%s">%s</a>' % (links[k], labels[k]))

                if k == len(labels) - 1:
                    f.write('\n\n')
                elif (labels[k][-1] in '0123456789' and 
                      labels[k+1][0] in '123456789'):
                    f.write(' &nbsp;\n')
                else:
                    f.write(' |\n')

        f.write('<hr/>\n')
        f.write('<div align="left">\n')

        for key in keys:

          title = info_dict[key][1]
          is_movie = info_dict[key][2]
          is_color = info_dict[key][3]

          escaped = title.encode('ascii', 'xmlcharrefreplace')
          unquoted = escaped.replace('"', '&quot;')

          f.write('  <div class="floated_img" align="center">\n')
          f.write('    <table border="0" width="200">\n')
          f.write('      <tr>\n')
          f.write('        <td style="vertical-align:top;height:110px;">\n')
          f.write('          <a href="%s">\n' %
                               piapage.PiaPage.local_html_url_for_id(key))
          f.write('            <img src="%s"\n' %
                               piapage.PiaPage.local_thumbnail_url_for_id(key))
          f.write('                 alt="%s: %s"\n' % (key, unquoted))
          f.write('                 align="center" height="100">\n')
          f.write('          </a>\n')
          f.write('        </td>\n')
          f.write('      </tr>\n')
          f.write('      <tr>\n')
          f.write('        <td style="vertical-align:top;height:%dpx">\n' % h)
          f.write('\n')

          if is_movie:
              f.write('          <img src="/icons-local/movie_icon.png"\n')
              f.write('               alt="Movie icon">\n')

          f.write('          <font size="2">\n')
          f.write('            <a href="%s">\n' %
                                 piapage.PiaPage.local_html_url_for_id(key))
          f.write('              %s\n' % escaped)

          f.write('            </a>\n')
          f.write('          </font>\n')
          f.write('        </td>\n')
          f.write('      </tr>\n')
          f.write('    </table>\n')
          f.write('  </div>\n\n')

        f.write('</div>\n\n')

################################################################################

JEKYLL_ROOT_ = '/Users/Shared/GitHub/pds-website/website/'

f = open('piapage_catalog.pickle')
info_dict = pickle.load(f)
f.close()

################################################################################
# Cassini by date
################################################################################

info_by_year = {}
all_info = []

for (id, info) in info_dict.items():

    (release_date, title, is_movie, is_color, is_grayscale,
     missions, hosts, host_types, instruments, detectors,
     targets, target_types, systems, extra_keywords, dates,
     local_html_url, local_thumbnail_url,
     local_small_url, local_medium_url) = info

    if missions[0] != 'Cassini-Huygens': continue
    year = release_date[:4]
    if year in info_by_year:
        info_by_year[year].append((release_date, id))
    else:
        info_by_year[year] = [(release_date, id)]

    all_info.append((release_date, id))

years = info_by_year.keys()
years.sort()

for year in years:
    info_by_year[year].sort()
    print year, len(info_by_year[year])

# 1997 5
# 1999 4
# 2000 30
# 2001 17
# 2002 7
# 2003 5
# 2004 284
# 2005 509
# 2006 379
# 2007 356
# 2008 347
# 2009 344
# 2010 308
# 2011 109
# 2012 97
# 2013 114
# 2014 81
# 2015 100
# 2016 76
# 2017 105
# 2018 15

divs = ['1997-01', '2004-01', '2004-07',
        '2005-01', '2005-04', '2005-07', '2005-10',
        '2006-01', '2006-04', '2006-07', '2006-10',
        '2007-01', '2007-04', '2007-07', '2007-10',
        '2008-01', '2008-04', '2008-07', '2008-10',
        '2009-01', '2009-04', '2009-07', '2009-10',
        '2010-01', '2010-04', '2010-07', '2010-10',
        '2011-01', '2012-01', '2013-01', '2014-01', 
        '2015-01', '2016-01', '2017-01', '2018-01', '2999-01']

filepaths = []
labels = []
links  = []
for before in divs[:-1]:
    links.append('cassini_' + before + '.html')
    filepaths.append(JEKYLL_ROOT_ + 'galleries/overviews/' + links[-1])

    # Default is by quarters
    month = int(before[5:])
    q = {1: 'Q1', 4: 'Q2', 7: 'Q3', 10: 'Q4'}[month]
    labels.append(before[:4] + ' ' + q)

labels[0] = '1997-2003'
labels = [l if l < '2011' else l[:4] for l in labels]

# Better name for starting point
links[0] = 'cassini.html'
filepaths[0] = JEKYLL_ROOT_ + 'galleries/overviews/' + links[0]

all_info.sort()
for k in range(len(filepaths)):
    before = divs[k]
    after  = divs[k+1]
    keys = [pair[1] for pair in all_info if before <= pair[0] and
                                            pair[0] < after]

    label = labels[k]
    print label, len(keys)

    if 'Q' in label:
        suffix = 'Quarter %s of %s' % (label[-1], label[:4])
    else:
        suffix = label

    title = 'Cassini Press Releases from ' + suffix
    jekyll_thumbnail_gallery(filepaths[k], title, keys, info_dict,
                             k, labels, links)

# 1997-2003 68
# 2004 Q1 55
# 2004 Q3 229
# 2005 Q1 144
# 2005 Q2 104
# 2005 Q3 138
# 2005 Q4 123
# 2006 Q1 92
# 2006 Q2 94
# 2006 Q3 85
# 2006 Q4 108
# 2007 Q1 97
# 2007 Q2 73
# 2007 Q3 77
# 2007 Q4 109
# 2008 Q1 88
# 2008 Q2 73
# 2008 Q3 83
# 2008 Q4 103
# 2009 Q1 81
# 2009 Q2 85
# 2009 Q3 88
# 2009 Q4 90
# 2010 Q1 98
# 2010 Q2 77
# 2010 Q3 88
# 2010 Q4 45
# 2011 109
# 2012 97
# 2013 114
# 2014 81
# 2015 100
# 2016 76
# 2017 105
# 2018 15

################################################################################
# Cassini by target
################################################################################

info_by_target = {}

for (id, info) in info_dict.items():

    (release_date, title, is_movie, is_color, is_grayscale,
     missions, hosts, host_types, instruments, detectors,
     targets, target_types, systems, extra_keywords, dates,
     local_html_url, local_thumbnail_url,
     local_small_url, local_medium_url) = info

    if missions[0] != 'Cassini-Huygens': continue

    for target in targets:
        if target in info_by_target:
            info_by_target[target].append((release_date, id))
        else:
            info_by_target[target] = [(release_date, id)]

targets = info_by_target.keys()
targets.sort()

for target in targets:
    info_by_target[target].sort()
    print target, len(info_by_target[target])

#  10
# 951 Gaspra 1
# A Ring 366
# Adrastea 2
# Aegaeon 6
# Anthe 7
# Atlas 77
# B Ring 207
# C Ring 112
# Callisto 5
# Calypso 6
# Carina Nebula 1
# Cassini Division 115
# Charon 1
# D Ring 35
# Daphnis 69
# Dione 276
# E Ring 41
# Earth 396
# Enceladus 435
# Encke Gap 162
# Epimetheus 142
# Epsilon Ring 1
# Europa 10
# F Ring 451
# G Ring 35
# Ganymede 11
# Gossamer Ring 2
# HD339457 1
# Helene 20
# Himalia 1
# Hyperion 46
# Iapetus 91
# Io 14
# Janus 180
# Jupiter 103
# Jupiter Rings 4
# Main Ring 1
# Mars 15
# Masursky 1
# Mercury 17
# Methone 6
# Metis 2
# Mimas 291
# Miranda 1
# Moon 27
# Neptune 7
# Neptune Rings 1
# Pallene 8
# Pan 114
# Pandora 148
# Phoebe 32
# Pleiades 2
# Pluto 5
# Polydeuces 5
# Prometheus 223
# Rhea 234
# Saturn 2740
# Saturn Rings 1266
# Sun 1847
# Telesto 16
# Tethys 272
# Titan 618
# Triton 1
# Uranus 6
# Uranus Rings 2
# Venus 14

KEYS = {}
KEYS['Jupiter'] = [
    'Jupiter',
    'Jupiter Rings',
    'Metis',
    'Adrastea',
    'Io',
    'Europa',
    'Ganymede',
    'Callisto',
    'Himalia',
]

KEYS['Saturn'] = [
    'Saturn',
    'Saturn Rings',
    'D Ring',
    'C Ring',
    'B Ring',
    'Cassini Division',
    'Encke Gap',
    'A Ring',
    'F Ring',
    'G Ring',
    'E Ring',
    'Pan',
    'Daphnis',
    'Atlas',
    'Prometheus',
    'Pandora',
    'Epimetheus',
    'Janus',
    'Aegaeon',
    'Mimas',
    'Methone',
    'Anthe',
    'Pallene',
    'Enceladus',
    'Tethys',
    'Telesto',
    'Calypso',
    'Dione',
    'Helene',
    'Polydeuces',
    'Rhea',
    'Titan',
    'Hyperion',
    'Iapetus',
    'Phoebe',
]

for planet in ('Jupiter', 'Saturn'):
  filepaths = []
  labels   = []
  links    = []
  titles   = []
  keylists = []

  for target in KEYS[planet]:
    items = info_by_target[target]
    count = len(items)
    pages = int((count + 199) // 200)

    if target == 'Jupiter Rings':
        target_title = "Jupiter's Ring System"
    elif target == 'Saturn Rings':
        target_title = "Saturn's Ring System"
    elif target == 'Uranus Rings':
        target_title = "the Uranian Ring System"
    elif target == 'Neptune Rings':
        target_title = "Neptune's Ring System"
    elif 'Ring' in target or 'Gap' in target:
        target_title = 'the ' + target
    else:
        target_title = target

    if pages == 0: continue

    if pages == 1:
        link = 'cassini_' + \
               target.lower().replace(' ', '_') + '.html'
        filepath = JEKYLL_ROOT_ + 'galleries/overviews/' + link
        label = target
        title = 'Cassini Press Releases Referring to %s' % target_title
        keys = [item[1] for item in items]

        filepaths.append(filepath)
        labels.append(label)
        links.append(link)
        titles.append(title)
        keylists.append(keys)
        continue

    page_size = int(count / float(pages) + 0.5)

    start = 0
    for page in range(pages):

        if page == 0:
          link = 'cassini_' + target.lower().replace(' ', '_') + '.html'
        else:
          link = 'cassini_' + \
               target.lower().replace(' ', '_') + '_p' + ('%02d' % (page+1)) + \
               '.html'

        filepath = JEKYLL_ROOT_ + 'galleries/overviews/' + link

        if page == 0:
            label = target + ' &nbsp; p.' + str(page+1)
        else:
            label = str(page+1)

        title = 'Cassini Press Releases Referring to %s (p. %d)' % \
                                                        (target_title, page+1)

        stop = min(start + page_size, len(items))
        keys = [item[1] for item in items[start:stop]]
        start = stop
        print target, page+1, len(keys)

        filepaths.append(filepath)
        labels.append(label)
        links.append(link)
        titles.append(title)
        keylists.append(keys)

  for k in range(len(filepaths)):
    jekyll_thumbnail_gallery(filepaths[k], titles[k], keylists[k], info_dict,
                             k, labels, links)

################################################################################
# Voyager by encounter
################################################################################

info_by_target = {}

for (id, info) in info_dict.items():

    (release_date, title, is_movie, is_color, is_grayscale,
     missions, hosts, host_types, instruments, detectors,
     targets, target_types, systems, extra_keywords, dates,
     local_html_url, local_thumbnail_url,
     local_small_url, local_medium_url) = info

    if 'Voyager' not in missions: continue
    if 'Cassini-Huygens' in missions: continue

    for target in targets:
        if target in info_by_target:
            info_by_target[target].append((release_date, id))
        else:
            info_by_target[target] = [(release_date, id)]

targets = info_by_target.keys()
targets.sort()

for target in targets:
    info_by_target[target].sort()
    print target, len(info_by_target[target])

# 1989N2 1
# 67P/Churyumov-Gerasimenko 1
# A Ring 18
# Adrastea 4
# Alpha Ring 3
# Amalthea 2
# Ariel 7
# B Ring 20
# Beta Ring 3
# Bianca 1
# C Ring 10
# Callisto 36
# Cassini Division 15
# Charon 1
# Cressida 1
# D Ring 1
# Delta Ring 1
# Dione 17
# E Ring 1
# Earth 107
# Enceladus 8
# Encke Gap 7
# Epsilon Ring 9
# Eta Ring 5
# Europa 41
# F Ring 16
# Five Ring 4
# Four Ring 1
# G Ring 1
# Gamma Ring 4
# Ganymede 76
# Gossamer Ring 4
# Halo 7
# Iapetus 2
# Io 124
# Juliet 1
# Jupiter 243
# Jupiter Rings 13
# Leverrier Ring 1
# Main Ring 5
# Mars 13
# Mercury 18
# Metis 4
# Mimas 11
# Miranda 14
# Moon 39
# Neptune 85
# Neptune Rings 9
# Nereid 1
# Oberon 4
# Phoebe 3
# Pluto 14
# Portia 1
# Puck 1
# Rhea 11
# Saturn 122
# Saturn Rings 48
# Six Ring 4
# Sun 136
# Tethys 14
# Thebe 1
# Titan 16
# Titania 6
# Triton 38
# Umbriel 3
# Uranus 66
# Uranus Rings 20
# Venus 9

KEYS = {}
KEYS['Jupiter'] = [
    'Jupiter',
    'Jupiter Rings',
    'Metis',
    'Adrastea',
    'Io',
    'Europa',
    'Ganymede',
    'Callisto',
]

KEYS['Saturn'] = [
    'Saturn',
    'Saturn Rings',
    'Atlas',
    'Prometheus',
    'Pandora',
    'Epimetheus',
    'Janus',
    'Aegaeon',
    'Mimas',
    'Methone',
    'Anthe',
    'Pallene',
    'Enceladus',
    'Tethys',
    'Telesto',
    'Calypso',
    'Dione',
    'Helene',
    'Polydeuces',
    'Rhea',
    'Titan',
    'Hyperion',
    'Iapetus',
    'Phoebe',
]

KEYS['Uranus'] = [
    'Uranus',
    'Uranus Rings',
    'Portia',
    'Puck',
    'Miranda',
    'Ariel',
    'Umbriel',
    'Titania',
    'Oberon',
]

KEYS['Neptune'] = [
    'Neptune',
    'Neptune Rings',
    'Thalassa',
    'Triton',
    'Nereid',
]

for planet in ('Jupiter', 'Saturn', 'Uranus', 'Neptune'):
  filepaths = []
  labels   = []
  links    = []
  titles   = []
  keylists = []

  for target in KEYS[planet]:
    if target not in info_by_target: continue

    items = info_by_target[target]
    count = len(items)
    pages = int((count + 199) // 200)

    if target == 'Jupiter Rings':
        target_title = "Jupiter's Ring System"
    elif target == 'Saturn Rings':
        target_title = "Saturn's Ring System"
    elif target == 'Uranus Rings':
        target_title = "the Uranian Ring System"
    elif target == 'Neptune Rings':
        target_title = "Neptune's Ring System"
    elif 'Ring' in target or 'Gap' in target:
        target_title = 'the ' + target
    else:
        target_title = target

    if pages == 0: continue

    if pages == 1:
        link = 'voyager_' + \
               target.lower().replace(' ', '_') + '.html'
        filepath = JEKYLL_ROOT_ + 'galleries/overviews/' + link
        label = target
        title = 'Voyager Press Releases Referring to %s' % target_title
        keys = [item[1] for item in items]

        filepaths.append(filepath)
        labels.append(label)
        links.append(link)
        titles.append(title)
        keylists.append(keys)
        continue

    page_size = int(count / float(pages) + 0.5)

    start = 0
    for page in range(pages):

        if page == 0:
            link = 'voyager_' + \
               target.lower().replace(' ', '_') + '.html'
        else:
            link = 'voyager_' + \
               target.lower().replace(' ', '_') + '_p' + ('%02d' % (page+1)) + \
               '.html'
            
        filepath = JEKYLL_ROOT_ + 'galleries/overviews/' + link

        if page == 0:
            label = target + ' &nbsp; p.' + str(page+1)
        else:
            label = str(page+1)

        title = 'Voyager Press Releases Referring to %s (p. %d)' % \
                                                        (target_title, page+1)

        stop = min(start + page_size, len(items))
        keys = [item[1] for item in items[start:stop]]
        start = stop
        print target, page+1, len(keys)

        filepaths.append(filepath)
        labels.append(label)
        links.append(link)
        titles.append(title)
        keylists.append(keys)

  for k in range(len(filepaths)):
    if planet == 'Jupiter':
        text_lines = 5
    else:
        text_lines = 3
    jekyll_thumbnail_gallery(filepaths[k], titles[k], keylists[k], info_dict,
                             k, labels, links, text_lines)

################################################################################
# New Horizons by date
################################################################################

info_by_year = {}
all_info = []

for (id, info) in info_dict.items():

    (release_date, title, is_movie, is_color, is_grayscale,
     missions, hosts, host_types, instruments, detectors,
     targets, target_types, systems, extra_keywords, dates,
     local_html_url, local_thumbnail_url,
     local_small_url, local_medium_url) = info

    if missions[0] != 'New Horizons': continue
    
    year = release_date[:4]
    if year in info_by_year:
        info_by_year[year].append((release_date, id))
    else:
        info_by_year[year] = [(release_date, id)]

    all_info.append((release_date, id))

years = info_by_year.keys()
years.sort()

for year in years:
    info_by_year[year].sort()
    print year, len(info_by_year[year])

# 2007 56
# 2008 2
# 2010 3
# 2014 1
# 2015 105
# 2016 41
# 2017 19
# 2018 2

divs = ['2007', '2008', '2010', '2014', '2015', '2016',
        '2017', '2018', '2999']

filepaths = []
labels = []
links  = []
for before in divs[:-1]:
    links.append('new_horizon_' + before + '.html')
    filepaths.append(JEKYLL_ROOT_ + 'galleries/overviews/' + links[-1])
    labels.append(before)

links[0] = 'new_horizons.html'
filepaths[0] = JEKYLL_ROOT_ + 'galleries/overviews/' + links[0]

all_info.sort()
for k in range(len(filepaths)):
    before = divs[k]
    after  = divs[k+1]
    keys = [pair[1] for pair in all_info if before <= pair[0] and
                                            pair[0] < after]

    label = labels[k]
    print label, len(keys)

    title = 'New Horizons Press Releases from ' + labels[k]
    jekyll_thumbnail_gallery(filepaths[k], title, keys, info_dict,
                             k, labels, links)

################################################################################
# Galileo by date
################################################################################

info_by_year = {}
all_info = []

for (id, info) in info_dict.items():

    (release_date, title, is_movie, is_color, is_grayscale,
     missions, hosts, host_types, instruments, detectors,
     targets, target_types, systems, extra_keywords, dates,
     local_html_url, local_thumbnail_url,
     local_small_url, local_medium_url) = info

    if missions[0] != 'Galileo': continue
    
    year = release_date[:4]
    if year in info_by_year:
        info_by_year[year].append((release_date, id))
    else:
        info_by_year[year] = [(release_date, id)]

    all_info.append((release_date, id))

years = info_by_year.keys()
years.sort()

for year in years:
    info_by_year[year].sort()
    print year, len(info_by_year[year])

# 1996 56
# 1997 141
# 1998 256
# 1999 50
# 2000 61
# 2001 27
# 2002 16
# 2004 1
# 2005 1
# 2007 1
# 2011 3
# 2013 7
# 2014 6
# 2015 1
# 2016 1
# 2017 3
# 2018 1

divs = ['1996', '1997', '1998', '1999', '2000', '2001', '2999']

filepaths = []
labels = []
links  = []
suffixes = []
for before in divs[:-1]:
    links.append('galileo_' + before + '.html')
    filepaths.append(JEKYLL_ROOT_ + 'galleries/overviews/' + links[-1])
    labels.append(before)
    suffixes.append(before)

labels[-1] = '2001...'
suffixes[-1] = 'after 2000'

links[0] = 'galileo.html'
filepaths[0] = JEKYLL_ROOT_ + 'galleries/overviews/' + links[0]

all_info.sort()
for k in range(len(filepaths)):
    before = divs[k]
    after  = divs[k+1]
    keys = [pair[1] for pair in all_info if before <= pair[0] and
                                            pair[0] < after]

    label = labels[k]
    print label, len(keys)

    title = 'Galileo Press Releases from ' + suffixes[k]

    jekyll_thumbnail_gallery(filepaths[k], title, keys, info_dict,
                             k, labels, links, text_lines=5)

