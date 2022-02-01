########################################################################################################################
# dicts/KEYWORDS.py
#
# To use:
#   from KEYWORDS import KEYWORDS
#
# Dictionary structure used for scraping keywords from captions. Each dictionary value is a list of tuples
#   (regular expression, [keywords])
# where the list of keywords can contain grep string replacement patterns. If the regular expression matches any text
# found in the caption, then the keywords provided are added to the list.
#
# Keywords can have suffixes indicating the type of the keyword:
#   +t = Target
#   +T = Target Type
#   +s = System
#   +m = Mission
#   +h = Host
#   +H = Host Type
#   +i = Instrumen
#   +d = Detector
#   +X = trigger new rules but don't create a new keyword
#
# KEYWORDS is actually a dictionary keyed by a category. KEYWORDS['General'] is the list of keywords always searched.
# Additional keys are used if and only if the key of that dictionary is also found as a keyword. For example, if
# 'Saturn' is found among the keywords, then KEYWORDS['Saturn'] is also checked for matching text in the caption.
#
# This dictionary will need to be updated as new data sets are added to the gallery.
########################################################################################################################

KEYWORDS = {}

KEYWORDS['General'] = [

# Target categories
    ('(?<!omets and )[Aa]steroids?(?!s? and comet)',    ['Asteroid+X']),    # does not create a new target type, just triggers new rules
    ('(?<!roids and )[Cc]omets?(?!s? and aster)',       ['Comet+X']),       # ditto

    ('Moon(?!s)',                       ['Moon+X']),    # needs confirmation
    ('Lunar(?! and Plan)',              ['Moon+X']),
    ('[Oo]ur moon',                     ['Moon+X']),

    ('KBO',                             ['KBO+T', 'Kuiper Belt+s']),
    ('Kuiper Belt',                     ['KBO+T', 'Kuiper Belt+s']),
    ('(Trans-Neptunian|TNO|TNOs)',      ['KBO+T', 'Kuiper Belt+s']),

# Target names
    ('(Mercury|Mercurian)',             ['Mercury+t', 'Planet+T']),
    ('Venus',                           ['Venus+t', 'Planet+T']),
    ('(Mars(?![a-z])|Martian)',         ['Mars+t', 'Planet+T']),

    ("Jupiter(?!'s)",                   ['Jupiter+t', 'Planet+T']),
    ("Jupiter's",                       ['Jupiter+s']),
    ('[Jj]ovian',                       ['Jupiter+s']),
    ('Galilean',                        ['Jupiter+s', 'Satellite+T']),
    ('Io(?![a-z])',                     ['Jupiter+s', 'Satellite+T', 'Io+t'      ]),
    ('Europa',                          ['Jupiter+s', 'Satellite+T', 'Europa+t'  ]),
    ('Ganymede',                        ['Jupiter+s', 'Satellite+T', 'Ganymede+t']),
    ('Callisto',                        ['Jupiter+s', 'Satellite+T', 'Callisto+t']),
    ("Saturn(?!ian)(?!'s)",             ['Saturn+t', 'Planet+T']),
    ("[Ss]aturn(ian|'s)",               ['Saturn+s']),
    ('Kronian',                         ['Saturn+s']),
    ('Titan(?! [IV])(?!/Cen)(?!ia)',    ['Saturn+s', 'Satellite+T', 'Titan+t'    ]),
    ('Enceladus',                       ['Saturn+s', 'Satellite+T', 'Enceladus+t']),
    ("Uranus(?!')",                     ['Uranus+t', 'Planet+T']),
    ("Uran(ian|us')",                   ['Uranus+s']),
    ("Neptune(?!'s)",                   ['Neptune+t', 'Planet+T']),
    ("(Neptune's|Neptunian)",           ['Neptune+s']),
    ('Triton',                          ['Neptune+s', 'Satellite+T', 'Triton+t']),
    ('(Pluto(?!n)|Plutonian|Charon)',   ['Pluto+t+s', 'Dwarf Planet+T', 'Kuiper Belt+s', 'KBO+T']),

    ('Ceres[^a-z]',                     ['Dwarf Planet+T', 'Asteroid+T', 'Main Belt+s', '1 Ceres+t']),
    ('Vesta[^a-z]',                     ['Asteroid+T', 'Main Belt+s', '4 Vesta+t'   ]),
    ('Gaspra',                          ['Asteroid+T', 'Main Belt+s', '951 Gaspra+t']),
    ('Lutetia',                         ['Asteroid+T', 'Main Belt+s', '21 Lutetia+t']),
    ('1719 Jens',                       ['Asteroid+T', 'Main Belt+s', '1719 Jens+t' ]),
    ('Klotho[^a-z]',                    ['Asteroid+T', 'Main Belt+s', '97 Klotho+t' ]),
    ('Lina[^a-z]',                      ['Asteroid+T', 'Main Belt+s', '468 Lina+t'  ]),
    ('Psyche[^a-z]',                    ['Asteroid+T', 'Main Belt+s', '16 Psyche+t', 'Psyche+m+h']),

    ('Haumea',                          ['136108 Haumea+t',   'KBO+T', 'Kuiper Belt+s', 'Dwarf Planet+T']),
    ('Makemake',                        ['136472 Makemake+t', 'KBO+T', 'Kuiper Belt+s', 'Dwarf Planet+T']),
    ('Eris|2003 UB313',                 ['136199 Eris+t',     'KBO+T', 'Kuiper Belt+s', 'Dwarf Planet+T']),
    ('Quaoar',                          ['50000 Quaoar+t',    'KBO+T', 'Kuiper Belt+s', 'Dwarf Planet+T']),
    ('(MU69|Ultima Thule)',             ['486958 Arrokoth+t', 'KBO+T', 'Kuiper Belt+s', 'New Horizons+m+h']),
    ('(486958|Arrokoth)',               ['486958 Arrokoth+t', 'KBO+T', 'Kuiper Belt+s', 'New Horizons+m+h']),

    ('(?<!Edmond )Halley(?! [Cc]rater)',['Comet+T', 'Periodic Comets+s', '1P/Halley+t'                ]),
    ('Borrelly',                        ['Comet+T', 'Periodic Comets+s', '19P/Borrelly+t'             ]),
    ('Wild 2',                          ['Comet+T', 'Periodic Comets+s', '81P/Wild+t'                 ]),
    ('Churn?yu?mov.Gerasimer?nko',      ['Comet+T', 'Periodic Comets+s', '67P/Churyumov-Gerasimenko+t']),   # matches known mis-spellings
    ('Giacobini.Zinner',                ['Comet+T', 'Periodic Comets+s', '21P/Giacobini-Zinner+t'     ]),
    ('Grigg.Skjellerup',                ['Comet+T', 'Periodic Comets+s', '26P/Grigg-Skjellerup+t'     ]),
    ('81P/Wild',                        ['Comet+T', 'Periodic Comets+s', '81P/Wild+t'                 ]),
    ('Tempel 1',                        ['Comet+T', 'Periodic Comets+s', '9P/Tempel+t'                ]),
    ('Hartley 2',                       ['Comet+T', 'Periodic Comets+s', '103P/Hartley+t'             ]),
    ('Schwassmann.Wachmann',            ['Comet+T', 'Periodic Comets+s']),
    ('Hale.Bopp',                       ['Comet+T', 'C/1995 O1 (Hale-Bopp)+t']),
    ('Shoemaker.Levy.9',                ['Comet+T', 'Shoemaker-Levy 9+t', 'Jupiter+t', 'Planet+T']),
    ('S.?L.?9',                         ['Comet+T', 'Shoemaker-Levy 9+t', 'Jupiter+t', 'Planet+T']),

    ('Exo-(Mercury|Venus|Earth|Mars|Jupiter|Saturn|Uranus|Neptune|Pluto)', ['Exoplanet+T']),
    ('[Dd]ebris dis[ck]s?[^a-z]',               ['Exoplanet+T']),
    ('([Rr]ing|[Dd]isk|[Dd]isc)s? of debris',   ['Exoplanet+T']),
    ('([Ee]xoplanet|[Ee]xtrasolar planet)',     ['Exoplanet+T']),
    ('[Pp]lanet-forming dis[ck]s?[^a-z]',       ['Exoplanet+T']),
    ('[Pp]lanet-forming material',              ['Exoplanet+T']),
    ('[Rr]ings? of.{0,20} debris',              ['Exoplanet+T']),
    ('hot.Jupiter',                             ['Exoplanet+T']),
    ('[Hh]ot gas giant',                        ['Exoplanet+T']),
    ('[Pp]rotoplanetary dis[ck]s?[^a-z]',       ['Exoplanet+T']),
#     ('planetary dis[ck]s?[^a-z]',           ['Exoplanet+X']),       # careful not to match "planet's disk"
    ('Jupiters[^a-z]',                          ['Exoplanet+T']),
#     ('Neptunes[^a-z]',                      ['Exoplanet+X']),
#     ('brown dwarf',                         ['Exoplanet+X']),
#     ('[Ss]tellar [Dd]isdis[ck]s?[^a-z]',    ['Exoplanet+X']),
    ('55 Cancri',                           ['Exoplanet+T', '55 Cancri+t+s'         ]),
    ('61 Vir',                              ['Exoplanet+T', '61 Vir+t+s'            ]),
    ('(CoKu Tau 4)',                        ['Exoplanet+T', r'\1+t+s'               ]),
    ('Epsilon Eridani',                     ['Exoplanet+T', 'Epsilon Eridani+t+s'   ]),
    ('EX Lupi',                             ['Exoplanet+T', 'EX Lupi+t+s'           ]),
    ('Fomalhaut',                           ['Exoplanet+T', 'Fomalhaut+t+s'         ]),
    ('G29-38',                              ['Exoplanet+T', 'G29-38+t+s'            ]),
    ('GJ 436',                              ['Exoplanet+T', 'GJ 436+t+s'            ]),
    ('HAT-P.11',                            ['Exoplanet+T', 'HAT-P-11+t+s'          ]),
    ('HD (69830|80606|95086|98800)',        ['Exoplanet+T', r'HD \1+t+s'            ]),
    ('HD (113766|149026|157728|172555)',    ['Exoplanet+T', r'HD \1+t+s'            ]),
    ('HD (188553|188753|189733)',           ['Exoplanet+T', r'HD \1+t+s'            ]),
    ('HD (209458|219134)',                  ['Exoplanet+T', r'HD \1+t+s'            ]),
    ('HIP (79124|116454)',                  ['Exoplanet+T', r'HIP \1+t+s'           ]),
    ('HR ?(8799)',                          ['Exoplanet+T', r'HR \1+t+s'            ]),
    ('(IC 1396)',                           ['Exoplanet+T', r'\1+t+s'               ]),
    ('K2.(\d+)',                            ['Exoplanet+T', r'K2-\1+t+s'            ]),
    ('KELT.9',                              ['Exoplanet+T', 'KELT-9+t+s'            ]),
    ('Kepler.(\d+)',                        ['Exoplanet+T', r'Kepler-\1+t+s'        ]),
    ('KIC (\d+)',                           ['Exoplanet+T', r'KIC \1+t+s'           ]),
    ('KOI.?961',                            ['Exoplanet+T', r'Kepler-42+t+s'        ]),     # renamed
    ('(LHS 3844)',                          ['Exoplanet+T', r'\1+t+s'               ]),
    ('(L1157)',                             ['Exoplanet+T', r'\1+t+s'               ]),
    ('M(inkowski )?2-9',                    ['Exoplanet+T', 'Minkowski 2-9+t+s'     ]),
    ('(OTS 44)',                            ['Exoplanet+T', r'\1+t+s'               ]),
    ('(Pr02\d\d) ?[a-z]',                   ['Exoplanet+T', r'\1+t+s'               ]),
    ('TOI.700',                             ['Exoplanet+T', r'TOI 700+t+s'          ]),
    ('TRAPPIST.1',                          ['Exoplanet+T', 'TRAPPIST-1+t+s'        ]),
    ('TW Hydrae',                           ['Exoplanet+T', 'TW Hydrae+t+s'         ]),
    ('UCF-1.01',                            ['Exoplanet+T', 'UCF-1.01+t+s'          ]),
    ('[uU]psilon Andromedae',               ['Exoplanet+T', 'Upsilon Andromedae+t+s']),
    ('UX Tau A',                            ['Exoplanet+T', 'UX Tau A+t+s'          ]),
    ('[^A-Za-z](VB 10)',                    ['Exoplanet+T', r'\1+t+s'               ]),
    ('WASP-12',                             ['Exoplanet+T', 'WASP-12+t+s'           ]),

    ('[Hh]eliosphere',                      ['Heliosphere+t+T', 'Solar System+s']),

# Missions and Instruments
    ('(HST|Hubble.*[Tt]elescope)',          ['Hubble Space Telescope (HST)+m', 'Hubble Space Telescope+h', 'Space Telescope+H']),
    ('(JWST|Webb.*[Tt]elescope)',           ['James Webb Space Telscope (JWST)+m+h', 'Space Telescope+H']),
    ('(Voyager|Mariner)',                   [r'\1+m', 'Flyby Spacecraft+H']),
    ('Pioneer(?! Venus).{1,20}(mission|spacecraft)', ['Pioneer+m']),
    ('(Voyager|Mariner|Pioneer) ([1-9]\d)', [r'\1 \2+h', r'\1+m']),
    ('Cassini(?! [Dd]ivision)',             ['Cassini-Huygens+m']),
    ('(Saturn|Cassini).*Huygens',           ['Cassini-Huygens+m']),
    ('New Horizons',                        ['New Horizons+m+h', 'Flyby Spacecraft+H']),
    ('Juno',                                ['Juno+m+h', 'Orbiter+H']),

    ('(MGS|MRO|MEX|MOC|MSL|MER|MAVEN)',     ['Mars+t', 'Planet+T']),
    ('Perseverance',                        ['Mars+t', 'Planet+T', 'Mars 2020+m', 'Perseverance+h', 'Rover+H']),
    ('Ingenuity',                           ['Mars+t', 'Planet+T', 'Mars 2020+m', 'Ingenuity+h', 'Helicopter+H']),
    ('Phoenix',                             ['Mars+t', 'Planet+T', 'Phoenix+m', 'Phoenix Lander+h', 'Lander+H']),
    ('Viking',                              ['Mars+t', 'Planet+T', 'Viking+m']),
    ('(Viking [12]).*[Oo]rbit',             [r'\1 Orbiter+h', 'Orbiter+H']),
    ('(Viking [12]).*[Ll]ander',            [r'\1 Lander+h', 'Lander+H']),

    ('Rosetta(?! [Ss]tone)(?! [Bb]ranch)',  ['Comet+T', 'Rosetta+m', 'Rosetta Orbiter+h', '67P/Churyumov-Gerasimenko+t', 'Orbiter+H', 'Periodic Comets+s']),
    ('Philae(?! [Ss]ulcus)',                ['Comet+T', 'Rosetta+m', '67P/Churyumov-Gerasimenko+t', 'Philae Lander+h', 'Lander+H', 'Periodic Comets+s']),
    ('Deep Impact',                         ['Comet+T', 'Deep Impact+m+h', '9P/Tempel+t', 'Impactor+H']),
    ('HIFI',                                ['Comet+T', 'Herschel Space Observatory+m+h', 'Space Telescope+H', 'Heterodyne Instrument for the Far Infrared (HIFI)+i']),
    ('Dawn.{1,20}(mission|spacecraft)',     ['Asteroid+T', 'Main Belt+s', 'Dawn+m+h', 'Orbiter+H']),
    ('(Deep Space 1|DS1)',                  ['Deep Space 1+h', 'Deep Space 1 (DS1)+m', 'Flyby Spacecraft+H']),
    ('(NEAR|Near Earth.{1,30}Rendez)',      ['Asteroid+T', 'NEAR Shoemaker+m+h', 'Orbiter+H']),
    (r"Chang'e",                            ["Chang'e+m", 'Moon+t', 'Satellite+T', 'Earth+s']),

    ('Kepler (?![Cc]rater)',                ['Kepler+m+h', 'Infrared']),
    ('Spitzer',                             ['Spitzer Space Telescope+m+h', 'Space Telescope+H', 'Infrared']),
    ('Planck.*[Tt]elescope',                ['Planck+h+m', 'Space Telescope+s', 'Infrared']),
    ('Herschel Space Telescope',            ['Herschel Space Observatory+h', 'Herschel Space Observatory+m', 'Space Telescope+H', 'Infrared']),
    ('Arecibo',                             ['Arecibo Radar+i', 'Arecibo Observatory+h', 'National Astronomy and Ionosphere Center (NAIC)+m']),
    ('ZTF',                                 ['Asteroid+T', 'Near Earth Objects+s', 'Zwicky Transient Facility+h', 'Zwicky Transient Facility (ZTF)+m']),
    ('(DSN|Deep Space Network)',            ['Deep Space Network (DSN)+m', 'Radio']),
    ('(NRAO|National Radio Astronomy Obs)', ['National Radio Astronomy Observatory (NRAO)+m', 'Ground-Based Observatory+H']),
    ('(VLBA|Very Long Baseline Array)',     ['Very Long Baseline Array (VLBA)+h', 'National Radio Astronomy Observatory (NRAO)+m', 'Ground-Based Observatory+H']),
    ('Chandra X-[Rr]ay',                    ['Chandra X-ray Observatory+h', 'Chandra X-ray Observatory (CXO)+m']),
    ('La Sagra Sky Survey',                 ['La Sagra Sky Survey (LSSS)+i', 'Astronomical Observatory of Mallorca+m', 'La Sagra Observatory+h']),
    ('ROSINA',                              ['Rosetta Orbiter Spectrometer for Ion and Neutral Analysis (ROSINA)+i', 'Rosetta Orbiter+h', 'Rosetta+m', 'Comet+T']),

    ('\(NAC\)',                             ['Narrow Angle Camera (NAC)+d']),
    ('\(WAC\)',                             ['Wide Angle Camera (WAC)+d']),

# Other general keywords
    ('([Uu]ltra.?violet|EUV|FUV|[^\w]UV)',          ['Ultraviolet']),
    ('[Rr]adio(?![a-z])',                           ['Radio']),
    ('[Ww]ater',                                    ['Water']),
    ('[Mm]ethane',                                  ['Methane']),
    ('[Aa]mmonia',                                  ['Ammonia']),
    ('[Cc]rater',                                   ['Crater']),
    ('([Mm]ountains{0,1}|Mons|Montes)',             ['Mountain']),
    ('[Dd]ust',                                     ['Dust']),
    ('[Dd]une',                                     ['Dune']),
    ('[Hh]az(y|e)',                                 ['Haze', 'Atmosphere']),
    ('[Aa]tmospher(e|es|ic)',                       ['Atmosphere']),
    ('[Pp]lume',                                    ['Plume']),
    ('[Vv]olcan(o|os|oes|ism|ic)',                  ['Volcano']),
    ('([Ss]torm|[Rr]ed [Ss]pot|[Dd]ark [Ss]pot)',   ['Storm', 'Atmosphere']),
    ('[Ss]hadow',                                   ['Shadow']),
    ('[Oo]ccultation',                              ['Occultation']),
    ('[Ee]clipse',                                  ['Eclipse']),
    ('[Mm]agnet(ism|ic|osphere)',                   ['Magnetosphere']),
    ('[Mm]ap(?![a-z])',                             ['Map']),
    ('[Aa]rtist',                                   ['Artwork']),
    ('[Aa]rtwork',                                  ['Artwork']),
    ('Lithograph',                                  ['Artwork']),
    ('[Cc]ollision',                                ['Collision']),
    ('[Ii]mpact',                                   ['Impact']),
    ('[Rr][Aa][Dd][Aa][Rr]',                        ['Radar']),
    ('(WISE|[Ii]nfra.?[Rr]ed|IR)',                  ['Infrared']),
    ('[Tt]hermal',                                  ['Thermal']),
    ('([Rr]otat|[Ss]pin(|s|ning)|[Tt]umbl)',        ['Rotation']),
    ('([Pp]lanet|Jupiter|Saturn|Uran|Neptun).* [R]ing', ['Disk']),
]

