################################################################################
# dicts/__init__.py
#
# This is a collection of data structures that are used to standardize keywords
# for targets, instruments, missions, etc., and to define associations between
# keywords. Note that these must be actively maintained and updated as we create
# galleries for new data sets.
#
# Usage:
#   from dicts import *
#
# These dictionaries translate an abbreviation or short name to a full name
#   DETECTOR_FULL_NAMES
#   INSTRUMENT_FULL_NAMES
#   HOST_FULL_NAMES
#   MISSION_FULL_NAMES
#   TARGET_FULL_NAMES
#
# These dictionaries translate one keyword to the name of an associated keyword
#   HOST_FROM_INSTRUMENT
#   INSTRUMENT_FROM_DETECTOR
#   SYSTEM_FROM_TARGET
#
# HOST_INFO returns (full host name, full mission name, host type) for a host
# name or abbreviation.
################################################################################

from DETECTOR_FULL_NAMES        import DETECTOR_FULL_NAMES
from HOST_FROM_INSTRUMENT       import HOST_FROM_INSTRUMENT
from HOST_FULL_NAMES            import HOST_FULL_NAMES
from HOST_INFO                  import HOST_INFO
from INSTRUMENT_FROM_DETECTOR   import INSTRUMENT_FROM_DETECTOR
from INSTRUMENT_FULL_NAMES      import INSTRUMENT_FULL_NAMES
from MISSION_FULL_NAMES         import MISSION_FULL_NAMES
from SYSTEM_FROM_TARGET         import SYSTEM_FROM_TARGET
from TARGET_FULL_NAMES          import TARGET_FULL_NAMES

from KEYWORDS                   import KEYWORDS

################################################################################
