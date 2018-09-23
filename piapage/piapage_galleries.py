#!/usr/bin/env python
################################################################################

import sys
import os
import piapage
import gallerypage
import galleries

CATALOG = piapage.load_catalog()
FILEROOT = gallerypage.GalleryPage.JEKYLL_ROOT_ + \
           gallerypage.GalleryPage.GALLERIES_SUBDIR_

MARS_TARGETS = [
    'Phobos',
    'Deimos',
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
                          'NASA Planetary Press Releases',
                          merge_limit=200)

################################################################################
# Mars by date and target
################################################################################

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if gallery_page.systems[0] == 'Mars':
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'mars', 'Mars Press Releases',
                          merge_limit=200)

galleries.by_target(filtered, FILEROOT, 'target', 'NASA Press Releases',
                    MARS_TARGETS, page_limit=100)

################################################################################
# Cassini by date and target
################################################################################

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if gallery_page.missions[0] == 'Cassini-Huygens':
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'cassini',
                          'Cassini Press Releases',
                          merge_limit=200)

galleries.by_target(filtered, FILEROOT, 'cassini', 'Cassini Press Releases',
                    JUPITER_TARGETS, page_limit=100)

galleries.by_target(filtered, FILEROOT, 'cassini', 'Cassini Press Releases',
                    SATURN_TARGETS, page_limit=100)

################################################################################
# New Horizons
################################################################################

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if gallery_page.missions[0] == 'New Horizons':
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'new_horizons',
                          'New Horizons Press Releases',
                          merge_limit=80)

################################################################################
# Galileo
################################################################################

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if gallery_page.missions[0] == 'Galileo':
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'galileo',
                          'Galileo Press Releases',
                          merge_limit=100)

################################################################################
# Dawn
################################################################################

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if gallery_page.missions[0] == 'Dawn':
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'dawn',
                          'Dawn Press Releases',
                          merge_limit=100)

################################################################################
# MESSENGER
################################################################################

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if gallery_page.missions[0] == 'MESSENGER':
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'messenger',
                          'MESSENGER Press Releases',
                          merge_limit=200)

################################################################################
# Juno
################################################################################

filtered = {}
for (key, gallery_page) in CATALOG.iteritems():
    if gallery_page.missions[0] == 'Juno':
        filtered[key] = gallery_page

galleries.by_release_date(filtered, FILEROOT, 'juno',
                          'Juno Press Releases',
                          merge_limit=100)

################################################################################
# Voyager
################################################################################

for targets in [JUPITER_TARGETS, SATURN_TARGETS,
                URANUS_TARGETS, NEPTUNE_TARGETS]:

    filtered = {}
    system = targets[0]

    for (key, gallery_page) in CATALOG.iteritems():
        if gallery_page.missions[0] != 'Voyager': continue
        if gallery_page.systems[0] != system: continue

        filtered[key] = gallery_page

    galleries.by_target(filtered, FILEROOT, 'voyager',
                              'Voyager/%s Press Releases' % system,
                              targets, page_limit=200)

################################################################################
# By planet and target
################################################################################

galleries.by_target(CATALOG, FILEROOT, 'target', 'NASA Press Releases',
                    JUPITER_TARGETS, page_limit=100)

galleries.by_target(CATALOG, FILEROOT, 'target', 'NASA Press Releases',
                    SATURN_TARGETS, page_limit=100)

galleries.by_target(CATALOG, FILEROOT, 'target', 'NASA Press Releases',
                    URANUS_TARGETS, page_limit=100)

galleries.by_target(CATALOG, FILEROOT, 'target', 'NASA Press Releases',
                    NEPTUNE_TARGETS, page_limit=100)

galleries.by_target(CATALOG, FILEROOT, 'target', 'NASA Press Releases',
                    PLUTO_TARGETS, page_limit=100)

################################################################################
################################################################################
