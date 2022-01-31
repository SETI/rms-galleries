#!/usr/bin/env python2
################################################################################

import sys
import os
import piapage
import galleries
from gallerypage import GalleryPage

CATALOG = piapage.load_catalog()
FILEROOT = GalleryPage.JEKYLL_ROOT_ + GalleryPage.GALLERIES_SUBDIR_
DEBUG = False

MARS_TARGETS = [
    'Phobos',
    'Deimos',
    'Mars',
]

JUPITER_TARGETS = [
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

SATURN_TARGETS = [
    'Saturn',
    'Saturn Rings',
    'D Ring',
    'C Ring',
    'B Ring',
    'Cassini Division',
    'A Ring',
    'Encke Gap',
    'Pan',
    'Daphnis',
    'Atlas',
    'Prometheus',
    'F Ring',
    'Pandora',
    'Epimetheus',
    'Janus',
    'G Ring',
    'Aegaeon',
    'Mimas',
    'Methone',
    'Anthe',
    'Pallene',
    'E Ring',
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

URANUS_TARGETS = [
    'Uranus',
    'Uranus Rings',
    'Bianca',
    'Cressida',
    'Juliet',
    'Portia',
    'Puck',
    'Miranda',
    'Ariel',
    'Umbriel',
    'Titania',
    'Oberon',
]

NEPTUNE_TARGETS = [
    'Neptune',
    'Neptune Rings',
    'Thalassa',
    'Proteus',
    'Triton',
    'Nereid',
]

PLUTO_TARGETS = [
    'Pluto',
    'Charon',
    'Styx',
    'Nix',
    'Kerberos',
    'Hydra',
]

################################################################################
# Everything
################################################################################

galleries.by_release_date(CATALOG, FILEROOT, 'all',
                          'NASA Planetary Press Releases')

################################################################################
# System by date
################################################################################

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Mercury' in gallery_page.targets or 'Mercury' in gallery_page.systems:
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'mercury',
                          'NASA Press Releases referencing Mercury')

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Venus' in gallery_page.targets or 'Venus' in gallery_page.systems:
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'venus',
                          'NASA Press Releases referencing Venus')

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Moon' in gallery_page.targets:
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'moon',
                          'NASA Press Releases about the Moon')

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Mars' in gallery_page.targets or 'Mars' in gallery_page.systems:
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'mars',
                          'NASA Press Releases about Mars')

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Jupiter' in gallery_page.targets or 'Jupiter' in gallery_page.systems:
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'jupiter',
                          'NASA Press Releases about the Jupiter System')

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Saturn' in gallery_page.targets or 'Saturn' in gallery_page.systems:
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'saturn',
                          'NASA Press Releases about the Saturn System')

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Uranus' in gallery_page.targets or 'Uranus' in gallery_page.systems:
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'uranus',
                          'NASA Press Releases about the Uranus System')

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Neptune' in gallery_page.targets or 'Neptune' in gallery_page.systems:
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'neptune',
                          'NASA Press Releases about the Neptune System')

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Pluto' in gallery_page.targets or 'Pluto' in gallery_page.systems:
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'pluto',
                          'NASA Press Releases about the Pluto System')

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if ('KBO' in gallery_page.target_types or
        'Kuiper Belt' in gallery_page.systems):
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'kbos',
                          'NASA Press Releases about the Kuiper Belt')

################################################################################
# Target types by date
################################################################################

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Asteroid' in gallery_page.target_types:
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'asteroids',
                          'NASA Press Releases about Asteroids')

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Comet' in gallery_page.target_types:
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'comets',
                          'NASA Press Releases about Comets')

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Exoplanet' in gallery_page.target_types:
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'exoplanets',
                          'NASA Press Releases about Exoplanetary Systems')

################################################################################
# Mission by date
################################################################################

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Cassini-Huygens' in gallery_page.missions:
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'cassini',
                          'Cassini Press Releases')

