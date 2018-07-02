########################################################################################################################
# keywords.py
#
# To use:
#   from keywords import KEYWORDS
########################################################################################################################

# Format is (regular expression, (keywords)) where the keywords can contain string replacement patterns
# Keywords can have suffixes indicating the type of the keyword:
#   +t = Target
#   +T = Target Type
#   +p = Planet
#   +m = Mission
#   +i = Instrument

KEYWORDS = {}

KEYWORDS['General'] = [

# Target categories
    (r'[Aa]steroids{0,1}',                              ['Asteroid+T']),
    (r'[Cc]omets{0,1}',                                 ['Comet+T']),
    (r'(Jup|Jov|Sat|Ura|Nep).* [Rr]ings{0,1}',          ['Ring+T']),
    (r'[Rr]ings{0,1} .* (Jup|Jov|Sat|Ura|Nep)\w+',      ['Ring+T']),
    (r'[Mm]inor [Pp]lanet{0,1}',                        ['Asteroid+T']),
    (r'KBOs{0,1}',                                      ['TNO+T']),
    (r'Kuiper Belt',                                    ['TNO+T']),
    (r'(Trans-Neptunian|TNO|TNOs)',                     ['TNO+T']),

# Target names
    (r'([Ss]un)',                                       ['Sun+t+T']),
    (r'(Mercury|Mercurian)',                            ['Mercury+t+p', 'Planet+T']),
    (r'(Venus|Venusian)',                               ['Venus+t+p', 'Planet+T']),
    (r'([Ee]arth|[Tt]errestrial)',                      ['Earth+t+p', 'Planet+T']),
    (r'(Moon(?!s)|Lunar)',                              ['Moon+t', 'Satellite+T', 'Earth+p']),
    (r'(Mars(?![a-z])|Martian)',                        ['Mars+t+p', 'Planet+T']),
    (r'(Jupiter|[Jj]ovian|Io|Europa|Ganymede|Callisto)',['Jupiter+t+p', 'Planet+T']),
    (r'Galilean',                                       ['Jupiter+t+p', 'Planet+T']),
    (r'(Saturn|[Ss]aturnian|Kronian|Titan|Enceladus)',  ['Saturn+t+p', 'Planet+T']),
    (r'(Uranus|Uranian)',                               ['Uranus+t+p', 'Planet+T']),
    (r'(Neptune|Neptunian|Triton)',                     ['Neptune+t+p', 'Planet+T']),
    (r'(Pluto|Plutonian|Charon)',                       ['Pluto+t', 'Dwarf Planet+T']),
    (r'Ceres',                                          ['1 Ceres+t', 'Asteroid+T', 'Dwarf Planet+T']),
    (r'Pallas',                                         ['2 Pallas+t', 'Asteroid+T']),
    (r'Vesta',                                          ['4 Vesta+t', 'Asteroid+T']),
    (r'Eros',                                           ['433 Eros+t', 'Asteroid+T']),
    (r'Gaspra',                                         ['951 Gaspra+t', 'Asteroid+T']),
    (r'Lutetia',                                        ['21 Lutetia+t', 'Asteroid+T']),
    (r'Steins',                                         ['2867 Steins+t', 'Asteroid+T']),
    (r'Mathilde',                                       ['253 Mathilde+t', 'Asteroid+T']),
    (r'Toutatis',                                       ['4179 Toutatis+t', 'Asteroid+T']),
    (r'(MU69|Ultima)',                                  ['Ultima Thule+t', 'TNO+T', 'New Horizons+m']),
    (r'(Haumea|Makemake|Eris)',                         [r'$+t', 'TNO+T', 'Dwarf Planet+T']),

# Missions and Instruments
    (r'[Ii]nfra(|-)red|IR',                             ['Infrared']),
    (r'[Uu]ltra(|-)violet|UV|FUV',                      ['Ultraviolet']),
    (r'[Rr]adio',                                       ['Radio']),
    (r'RADAR',                                          ['RADAR+i']),
    (r'(HST|Hubble.*[Tt]elescope)',                     ['Hubble Space Telescope (HST)+m+h']),
    (r'(JWST|Webb.*[Tt]elescope)',                      ['James Webb Space Telscope (JWST)+m+h']),
    (r'(Voyager|Mariner|Pioneer)',                      [r'$+m']),
    (r'Jup.*Galileo',                                   [r'Galileo+m', r'Galileo Orbiter+h', 'Jupiter+p']),
    (r'Galileo.*Jup',                                   [r'Galileo+m', r'Galileo Orbiter+h', 'Jupiter+p']),
    (r'Cassini (?![Dd]ivision)',                        ['Cassini Orbiter+h', 'Cassini-Huygens+m']),   # don't match "Cassini Division"
    (r'New Horizons',                                   ['New Horizons+m+h']),
    (r'Juno',                                           ['Juno+m+h', 'Jupiter+p', 'Planet+T']),
    (r'Magellan',                                       ['Magellan+m', 'Venus+t+p', 'Planet+T']),
    (r'Messenger.*Mercury',                             ['Messenger+m', 'Mercury+t+p', 'Planet+T']),
    (r'Mercury.*Messenger',                             ['Messenger+m', 'Mercury+t+p', 'Planet+T']),
    (r'Dawn.*(Ceres|Vesta)',                            ['Dawn+m+h', 'Asteroid+T']),
    (r'(Ceres|Vesta).*Dawn',                            ['Dawn+m+h', 'Asteroid+T']),
    (r'Deep Impact',                                    ['Deep Impact+m+h']),
    (r'(Rosetta|Philae)',                               ['Rosetta+m+h', '67P/Churyumov-Gerasimenko+t', 'Comet+T']),
    (r'(?:Voyager|Pioneer|Mariner) (?:[1-9][0-9]*)',    [r'$+h']),
    (r'MAVEN',                                          [r'Mars Atmosphere and Volatile Evolution (MAVEN)+m+h', 'Mars+t', 'Planet+T']),
    (r'Mars Atmosphere and Volatile Evolution',         [r'Mars Atmosphere and Volatile Evolution (MAVEN)+m+h', 'Mars+t', 'Planet+T']),
    (r'Viking',                                         ['Viking+m', 'Mars+t+p', 'Planet+T']),
    (r'(Viking [12]).*[Oo]rbit',                        ['$ Orbiter+h']),
    (r'(Viking [12]).*[Ll]ander',                       ['$ Lander+h', 'Lander']),
    (r'(MGS|Mars Global Surveyor)',                     ['Mars Global Surveyor (MGS)+m+h', 'Mars+t+p', 'Planet+T']),
    (r'Mars Odyssey',                                   ['2001 Mars Odyssey+m', 'Mars+t', 'Planet+T']),
    (r'(MOC|Mars Orbiter Camera)',                      ['Mars Orbiter Camera (MOC)+i', 'Mars Global Surveyor (MGS)+m+h', 'Mars+t+p', 'Planet+T']),
    (r'(MSL|Curiosity|Mars [Ss]cience [Ll]aboratory)',  ['Mars Science Laboratory (MSL)+m+h', 'Mars+t+p', 'Planet+T', 'Rover']),
    (r'(MRO|Mars [Rr]econnaissance [Oo]rbiter)',        ['Mars Reconnaissance Orbiter (MRO)+m+h,', 'Mars+t+p', 'Planet+T']),
    (r'(MER|Opportunity|Spirit|Mars [Ee]xploration [Rr]over)',
                                                        ['Mars Exploration Rover (MER)+m', 'Mars+t', 'Planet+T', 'Rover']),
    (r'MER-A',                                          ['Spirit (MER-A)+h']),
    (r'MER-B',                                          ['Opportunity (MER-B)+h']),
    (r'(Mars [Ee]xpress|Beagle)',                       ['Mars Express+m', 'Mars+t', 'Planet+T']),
    (r'Mars [Pp]athfinder',                             ['Mars Pathfinder (MPF)+m', 'Mars+t', 'Planet+T', 'Lander']),
    (r'Mar(s|tian).*[Rr]over',                          ['Mars+t+p', 'Planet+T', 'Rover']),
    (r'[Rr]over.*Mar(s|tian)',                          ['Mars+t+p', 'Planet+T', 'Rover']),
    (r'Mar(s|tian).*[Ll]ander',                         ['Mars+t+p', 'Planet+T', 'Lander']),
    (r'[Ll]ander.*Mar(s|tian)',                         ['Mars+t+p', 'Planet+T', 'Lander']),
    (r'(NEAR|Near Earth Asteroid Rendezvous)',          ['NEAR Shoemaker+m', '433 Eros+t', 'Asteroid+T']),
    (r"Chang'e",                                        ["Chang'e+m", "Moon+t", "Satellite+T", "Earth+p"]),

# Other general keywords
    (r'[Ww]ater',                                       ['Water']),
    (r'[Mm]ethane',                                     ['Methane']),
    (r'[Aa]mmonia',                                     ['Ammonia']),
    (r'[Cc]raters{0,1}',                                ['Crater']),
    (r'([Mm]ountains{0,1}|Mons|Montes)',                ['Mountain']),
    (r'[Dd]ust',                                        ['Dust']),
    (r'[Dd]unes{0,1}',                                  ['Dune']),
    (r'[Hh]azes{0,1}',                                  ['Haze', 'Atmosphere']),
    (r'[Aa]tmospher(e|es|ic)',                          ['Atmosphere']),
    (r'[Pp]lumes{0,1}',                                 ['Plume']),
    (r'[Vv]olcan(o|os|oes|ism|ic)',                     ['Volcano']),
    (r'([Ss]torms{0,1}|[Rr]ed [Ss]pot|[Dd]ark [Ss]pot)',['Storm', 'Atmosphere']),
    (r'[Ss]hadows{0,1}',                                ['Shadow']),
    (r'[Oo]ccultations{0,1}',                           ['Occultation']),
    (r'[Ee]clipses{0,1}',                               ['Eclipse']),
    (r'[Mm]agnet(ism|ic|osphere)',                      ['Magnetosphere']),
    (r'[Mm]ap',                                         ['Map']),
]

