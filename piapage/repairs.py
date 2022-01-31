################################################################################

import re
from gallerypage import GalleryPage

def repair_tables(missions, hosts, instruments, targets, systems):
    """Replace weird values in the PIA tables."""

    #### Always ensure that each list has at least one element, possibly blank

    if 'Sol' in systems[0]:
        systems[0] = ''

    if 'Unknown' in systems[0]:
        systems[0] = ''

    if 'Sol' in targets[0]:
        targets[0] = 'Sun'
        systems[0] = 'Sun'

    if 'Rosetta' in missions:
        if targets[0] == 'Comet':
            targets[0] = '67P/Churyumov-Gerasimenko'

    if missions[0] == 'Magellan' and len(hosts) > 1:
        if 'Magellan' in hosts[1:]:
            hosts.remove('Magellan')
            hosts = ['Magellan'] + hosts

        if 'Arecibo Observatory' in hosts:
            if 'Arecibo' in instruments[0]:
                instruments = instruments[1:] + [instruments[0]]

    if missions[0] == 'Magellan' and 'Radar System' in instruments:
        k = instruments.index('Radar System')
        instruments[k] = 'Imaging Radar'

        if 'Pioneer Venus Orbiter' in hosts:
            instruments.append('Surface Radar Mapper (ORAD)')

    if 'Dawn' in missions and 'Field Experiment' in hosts:
        hosts = ['Dawn']

    if 'Mars Pathfinder (MPF)' in missions and 'Field Experiment' in hosts:
        hosts.remove('Field Experiment')
        hosts = hosts or ['']

    if 'Hubble Space Telescope' in instruments:
        instruments.remove('Hubble Space Telescope')
        instruments = instruments or ['']
        if not hosts[0]:
            hosts[0] = 'Hubble Space Telescope'

    if ('MESSENGER' in missions and \
        'Gamma-ray Spectrometer (GRS)' in instruments):
            k = instruments.index('Gamma-ray Spectrometer (GRS)')
            instruments[k] = 'Gamma-Ray and Neutron Spectrometer (GRNS)'

    if ('MESSENGER' in missions and \
        'Neutron Spectrometer' in instruments):
            k = instruments.index('Neutron Spectrometer')
            instruments[k] = 'Gamma-Ray and Neutron Spectrometer (GRNS)'

    if ('2001 Mars Odyssey' in missions and \
        'Neutron Spectrometer' in instruments):
            k = instruments.index('Neutron Spectrometer')
            instruments[k] = 'Gamma-Ray Spectrometer (GRS)'

    if 'Mars Volcanic Emission Life Scout (MARVEL)' in instruments:
        instruments.remove('Mars Volcanic Emission Life Scout (MARVEL)')
        instruments = instruments or ['']
        if not hosts[0]:
            hosts[0] = 'MARVEL'

    if 'VIRTIS' in instruments and 'Venus Express' in hosts:
        hosts.remove('Venus Express')
        hosts = ['Venus Express'] + hosts

    if 'Cassini-Huygens' in missions and \
       'Infrared Spectrometer' in instruments:
            k = instruments.index('Infrared Spectrometer')
            instruments[k] = 'Composite Infrared Spectrometer (CIRS)'

    if 'Cassini-Huygens' in missions and \
       'Infrared Spectrometer (IRS)' in instruments:
            k = instruments.index('Infrared Spectrometer (IRS)')
            instruments[k] = 'Composite Infrared Spectrometer (CIRS)'

    if 'Perseverance' in missions:
        k = missions.index('Perseverance')
        missions[k] = 'Mars 2020'
        if 'Perseverance' not in hosts:
            if hosts[0]:
                hosts = ['Perseverance'] + hosts
            else:
                hosts[0] = 'Perseverance'

    if 'Kepler' in missions and not 'Kepler' in hosts:
        hosts.append('Kepler')

    if 'Psyche' == missions[0]:
        if 'Asteroid' in targets:
            k = targets.index('Asteroid')
            targets[k] ='16 Psyche'

    if ('WISE' in missions[0] or 'WISE' in hosts[0]
        or 'WISE' in instruments[0]):
            found = False
            for k,mission in enumerate(missions):
                if 'WISE' in mission:
                    missions[k] = 'Near-Earth Object Wide-field Infrared Survey Explorer (NEOWISE)'
                    found = True
                    break
            if not found:
                missions.append('Near-Earth Object Wide-field Infrared Survey Explorer (NEOWISE)')

            found = False
            for k,host in enumerate(hosts):
                if 'WISE' in host:
                    hosts[k] = 'NEOWISE'
                    found = True
                    break
            if not found:
                hosts.append('NEOWISE')

            found = False
            for k,inst in enumerate(instruments):
                if 'WISE' in inst:
                    instruments[k] = 'NEOWISE Telescope'
                    found = True
                    break
            if not found:
                hosts.append('NEOWISE Telescope')

    if 'NEAR' in missions[0]:
        missions[0] = 'NEAR Shoemaker'

    if 'New Horizons' == missions[0]:
        if 'Kuiper Belt Object' in targets:
            k = targets.index('Kuiper Belt Object')
            targets[k] ='486958 Arrokoth'

    if targets[0] == 'teins' or targets[0][1:] == 'teins':
        targets[0] = '2867 &Scaron;teins'

    if 'Visible Light' in instruments:
        instruments.remove('Visible Light')
        if not instruments:
            instruments = ['']

    if 'Ultraviolet Light' in instruments:
        instruments.remove('Ultraviolet Light')
        if not instruments:
            instruments = ['']

    return (missions, hosts, instruments, targets, systems)

NOT_PLANETARY = [
    'PIA01829',
    'PIA01836',
    'PIA01918',
    'PIA02587',
    'PIA03048',
    'PIA03244',
    'PIA03375',
    'PIA03420',
    'PIA04302',
    'PIA04935',
    'PIA04939',
    'PIA04940',
    'PIA08040',
    'PIA08041',
    'PIA08042',
    'PIA09072',
    'PIA09178',
    'PIA09194',
    'PIA09267',
    'PIA10111',
    'PIA10926',
    'PIA11062',
    'PIA11163',
    'PIA11376',
    'PIA11447',
    'PIA11726',
    'PIA11726',
    'PIA11749',
    'PIA12110',
    'PIA13005',
    'PIA13102',
    'PIA13111',
    'PIA13112',
    'PIA13119',
    'PIA13216',
    'PIA13217',
    'PIA13358',
    'PIA13440',
    'PIA13450',
    'PIA14038',
    'PIA14100',
    'PIA14108',
    'PIA14403',
    'PIA14720',
    'PIA14722',
    'PIA15420',
    'PIA15481',
    'PIA15482',
    'PIA15637',
    'PIA15806',
    'PIA15909',
    'PIA16022',
    'PIA16024',
    'PIA16438',
    'PIA16601',
    'PIA16604',
    'PIA16613',
    'PIA16689',
    'PIA16690',
    'PIA16885',
    'PIA16886',
    'PIA16839',
    'PIA17552',
    'PIA17553',
    'PIA17562',
    'PIA17834',
    'PIA17991',
    'PIA17992',
    'PIA17997',
    'PIA18001',
    'PIA18003',
    'PIA18004',
    'PIA18013',
    'PIA18164',
    'PIA18168',
    'PIA18452',
    'PIA18846',
    'PIA19318',
    'PIA19333',
    'PIA19339',
    'PIA19341',
    'PIA20027',
    'PIA20055',
    'PIA20060',
    'PIA20064',
    'PIA20065',
    'PIA20583',
    'PIA20699',
    'PIA20912',
    'PIA20914',
    'PIA21073',
    'PIA21075',
    'PIA21090',
    'PIA21114',
    'PIA21474',
    'PIA21752',
    'PIA22084',
    'PIA22350',
    'PIA22351',
    'PIA22352',
    'PIA22353',
    'PIA22358',
    'PIA22359',
    'PIA23409',
    'PIA23588',
    'PIA24432',
    'PIA24434',
    'PIA24573',
    'PIA24578',
    'PIA24868',
]