# Keywords to search for if 'Mercury' appears
KEYWORDS['Mercury'] = [
    ('MESSENGER',                       ['MESSENGER+m', 'Mercury+t', 'Planet+T', 'Orbiter+H']),
    ('Messenger',                       ['MESSENGER+m', 'Mercury+t', 'Planet+T', 'Orbiter+H']),
]

# Keywords to search for if 'Venus' appears
KEYWORDS['Venus'] = [
    ('Pioneer Venus',                   ['Venus+t', 'Planet+T', 'Pioneer Venus+m', 'Pioneer Venus Orbiter+h', 'Flyby Spacecraft+H']),
    ('Magellan',                        ['Venus+t', 'Planet+T', 'Magellan+m+h', 'Orbiter+H']),
]

KEYWORDS['Moon'] = [
    ('LCROSS',                          ['Moon+T', 'Earth+s', 'Satellite+T']),
]

# Keywords to search for if 'Mars' appears
KEYWORDS['Mars'] = [
    ('Mars Atmosphere and Volatile Evolutio[nN]',   ['Mars+t', 'Planet+T', 'MAVEN+h', 'Mars Atmosphere and Volatile Evolution (MAVEN)+m', 'Orbiter+H']),
    ('MAVEN',                                       ['Mars+t', 'Planet+T', 'MAVEN+h', 'Mars Atmosphere and Volatile Evolution (MAVEN)+m', 'Orbiter+H']),
    ('(MGS|Mars Global Surveyor)',                  ['Mars+t', 'Planet+T', 'Mars Global Surveyor+h', 'Mars Global Surveyor (MGS)+m', 'Orbiter+H']),
    ('Mars Odyssey',                                ['Mars+t', 'Planet+T', 'Mars Odyssey+h', '2001 Mars Odyssey+m', 'Orbiter+H']),
    ('Beagle 2',                                    ['Mars+t', 'Planet+T', 'Mars Express+m', 'Mars Express Lander+h', 'Lander+H']),
    ('(MOC|Mars Orbiter Camera)',                   ['Mars+t', 'Planet+T', 'Mars Orbiter Camera (MOC)+i', 'Mars Global Surveyor+h', 'Mars Global Surveyor (MGS)+m', 'Orbiter+H']),
    ('(MSL|Mars [Ss]cience [Ll]aboratory)',         ['Mars+t', 'Planet+T', 'Mars Science Laboratory (MSL)+m', 'Curiosity Rover+h', 'Rover+H']),
    ('Curiosity',                                   ['Mars+t', 'Planet+T', 'Mars Science Laboratory (MSL)+m', 'Curiosity Rover+h', 'Rover+H']),
    ('(MRO|Mars [Rr]econnaissance [Oo]rbiter)',     ['Mars+t', 'Planet+T', 'Mars Reconnaissance Orbiter+h,', 'Mars Reconnaissance Orbiter (MRO)+m,', 'Orbiter+H']),
    ('(MER|Mars [Ee]xploration [Rr]over)',          ['Mars+t', 'Planet+T', 'Mars Exploration Rover (MER)+m', 'Rover+H']),
    ('Spirit',                                      ['Mars+t', 'Planet+T', 'Mars Exploration Rover (MER)+m', 'Rover+H', 'Spirit (MER-A)+h']),
    ('Opportunity',                                 ['Mars+t', 'Planet+T', 'Mars Exploration Rover (MER)+m', 'Rover+H', 'Opportunity (MER-B)+h']),
    ('(MPF|Mars [Pp]athfinder)',                    ['Mars+t', 'Planet+T', 'Mars Pathfinder (MPF)+m']),
    ('InSight',                                     ['Mars+t', 'Planet+T', 'InSight+m', 'InSight Lander+h', 'Lander+H']),
    ('(MEX|Mars Express)',                          ['Mars+t', 'Planet+T', 'Mars Express+m']),

    ('MER-A',                                       ['Spirit (MER-A)+h']),
    ('MER-B',                                       ['Opportunity (MER-B)+h']),
    ('(MPF|Mars [Pp]athfinder).{1,20}Lander',       ['Mars Pathfinder Lander+h', 'Lander+H']),
    ('(MPF|Mars [Pp]athfinder).{1,20}Rover',        ['Mars Pathfinder Rover+h', 'Rover+H']),
    ('(MEX|Mars Express).{1,20}([Oo]rbiter|[Ss]pacecraft)',  ['Mars Express Orbiter+h', 'Orbiter+H']),
    ('(MEX|Mars Express).{1,20}Lander',             ['Mars Express Lander+h', 'Lander+H']),
    ('(MGS|Mars Global Surveyor).*thermal emission spectrometer',
                                                    ['Thermal Emission Spectrometer (TES)+i']),
    ('InSight.{0,20}seismom',                       ['Seismic Experiment for Interior Structure (SEIS)+i']),

    ('CRISM',                   ['Mars+t', 'Planet+T', 'Mars Reconnaissance Orbiter+h,', 'Mars Reconnaissance Orbiter (MRO)+m,', 'Orbiter+H', 'Compact Reconnaissance Imaging Spectrometer for Mars (CRISM)+i']),
    ('OMEGA',                   ['Mars+t', 'Planet+T', 'Mars Express+m', 'Mars Express Orbiter+h', 'Orbiter+H', 'Visible and Infrared Mineralogical Mapping Spectrometer (OMEGA)+i']),
    ('SEIS',                    ['Mars+t', 'Planet+T', 'InSight+m', 'InSight Lander+h', 'Lander+H', 'Seismic Experiment for Interior Structure (SEIS)+i']),
    ('APSS',                    ['Mars+t', 'Planet+T', 'InSight+m', 'InSight Lander+h', 'Lander+H', 'Auxiliary Payload Subsystem (APSS)+i']),
    ('TWINS',                   ['Mars+t', 'Planet+T', 'InSight+m', 'InSight Lander+h', 'Lander+H', 'Temperature and Wind for InSight (TWINS)+i']),
    ('HP3',                     ['Mars+t', 'Planet+T', 'InSight+m', 'InSight Lander+h', 'Lander+H', 'Heat Flow and Physical Properties Package (HP3)+i']),
    ('ICC',                     ['Mars+t', 'Planet+T', 'InSight+m', 'InSight Lander+h', 'Lander+H', 'Mars+t', 'Instrument Context Camera (ICC)+i']),
    ('WATSON',                  ['Mars+t', 'Planet+T', 'Mars 2020+m', 'Perseverance+h', 'Rover+H', 'Wide Angle Topographic Sensor for Operations and Engineering (WATSON)+i']), 

    ('Phobos',                  ['Mars+s', 'Satellite+T', 'Phobos+t']),
    ('Deimos',                  ['Mars+s', 'Satellite+T', 'Deimos+t']),
]