# Keywords to search for if 'Mars' appears
KEYWORDS['Mars'] = [
    (r'Spirit',                                         ['Spirit (MER-A)+h']),
    (r'Opportunity',                                    ['Opportunity (MER-B)+h']),
]

# Keywords to search for if 'Jupiter' appears
KEYWORDS['Jupiter'] = [
    (r' [Rr]ing',                                       [r'Jupiter Rings+t', 'Ring+T']),
    (r'[Mm]ain [Rr]ings{0,1}',                          ['Main Ring+t', 'Ring+T']),
    (r'[Rr]ings{0,1} .*[Hh]alo',                        ['Halo+t', 'Ring+T']),
    (r'[Hh]alo .*[Rr]ings{0,1}',                        ['Halo+t', 'Ring+T']),
    (r'[Gg]ossamer',                                    ['Gossamer Ring+t', 'Ring+T']),
    (r'(Adrastea|Metis|Amalthea|Thebe)',                [r'$+t', 'Satellite+T']),
    (r'(Io|Europa|Ganymede|Callisto)',                  [r'$+t', 'Satellite+T']),
    (r'(Themisto|Leda|Himalia|Lysithea|Elara|Dia)',     [r'$+t', 'Satellite+T', 'Irregular+T']),
    (r'(Carpo|Euporie|Thelxinoe|Euanthe|Helike)',       [r'$+t', 'Satellite+T', 'Irregular+T']),
    (r'(Orthosie|Iocaste|Praxidike|Harpalyke|Mneme)',   [r'$+t', 'Satellite+T', 'Irregular+T']),
    (r'(Hermippe|Thyone|Ananke|Herse|Aitne|Kale)',      [r'$+t', 'Satellite+T', 'Irregular+T']),
    (r'(Taygete|Chaldene|Erinome|Aoede|Kallichore)',    [r'$+t', 'Satellite+T', 'Irregular+T']),
    (r'(Kalyke|Carme|Callirrhoe|Eurydome|Pasithee)',    [r'$+t', 'Satellite+T', 'Irregular+T']),
    (r'(Kore|Cyllene|Eukelade|Pasiphae|Hegemone)',      [r'$+t', 'Satellite+T', 'Irregular+T']),
    (r'(Arche|Isonoe|Sinope|Sponde|Autonoe|Megaclite)', [r'$+t', 'Satellite+T', 'Irregular+T']),
    ('S/20[0-9][0-9] *J *[1-9][0-9]*',                  [r'$+t', 'Satellite+T', 'Irregular+T']),
]