galleries.by_target(filtered, FILEROOT, 'cassini', 'Cassini Press Releases',
                    JUPITER_TARGETS, page_limit=100)

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'New Horizons' in gallery_page.missions:
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'new_horizons',
                          'New Horizons Press Releases')

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Juno' in gallery_page.missions:
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'juno',
                          'Juno Press Releases')

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Galileo' in gallery_page.missions:
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'galileo',
                          'Galileo Press Releases')

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Dawn' in gallery_page.missions:
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'dawn',
                          'Dawn Press Releases')

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'MESSENGER' in gallery_page.missions:
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'messenger',
                          'MESSENGER Press Releases')

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Voyager' in gallery_page.missions:
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'voyager',
                          'Voyager Press Releases')

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Rosetta' in gallery_page.missions:
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'rosetta',
                          'Rosetta Press Releases')

################################################################################
# Mission by system and date
################################################################################

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Cassini-Huygens' in gallery_page.missions and \
        ('Jupiter' in gallery_page.targets or 'Jupiter' in gallery_page.systems):
            filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'cassini_jupiter',
                          'Press Releases for the Cassini Jupiter Flyby')

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Cassini-Huygens' in gallery_page.missions and \
        ('Saturn' in gallery_page.targets or 'Saturn' in gallery_page.systems):
            filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'cassini_saturn',
                          'Press Releases for Cassini at Saturn')

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Voyager' in gallery_page.missions and \
        ('Jupiter' in gallery_page.targets or 'Jupiter' in gallery_page.systems):
            filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'voyager_jupiter',
                          'Press Releases for the Voyager Jupiter Flyby')

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Voyager' in gallery_page.missions and \
        ('Saturn' in gallery_page.targets or 'Saturn' in gallery_page.systems):
            filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'voyager_saturn',
                          'Press Releases For the Voyager Saturn Flyby')

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Voyager' in gallery_page.missions and \
        ('Uranus' in gallery_page.targets or 'Uranus' in gallery_page.systems):
            filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'voyager_uranus',
                          'Press Releases For the Voyager Uranus Flyby')

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Voyager' in gallery_page.missions and \
        ('Neptune' in gallery_page.targets or 'Neptune' in gallery_page.systems):
            filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'voyager_neptune',
                          'Press Releases For the Voyager Neptune Flyby')

################################################################################
# By system and target
################################################################################

galleries.by_target(CATALOG, FILEROOT, 'target', 'Mars System Press Releases',
                    MARS_TARGETS)

galleries.by_target(CATALOG, FILEROOT, 'target', 'Jupiter System Press Releases',
                    JUPITER_TARGETS)

galleries.by_target(CATALOG, FILEROOT, 'target', 'Saturn System Press Releases',
                    SATURN_TARGETS)

galleries.by_target(CATALOG, FILEROOT, 'target', 'Uranus System Press Releases',
                    URANUS_TARGETS)

galleries.by_target(CATALOG, FILEROOT, 'target', 'Neptune System Press Releases',
                    NEPTUNE_TARGETS)

galleries.by_target(CATALOG, FILEROOT, 'target', 'Pluto System Press Releases',
                    PLUTO_TARGETS)

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Asteroid' in gallery_page.target_types:
        filtered[key] = gallery_page

targets = set()
skipped = set()
for page in filtered.values():
    for target in page.targets:
        target_types = GalleryPage.target_types_from_target(target)
        if 'Asteroid' in target_types and 'KBO' not in target_types:
            targets.add(target)

def asteroid_sort(key):

    if key[0] == '(':
        key = key[1:].replace(')','')

    parts = key.partition(' ')
    try:
        intval = int(parts[0])
    except ValueError:
        if key == 'Pluto':
            return (-200, 'Pluto')
        if key == 'Charon':
            return (-100, 'Charon')
        return (1000000000, key.lower())    # names after numbers

    if intval >= 1990 and intval < 2030:    # years last
        intval += 1000000000

    return (intval, parts[2].lower())

targets = list(targets)
targets.sort(key=asteroid_sort)
galleries.by_target(filtered, FILEROOT, 'asteroid', 'Asteroid Press Releases',
                    targets)

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Comet' in gallery_page.target_types:
        filtered[key] = gallery_page

targets = set()
skipped = set()
for page in filtered.values():
    for target in page.targets:
        if 'Comet' in GalleryPage.target_types_from_target(target):
            targets.add(target)
        else:
            skipped.add(target)

