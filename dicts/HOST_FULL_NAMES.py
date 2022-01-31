################################################################################
# dicts/HOST_FULL_NAMES.py
#
# Usage:
#   from HOST_FULL_NAMES import HOST_FULL_NAMES
#
# HOST_FULL_NAMES is a dictionary that translates the lower-case name or
# abbreviation of an instrument host into its full name.
################################################################################

from .HOST_INFO import HOST_INFO

HOST_FULL_NAMES = {
    '2001 Mars Odyssey'     : 'Mars Odyssey',
    'acrimsat satellite'    : 'Active Cavity Irradiance Monitor Satellite (AcrimSat)',
    'cassini'               : 'Cassini Orbiter',
    'catalina sky survay'   : 'Steward Observatory',
    'curiosity'             : 'Curiosity',
    'dart'                  : 'DART',
    'deep impact  (dixi)'   : 'Deep Impact',
    'deep impact (dixi)'    : 'Deep Impact',
    'deep space 1 (ds1)'    : 'Deep Space 1',
    'huygens lander'        : 'Huygens Probe',
    'huygens'               : 'Huygens Probe',
    'insight'               : 'InSight Lander',
    'kepler spacecraft'     : 'Kepler',
    'mars express (mex)'    : 'Mars Express',
    'mars global surveyor orbiter' : 'Mars Global Surveyor',
    'mars science laboratory (msl)': 'Curiosity',
    'maven'                 : 'MAVEN',
    'neocam'                : 'Near-Earth Object Camera',
    'opportunity'           : 'Opportunity (MER-B)',
    'phoenix lander'        : 'Phoenix Lander',
    'phoenix'               : 'Phoenix Lander',
    'pioneer venus orbiter' : 'Pioneer Venus',
    'rosetta'               : 'Rosetta Orbiter',
    'sdo'                   : 'Solar Dynamics Observatory (SDO)',
    'spirit'                : 'Spirit (MER-A)',
    'spitzer telescope'     : 'Spitzer Space Telescope',
    'stardustnext'          : 'Stardust',
    'viking lander 1'       : 'Viking 1 Lander',
    'viking lander 2'       : 'Viking 2 Lander',
    'viking orbiter 1'      : 'Viking 1 Orbiter',
    'viking orbiter 2'      : 'Viking 2 Orbiter',
    'ztf'                   : 'Zwicky Transient Facility',
    'neowise telescope'     : 'NEOWISE',
    'goldstone antenna'     : 'Goldstone Deep Space Communications Complex (GDSCC)',

    'chandra x-ray observatory' : 'Chandra X-ray Observatory',
    'cxo'                       : 'Chandra X-ray Observatory',
    'juice'                 : 'Jupiter Icy Moons Explorer',
}

HOST_FULL_NAMES.update({k:v[0] for (k,v) in HOST_INFO.items()})

################################################################################