# Keywords to search for if 'Saturn' appears
KEYWORDS['Saturn'] = [
    (r'(?<!Cassini-)Huygens',                           ['Huygens Probe+h', 'Cassini-Huygens+m', 'Lander']), # not if it says "Cassini-Huygens"
    (r' [Rr]ing',                                       [r'Saturn Rings+t', 'Ring+T']),
    (r'([A-G])[- ][Rr]ing',                             [r'$ Ring+t', 'Ring+T']),
    (r'([A-G])-{0,1},{0,1} and [A-G][- ][Rr]ings',      [r'$ Ring+t', 'Ring+T']),
    (r'[A-G]-{0,1},{0,1} and ([A-G])[- ][Rr]ings',      [r'$ Ring+t', 'Ring+T']),
    (r'([A-G])-{0,1}, [A-G].{0,20} [A-G][- ][Rr]ings',  [r'$ Ring+t', 'Ring+T']),
    (r'Cassini [Dd]ivision',                            ['Cassini Division+t', 'Ring+T', 'Gap+T']),
    (r'Encke ([Dd]ivision|[Gg]ap)',                     ['Encke Gap+t', 'Ring+T', 'Gap+T']),
    ('(Pan|Daphnis|Atlas|Prometheus|Pandora)',          [r'$+t', 'Satellite+T']),
    ('(Epimetheus|Janus)',                              [r'$+t', 'Satellite+T']),
    ('(Aegaeon|Methone|Anthe|Pallene|Telesto)',         [r'$+t', 'Satellite+T']),
    ('(Calypso|Dione|Helene|Polydeuces)',               [r'$+t', 'Satellite+T']),
    ('(Mimas|Enceladus|Tethys|Dione|Rhea)',             [r'$+t', 'Satellite+T']),
    ('(Titan|Hyperion|Iapetus)',                        [r'$+t', 'Satellite+T']),
    ('Phoebe',                                          ['Phoebe+t', 'Satellite+T', 'Irregular+T']),
    ('(Kiviuq|Ijiraq|Paaliaq|Skathi|Albiorix|Bebhionn)',[r'$+t', 'Satellite+T', 'Irregular+T']),
    ('(Erriapus|Skoll|Siarnaq|Tarqeq|Greip|Hyrrokkin)', [r'$+t', 'Satellite+T', 'Irregular+T']),
    ('(Jarnsaxa|Tarvos|Mundilfari|Bergelmir|Narvi)',    [r'$+t', 'Satellite+T', 'Irregular+T']),
    ('(Suttungr|Hati|Farbauti|Thrymr|Aegir|Bestla)',    [r'$+t', 'Satellite+T', 'Irregular+T']),
    ('(Fenrir|Surtur|Kari|Ymir|Loge|Fornjot)',          [r'$+t', 'Satellite+T', 'Irregular+T']),
    (r'S/2004 *S *([36])',                              [r'S/2004 S $+t', 'Moonlet', 'Clump', 'F Ring+t']),
    (r'S/2004 *S *([1245789][0-9]*)',                   [r'S/2004 S $+t', 'Satellite+T', 'Irregular+T']),
    (r'(S/200[0-35-9]) *S *([1-9][0-9]*)',              [r'$+t', 'Satellite+T', 'Irregular+T']),
    (r'(S/20[1-9][0-9]) *S *([1-9][0-9]*)',             [r'$+t', 'Satellite+T', 'Irregular+T']),
]