def comet_sort(key):
    if key[1] == '/':
        return (88888, key[0], key[2:].lower())

    parts = key.rpartition('/')
    if parts[0]:
        return (int(parts[0][:-1]), parts[0][-1], parts[2])

    return (99999, key.lower())

targets = list(targets)
targets.sort(key=comet_sort)
galleries.by_target(filtered, FILEROOT, 'comet', 'Comet Press Releases',
                    targets)

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if ('KBO' in gallery_page.target_types or
        'Kuiper Belt' in gallery_page.systems):
        filtered[key] = gallery_page

targets = set()
skipped = set()
for page in filtered.values():
    for target in page.targets:
        target_types = GalleryPage.target_types_from_target(target)
        if 'Kuiper Belt' in GalleryPage.systems_from_target(target):
            targets.add(target)
        elif 'KBO' in target_types and 'Asteroid' not in target_types:
                targets.add(target)
        else:
            skipped.add(target)

targets = list(targets)
targets.sort(key=asteroid_sort)
targets.remove('2003 UB313')    # alt name for Eris
galleries.by_target(filtered, FILEROOT, 'kbo', 'KBO Press Releases',
                    targets)

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if 'Exoplanet' in gallery_page.target_types:
        filtered[key] = gallery_page

targets = set()
skipped = set()
for page in filtered.values():
    for target in page.targets:
        if 'Exoplanet' in GalleryPage.target_types_from_target(target):
            targets.add(target)
        else:
            skipped.add(target)

def exoplanet_sort(key):

    # replace dashes and dots with spaces
    key = key.replace('-',' ').replace('.',' ')

    # split into ints and strings
    new_keys = []
    item = None
    for c in key:
        if c == ' ':
            if item is not None:
                new_keys.append(item)
            item = None
        elif c.isdigit():
            if item is None:
                item = int(c)
            elif isinstance(item,int):
                item = item * 10 + int(c)
            else:
                new_keys.append(item)
                item = int(c)
        else:
            c = c.lower()
            if item is None:
                item = c
            elif isinstance(item,int):
                new_keys.append(item)
                item = c
            else:
                item += c

    if item is not None:
        new_keys.append(item)

    return tuple(new_keys)

targets = list(targets)
targets.sort(key=exoplanet_sort)
galleries.by_target(filtered, FILEROOT, 'exoplanet', 'Exoplanet Press Releases',
                    targets)

################################################################################
# Debugging
################################################################################

if DEBUG:
    filtered = {}
    for (key, gallery_page) in CATALOG.iteritems():
        if gallery_page.is_planetary and gallery_page.targets[0] == '':
            filtered[key] = gallery_page

    galleries.by_release_date(filtered, FILEROOT, 'no_targets',
                              'No Primary Target')

    filtered = {}
    for (key, gallery_page) in CATALOG.iteritems():
        if gallery_page.is_planetary and gallery_page.target_types[0] == '':
            filtered[key] = gallery_page

    galleries.by_release_date(filtered, FILEROOT, 'no_target_types',
                              'No Primary Target Type')

    filtered = {}
    for (key, gallery_page) in CATALOG.iteritems():
        if gallery_page.is_planetary and gallery_page.systems[0] == '':
            filtered[key] = gallery_page

    galleries.by_release_date(filtered, FILEROOT, 'no_systems',
                              'No Primary System')

    filtered = {}
    for (key, gallery_page) in CATALOG.iteritems():
        if gallery_page.is_planetary and gallery_page.missions[0] == '':
            filtered[key] = gallery_page

    galleries.by_release_date(filtered, FILEROOT, 'no_missions',
                              'No Primary Mission')

    filtered = {}
    for (key, gallery_page) in CATALOG.iteritems():
        if gallery_page.is_planetary and gallery_page.hosts[0] == '':
            filtered[key] = gallery_page

    galleries.by_release_date(filtered, FILEROOT, 'no_hosts',
                              'No Primary Host')

    filtered = {}
    for (key, gallery_page) in CATALOG.iteritems():
        if gallery_page.is_planetary and gallery_page.host_types[0] == '':
            filtered[key] = gallery_page

    galleries.by_release_date(filtered, FILEROOT, 'no_host_types',
                              'No Primary Host Type')

################################################################################