EXCLUDED_MISSIONS = set([
    'Aqua',
    'Aura',
    'FINESSE',
    'GALEX',
    'GRACE',
    'NuSTAR',
    'SRTM',
    'Terra',
    'UAVSAR',
])

# Listed keywords are removed
# If a keyword begins with "+", it is retained
# A keyword beginning with "=" requires an exact match, so "=Planet" does not remove "Dwarf Planet"
# A keyword beginning with "t=" requires an exact match under targets, so "t=Jupiter" does not remove system Jupiter
# A keyword beginning with "T=" requires an exact match under target types
# A keyword beginning with "t+value" adds "value" as a target
# A keyword beginning with "T+value" adds "value" as a target type

REMOVALS = {
    'PIA00012': ('Mercury', 'Moon', 'Earth'),
    'PIA00067': ('Moon', 'Earth', 'Satellite'),
    'PIA00078': ('Ida',),
    'PIA00129': ('Titan', 'Saturn'),
    'PIA00143': ('Jupiter', 'Saturn', 'Neptune'),
    'PIA00209': ('Mars',),
    'PIA00273': ('Mars',),
    'PIA00299': ('Main Belt', 's+Main Belt'),
    'PIA00351': ('Mercury', 'Moon'),
    'PIA00352': ('Mercury', 'Moon'),
    'PIA00357': ('Halo', 'Ring'),
    'PIA00442': ('Neptune', 'Planet'),
    'PIA00457': ('Mars', 'Mercury'),
    'PIA00496': ('Jupiter', 'Mars'),
    'PIA00514': ('Shoemaker', 'Comet', 'Voyager', 'Flyby Spacecraft'),
    'PIA00549': ('Shoemaker', 'Comet', 'Voyager', 'Flyby Spacecraft'),
    'PIA00581': ('Shoemaker', 'Comet', 'Voyager', 'Flyby Spacecraft'),
    'PIA00726': ('Neptune', 'Uranus', 'Saturn', 'Venus', 'Voyager'),
    'PIA00728': ('Gaspra', 'Main Belt', 'Asteroid', 't+Jupiter', 's+Earth', 's+Jupiter', 'T+Planet'),
    'PIA00825': ('Mars', 'Planet'),
    'PIA00854': ('Shoemaker', 'Comet', 'Voyager', 'Flyby Spacecraft'),
    'PIA01195': ('Titan', 'Saturn', 'Satellite'),
    'PIA01197': ('Titan', 'Saturn', 'Satellite'),
    'PIA01225': ('Halo', 'Ring'),
    'PIA01289': ('Jupiter', 'Planet'),
    'PIA01291': ('Jupiter', 'Planet'),
    'PIA01319': ('Comet',),
    'PIA01400': ('Mercury',),
    'PIA01465': ('Mars', 'Mercury'),
    'PIA01480': ('s+Jupiter', 's+Saturn', 's+Uranus', 's+Neptune', 't+Jupiter', 't+Saturn', 't+Uranus', 't+Neptune', 'T+Planet'),
    'PIA01510': ('Mars', 'Mercury'),
    'PIA01514': ('Mars', 'Mercury'),
    'PIA01606': ('Shoemaker', 'Comet', 'Voyager', 'Flyby Spacecraft'),
    'PIA01969': ('Jupiter', 'Neptune', 'Uranus'),
    'PIA01970': ('Mars', 'Mercury', 'Moon'),
    'PIA01987': ('Mercury', 'Moon'),
    'PIA02107': ('T+Comet', 'Exoplanet'),
    'PIA02234': ('Mars', 'Venus'),
    'PIA02236': ('Moon', 'Venus', 'Satellite'),
    'PIA02237': ('Moon', 'Venus', 'Satellite'),
    'PIA02441': ('Mercury', 'Venus'),
    'PIA02442': ('Mercury', 'Venus'),
    'PIA02449': ('Mercury', 'Mars', 'Voyager', 'Viking', 'Ida', 'Gaspra', 'Near Earth Objects', 'Eros', 'Camera'),
    'PIA02478': ('Ida',),
    'PIA02490': ('Uranus', 'Planet'),
    'PIA02588': ('Saturn',),
    'PIA02592': ('Saturn', 'Moon', 'Earth'),
    'PIA02593': ('Mercury',),
    'PIA02821': ('Saturn',),
    'PIA02826': ('Mercury', 'Moon'),
    'PIA02837': ('Mercury', 'Moon', 'Earth', 'Voyager', 'Flyby Spacecraft'),
    'PIA02862': ('Pluto', 'Dwarf Planet', 'Saturn', 'Mercury', 'Titan', 'Galileo', 'Voyager', 'Flyby', 'Kuiper Belt', 'KBO'),
    'PIA02885': ('Wild', 'Comet'),
    'PIA02886': ('Wild', 'Comet'),
    'PIA03139': ('Ida', 'Gaspra', 'Main Belt'),
    'PIA03153': ('Pluto', 'Dwarf Planet', 'Kuiper Belt', 'KBO'),
    'PIA03245': ('Earth', 't+81P/Wild', 'T+Comet', 's+Periodic Comets'),
    'PIA03247': ('Earth', 't+81P/Wild', 'T+Comet', 's+Periodic Comets'),
    'PIA03248': ('Earth', 't+81P/Wild', 'T+Comet', 's+Periodic Comets'),
    'PIA03249': ('Earth', 't+81P/Wild', 'T+Comet', 's+Periodic Comets'),
    'PIA03451': ('Saturn',),
    'PIA03473': ('Saturn',),
    'PIA03474': ('Saturn',),
    'PIA03476': ('Saturn', 'Moon', 'Earth'),
    'PIA03478': ('Saturn',),
    'PIA03520': ('Cygnus',),
    'PIA03521': ('Cygnus', 'Jupiter', 'Saturn', 'Planet'),
    'PIA03652': ('Jupiter', 'Neptune', 'Uranus', 'Ring', 'Asteroid', 'Comet', 'Planet'),
    'PIA03793': ('Mercury', 'Moon', 'Venus'),
    'PIA03832': ('Neptune',),
    'PIA04529': ('Mercury', 'Venus'),
    'PIA04531': ('Mercury', 'Venus'),
    'PIA04532': ('Mercury',),
    'PIA04603': ('Mercury',),
    'PIA04729': ('Moon', 'Venus'),
    'PIA04942': ('Asteroid', 'Comet'),
    'PIA04943': ('Jupiter', 'Neptune', 'Asteroid', 'Kuiper Belt', 'KBO', 'Planet'),
    'PIA05386': ('Jupiter',),
    'PIA05391': ('Jupiter',),
    'PIA05417': ('Jupiter',),
    'PIA05557': ('Phobos',),
    'PIA05565': ('Mars', 'Mercury', 'Venus', 'Pluto', 'Asteroid', 'Planet', 'T=', 'T+Dwarf Planet'),
    'PIA05567': ('Moon', 'Satellite'),
    'PIA05569': ('Jupiter', 'Mars', 'Planet', 'Asteroid'),
    'PIA05842': ('Mercury',),
    'PIA05843': ('Mercury',),
    'PIA05981': ('Jupiter',),
    'PIA05982': ('Jupiter',),
    'PIA06064': ('Jupiter',),
    'PIA06073': ('Neptune', 'Kuiper', 'Comet', 'KBO'),
    'PIA06082': ('Jupiter',),
    'PIA06083': ('Jupiter',),
    'PIA06145': ('Jupiter', 'Mars', 'Saturn', 'Jupiter'),
    'PIA06170': ('Callisto', 'Jupiter', 'Ganymede', 'Voyager', 'Galileo'),
    'PIA06171': ('Callisto', 'Jupiter', 'Mars'),
    'PIA06177': ('Neptune', 'Uranus'),
    'PIA06196': ('Jupiter',),
    'PIA06400': ('Neptune', 'Kuiper', 'Comet', 'KBO', 'Asteroid'),
    'PIA06514': ('Jupiter',),
    'PIA06539': ('Epsilon Ring', 'Uranus', 'Voyager'),
    'PIA06592': ('Jupiter',),
    'PIA06821': ('Callisto', 'Jupiter', 'Satellite', 'Titan', 'Saturn'),
    'PIA06822': ('Prometheus', 'Titan'),
    'PIA06827': ('Io', 'Jupiter', 'Satellite'),
    'PIA06828': ('Europa', 'Jupiter', 'Satellite'),
    'PIA06829': ('Satellite', 'Dwarf Planet', 'Pluto', 'Moon', 'Charon', 'Kuiper Belt', 'KBO'),
    'PIA06830': ('Mathilde', 'Asteroid', 'Main Belt', 't+Mars', 'T+Planet', 'm+2001 Mars Odyssey', 'h+Mars Odyssey'),
    'PIA06831': ('Ida', 'Asteroid', 'Main Belt', 't+Mars', 'T+Planet', 'm+2001 Mars Odyssey', 'h+Mars Odyssey'),
    'PIA06833': ('Gaspra', 'Asteroid', 'Main Belt', 't+Mars', 'T+Planet', 'm+2001 Mars Odyssey', 'h+Mars Odyssey'),
    'PIA06842': ('Venus',),
    'PIA06847': ('Jupiter', 'Satellite', 'Ganymede', 'Titan', 'Saturn'),
    'PIA07094': ('Jupiter', 'Io'),
    'PIA07098': ('Kuiper Belt', 'Comet', 'KBO'),
    'PIA07099': ('Comet', 'KBO', 'Kuiper', 'T+Exoplanet'),
    'PIA07217': ('Dwarf Planet', 'Kuiper Belt', 'KBO'),
    'PIA07218': ('Pluto', 'Dwarf Planet', 'Kuiper Belt', 'KBO'),
    'PIA07222': ('Mars', 'Jupiter', 'Planet'),
    'PIA07490': ('Jupiter', 'Planet', 'T+Exoplanet'),
    'PIA07518': ('Jupter',),
    'PIA07583': ('Mercury', 'Moon'),
    'PIA07672': ('Jupiter',),
    'PIA07805': ('Neptune',),
    'PIA07878': ('M11',),
    'PIA07852': ('Pluto', 'Asteroid', 'Comet', 'Dwarf Planet', 'Kuiper Belt', 'KBO', 's=', 'Hale-Bopp'),
    'PIA07961': ('Callisto', 'Ganymede', 'Jupiter'),
    'PIA08003': ('Pluto',),
    'PIA08006': ('Jupiter', 'Planet'),
    'PIA08060': ('Mercury', 'Venus'),
    'PIA08323': ('Neptune',),
    'PIA08324': ('Neptune',),
    'PIA08327': ('Neptune',),
    'PIA08452': ('73P/Schwassman-Wachmann',),   # mis-spelling
    'PIA08566': ('Halley', 'Comet'),
    'PIA08567': ('Halley', 'Comet'),
    'PIA08753': ('Viking', 'Voyager', 'Flyby'),
    'PIA08754': ('Viking', 'Voyager', 'Flyby'),
    'PIA08943': ('Mercury',),
    'PIA09117': ('Jupiter', 'Saturn', 'Planet', 'T+Exoplanet'),
    'PIA09227': ('Dwarf Planet', 'Planet', 'Pluto', 'Jupiter', 'T+Exoplanet', 'Kuiper Belt', 'KBO'),
    'PIA09228': ('Comet', 'Asteroid', 'T+Exoplanet'),
    'PIA09229': ('Comet', 'Asteroid', 'T+Exoplanet'),
    'PIA09231': ('Pluto', 'Dwarf Planet', 'Kuiper Belt', 'KBO'),
    'PIA09237': ('Mercury',),
    'PIA09238': ('Mercury',),
    'PIA09239': ('Mercury',),
    'PIA09242': ('Mercury',),
    'PIA09247': ('Pluto', 'Dwarf Planet', 'Kuiper Belt', 'KBO'),
    'PIA09248': ('Pluto', 'Dwarf Planet', 'Kuiper Belt', 'KBO'),
    'PIA09252': ('Pluto', 'Dwarf Planet', 'Kuiper Belt', 'KBO'),
    'PIA09254': ('Pluto', 'Dwarf Planet', 'Kuiper Belt', 'KBO'),
    'PIA09258': ('Pluto', 'Dwarf Planet', 'Kuiper Belt', 'KBO'),
    'PIA09264': ('Pluto', 'Dwarf Planet', 'Kuiper Belt', 'KBO'),
    'PIA09352': ('Pluto', 'Dwarf Planet', 'Kuiper Belt', 'KBO'),
    'PIA09378': ('Jupiter', 'Venus', 'Saturn', 'Planet', 'Satellite'),
    'PIA09700': ('Venus',),
    'PIA09910': ('Jupiter',),
    'PIA09911': ('Exoplanet',),
    'PIA09939': ('Hydra', 'Jupiter', 'Mars', 'Pluto', 'Asteroid', 'Comet', 'Planet', 'Kuiper Belt', 'KBO'),
    'PIA10099': ('Pluto', 'Dwarf Planet', 'Kuiper Belt', 'KBO'),
    'PIA10100': ('Pluto', 'Dwarf Planet', 'Kuiper Belt', 'KBO'),
    'PIA10107': ('Jupiter', 'Pluto', 'Saturn', 'Uranus', 'Planet', 'Kuiper Belt', 'KBO', 's='),
    'PIA10118': ('Mercury', 'Pluto', 'Dwarf Planet', 'Kuiper Belt', 'KBO', 'Planet'),
    'PIA10125': ('Moon',),
    'PIA10246': ('Exoplanet',),
    'PIA10249': ('Pluto', 'Dwarf Planet', 'Galileo', 'Cassini', 'Probe', 'Kuiper Belt', 'KBO'),
    'PIA10418': ('Venus',),
    'PIA10544': ('Jupiter', 'Asteroid',),
    'PIA10635': ('Mars', 'Venus', 'Moon', 'Earth', 'Satellite'),
    'PIA11228': ('Jupiter', 'Planet', 'Asteroid'),
    'PIA11375': ('Jupiter', 'Uranus', 'Asteroid', 'Kuiper', 'Comet', 'KBO', 'Planet'),
    'PIA11376': ('Jupiter', 'Uranus', 'Asteroid', 'Kuiper', 'Comet', 'KBO', 'Planet'),
    'PIA11390': ('Comet',),
    'PIA11735': ('Asteroid', 'T+Exoplanet'),
    'PIA11747': ('Jupiter', 'Planet',),
    'PIA11800': ('Jupiter', 'Planet', 'T+Exoplanet'),
    'PIA11986': ('T+Exoplanet',),
    'PIA12008': ('Comet',),
    'PIA12038': ('Jupiter',),
    'PIA12066': ('Cepheus',),
    'PIA12067': ('Carina',),
    'PIA12221': ('Tempel', 'Comet', 't+Moon', 'T+Moon', 's+Earth', 'T+Comet'),
    'PIA12256': ('Titan',),
    'PIA12336': ('Pluto', 'Planet', 'Neptune', 'Comet', 'Kuiper Belt', 'KBO', 's='),
    'PIA12375': ('Saturn', 'Comet', 't+Heliosphere', 'T+Heliosphere', 's+Solar System'),
    'PIA12826': ('Jupiter',),
    'PIA12854': ('Exoplanet',),
    'PIA12855': ('Exoplanet',),
    'PIA13054': ('Neptune', 'Planet'),
    'PIA13110': ('Near Earth Objects',),
    'PIA13115': ('2007 VG119', 'Asteroid'),
    'PIA13457': ('Catalina', 'Halley', 'Near Earth Objects', 'Asteroid'),
    'PIA13546': ('Exoplanet',),
    'PIA13568': ('Tempel',),
    'PIA13764': ('Ring',),
    'PIA13765': ('Ring',),
    'PIA13829': ('Jupiter', 'Planet'),
    'PIA13890': ('Ceres', 'Dwarf Planet'),
    'PIA14079': ('Mars', 'Venus'),
    'PIA14100': ('Comet',),
    'PIA14251': ('Quixote', 'Main Belt', 'Asteroid', 'Comet', 't+Mars', 'T+Planet'),
    'PIA14316': ('Lutetia',),
    'PIA14734': ('Comet',),
    'PIA14850': ('Mars', 'Venus'),
    'PIA14870': ('Comet',),
    'PIA14935': ('Mercury', 'Mars'),
    'PIA15019': ('Comet',),
    'PIA15420': ('Uranus', 'Neptune', 'Planet'),
    'PIA15425': ('Comet',),
    'PIA15485': ('Tempel', 'Probe', 'Comet', 'Deep Impact'),
    'PIA15621': ('Neptune', 'Planet'),
    'PIA15622': ('Neptune', 'Planet', 'Hubble'),
    'PIA15623': ('Mercury', 'Neptune'),
    'PIA15629': ('Comet',),
    'PIA15800': ('Comet', 'm=Exoplanet', 'T+Exoplanet'),
    'PIA15808': ('Neptune', 'Planet'),
    'PIA15820': ('Exoplanet', 't+Venus', 'T+Planet', 't+Sun', 'T+Sun'),
    'PIA16033': ('Jupiter', 'Planet', 'Fomalhaut'),
    'PIA16115': ('Ida', 'Ceres'),
    'PIA16165': ('Venus',),
    'PIA16211': ('Near Earth Objects', 's+Trojans'),
    'PIA16212': ('Jupiter', 'Planet', 'Asteroid', 'T+Exoplanet'),
    'PIA16467': ('Comet',),
    'PIA16636': ('t=Jupiter', 't=Saturn', 'Planet', 'T+Satellite', 't+Europa', 't+Enceladus'),
    'PIA16666': ('Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune'),
    'PIA16823': ('Venus',),
    'PIA16888': ('T+Exoplanet',),
    'PIA17041': ('Mars', 'Planet'),
    'PIA17046': ('Neptune', 'Comet'),
    'PIA17178': ('Neptune',),
    'PIA17251': ('C/2012 S1 (Comet ISON)',),
    'PIA17304': ('Sun', 's=Jupiter', 's+Solar System'),
    'PIA17308': ('Neptune', 't=Kuiper Belt'),
    'PIA17457': ('Venus',),
    'PIA17550': ('Comet', 'Asteroid', 'T+Exoplanet'),
    'PIA17795': ('Churymov',),      # spelling error in caption
    'PIA17796': ('Churymov',),      # spelling error in caption
    'PIA17801': ('Pluto',),
    'PIA17848': ('T+Exoplanet',),
    'PIA17990': ('Pluto', 'Saturn', 'T+KBO', 's+Kuiper Belt'),
    'PIA17998': ('t=Exoplanet', 'Jupiter', 'Planet'),
    'PIA18153': ('Mars', 'Planet'),
    'PIA18281': ('Exoplanet', 's+Saturn'),
    'PIA18291': ('Exoplanet', 'Kepler', 'Space Telescope', 's+Saturn'),
    'PIA18306': ('Uranus',),
    'PIA18365': ('Mercury',),
    'PIA18402': ('Churnyumov',),    # spelling error in caption
    'PIA18411': ('Pluto', 'KBO', 'Dwarf Planet', 'Kuiper Belt'),
    'PIA18423': ('Gerasimernko',),  # spelling error in caption
    'PIA18441': ('Mars', 'Moon', 'Titan', 'Venus'),
    'PIA18837': ('Planet', 'Neptune', 'T+Exoplanet'),
    'PIA18838': ('T+Exoplanet',),
    'PIA19055': ('Mars', 'Venus'),
    'PIA19101': ('Mercury', 'Venus'),
    'PIA19344': ('Neptune',),
    'PIA20040': ('Comet'),
    'PIA20053': ('Comet',),
    'PIA20068': ('Moon', 'Satellite'),
    'PIA20118': ('Near Earth Objects', 'Asteroid'),
    'PIA20119': ('Near Earth Objects', 'Asteroid'),
    'PIA20201': ('Neptune', 'Voyager'),
    'PIA20202': ('Neptune', 'Voyager'),
    'PIA20208': ('Pluto', 'Triton', 'Neptune', 'Satellite', 'Dwarf Planet', 'Kuiper Belt', 'KBO'),
    'PIA20279': ('2003 SD2020',),
    'PIA20336': ('Neptune', 'Triton', 'Voyager'),
    'PIA20503': ('Mars', 'Venus'),
    'PIA20546': ('Mercury', 'Venus'),
    'PIA20641': ('Mercury', 'Venus'),
    'PIA20692': ('Neptune',),
    'PIA21024': ('Pluto', 'Dwarf Planet'),
    'PIA21090': ('Neptune', 'Uranus'),
    'PIA21422': ('Europa', 'Io', 'Jupiter', 'Neptune', 'Planet', 'Satellite', 't+TRAPPIST-1', 's+TRAPPIST-1'),
    'PIA21440': ('t+Saturn',),
    'PIA21468': ('Europa', 'Io', 'Jupiter', 'Neptune', 'Planet', 'Satellite', 't+TRAPPIST-1', 'Transiting Planets', 's+TRAPPIST-1'),
    'PIA21589': ('t=', 't+Pluto', 's+Pluto', 'T+Dwarf Planet', 's+Kuiper Belt', 'T+KBO', 't+486958 Arrokoth'),
    'PIA21629': ('Voyager', 'Mercury', 'Pluto', 'Uranus', 'Dwarf Planet', 'Kuiper Belt', 'KBO'),
    'PIA21712': ('Impact', 'Atmosphere'),
    'PIA21944': ('Ring', 'Mercury' 'Asteroid', 'Uranus', 'Planet', 'Voyager'),
    'PIA22075': ('Mercury',),
    'PIA22088': ('Neptune', 'Planet'),
    'PIA22233': ('Exoplanet', 't+Mars', 'T+Planet'),
    'PIA22565': ('Jupiter', 'Planet'),
    'PIA22566': ('Pluto', 'Planet', 't+Heliosphere', 'T+Heliosphere', 's+Solar System', 'Kuiper Belt', 'KBO'),
    'PIA22648': ('Mercury',),
    'PIA22835': ('Pluto', 'Dwarf Planet', 'KBO', 'Kuiper Belt', 's='),
    'PIA22916': ('t+Heliosphere', 'T+Heliosphere', 's+Solar System'),
    'PIA22921': ('Neptune', 'Planet'),
    'PIA22924': ('t+Heliosphere', 'T+Heliosphere', 's+Solar System'),
    'PIA23003': ('Neptune', 'Planet', 't+K2-138', 's+K2-138'),
    'PIA23004': ('Neptune', 'Planet'),
    'PIA23165': ('Asteroid', 'Near Earth Objects'),
    'PIA23214': ('Goldstone',),
    'PIA23433': ('t=Saturn', 'T=Planet'),
    'PIA23435': ('t=Saturn', 'T=Planet'),
    'PIA23443': ('Venus', 'Mercury'),
    'PIA23462': ('t=', 'C/2019 Q4'),
    'PIA23497': ('Juno', 't+Moon', 'T+Satellite', 's+Earth'),
    'PIA23589': ('Near Earth', 't='),
    'PIA23617': ('Goldstone',),
    'PIA23681': ('Sun', 't+Jupiter', 't+Saturn', 't+Uranus', 't+Neptune', 'T+Planet', 's+Solar System'),
    'PIA23682': ('Goldstone',),
    'PIA23793': ('Moon', 'Satellite', 'Earth'),
    'PIA23796': ('Goldstone',),
    'PIA23797': ('Goldstone', 'Satellite', 'Planet', 'Mars', 'Moon', 'Earth'),
    'PIA23964': ('Moon', 'Satellite', 'Earth'),
    'PIA23967': ('Moon', 'Satellite', 'Earth'),
    'PIA24024': ('Moon', 'Satellite', 'Earth'),
    'PIA24025': ('t=Moon', 'Satellite', 'Earth'),
    'PIA24026': ('t=Moon', 'Satellite', 'Earth'),
    'PIA24038': ('Asteroid', 'i=ZTF', 'h+Zwicky Transient Facility'),
    'PIA24047': ('Moon', 'Satellite', 'Earth'),
    'PIA24048': ('Moon', 'Satellite', 'Earth'),
    'PIA24049': ('Moon', 'Satellite', 'Earth'),
    'PIA24108': ('Moon', 'Satellite', 'Earth'),
    'PIA24109': ('Moon', 'Satellite', 'Earth'),
    'PIA24110': ('Moon', 'Satellite', 'Earth'),
    'PIA24140': ('Earth',),
    'PIA24161': ('Mars', 'Planet'),
    'PIA24163': ('Goldstone', 'Satellite', 'Planet', 'Mars', 'Moon', 'Earth'),
    'PIA24169': ('Earth',),
    'PIA24170': ('Earth',),
    'PIA24174': ('Moon', 'Satellite', 'Earth'),
    'PIA24175': ('Moon', 'Satellite', 'Earth'),
    'PIA24178': ('Voyager', 'Pioneer', 'Flyby'),
    'PIA24499': ('Moon', 'Satellite', 'Earth'),
    'PIA24178': ('Voyager', 'Pioneer', 'Flyby'),
    'PIA24526': ('Moon', 'Satellite', 'Earth'),
    'PIA24527': ('Moon', 'Satellite', 'Earth'),
    'PIA24528': ('Moon', 'Satellite', 'Earth'),
    'PIA24566': ('Moon', 'Earth', 'Satellite'),
    'PIA24585': ('Moon', 'Satellite', 'Earth'),
    'PIA24615': ('Moon', 'Satellite', 'Earth'),
    'PIA24667': ('Moon', 'Satellite', 'Earth'),
    'PIA24668': ('Moon', 'Satellite', 'Earth'),
    'PIA24931': ('Moon', 'Earth', 'Satellite'),
    'PIA24932': ('Moon', 'Earth', 'Satellite'),
    'PIA24933': ('Moon', 'Earth', 'Satellite'),
    'PIA24936': ('Moon', 'Earth', 'Satellite'),
    'PIA24948': ('Moon', 'Satellite', 'Earth'),
}