# Keywords to search for if 'Uranus' appears
KEYWORDS['Uranus'] = [
    (r' [Rr]ing',                                       [r'Uranus Rings+t', 'Ring+T']),
    (r'[Zz]eta(, | | .{0,20} )[Rr]ings{0,1}',           ['Zeta Ring+t', 'Ring+T']),
    (r'(6|six|Six)(, | | .{0,20} )[Rr]ings{0,1}',       ['6 Ring+t', 'Ring+T']),
    (r'(5|five|Five)(, | | .{0,20} )[Rr]ings{0,1}',     ['5 Ring+t', 'Ring+T']),
    (r'(4|four|Four)(, | | .{0,20} )[Rr]ings{0,1}',     ['4 Ring+t', 'Ring+T']),
    (r'[Aa]lpha(, | | .{0,20} )[Rr]ings{0,1}',          ['Alpha Ring+t', 'Ring+T']),
    (r'[Bb]eta(, | | .{0,20} )[Rr]ings{0,1}',           ['Beta Ring+t', 'Ring+T']),
    (r'[Ee]ta(, | | .{0,20} )[Rr]ings{0,1}',            ['Eta Ring+t', 'Ring+T']),
    (r'[Gg]amma(, | | .{0,20} )[Rr]ings{0,1}',          ['Gamma Ring+t', 'Ring+T']),
    (r'[Dd]elta(, | | .{0,20} )[Rr]ings{0,1}',          ['Delta Ring+t', 'Ring+T']),
    (r'[Ll]ambda(, | | .{0,20} )[Rr]ings{0,1}',         ['Lambda Ring+t', 'Ring+T']),
    (r'[Ee]psilon(, | | .{0,20} )[Rr]ings{0,1}',        ['Epsilon Ring+t', 'Ring+T']),
    (r'[Nn]u(, | | .{0,20} )[Rr]ings{0,1}',             ['Nu Ring+t', 'Ring+T']),
    (r'[Mm]u(, | | .{0,20} )[Rr]ings{0,1}',             ['Mu Ring+t', 'Ring+T']),
    (r'(Cordelia|Ophelia|Bianca|Cressida|Desdemona)',   [r'$+t', 'Satellite+T']),
    (r'(Juliet|Portia|Rosalind|Cupid|Belinda)',         [r'$+t', 'Satellite+T']),
    (r'(Perdita|Puck|Mab)',                             [r'$+t', 'Satellite+T']),
    (r'(Miranda|Ariel|Umbriel|Titania|Oberon)',         [r'$+t', 'Satellite+T']),
    (r'(Francisco|Caliban|Stephano|Trinculo|Sycorax)',  [r'$+t', 'Satellite+T', 'Irregular+T']),
    (r'(Margaret|Prospero|Setebos|Ferdinand)',          [r'$+t', 'Satellite+T', 'Irregular+T']),
]