# Keywords to search for if 'Jupiter' appears
KEYWORDS['Jupiter'] = [
    ('Galileo.{1,20}[Oo]rbiter',        ['Jupiter+s', 'Galileo+m', 'Galileo Orbiter+h', 'Orbiter+H']),
    ('Galileo.{1,20}[Ss]pacecraft',     ['Jupiter+s', 'Galileo+m', 'Galileo Orbiter+h', 'Orbiter+H']),
    ('Galileo.{1,20}[Mm]ission',        ['Jupiter+s', 'Galileo+m', 'Galileo Orbiter+h', 'Orbiter+H']),
    ('Galileo.{1,40}Probe',             ['Jupiter+t', 'Planet+T', 'Galileo+m', 'Galileo Probe+h', 'Probe+H']),
    ('Jup.*Probe.*Galileo',             ['Jupiter+t', 'Planet+T', 'Galileo+m', 'Galileo Probe+h', 'Probe+H']),
    ('JUICE',                           ['Jupiter+t+s', 'Planet+T', 'Jupiter Icy Moons Explorer+h', 'Jupiter Icy Moons Explorer (JUICE)+m']),
    ('RIME',                            ['Jupiter+t+s', 'Planet+T', 'Jupiter Icy Moons Explorer+h', 'Jupiter Icy Moons Explorer (JUICE)+m', 'Radar for Icy Moon Exploration (RIME)+i']),
    ('PPR',                             ['Jupiter+t+s', 'Planet+T', 'Galileo Orbiter+h', 'Orbiter+H', 'Photopolarimeter-Radiometer (PPR)+i']),

    ('S/20[0-9][0-9] *J *[1-9][0-9]*',  ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('Jovian.{0,10} [Rr]ing',           ['Jupiter+s', 'Jupiter Rings+t', 'Ring+T']),
    ('Jupiter.{0,20} [Rr]ing',          ['Jupiter+s', 'Jupiter Rings+t', 'Ring+T']),
    (' [Rr]ing.{0,10}Jupiter',          ['Jupiter+s', 'Jupiter Rings+t', 'Ring+T']),
    ('[Mm]ain [Rr]ing',                 ['Jupiter+s', 'Main Ring+t', 'Jupiter Rings+t', 'Ring+T']),
    (' [Rr]ings{0,1} .{0,20}[Hh]alo',   ['Jupiter+s', 'Halo+t', 'Jupiter Rings+t', 'Ring+T']),
    ('[Hh]alo .{0,10}[^\w][Rr]ing',     ['Jupiter+s', 'Halo+t', 'Jupiter Rings+t', 'Ring+T']),
    ('[Gg]ossamer',                     ['Jupiter+s', 'Gossamer Ring+t', 'Jupiter Rings+t', 'Ring+T']),

    ('(Adrastea)',                  ['Jupiter+s', r'\1+t', 'Satellite+T']),
    ('(Metis)',                     ['Jupiter+s', r'\1+t', 'Satellite+T']),
    ('(Amalthea)',                  ['Jupiter+s', r'\1+t', 'Satellite+T']),
    ('(Thebe)',                     ['Jupiter+s', r'\1+t', 'Satellite+T']),
    ('Io(?![a-z])',                 ['Jupiter+s', r'\1+t', 'Satellite+T']),
    ('(Europa)',                    ['Jupiter+s', r'\1+t', 'Satellite+T']),
    ('(Ganymede)',                  ['Jupiter+s', r'\1+t', 'Satellite+T']),
    ('(Callisto)',                  ['Jupiter+s', r'\1+t', 'Satellite+T']),
    ('(Themisto)',                  ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Leda)',                      ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Himalia)',                   ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Lysithea)',                  ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Elara)',                     ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Dia)(?![a-z])',              ['Jupiter+s', 'Dia+t', 'Satellite+T', 'Irregular+T']),
    ('(Carpo)',                     ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Euporie)',                   ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Thelxinoe)',                 ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Euanthe)',                   ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Helike)',                    ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Orthosie)',                  ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Iocaste)',                   ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Praxidike)',                 ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Harpalyke)',                 ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Mneme)',                     ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Hermippe)',                  ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Thyone)',                    ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Ananke)',                    ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Herse)',                     ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Aitne)',                     ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Kale)',                      ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Taygete)',                   ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Chaldene)',                  ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Erinome)',                   ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Aoede)',                     ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Kallichore)',                ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Kalyke)',                    ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Carme)',                     ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Callirrhoe)',                ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Eurydome)',                  ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Pasithee)',                  ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Kore)',                      ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Cyllene)',                   ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Eukelade)',                  ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Pasiphae)',                  ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Hegemone)',                  ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Arche(?![a-z]))',            ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Isonoe)',                    ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Sinope)',                    ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Sponde)',                    ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Autonoe)',                   ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Megaclite)',                 ['Jupiter+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
]

