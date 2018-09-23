################################################################################
# dicts/MISSION_FROM_HOST.py
#
# Usage:
#   from MISSION_FROM_HOST import MISSION_FROM_HOST
#
# MISSION_FROM_HOST is a dictionary that translates the lower-case name or
# abbreviation of a mission into a tuple containing the full name of the
# associated instrument host and the instrument host type (e.g., "Orbiter" or
# "Probe").
################################################################################

MISSION_FROM_HOST = {
    'arecibo observatory'               : ('Arecibo Observatory', 'Ground-Based Observatory'),
    'cassini orbiter'                   : ('Cassini-Huygens', 'Orbiter'),
    'clementine 1'                      : ('LCROSS', 'Orbiter'),
    'curiosity rover'                   : ('Mars Science Laboratory (MSL)', 'Rover'),
    'galileo orbiter'                   : ('Galileo', 'Orbiter'),
    'galileo probe'                     : ('Galileo', 'Probe'),
    'gemini north telescope'            : ('Gemini North Telescope', 'Ground-Based Telescope'),
    'hubble space telescope (hst)'      : ('Hubble Space Telescope (HST)', 'Orbiting Telescope'),
    'huygens probe'                     : ('Cassini-Huygens', 'Probe'),
    'infrared telescope facility (irtf)': ('Infrared Telescope Facility (IRTF)', 'Ground-Based Telescope'),
    'keck 1 telescope'                  : ('W. M. Keck Observatory', 'Ground-Based Telescope'),
    'keck 2 telescope'                  : ('W. M. Keck Observatory', 'Ground-Based Telescope'),
    'kepler'                            : ('Kepler', 'Orbiting Telescope'),
    'mariner 1'                         : ('Mariner', 'Flyby Spacecraft'),
    'mariner 10'                        : ('Mariner', 'Flyby Spacecraft'),
    'mariner 2'                         : ('Mariner', 'Flyby Spacecraft'),
    'mariner 3'                         : ('Mariner', 'Flyby Spacecraft'),
    'mariner 4'                         : ('Mariner', 'Flyby Spacecraft'),
    'mariner 5'                         : ('Mariner', 'Flyby Spacecraft'),
    'mariner 6'                         : ('Mariner', 'Flyby Spacecraft'),
    'mariner 7'                         : ('Mariner', 'Flyby Spacecraft'),
    'mariner 8'                         : ('Mariner', 'Flyby Spacecraft'),
    'mariner 9'                         : ('Mariner', 'Flyby Spacecraft'),
    'mars global surveyor (mgs)'        : ('Mars Global Surveyor (MGS)', 'Orbiter'),
    'mars helicopter'                   : ('Mars 2020 Rover', 'Flier'),
    'mars pathfinder lander'            : ('Mars Pathfinder (MPF)', 'Lander'),
    'mars pathfinder rover'             : ('Mars Pathfinder (MPF)', 'Rover'),
    'mars volcanic emission life scout (marvel)'
                                        : ('Mars Scout', 'Orbiter'),
    'opportunity (mer-b)'               : ('Mars Exploration Rover (MER)', 'Rover'),
    'philae lander'                     : ('Rosetta', 'Lander'),
    'phoenix mars lander'               : ('Phoenix', 'Lander'),
    'pioneer 10'                        : ('Pioneer', 'Flyby Spacecraft'),
    'pioneer 11'                        : ('Pioneer', 'Flyby Spacecraft'),
    'pioneer 6'                         : ('Pioneer', 'Flyby Spacecraft'),
    'pioneer 7'                         : ('Pioneer', 'Flyby Spacecraft'),
    'pioneer 8'                         : ('Pioneer', 'Flyby Spacecraft'),
    'pioneer 9'                         : ('Pioneer', 'Flyby Spacecraft'),
    'rosetta orbiter'                   : ('Rosetta', 'Orbiter'),
    'siding spring observatory (sdo)'   : ('Siding Spring Observatory (SDO)', 'Ground-Based Telescope'),
    'spirit (mer-a)'                    : ('Mars Exploration Rover (MER)', 'Rover'),
    'subaru telescope'                  : ('Subaru Telescope', 'Ground-Based Telescope'),
    'surveyor 1'                        : ('Surveyor', 'Lander'),
    'surveyor 2'                        : ('Surveyor', 'Lander'),
    'surveyor 3'                        : ('Surveyor', 'Lander'),
    'surveyor 4'                        : ('Surveyor', 'Lander'),
    'surveyor 5'                        : ('Surveyor', 'Lander'),
    'surveyor 6'                        : ('Surveyor', 'Lander'),
    'surveyor 7'                        : ('Surveyor', 'Lander'),
    'viking 1 lander'                   : ('Viking', 'Lander'),
    'viking 1 orbiter'                  : ('Viking', 'Orbiter'),
    'viking 2 lander'                   : ('Viking', 'Lander'),
    'viking 2 orbiter'                  : ('Viking', 'Orbiter'),
    'viking lander'                     : ('Viking', 'Lander'),
    'viking orbiter'                    : ('Viking', 'Orbiter'),
    'voyager 1'                         : ('Voyager', 'Flyby Spacecraft'),
    'voyager 2'                         : ('Voyager', 'Flyby Spacecraft'),
    'w. m. keck observatory'            : ('W. M. Keck Observatory', 'Ground-Based Telescope'),
    'xombie'                            : ('Mars 2020 Rover', 'Rover'),
}

################################################################################