# Keywords to search for if 'Neptune' appears
KEYWORDS['Neptune'] = [
    (r' [Rr]ing',                                       [r'Neptune Rings+t', 'Ring+T']),
    (r'Adams .*[Rr]ings{0,1}',                          ['Adams Ring+t', 'Ring+T']),
    (r'Lassell',                                        ['Lassell Ring+t', 'Ring+T']),
    (r'Le {0,1}[Vv]errier',                             ['Leverrier Ring+t', 'Ring+T']),
    (r'Galle',                                          ['Galle Ring+t', 'Ring+T']),
    (r'Libert[ye] .*[Aa]rcs{0,1}',                      ['Liberte+t', 'Adams Ring+t', 'Ring+T', 'Arc+T']),
    (r'(Egalite|Equality) .*[Aa]rcs{0,1}',              ['Egalite+t', 'Adams Ring+t', 'Ring+T', 'Arc+T']),
    (r'Fraternit[ye] .*[Aa]rcs{0,1}',                   ['Fraternite+t', 'Adams Ring+t', 'Ring+T', 'Arc+T']),
    (r'Courage .*[Aa]rcs{0,1}',                         ['Courage+t', 'Adams Ring+t', 'Ring+T', 'Arc+T']),
    (r'(Naiad|Thalassa|Despina|Galatea|Larissa)',       [r'$+t', 'Satellite+T']),
    (r'S/2004 *N *1',                                   ['S/2004 N 1+t', 'Satellite+T']),
    (r'Proteus',                                        ['Proteus+t', 'Satellite+T']),
    (r'Triton',                                         ['Triton+t', 'Satellite+T']),
    (r'Nereid',                                         ['Nereid+t', 'Satellite+T', 'Irregular+T']),
    (r'(Halimede|Sao|Laomedeia|Psamathe|Neso)',         [r'$+t', 'Satellite+T', 'Irregular+T']),
]