# Keywords to search for if 'Saturn' appears
KEYWORDS['Saturn'] = [
    ('(?<!Cassini-)Huygens',        ['Saturn+s', 'Huygens Probe+h', 'Cassini-Huygens+m', 'Lander+H']), # not if it says "Cassini-Huygens"
    ('(?<!imas |adus |thys |ione |Rhea |itan |rion |etus |oebe )Atlas',
                                                        ['Saturn+s', 'Atlas+t', 'Satellite+T']),
    (' ([A-G])[- ][Rr]ing',                             ['Saturn+s', r'\1 Ring+t', 'Saturn Rings+t', 'Ring+T']),
    (' ([A-G])-{0,1},{0,1} and [A-G][- ][Rr]ings',      ['Saturn+s', r'\1 Ring+t', 'Saturn Rings+t', 'Ring+T']),
    (' [A-G]-{0,1},{0,1} and ([A-G])[- ][Rr]ings',      ['Saturn+s', r'\1 Ring+t', 'Saturn Rings+t', 'Ring+T']),
    (' ([A-G])-{0,1}, [A-G].{0,20} [A-G][- ][Rr]ings',  ['Saturn+s', r'\1 Ring+t', 'Saturn Rings+t', 'Ring+T']),
    ('Saturn.{0,20} [Rr]ing',       ['Saturn+s', 'Saturn Rings+t', 'Ring+T']),
    (' [Rr]ing.{0,10}Saturn',       ['Saturn+s', 'Saturn Rings+t', 'Ring+T']),
    ('Cassini [Dd]ivision',         ['Saturn+s', 'Cassini Division+t', 'Saturn Rings+t', 'Ring+T', 'Gap+T']),
    ('Encke ([Dd]ivision|[Gg]ap)',  ['Saturn+s', 'Encke Gap+t', 'Saturn Rings+t', 'Ring+T', 'Gap+T']),

    ('moon[\., s]',                 ['Saturn+s', 'Satellite+T']),
    ('satellite[\., s]',            ['Saturn+s', 'Satellite+T']),
    ('(Pan)(?![a-z])',              ['Saturn+s', r'\1+t', 'Satellite+T']),
    ('(Daphnis)',                   ['Saturn+s', r'\1+t', 'Satellite+T']),
    ('(Prometheus)',                ['Saturn+s', r'\1+t', 'Satellite+T']),
    ('(Pandora)',                   ['Saturn+s', r'\1+t', 'Satellite+T']),
    ('(Epimetheus)',                ['Saturn+s', r'\1+t', 'Satellite+T']),
    ('(Janus)',                     ['Saturn+s', r'\1+t', 'Satellite+T']),
    ('(Aegaeon)',                   ['Saturn+s', r'\1+t', 'Satellite+T']),
    ('(Methone)',                   ['Saturn+s', r'\1+t', 'Satellite+T']),
    ('(Anthe)',                     ['Saturn+s', r'\1+t', 'Satellite+T']),
    ('(Pallene)',                   ['Saturn+s', r'\1+t', 'Satellite+T']),
    ('(Telesto)',                   ['Saturn+s', r'\1+t', 'Satellite+T']),
    ('(Calypso)',                   ['Saturn+s', r'\1+t', 'Satellite+T']),
    ('(Dione)',                     ['Saturn+s', r'\1+t', 'Satellite+T']),
    ('(Helene)',                    ['Saturn+s', r'\1+t', 'Satellite+T']),
    ('(Polydeuces)',                ['Saturn+s', r'\1+t', 'Satellite+T']),
    ('(Mimas)',                     ['Saturn+s', r'\1+t', 'Satellite+T']),
    ('(Enceladus)',                 ['Saturn+s', r'\1+t', 'Satellite+T']),
    ('(Tethys)',                    ['Saturn+s', r'\1+t', 'Satellite+T']),
    ('(Dione)',                     ['Saturn+s', r'\1+t', 'Satellite+T']),
    ('(Rhea)',                      ['Saturn+s', r'\1+t', 'Satellite+T']),
    ('(Hyperion)',                  ['Saturn+s', r'\1+t', 'Satellite+T']),
    ('(Iapetus)',                   ['Saturn+s', r'\1+t', 'Satellite+T']),
    ('(Phoebe)',                    ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Kiviuq)',                    ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Ijiraq)',                    ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Paaliaq)',                   ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Skathi)',                    ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Albiorix)',                  ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Bebhionn)',                  ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Erriapus)',                  ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Skoll)',                     ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Siarnaq)',                   ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Tarqeq)',                    ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Greip)',                     ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Hyrrokkin)',                 ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Jarnsaxa)',                  ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Tarvos)',                    ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Mundilfari)',                ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Bergelmir)',                 ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Narvi)',                     ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Suttungr)',                  ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Hati)',                      ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Farbauti)',                  ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Thrymr)',                    ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Aegir)',                     ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Bestla)',                    ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Fenrir)',                    ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Surtur)',                    ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Kari)',                      ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Ymir)',                      ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Loge)',                      ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Fornjot)',                   ['Saturn+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('S/2004 *S *1',                ['Saturn+s', 'Methone+t', 'Satellite+T']),
    ('S/2004 *S *2',                ['Saturn+s', 'Pallene+t', 'Satellite+T']),
    ('S/2004 *S *5',                ['Saturn+s', 'Polydeuces+t', 'Satellite+T']),
    ('S/2004 *S *([36])',           ['Saturn+s', 'F Ring+t', 'Moonlet', 'Clump']),
    ('S/2005 *S *1',                ['Saturn+s', 'Daphnis+t', 'Satellite+T']),
    ('S/2007 *S *4',                ['Saturn+s', 'Anthe+t', 'Satellite+T']),
    ('S/2008 *S *1',                ['Saturn+s', 'Aegaeon+t', 'Satellite+T']),
]

