################################################################################
# dicts/INSTRUMENT_FROM_DETECTOR.py
#
# Usage:
#   from INSTRUMENT_FROM_DETECTOR import INSTRUMENT_FROM_DETECTOR
#
# INSTRUMENT_FROM_DETECTOR is a dictionary that translates the lower-case name
# or abbreviation of a detector into the full name of the associated instrument.
# In cases where the detector name has been re-used, multiple instrument names
# are returned in a list.
################################################################################

INSTRUMENT_FROM_DETECTOR = {
    'hrc'                   : 'Advanced Camera for Surveys (ACS)',
    'sbn'                   : 'Advanced Camera for Surveys (ACS)',
    'wfc'                   : 'Advanced Camera for Surveys (ACS)',
    'uvis'                  : 'Wide Field Camera 3 (WFC3)',
    'ir'                    : 'Wide Field Camera 3 (WFC3)',
    'optical microscope'    : 'Microscopy, Electrochemistry, and Conductivity Analyzer (MECA)',
    'wide angle camera'     : ['Imaging Science Subsystem (ISS)',
                               'Mercury Dual Imaging System (MDIS)'],
    'narrow angle camera'   : ['Imaging Science Subsystem (ISS)',
                               'Mercury Dual Imaging System (MDIS)'],
}

################################################################################