# Keywords to search for if 'Pluto' appears
KEYWORDS['Pluto'] = [
    (r'(Charon|Styx|Nix|Kerberos|Hydra)',               [r'$+t', 'Satellite+T', 'Pluto+p']),
]

# Keywords to search for if 'Comet' appears
KEYWORDS['Comet'] = [
    (r'Borrelly',                                       ['19P/Borrelly+t']),
    (r'Wild',                                           ['81P/Wild+t']),
    (r'Halley',                                         ['1P/Halley+t']),
    (r'(Churyumov|Gerasimenko)',                        ['67P/Churyumov-Gerasimenko+t']),
    (r'(Giacobini|Zinner)',                             ['21P/Giacobini-Zinner+t']),
    (r'(Hartley)',                                      ['103P/Hartley+t']),
]

# Keywords to search for if 'Ring+T' appears
KEYWORDS['Ring'] = [
    (r'[Cc]lumps{0,1}',                                 ['Clump']),
    (r'[Gg]aps{0,1}',                                   ['Gap']),
    (r'[Pp]ropellers{0,1}',                             ['Propeller', 'Saturn+p', 'Ring+T']),
    (r'[Ww]aves{0,1}',                                  ['Wave']),
    (r'[Mm]oonlets{0,1}',                               ['Moonlet']),
]

# Keywords to search for if 'HST' appears
KEYWORDS['HST'] = [
    ('(ACS|Advanced Camera for Surveys)',               ['Advanced Camera for Surveys (ACS)+i', 'Visual']),
    ('(WFPC2|Wide[- ]Field[/ ]Planetary Camera(| 2))',  ['Wide Field/Planetary Camera 2 (WFPC2)+i', 'Visual', 'Infrared']),
    ('(NICMOS)',                                        ['Near Infrared Camera and Multi-Object Spectrometer (NICMOS)+i', 'Infrared']),
    ('(WFC|Wide[- ]Field Channel)',                     ['Advanced Camera for Surveys (ACS)+i', 'Wide Field Channel (WFC)+i', 'Visual', 'Infrared']),
    ('(HRC|High[- ]Resolution Channel)',                ['Advanced Camera for Surveys (ACS)+i', 'High-Resolution Channel (HRC)+i', 'Visual', 'Infrared']),
    ('(SBC|Solar[- ]Blind Channel)',                    ['Advanced Camera for Surveys (ACS)+i', 'Solar Blind Channel (SBC)+i', 'Ultraviolet']),
    ('(WFC3|Wide Field Camera 3)',                      ['Wide Field Camera 3 (WFC3)+i']),
    ('(WFC3|Wide Field Camera 3).*(UVIS|Ultra.*|ultra.*)',
                                                        ['Ultraviolet and Visual Channel (UVIS)+i', 'Visual', 'Ultraviolet']),
    ('(UVIS|[Uu]ltra).*(WFC3|Wide Field Camera 3)',     ['Ultraviolet and Visual Channel (UVIS)+i+i', 'Visual', 'Ultraviolet']),
    ('(WFC3|Wide Field Camera 3).*(IR|[Ii]nfra.*)',     ['Infrared Channel (IR)+i', 'Infrared']),
    ('(IR|[Ii]nfra).*(WFC3|Wide Field Camera 3)',       ['Infrared Channel (IR)+i', 'Infrared']),
]