ASTEROID1 = re.compile('[12]\d\d\d [A-Z][A-Z]?\d*$')
ASTEROID2 = re.compile('[12]\d\d\d [A-Z][A-Z]?\d* +.*$')
COMET1 = re.compile('\d+P/[A-Z][A-Za-z0-9 -]+$')
COMET2 = re.compile('[CP]/[12]\d\d\d [A-Z][A-Z]?\d*$')
COMET3 = re.compile('[CP]/[12]\d\d\d [A-Z][A-Z]?\d* +\(.*\)$')

def repair_piapage(page):

    page.might_be_planetary = True

    # Omit images that are not planetary at all
    if page.id in NOT_PLANETARY:
        page.might_be_planetary = False
        return

    # Certain missions are always excluded
    for mission in EXCLUDED_MISSIONS:
        if mission in page.missions[0]:
            page.might_be_planetary = False
            return

    # Earth and Sun are never secondary targets
    for removal in ('Earth', 'Sun'):
        if removal in page.targets[1:]:
            page._targets_filled.remove(removal)
        if removal in page.target_types[1:]:
            page._target_types_filled.remove(removal)

    # Replace target = "Asteroid" if there's a more specific target
    if page.targets[0] == 'Asteroid':
        if not page.target_types[0]:
            page._target_types_filled[0] = 'Asteroid'

        for target in page._targets_filled[1:]:
            for regex in (ASTEROID1, ASTEROID2):
                if regex.match(target):
                    page._targets_filled.remove(target)
                    page._targets_filled[0] = target
                    break

    # Replace target = "Comet" if there's a more specific target
    if page.targets[0] == 'Comet':
        if not page.target_types[0]:
            page._target_types_filled[0] = 'Comet'

        for target in page._targets_filled[1:]:
            for regex in (COMET1, COMET2, COMET3):
                if regex.match(target):
                    page._targets_filled.remove(target)
                    page._targets_filled[0] = target
                    break

    # Otherwise, just replace "Comet" or "Asteroid" with a blank target
    if page.targets[0] in ('Comet', 'Asteroid'):
        page._targets_filled[0] = ''

    # If one comet/asteroid name fits inside another, replace short with long
    # and then remove the duplicate
    if ('Comet' in page.target_types
        or 'Asteroid' in page.target_types
        or 'KBO' in page.target_types):
            short_loc = -1
            long_loc = -1
            for k,target in enumerate(page.targets):
                if ASTEROID1.match(target):
                    short_loc = k
                if ASTEROID2.match(target):
                    long_loc = k

            if short_loc >= 0 and long_loc >= 0:
                page._targets_filled[short_loc] = page._targets_filled[long_loc]
                del page._targets_filled[max(short_loc, long_loc)]

            short_loc = -1
            long_loc = -1
            for k,target in enumerate(page.targets):
                if COMET2.match(target):
                    short_loc = k
                if COMET3.match(target):
                    long_loc = k

            if short_loc >= 0 and long_loc >= 0:
                page._targets_filled[short_loc] = page._targets_filled[long_loc]
                loc = max(short_loc, long_loc)
                del page._targets_filled[max(short_loc, long_loc)]

    # Too many extraneous targets for Dawn
    if page.missions[0] == 'Dawn' and len(page.targets) == 2:
        if page.targets == ['1 Ceres', '4 Vesta']:
            page._targets_filled = ['1 Ceres']
            page._target_types_filled = ['Asteroid', 'Dwarf Planet']
        if page.targets == ['4 Vesta', '1 Ceres']:
            page._targets_filled = ['4 Vesta']
            page._target_types_filled = ['Asteroid']

    # Background text for Mariner 10
    if page.hosts[0] == 'Mariner 10':
        page._targets_filled = page.targets[:1]     # just keep first target
        if page.targets[0] == 'Moon':
            page._systems_filled = ['Earth']
            page._target_types_filled = ['Satellite']
        else:
            page._systems_filled = ['']
            page._target_types_filled = ['Planet']

    ######### Identify removals...

    removals = REMOVALS.get(page.id, [])
    if isinstance(removals, str):
        removals = [removals]
    else:
        removals = list(removals)       # convert to a list

    # Handle "between Mars and Jupiter", etc.
    if (page.systems[0] == 'Main Belt'
        or 'WISE' in page.missions[0]
        or 'WISE' in page.hosts[0]
        or page.missions[0] == 'Psyche'
        or page.missions[0] == 'Dawn'
        or page.target_types[0] == 'Asteroid'):
            removals += ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', '=Planet']

    # Why do Titan releases keep referencing Mercury and the Moon?
    if page.targets[0] == 'Titan':
        removals += ['Mercury', 'Moon']

    # Exoplanet captions often refer to solar system planets
    if ((page.target_types[0] == 'Exoplanet' or
         page.target_types[:2] == ['', 'Exoplanet']) and
        ('Spitzer' in page.missions[0] or 'Kepler' in page.missions[0])):
        removals += ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn',
                     'Neptune', 'Pluto', 'Planet']

    # Press release images of Voyager
    if (page.missions[0] == 'Voyager'):         # this is ugly...
        if page.id in ('PIA17049'):
            removals += ['Sun',
                         's+', 's+Jupiter', 's+Saturn', 's+Uranus', 's+Neptune',
                         't+', 't+Jupiter', 't+Saturn', 't+Uranus', 't+Neptune',
                         'T+Planet']
        elif page.targets[0] == 'Sun' or page.id in ('PIA13899', 'PIA15173', 'PIA22835', 'PIA22921', 'PIA22922', 'PIA24572'):
            removals += ['Sun', 't+Heliosphere', 'T+Heliosphere', 's+Solar System']
        elif page.targets[0] == '':
            removals += ['s+Jupiter', 's+Saturn', 's+Uranus', 's+Neptune',
                         't+Jupiter', 't+Saturn', 't+Uranus', 't+Neptune',
                         'T+Planet']

    # Press release images of Clementine
    if (page.hosts[0] == 'Clementine' and
        not page.targets[0] and not page.targets[1:]):
            removals += ['t+Moon', 'T+Satellite', 's+Earth']

    # Press release images of Cassini
    if (page.missions[0] == 'Cassini-Huygens' and
        not page.targets[0] and not page.targets[1:]):
            removals += ['s+Saturn', 't+Saturn', 'T+Planet']

    # Press release images of Juno
    if (page.missions[0] == 'Juno' and
        not page.targets[0] and not page.targets[1:]):
            removals += ['t+Jupiter', 'T+Planet']

    # Press release images of Deep Space 1
    if (page.missions[0] == 'Deep Space 1 (DS1)' and
        not page.targets[0] and not page.targets[1:]):
            removals += ['t+9969 Braille', 'T+Asteroid', 's+Main Belt']

            if page.target_types[0] == 'Comet':
                removals += ['t+81P/Wild', 's+Periodic Comets']
            elif page.target_types[0] == 'Asteroid':
                removals += ['t+5535 Annefrank', 's+Main Belt']
            else:
                removals += ['t+81P/Wild', 'T+Comet', 's+Periodic Comets',
                             't+5535 Annefrank', 'T+Asteroid', 's+Main Belt']

    # Press release images of MESSENGER
    if page.missions[0] == 'MESSENGER' and not page.targets[0]:
        if page.target_types[0] in ('', 'Planet'):
            removals += ['t+Mercury', 'T+Planet']

    # Press release images of Stardust
    if page.missions[0] == 'Stardust' and not page.targets[0]:
        removals += ['t+81P/Wild', 'T+Comet', 's+Periodic Comets']

    # Press release images of Dawn
    if page.missions[0] == 'Dawn' and not page.targets[0]:
        removals += ['T+Asteroid', 'T+Dwarf Planet', 's+Main Belt', 't=', 't+4 Vesta', 't+1 Ceres']

    # Press release images of Kepler
    if (page.missions[0] == 'Kepler'  and
        not page.targets[0] and not page.targets[1:]):
            removals += ['T+Exoplanet']

    # Press release images of InSight, MarCo, Mars 2020
    if ((page.missions[0] == 'InSight' or page.missions[0][:4] == 'Mars')
        and not page.targets[0] and not page.targets[1:]):
            removals += ['t+Mars', 'T+Planet']

    # Remove MU69
    if '486958 Arrokoth' in page.targets:
        removals += ['MU69']

    ######## Begin removals

    # Removals from targets
    keys_to_remove = []
    for key in page.targets:
        for keyword in removals:
            if keyword[0] == '=' and keyword[1:] == key:
                keys_to_remove.append(key)
            if keyword[:2] == 't=' and keyword[2:] == key:
                keys_to_remove.append(key)
            if keyword in key:
                keys_to_remove.append(key)

    keys_to_remove = set(keys_to_remove)
    for key in set(keys_to_remove):
        page._targets_filled.remove(key)

    # Added targets
    for keyword in removals:
        if keyword[:2] == 't+':
            page._targets_filled.append(keyword[2:])

    if not page._targets_filled:
        page._targets_filled = ['']

    # Removals from target_types
    keys_to_remove = []
    for key in page.target_types:
        for keyword in removals:
            if keyword[0] == '=' and keyword[1:] == key:
                keys_to_remove.append(key)
            if keyword[:2] == 'T=' and keyword[2:] == key:
                keys_to_remove.append(key)
            if keyword in key:
                keys_to_remove.append(key)

    keys_to_remove = set(keys_to_remove)
    for key in set(keys_to_remove):
        page._target_types_filled.remove(key)

    # Added target_types
    for keyword in removals:
        if keyword[:2] == 'T+':
            page._target_types_filled.append(keyword[2:])

    if not page._target_types_filled:
        page._target_types_filled = ['']

    # Removals from missions
    keys_to_remove = []
    for key in page.missions:
        for keyword in removals:
            if keyword[0] == '=' and keyword[1:] == key:
                keys_to_remove.append(key)
            if keyword[:2] == 'm=' and keyword[2:] == key:
                keys_to_remove.append(key)
            if keyword in key:
                keys_to_remove.append(key)

    keys_to_remove = set(keys_to_remove)
    for key in set(keys_to_remove):
        page._missions_filled.remove(key)

    # Added missions
    for keyword in removals:
        if keyword[:2] == 'm+':
            page._missions_filled.append(keyword[2:])

    if not page._missions_filled:
        page._missions_filled = ['']

    # Removals from hosts
    keys_to_remove = []
    for key in page.hosts:
        for keyword in removals:
            if keyword[0] == '=' and keyword[1:] == key:
                keys_to_remove.append(key)
            if keyword[:2] == 'h=' and keyword[2:] == key:
                keys_to_remove.append(key)
            if keyword in key:
                keys_to_remove.append(key)

    keys_to_remove = set(keys_to_remove)
    for key in set(keys_to_remove):
        page._hosts_filled.remove(key)

    # Added hosts
    for keyword in removals:
        if keyword[:2] == 'h+':
            page._hosts_filled.append(keyword[2:])

    if not page._hosts_filled:
        page._hosts_filled = ['']

    # Removals from instruments
    keys_to_remove = []
    for key in page.instruments:
        for keyword in removals:
            if keyword[0] == '=' and keyword[1:] == key:
                keys_to_remove.append(key)
            if keyword[:2] == 'i=' and keyword[2:] == key:
                keys_to_remove.append(key)
            if keyword in key:
                keys_to_remove.append(key)

    keys_to_remove = set(keys_to_remove)
    for key in set(keys_to_remove):
        page._instruments_filled.remove(key)

    # Added instruments
    for keyword in removals:
        if keyword[:2] == 'i+':
            page._instruments_filled.append(keyword[2:])

    if not page._instruments_filled:
        page._instruments_filled = ['']

    # Removals from systems
    keys_to_remove = []
    for key in page.systems:
        for keyword in removals:
            if keyword[0] == '=' and keyword[1:] == key:
                keys_to_remove.append(key)
            if keyword[:2] == 's=' and keyword[2:] == key:
                keys_to_remove.append(key)
            if keyword in key:
                keys_to_remove.append(key)

    keys_to_remove = set(keys_to_remove)
    for key in set(keys_to_remove):
        page._systems_filled.remove(key)

    # Added systems
    for keyword in removals:
        if keyword[:2] == 's+':
            page._systems_filled.append(keyword[2:])

    if not page._systems_filled:
        page._systems_filled = ['']

    # Removals from keywords
    keys_to_remove = []
    for key in page.keywords:
        for keyword in removals:
            if keyword[0] == '=' and keyword[1:] == key:
                keys_to_remove.append(key)
            if keyword[:2] == 'k=' and keyword[2:] == key:
                keys_to_remove.append(key)
            if keyword in key:
                keys_to_remove.append(key)

    keys_to_remove = set(keys_to_remove)
    for key in set(keys_to_remove):
        page._keywords.remove(key)

    # Added keywords
    for keyword in removals:
        if keyword[:2] == 'k+':
            page._keywords.append(keyword[2:])

    # Remove duplicates
    values = []
    for value in page.targets:
        if value not in values:
            values.append(value)
    page._targets_filled = values

    values = []
    for value in page.target_types:
        if value not in values:
            values.append(value)
    page._target_types_filled = values

    values = []
    for value in page.systems:
        if value not in values:
            values.append(value)
    page._systems_filled = values

    values = []
    for value in page.missions:
        if value not in values:
            values.append(value)
    page._missions_filled = values

    values = []
    for value in page.hosts:
        if value not in values:
            values.append(value)
    page._hosts_filled = values

    values = []
    for value in page.instruments:
        if value not in values:
            values.append(value)
    page._instruments_filled = values

    # Move a single secondary value forward if the primary is absent
    if len(page.targets) == 2 and not page.targets[0]:
        page._targets_filled = page._targets_filled[1:]

    if (len(page.systems) == 2 and not page.systems[0] and
            GalleryPage.system_from_target(page.targets[0])):
        page._systems_filled = page._systems_filled[1:]

    if len(page.target_types) == 2 and not page.target_types[0]:
        page._target_types_filled = page._target_types_filled[1:]

    if len(page.missions) == 2 and not page.missions[0]:
        page._missions_filled = page._missions_filled[1:]

    if len(page.hosts) == 2 and not page.hosts[0]:
        page._hosts_filled = page._hosts_filled[1:]

    if len(page.instruments) == 2 and not page.instruments[0]:
        page.instruments_filled = page._instruments_filled[1:]

    if len(page.detectors) == 2 and not page.detectors[0]:
        page._detectors_filled = page._detectors_filled[1:]

    # Reorder values if necessary
    host = GalleryPage.host_from_instrument(page.instruments[0])
    if host and page.hosts[0] != host:
        if host in page.hosts[1:]:
            page._hosts_filled.remove(host)
        if page.hosts[0]:
            page._hosts_filled = [host] + page.hosts
        else:
            page._hosts_filled = [host] + page.hosts[1:]

    mission = GalleryPage.mission_from_host(page.hosts[0])
    if mission and page.missions[0] != mission:
        if mission in page.missions[1:]:
            page._missions_filled.remove(mission)
        if page.missions[0]:
            page._missions_filled = [mission] + page.missions
        else:
            page._missions_filled = [mission] + page.missions[1:]

    host = GalleryPage.host_from_mission(page.missions[0])
    if host and page.hosts[0] != host:
        if host in page.hosts[1:]:
            page._hosts_filled.remove(host)
        if page.hosts[0]:
            page._hosts_filled = [host] + page.hosts
        else:
            page._hosts_filled = [host] + page.hosts[1:]

    host_type = GalleryPage.host_type_from_host(page.hosts[0])
    if host_type and page.host_types[0] != host_type:
        if host_type in page.host_types[1:]:
            page._host_types_filled.remove(host_type)
        if page.host_types[0]:
            page._host_types_filled = [host_type] + page.host_types
        else:
            page._host_types_filled = [host_type] + page.host_types[1:]

    target_type = GalleryPage.target_type_from_target(page.targets[0])
    if target_type and page.target_types[0] != target_type:
        if target_type in page.target_types[1:]:
            page._target_types_filled.remove(target_type)
        if page.target_types[0]:
            page._target_types_filled = [target_type] + page.target_types
        else:
            page._target_types_filled = [target_type] + page.target_types[1:]

    system = GalleryPage.system_from_target(page.systems[0])
    if system and page.systems[0] != system:
        if target_type in page.target_types[1:]:
            page._systems_filled.remove(system)
        if page.systems[0]:
            page._systems_filled = [system] + page.systems
        else:
            page._systems_filled = [system] + page.systems[1:]
    elif not system and page.targets[0] in ('Mercury', 'Venus'):
        if page._systems_filled[0]:
            page._systems_filled = [''] + page._systems_filled

    if not page.targets[0] and not page.targets[1:]:  # if no targets
        if not page.target_types[0] and page.target_types[1:]:
            page._target_types_filled = page.target_types[1:]
                # first target type is primary

        if not page.systems[0] and page.systems[1:]:
            page._systems_filled = page.systems[1:]
                # first system is primary

    if not page.hosts[0] and not page.hosts[1:]:      # if no hosts
        if not page.host_types[0] and page.host_types[1:]:
            page._hosts_filled = page.host_types[1:]
                # first host type is primary

    # If it's still an Earth image
    if page.targets == ['Earth'] and page.target_types == ['']:
        page._target_types_filled = ['Earth']

    if page.targets == ['Earth'] and page.systems == ['']:
        page._systems_filled = ['Earth']

    # Reorder for Pluto, which has two system and two target types
    if 'Pluto' in page.targets and not page.systems[0]:
        if 'Pluto' in page.systems:
            page._systems_filled.remove('Pluto')
        if '' in page.systems:
            page._systems_filled.remove('')
        page._systems_filled = ['Pluto'] + page._systems_filled

    if 'Pluto' in page.targets and not page.target_types[0]:
        if 'Dwarf Planet' in page.target_types:
            page._target_types_filled.remove('Dwarf Planet')
        if '' in page.target_types:
            page._target_types_filled.remove('')
        page._target_types_filled = ['Dwarf Planet'] + page._target_types_filled

    # Special cases...

    if page.id == 'PIA00545':
        page._targets_filled = ['', 'Mercury', 'Venus', 'Earth', 'Moon',
                                   'Mars', 'Jupiter', 'Saturn', 'Uranus',
                                   'Neptune']
        page._target_types_filled = ['', 'Planet', 'Satellite']
        page._systems_filled = ['', 'Earth',
                                   'Mars', 'Jupiter', 'Saturn', 'Uranus',
                                   'Neptune']
        page._missions_filled = ['', 'Mariner', 'Magellan', 'Galileo',
                                    'Viking', 'Voyager']
        page._hosts_filled = ['', 'Mariner 10', 'Magellan', 'Galileo Orbiter',
                                    'Viking Lander', 'Voyager 1', 'Voyager 2']
        page._host_types_filled = ['', 'Flyby Spacecraft', 'Orbiter']
        page._instruments_filled = ['']

    if page.id == 'PIA03153':
        page._targets_filled = ['', 'Mercury', 'Venus', 'Earth', 'Moon',
                                   'Mars', 'Jupiter', 'Saturn', 'Uranus',
                                   'Neptune']
        page._target_types_filled = ['', 'Planet', 'Satellite']
        page._systems_filled = ['', 'Earth',
                                   'Mars', 'Jupiter', 'Saturn', 'Uranus',
                                   'Neptune']
        page._missions_filled = ['', 'Mariner', 'Magellan', 'Galileo',
                                    'Mars Global Surveyor (MGS)', 'Cassini-Huygens',
                                    'Voyager']
        page._hosts_filled = ['', 'Mariner 10', 'Magellan', 'Galileo Orbiter',
                                    'Mars Global Surveyor', 'Cassini Orbiter',
                                    'Voyager 1', 'Voyager 2']
        page._host_types_filled = ['', 'Flyby Spacecraft', 'Orbiter']
        page._instruments_filled = ['']

    if page.id == 'PIA12256':
        page._targets_filled = ['Saturn Rings', 'Iapetus', 'Phoebe', 'Saturn']
        page._target_types_filled = ['Ring', 'Irregular', 'Planet']
        page._systems_filled = ['Saturn']
        page._missions_filled = ['Spitzer Space Telescope', 'Cassini-Huygens']
        page._hosts_filled = ['Spitzer Space Telescope', 'Cassini Orbiter']
        page._host_types_filled = ['Space Telescope', 'Orbiter']

    if page.id == 'PIA06350':
        page._targets_filled.remove('Saturn Rings')
        page._targets_filled = ['Saturn Rings'] + page._targets_filled
        page._target_types_filled.remove('Ring')
        page._target_types_filled = ['Ring'] + page._targets_filled

    # Both Arrokoth and MU69
    if page.targets[:3] == ['', '2014 MU69', '486958 Arrokoth']:
        page._targets_filled = ['486958 Arrokoth']
        page._target_types_filled = ['KBO']

    if page.id == 'PIA22573':
        page._targets_filled = ['Mars', 'Earth', 'Moon']
        page._systems_filled = ['Mars', 'Earth']
        page._target_types_filled = ['Planet', 'Satellite']

    if page.id == 'PIA24146':
        page._targets_filled = ['Moon', 'Mars']
        page._systems_filled = ['Earth', 'Mars']
        page._target_types_filled = ['Satellite', 'Planet']

    if page.id == 'PIA17308':
        page._targets_filled.remove('Pluto')
        page._targets_filled = ['Pluto'] + page._targets_filled
        page._systems_filled = page._systems_filled[::-1]

    if page.id == 'PIA24435':
        page._targets_filled = ['Mars']
        page._target_types_filled = ['Planet']
        page._systems_filled =['']
        page._missions_filled = ['Mars 2020', 'InSight']
        page._hosts_filled = ['Perseverance', 'Ingenuity', 'InSight Lander']
        page._host_types_filled = ['Rover', 'Helicopter', 'Lander']

################################################################################