# Keywords to search for if 'Uranus' appears
KEYWORDS['Uranus'] = [
    ('Uranian.{0,10} [Rr]ing',                  ['Uranus+s', 'Uranus Rings+t', 'Ring+T']),
    ('Uranus.{0,20} [Rr]ing',                   ['Uranus+s', 'Uranus Rings+t', 'Ring+T']),
    (' [Rr]ing.{0,10}Uranus',                   ['Uranus+s', 'Uranus Rings+t', 'Ring+T']),
    (' [Zz]eta(, | | .{0,20} )[Rr]ing',         ['Uranus+s', 'Zeta Ring+t', 'Uranus Rings+t', 'Ring+T']),
    (' (6|six|Six)(, | | .{0,20} )[Rr]ing',     ['Uranus+s', 'Six Ring+t', 'Uranus Rings+t', 'Ring+T']),
    (' (5|five|Five)(, | | .{0,20} )[Rr]ing',   ['Uranus+s', 'Five Ring+t', 'Uranus Rings+t', 'Ring+T']),
    (' (4|four|Four)(, | | .{0,20} )[Rr]ing',   ['Uranus+s', 'Four Ring+t', 'Uranus Rings+t', 'Ring+T']),
    (' [Aa]lpha(, | | .{0,20} )[Rr]ing',        ['Uranus+s', 'Alpha Ring+t', 'Uranus Rings+t', 'Ring+T']),
    (' [Bb]eta(, | | .{0,20} )[Rr]ing',         ['Uranus+s', 'Beta Ring+t', 'Uranus Rings+t', 'Ring+T']),
    (' [Ee]ta(, | | .{0,20} )[Rr]ing',          ['Uranus+s', 'Eta Ring+t', 'Uranus Rings+t', 'Ring+T']),
    (' [Gg]amma(, | | .{0,20} )[Rr]ing',        ['Uranus+s', 'Gamma Ring+t', 'Uranus Rings+t', 'Ring+T']),
    (' [Dd]elta(, | | .{0,20} )[Rr]ing',        ['Uranus+s', 'Delta Ring+t', 'Uranus Rings+t', 'Ring+T']),
    (' [Ll]ambda(, | | .{0,20} )[Rr]ing',       ['Uranus+s', 'Lambda Ring+t', 'Uranus Rings+t', 'Ring+T']),
    (' [Ee]psilon(?! +Eridani)(, | | .{0,20} )[Rr]ing',
                                                ['Uranus+s', 'Epsilon Ring+t', 'Uranus Rings+t', 'Ring+T']),
    (' [Nn]u(, | | .{0,20} )[Rr]ings?',         ['Uranus+s', 'Nu Ring+t', 'Uranus Rings+t', 'Ring+T']),
    (' [Mm]u(, | | .{0,20} )[Rr]ings?',         ['Uranus+s', 'Mu Ring+t', 'Uranus Rings+t', 'Ring+T']),
    ('(Cordelia)',                  ['Uranus+s', r'\1+t', 'Satellite+T']),
    ('(Ophelia)',                   ['Uranus+s', r'\1+t', 'Satellite+T']),
    ('(Bianca)',                    ['Uranus+s', r'\1+t', 'Satellite+T']),
    ('(Cressida)',                  ['Uranus+s', r'\1+t', 'Satellite+T']),
    ('(Desdemona)',                 ['Uranus+s', r'\1+t', 'Satellite+T']),
    ('(Juliet)',                    ['Uranus+s', r'\1+t', 'Satellite+T']),
    ('(Portia)',                    ['Uranus+s', r'\1+t', 'Satellite+T']),
    ('(Rosalind)',                  ['Uranus+s', r'\1+t', 'Satellite+T']),
    ('(Cupid)',                     ['Uranus+s', r'\1+t', 'Satellite+T']),
    ('(Belinda)',                   ['Uranus+s', r'\1+t', 'Satellite+T']),
    ('(Perdita)',                   ['Uranus+s', r'\1+t', 'Satellite+T']),
    ('(Puck)',                      ['Uranus+s', r'\1+t', 'Satellite+T']),
    ('(Mab)',                       ['Uranus+s', r'\1+t', 'Satellite+T']),
    ('(Miranda)',                   ['Uranus+s', r'\1+t', 'Satellite+T']),
    ('(Ariel)',                     ['Uranus+s', r'\1+t', 'Satellite+T']),
    ('(Umbriel)',                   ['Uranus+s', r'\1+t', 'Satellite+T']),
    ('(Titania)',                   ['Uranus+s', r'\1+t', 'Satellite+T']),
    ('(Oberon)',                    ['Uranus+s', r'\1+t', 'Satellite+T']),
    ('(Francisco)',                 ['Uranus+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Caliban)',                   ['Uranus+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Stephano)',                  ['Uranus+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Trinculo)',                  ['Uranus+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Sycorax)',                   ['Uranus+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Margaret)',                  ['Uranus+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Prospero)',                  ['Uranus+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Setebos)',                   ['Uranus+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Ferdinand)',                 ['Uranus+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
]

# Keywords to search for if 'Neptune' appears
KEYWORDS['Neptune'] = [
    ('Neptun.{0,20} [Rr]ing',       ['Neptune+s', 'Neptune Rings+t', 'Ring+T']),
    (' [Rr]ing.{0,10}Neptune',      ['Neptune+s', 'Neptune Rings+t', 'Ring+T']),
    ('Adams .[Rr]ings',             ['Neptune+s', 'Adams Ring+t', 'Neptune Rings+t', 'Ring+T']),
    ('Lassell',                     ['Neptune+s', 'Lassell Ring+t', 'Neptune Rings+t', 'Ring+T']),
    ('Le {0,1}[Vv]errier',          ['Neptune+s', 'Leverrier Ring+t', 'Neptune Rings+t', 'Ring+T']),
    ('Galle(?! +Crater)',           ['Neptune+s', 'Galle Ring+t', 'Neptune Rings+t', 'Ring+T']),
    ('Libert[ye] .*[Aa]rcs{0,1}',   ['Neptune+s', 'Liberte+t', 'Adams Ring+t', 'Neptune Rings+t', 'Ring+T', 'Arc+T']),
    ('(Egalite|Equality) .*[Aa]rc', ['Neptune+s', 'Egalite+t', 'Adams Ring+t', 'Neptune Rings+t', 'Ring+T', 'Arc+T']),
    ('Fraternit[ye] .*[Aa]rc',      ['Neptune+s', 'Fraternite+t', 'Adams Ring+t', 'Neptune Rings+t', 'Ring+T', 'Arc+T']),
    ('Courage .*[Aa]rc',            ['Neptune+s', 'Courage+t', 'Adams Ring+t', 'Neptune Rings+t', 'Ring+T', 'Arc+T']),
    ('(Naiad)',                     ['Neptune+s', r'\1+t', 'Satellite+T']),
    ('(Thalassa)',                  ['Neptune+s', r'\1+t', 'Satellite+T']),
    ('(Despina)',                   ['Neptune+s', r'\1+t', 'Satellite+T']),
    ('(Galatea)',                   ['Neptune+s', r'\1+t', 'Satellite+T']),
    ('(Larissa)',                   ['Neptune+s', r'\1+t', 'Satellite+T']),
    ('S/2004 *N *1',                ['Neptune+s', 'S/2004 N 1+t', 'Satellite+T']),
    ('Proteus',                     ['Neptune+s', 'Proteus+t', 'Satellite+T']),
    ('Triton',                      ['Neptune+s', 'Triton+t', 'Satellite+T']),
    ('Nereid',                      ['Neptune+s', 'Nereid+t', 'Satellite+T', 'Irregular+T']),
    ('(Halimede)',                  ['Neptune+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Sao)',                       ['Neptune+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Laomedeia)',                 ['Neptune+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Psamathe)',                  ['Neptune+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(Neso)',                      ['Neptune+s', r'\1+t', 'Satellite+T', 'Irregular+T']),
    ('(|S/)1989 *N *1',             ['Neptune+s', 'Proteus+t', 'Satellite+T']),
    ('(|S/)1989 *N *2',             ['Neptune+s', 'Thalassa+t', 'Satellite+T']),
]

# Keywords to search for if 'Pluto' appears
KEYWORDS['Pluto'] = [
    ('(Charon)',                    ['Pluto+s', r'\1+t', 'Satellite+T']),
    ('(Styx)',                      ['Pluto+s', r'\1+t', 'Satellite+T']),
    ('(Nix)',                       ['Pluto+s', r'\1+t', 'Satellite+T']),
    ('(Kerberos)',                  ['Pluto+s', r'\1+t', 'Satellite+T']),
    ('(Hydra)(?![a-z])',            ['Pluto+s', r'\1+t', 'Satellite+T']),
]

# Keywords to search for if 'Comet' appears
KEYWORDS['Comet'] = [
    ('(P/[12]\d\d\d [A-Z][A-Z]?\d* \([\w ]+?\))',   ['Comet+T', r'\1+t', 'Periodic Comets+s']),
    ('(C/[12]\d\d\d [A-Z][A-Z]?\d* \([\w ]+?\))',   ['Comet+T', r'\1+t']),
    ('(P/[12]\d\d\d [A-Z][A-Z]?\d*)',               ['Comet+T', r'\1+t', 'Periodic Comets+s']),
    ('(C/[12]\d\d\d [A-Z]+\d*)',                    ['Comet+T', r'\1+t']),
    ('(\d+P/[A-Z][A-Za-z-]+)( \d+|)',               ['Comet+T', r'\1+t', 'Periodic Comets+s']),
    ('C/2020 F3',                                   ['Comet+T', 'C/2020 F3 (NEOWISE)+t']),
    ('C/2018 Y1',                                   ['Comet+T', 'C/2018 Y1 (Iwamoto)+t']),
    ('Holmes',                                      ['Comet+T', '17P/Holmes+t', 'Periodic Comets+s']),
    ('Encke (?![Dd]iv|[Gg]ap)',                     ['Comet+T', '2P/Encke+t', 'Periodic Comets+s']),
    ('C/2013 A1',                                   ['Comet+T', 'C/2013 A1 (Siding Spring)+t']),
    ('Hyakutake',                                   ['Comet+T', 'C/1996 B2 (Hyakutake)+t']),
    ('ISON',                                        ['Comet+T', 'C/2012 S1 (ISON)+t']),
    ('Schwassmann-Wachmann 2',                      ['Comet+T', '31P/Schwassmann-Wachmann+t', 'Periodic Comets+s']),
    ('Schwassmann-Wachmann 3',                      ['Comet+T', '73P/Schwassmann-Wachmann+t', 'Periodic Comets+s']),
    ('Schwassmann-Wachmann [I1]',                   ['Comet+T', '29P/Schwassmann-Wachmann+t', 'Periodic Comets+s']),
    ('C/2012 K1',                                   ['Comet+T', 'C/2012 K1 (PANSTARRS)+t']),
    ('C/2014 C3',                                   ['Comet+T', 'C/2014 C3 (NEOWISE)+t']),
    ('(C/2019 Q4|Borisov)',                         ['Comet+T', '2I/Borisov+t', 'Interstellar Comets+s']),
    ('P/2016 BA14',                                 ['Comet+T', 'P/2016 BA14 (Pan-STARRS)+t', 'Periodic Comets+s']),
]

# Keywords to search for if 'Asteroid' appears
KEYWORDS['Asteroid'] = [
    ('Potentially.[Hh]azardous',                    ['Asteroid+T', 'Near Earth Objects+s']),
    ('(?<!/)(19|20)(\d\d [A-Z][A-Z]?\d*)[ ,;\.]',   ['Asteroid+T', r'\1\2+t']),
    ('\((\d\d+)\) ([A-Z][a-z]{3,99})',              ['Asteroid+T', r'\1 \2+t']),

    ("Dawn[ \.,']",                 ['Asteroid+T', 'Main Belt+s', 'Dawn+m+h', 'Orbiter+H']),
    ('Goldstone',                   ['Asteroid+T', 'Near Earth Objects+s', 'Radar', 'Deep Space Network (DSN)+m', 'Goldstone Deep Space Communications Complex (GDSCC)+h']),
    ('Catalina.{1,30}Survey',       ['Asteroid+T', 'Near Earth Objects+s', 'Catalina Sky Survey (CSS)+m', 'Steward Observatory+h', 'Ground-Based Observatory+H']),
#     ('WISE',                        ['Asteroid+T', 'Near Earth Objects+s', 'NEOWISE Telescope+i', 'NEOWISE+h', 'Near-Earth Object Wide-field Infrared Survey Explorer (NEOWISE)+m']),
    ('Asteroid Redirect ',          ['Asteroid+T', 'Asteroid Redirect Mission (ARM)+m']),

    ('(2016 WF9)',                  ['Asteroid+T', 'Near Earth Objects+s', r'\1+t']),
    ('Eros(?![a-z])',               ['Asteroid+T', 'Near Earth Objects+s', '433 Eros+t']),
    ('2003 SD2020',                 ['Asteroid+T', 'Near Earth Objects+s', '2003 SD220+t']),

    ('Malala',                      ['Asteroid+T', '316201 Malala+t',       'Near Earth Objects+s']),
    ('Didymos',                     ['Asteroid+T', '65803 Didymos+t',       'Near Earth Objects+s']),
    ('(92020 QG)',                  ['Asteroid+T', r'\1+t',                 'Near Earth Objects+s']),
    ('(3200 Phaethon)',             ['Asteroid+T', r'\1+t',                 'Near Earth Objects+s']),
    ('Apophis',                     ['Asteroid+T', '99942 Apophis+t',       'Near Earth Objects+s']),
    ('(4660 Nereus)',               ['Asteroid+T', r'\1+t',                 'Near Earth Objects+s']),
    ('(Don Quixote)',               ['Asteroid+T', r'3552 \1+t',            'Main Belt+s']),
    ('(S|&Scaron;)teins',           ['Asteroid+T', '2867 &Scaron;teins+t',  'Main Belt+s']),
    ('Mathilde',                    ['Asteroid+T', '253 Mathilde+t',        'Main Belt+s']),
    ('Ida[^a-z]',                   ['Asteroid+T', '243 Ida+t',             'Main Belt+s']),
    ('Masursky' ,                   ['Asteroid+T', '2685 Masursky+t',       'Main Belt+s']),
    ('Toutatis',                    ['Asteroid+T', '4179 Toutatis+t',       'Main Belt+s']),
    ('Annefrank',                   ['Asteroid+T', '5535 Annefrank+t',      'Main Belt+s']),
    ('Braille',                     ['Asteroid+T', '9969 Braille+t',        'Main Belt+s']),
    ('Itokawa',                     ['Asteroid+T', '25143 Itokawa+t',       'Main Belt+s']),
    ('Bennu',                       ['Asteroid+T', '101955 Bennu+t',        'Main Belt+s']),
    ('Ryugu',                       ['Asteroid+T', '162173 Ryugu+t',        'Main Belt+s']),
    ('2002 JF56',                   ['Asteroid+T', '2002 JF56+t',           'Main Belt+s']),
    ('Euphrosyne',                  ['Asteroid+T', '31 Euphrosyne+t',       'Main Belt+s']),
    ('Naozane',                     ['Asteroid+T', '5238 Naozane+t',        'Main Belt+s']),
    ('Kleopatra',                   ['Asteroid+T', '216 Kleopatra+t',       'Main Belt+s']),
    ('Pallas',                      ['Asteroid+T', '2 Pallas+t',            'Main Belt+s']),

    ('Dactyl',                      ['Satellite+T', '243 Ida I (Dactyl)+t', 'Satellite+T', '243 Ida+s+t', 'Asteroid+T', 'Main Belt+s']),

    ('NEO',                         ['Asteroid+T', 'Near Earth Objects+s']),
    ('[Nn]ear.Earth',               ['Asteroid+T', 'Near Earth Objects+s']),
    ('[Bb]inary',                   ['Asteroid+T', 'Binary']),
]

# Keywords to search for if 'Kuiper Belt' appears
KEYWORDS['Kuiper Belt'] = [
    ('(?<!/)(19|20)(\d\d [A-Z][A-Z]?\d*)(?![a-z])', ['Kuiper Belt+s', 'KBO+T', r'\1\2+t']),
    ('Sedna',                                       ['Kuiper Belt+s', 'KBO+T', '90377 Sedna+t', 'Dwarf Planet+T']),
    ('2003 UB313',                                  ['Kuiper Belt+s', 'KBO+T', '136199 Eris+t', 'Dwarf Planet+T']),
]

# Keywords to search for if 'Ring+T' appears
KEYWORDS['Ring'] = [
    ('[Cc]lumps{0,1}',                  ['Ring+T', 'Clump']),
    ('[Gg]aps{0,1}',                    ['Ring+T', 'Gap']),
    ('[Pp]ropellers{0,1}',              ['Ring+T', 'Propeller', 'Saturn Rings+t', 'Saturn+s']),
    ('[Ww]aves{0,1}',                   ['Ring+T', 'Wave']),
    ('[Mm]oonlets{0,1}',                ['Ring+T', 'Moonlet']),
]

# Keywords to search for if 'HST' appears
KEYWORDS['Hubble Space Telescope (HST)'] = [
    ('(WFC3|Wide Field Camera 3).*(UVIS|[Uu]ltra)',     ['Hubble Space Telescope+h', 'Hubble Space Telescope (HST)+m', 'Ultraviolet and Visual Channel (UVIS)+d', 'Visual', 'Ultraviolet']),
    ('(WFC3|Wide Field Camera 3).*(IR|[Ii]nfra)',       ['Hubble Space Telescope+h', 'Hubble Space Telescope (HST)+m', 'Infrared Channel (IR)+d', 'Infrared']),
    ('(ACS|Advanced Camera for Surveys)',               ['Hubble Space Telescope+h', 'Hubble Space Telescope (HST)+m', 'Advanced Camera for Surveys (ACS)+i', 'Visual']),
    ('(WFPC2|WF/PC2)',                                  ['Hubble Space Telescope+h', 'Hubble Space Telescope (HST)+m', 'Wide Field/Planetary Camera 2 (WFPC2)+i', 'Visual', 'Infrared']),
    ('(WFPC2|Wide[- ]Field[/ ]Planetary Camera(| 2))',  ['Hubble Space Telescope+h', 'Hubble Space Telescope (HST)+m', 'Wide Field/Planetary Camera 2 (WFPC2)+i', 'Visual', 'Infrared']),
    ('(NICMOS)',                                        ['Hubble Space Telescope+h', 'Hubble Space Telescope (HST)+m', 'Near Infrared Camera and Multi-Object Spectrometer (NICMOS)+i', 'Infrared']),
    ('(WFC|Wide[- ]Field Channel)',                     ['Hubble Space Telescope+h', 'Hubble Space Telescope (HST)+m', 'Advanced Camera for Surveys (ACS)+i', 'Wide Field Channel (WFC)+d', 'Visual', 'Infrared']),
    ('(HRC|High[- ]Resolution Channel)',                ['Hubble Space Telescope+h', 'Hubble Space Telescope (HST)+m', 'Advanced Camera for Surveys (ACS)+i', 'High-Resolution Channel (HRC)+d', 'Visual', 'Infrared']),
    ('(SBC|Solar[- ]Blind Channel)',                    ['Hubble Space Telescope+h', 'Hubble Space Telescope (HST)+m', 'Advanced Camera for Surveys (ACS)+i', 'Solar Blind Channel (SBC)+d', 'Ultraviolet']),
    ('(WFC3|Wide Field Camera 3)',                      ['Hubble Space Telescope+h', 'Hubble Space Telescope (HST)+m', 'Wide Field Camera 3 (WFC3)+i']),
    ('(UVIS|[Uu]ltra).*(WFC3|Wide Field Camera 3)',     ['Hubble Space Telescope+h', 'Hubble Space Telescope (HST)+m', 'Ultraviolet and Visual Channel (UVIS)+d', 'Visual', 'Ultraviolet']),
    ('(IR|[Ii]nfra).*(WFC3|Wide Field Camera 3)',       ['Hubble Space Telescope+h', 'Hubble Space Telescope (HST)+m', 'Infrared Channel (IR)+d', 'Infrared']),
]

# Keywords to search for if 'New Horizons' appears
KEYWORDS['New Horizons'] = [
    ('LORRI',                                           ['New Horizons+h+m', 'Long Range Reconnaissance Imager (LORRI)+i', 'Visual']),
    ('Long[- ][Rr]ange.*[Ii]mager',                     ['New Horizons+h+m', 'Long Range Reconnaissance Imager (LORRI)+i', 'Visual']),
    ('MVIC',                                            ['New Horizons+h+m', 'Multispectral Visible Imaging Camera (MVIC)+i']),
    ('LEISA',                                           ['New Horizons+h+m', 'Linear Etalon Imaging Spectral Array (LEISA)+i', 'Infrared']),
    ('REX',                                             ['New Horizons+h+m', 'Radio Science Experiment (REX)+i', 'Radio']),
]

# Keywords to search for if 'Cassini' appears
KEYWORDS['Cassini-Huygens'] = [
    ('(ISS|Imaging Science Subsystem)',                 ['Cassini Orbiter+h', 'Cassini-Huygens+m', 'Visual', 'Imaging Science Subsystem (ISS)+i']),
    ('([Ww]ide[- ][Aa]ngle)',                           ['Cassini Orbiter+h', 'Cassini-Huygens+m', 'Visual', 'Imaging Science Subsystem (ISS)+i', 'Wide Angle Camera+d']),
    ('([Nn]arrow[- ][Aa]ngle)',                         ['Cassini Orbiter+h', 'Cassini-Huygens+m', 'Visual', 'Imaging Science Subsystem (ISS)+i', 'Narrow Angle Camera+d']),
    ('(VIMS|Visual.{1,20}[Ss]pectrometer)',             ['Cassini Orbiter+h', 'Cassini-Huygens+m', 'Visual', 'Infrared', 'Visual and Infrared Mapping Spectrometer (VIMS)+i']),
    ('(UVIS|Ultra.{1,20}[Ss]pectrometer)',              ['Cassini Orbiter+h', 'Cassini-Huygens+m', 'Ultraviolet', 'Ultraviolet Imaging Spectrometer (UVIS)+i', 'Ultraviolet']),
    ('(CIRS|Composite.{1,20}[Ss]pectrometer)',          ['Cassini Orbiter+h', 'Cassini-Huygens+m', 'Infrared', 'Composite Infrared Spectrometer (CIRS)+i', 'Infrared']),
    ('(RSS|Radio.{1,20}[Ss]ubsystem)',                  ['Cassini Orbiter+h', 'Cassini-Huygens+m', 'Radio', 'Radioscience Subsystem (RSS)+i']),
    ('(CDA|Dust ([Dd]etector|[Aa]nalyzer))',            ['Cassini Orbiter+h', 'Cassini-Huygens+m', 'Dust', 'Cosmic Dust Analzer (CDA)+i']),
    ('(INMS|Ion (?:|&|and) Neutral Mass Spectrom)',     ['Cassini Orbiter+h', 'Cassini-Huygens+m', 'Ion and Neutral Mass Spectrometer (INMS)+i']),
    ('(MIMI|Magnetospheric Imaging Instrument)',        ['Cassini Orbiter+h', 'Cassini-Huygens+m', 'Magnetosphere', 'Magnetospheric Imaging Instrument (MIMI)+i']),
]

# Keywords to search for if 'Voyager' appears
KEYWORDS['Voyager'] = [
    ('(ISS|Imaging Science Subsystem)',                 ['Voyager+m', 'Imaging Science Subsystem (ISS)+i', 'Visual']),
    ('([Ww]ide[- ][Aa]ngle)',                           ['Voyager+m', 'Wide Angle Camera+d', 'Imaging Science Subsystem (ISS)+i', 'Visual']),
    ('([Nn]arrow[- ][Aa]ngle)',                         ['Voyager+m', 'Narrow Angle Camera+d', 'Imaging Science Subsystem (ISS)+i', 'Visual']),
    ('(PPS|[Pp]otopolarimeter)',                        ['Voyager+m', 'Photopolarimeter Subsystem (PPS)+i', 'Ultraviolet']),
    ('(UVS|Ultra.{1,20}[Ss]pectromet)',                 ['Voyager+m', 'Ultraviolet Spectrometer (UVS)+i', 'Ultraviolet']),
    ('(RSS|Radio.{1,20}[Ss]ubsystem)',                  ['Voyager+m', 'Radioscience Subsystem (RSS)+i', 'Radio']),
    ('(PLS|Plasma Science)',                            ['Voyager+m', 'Magnetosphere', 'Plasma Science Experiment (PLS)+i']),
    ('(CRS|Cosmic Ray)',                                ['Voyager+m', 'Cosmic Ray Subsystem (CRS)+i']),
    ('Plasma Wave Subsystem',                           ['Voyager+m', 'Plasma Wave Subsystem (PWS)+i']),
]

# Keywords to search for if 'Juno' appears
KEYWORDS['Juno'] = [
    ('Juno[Cc]am',                                      ['Juno+m', 'JunoCam+i', 'Visual']),
    ('(JIRAM|Jovian .{10,30}Mapper)',                   ['Juno+m', 'Jupiter Infrared Auroral Mapper (JIRAM)+i', 'Infrared']),
]

# Keywords to search for if 'Exoplanet' appears
KEYWORDS['Exoplanet'] = [
    ('Vega(?![a-z])',                                   ['Exoplanet+T', 'Vega+t+s'      ]),
    ('WASP[^\d]?(\d+)',                                 ['Exoplanet+T', r'WASP-\1+t+s'  ]),
    ('[Oo]rbit',                                        ['Orbit']),
    ('[Dd]isk',                                         ['Disk']),
]

# Keywords to search for if 'Deep Space Network (DSN)' appears
KEYWORDS['Deep Space Network (DSN)'] = [
    ('Goldstone',   ['Deep Space Network (DSN)+m', 'Goldstone Deep Space Communications Complex (GDSCC)+h', 'Radar', 'Goldstone Solar System Radar+i']),
    ('Canberra',    ['Deep Space Network (DSN)+m', 'Canberra Deep Space Communications Complex (CDSCC)+h']),
    ('Madrid',      ['Deep Space Network (DSN)+m', 'Madrid Deep Space Communications Complex (MDSCC)+h']),
]

########################################################################################################################