# Keywords to search for if 'New Horizons' appears
KEYWORDS['New Horizons'] = [
    ('LORRI',                                           ['Long Range Reconnaissance Imager (LORRI)+i', 'Visual']),
    ('Long[- ][Rr]ange.*[Ii]mager',                     ['Long Range Reconnaissance Imager (LORRI)+i', 'Visual']),
    ('MVIC',                                            ['Multispectral Visible Imaging Camera (MVIC)+i', 'Visual', 'Infrared']),
    ('LEISA',                                           ['Linear Etalon Imaging Spectral Array (LEISA)+i', 'Infrared']),
    ('REX',                                             ['Radio Science Experiment (REX)+i', 'Radio']),
]

# Keywords to search for if 'Cassini' appears
KEYWORDS['Cassini-Huygens'] = [
    ('(ISS|Imaging Science Subsystem)',                 ['Imaging Science Subsystem (ISS)+i', 'Visual', 'Infrared']),
    ('([Ww]ide[- ][Aa]ngle)',                           ['Imaging Science Subsystem (ISS) Wide Angle Camera+i', 'Visual', 'Infrared']),
    ('([Nn]arrow[- ][Aa]ngle)',                         ['Imaging Science Subsystem (ISS) Narrow Angle Camera+i', 'Visual', 'Infrared']),
    ('(VIMS|Visual.{1,20}[Ss]pectrometer)',             ['Visual and Infrared Mapping Spectrometer (VIMS)+i', 'Visual', 'Infrared']),
    ('(UVIS|Ultra.{1,20}[Ss]pectrometer)',              ['Ultraviolet Imaging Spectrometer (UVIS)+i', 'Ultraviolet']),
    ('(CIRS|Composite.{1,20}[Ss]pectrometer)',          ['Composite Infrared Spectrometer (CIRS)+i', 'Infrared']),
    ('(RSS|Radio.{1,20}[Ss]ubsystem)',                  ['Radioscience Subsystem (RSS)+i', 'Radio']),
    ('(CDA|Dust ([Dd]etector|[Aa]nalyzer))',            ['Cosmic Dust Analzer (CDA)+i', 'Dust']),
    ('(INMS|Ion (?:|&|and) Neutral Mass Spectrometer)', ['Ion and Neutral Mass Spectrometer (INMS)+i']),
    ('(MIMI|Magnetospheric Imaging Instrument)',        ['Magnetospheric Imaging Instrument (MIMI)+i']),
]

# Keywords to search for if 'Voyager' appears
KEYWORDS['Voyager'] = [
    ('(ISS|Imaging Science Subsystem)',                 ['Imaging Science Subsystem (ISS)+i', 'Visual']),
    ('([Ww]ide[- ][Aa]ngle)',                           ['Imaging Science Subsystem (ISS) Wide Angle Camera+i', 'Visual']),
    ('([Nn]arrow[- ][Aa]ngle)',                         ['Imaging Science Subsystem (ISS) Narrow Angle Camera+i', 'Visual']),
    ('(PPS|[Pp]otopolarimeter)',                        ['Photopolarimeter Subsystem (PPS)+i', 'Ultraviolet']),
    ('(UVS|Ultra.{1,20}[Ss]pectrometer)',               ['Ultraviolet Spectrometer (UVS)+i', 'Ultraviolet']),
    ('(RSS|Radio.{1,20}[Ss]ubsystem)',                  ['Radioscience Subsystem (RSS)+i', 'Radio']),
]

# Keywords to search for if 'Juno' appears
KEYWORDS['Juno'] = [
    ('Juno[Cc]am',                                      ['JunoCam+i', 'Visual']),
    ('(JIRAM|Jovian .{10,30}Mapper)',                   ['Jupiter Infrared and Auroral Mapper (JIRAM)+i', 'Infrared']),
]

########################################################################################################################

