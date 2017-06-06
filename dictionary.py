"""
http://worder.cat/wortsucher
    P I E R
    I D L E 
    N O S E
    S L E D
    
    C A N
    A G E
    R O W

    C A L L E T
    O P I A T E
    M I M B A R
    P E N I L E
    O C E L O T
    S E R E N E

def write(a):
    D = a.split()
    test = [e for e in D if 'Ä' not in e and 'Ö' not in e and 'Ü' not in e]
    with open('test.txt', 'w') as file:
        file.write("{}".format(test))
"""
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "

DICTIONARY_ = ['AB', 'AB', 'AA', 'BB']
DICTIONARY_ = ['CAN', 'AGE', 'ROW', 'CAR', 'AGO', 'NEW']
DICTIONARY_ = ['PIER', 'IDLE', 'NOSE', 'SLED', 'PINS', 'IDOL', 'ELSE', 'REED']
DICTIONARY_ = ['DEBIT', 'INANE', 'CUTUP', 'EROSE', 'RENTE', 'DICER', 'ENURE',
              'BATON', 'INUST', 'TEPEE']
DICTIONARY_ = ['CALLET', 'OPIATE', 'MIMBAR', 'PENILE', 'OCELOT',
               'SERENE', 'COMPOS', 'APIECE', 'LIMNER', 'LABILE', 'ETALON', 'TERETE']

DICTIONARY_ = ['PIER', 'IDLE', 'NOSE', 'SLED', 'PINS',
              'KIEL', 'KICK', 'KHAN', 'KIES', 'KIEW', 'KIMM', 'KILO', 'KILL', 'KESS',
              'KERN', 'KEIM', 'KEIL', 'KEHR', 'KEIN', 'KEKS', 'KERL', 'KENT', 'KIND',
              'KINN', 'KLEE', 'KLEB', 'KLAU', 'KLON', 'KLOO', 'KLUG', 'KLUB', 'KLOS',
              'KLAR', 'KLAG', 'KIRS', 'KIPP', 'KINO', 'KITS', 'KITT', 'KECK', 'KAUZ',
              'KADI', 'KAFF', 'KAIS', 'KAHN', 'KAHL', 'JUXE', 'KALB', 'KALI', 'KARO',
              'KARL', 'KARG', 'KATZ', 'KAUE', 'KAUT', 'KAUM', 'KAUF', 'KAPS', 'KAPP',
              'KAMM', 'KALT', 'KALK', 'KAMT', 'KANN', 'KANU', 'KANT', 'KNIE', 'KNOX',
              'LAGE', 'LADY', 'LADE', 'LAGO', 'LAGT', 'LAHR', 'LAHN', 'LAHM', 'LACK',
              'LACH', 'LABT', 'LABE', 'LAIB', 'LAIE', 'LAUB', 'LATZ', 'LAST', 'LAUE',
              'LAUF', 'LAVA', 'LAUT', 'LAUS', 'LASS', 'LARS', 'LAMM', 'LAME', 'LAMA',
              'LAND', 'LANG', 'LAOS', 'LANS', 'KOTS', 'KOST', 'KORN', 'KRAM', 'KRAN',
              'KRUD', 'KRIM', 'KREM', 'KORK', 'KORB', 'KOHM', 'KOHL', 'KOCH', 'KOJE',
              'KOKS', 'KOPF', 'KOMM', 'KRUG', 'KSZE', 'KUSS', 'KURZ', 'KURT', 'KURS',
              'KULI', 'KUFE', 'KUBA', 'KULT', 'KUND', 'KURE', 'KUNZ', 'JUTE', 'JUST',
              'HILF', 'HIEV', 'HIER', 'HING', 'HINZ', 'HIWI', 'HITS', 'HIRN', 'HIEO',
              'HIEB', 'HERR', 'HERD', 'HERB', 'HERZ', 'HEUS', 'HEXT', 'HEXE', 'HOBT',
              'HOCH', 'HORT', 'HORN', 'HOLZ', 'HOSE', 'HTML', 'HUFE', 'HUBS', 'HTTP',
              'HOLT', 'HOLM', 'HOHE', 'HOFS', 'HOFE', 'HOHL', 'HOHN', 'HOLE', 'HOLD',
              'HERA', 'HEMD', 'HART', 'HARN', 'HANS', 'HARZ', 'HASE', 'HAUE', 'HAST',
              'HASS', 'HANG', 'HANF', 'HALL', 'HALF', 'HALB', 'HALM', 'HALS', 'HAND',
              'HALT', 'HAUS', 'HAUT', 'HEIM', 'HEIL', 'HEHL', 'HEIO', 'HELD', 'HELM',
              'HELL', 'HEGT', 'HEGE', 'HECK', 'HEBT', 'HEBE', 'HEDY', 'HEER', 'HEFT',
              'HEFE', 'HUFS', 'HUGO', 'JEAN', 'JAZZ', 'JAVA', 'JEDE', 'JEEP', 'JENS',
              'JENE', 'JENA', 'JANS', 'JAHR', 'JACK', 'JAGD', 'JAGE', 'JAHN', 'JAGT',
              'JESU', 'JETS', 'JULI', 'JUDO', 'JUDE', 'JUNG', 'JUNI', 'JURY', 'JURE',
              'JURA', 'JUDA', 'JOYS', 'JOCH', 'JOBS', 'JIMS', 'JODS', 'JOGA', 'JOTA',
              'JOHN', 'IVAN', 'IDOL', 'IDEE', 'ICON', 'IGEL', 'IHRE', 'INGO', 'INFO',
              'IMAP', 'IBMS', 'IATA', 'HUPE', 'HUND', 'HUHN', 'HUPT', 'HURE', 'HUTS',
              'HURT', 'INKA', 'INNE', 'ISAR', 'IRRT', 'IRRE', 'ISBN', 'ISDN', 'ISST',
              'ISIS', 'IRIS', 'IRIN', 'IOTA', 'IONS', 'INST', 'IPSO', 'IRAK', 'IREN',
              'IRAN', 'LAXE', 'LDAP', 'NORD', 'NOCH', 'NOAH', 'NORM', 'NOTA', 'NSEC',
              'NOVA', 'NOTE', 'NIXE', 'NINA', 'NEWS', 'NEUN', 'NEUE', 'NICD', 'NIET',
              'NIMM', 'NILS', 'NULL', 'NUSS', 'OECD', 'ODER', 'ODEN', 'OFEN', 'OHIO',
              'OHRS', 'OHRE', 'OHNE', 'ODEM', 'OCHS', 'OBEN', 'OASE', 'NUTE', 'OBER',
              'OBIG', 'OBST', 'OBOE', 'NETZ', 'NETT', 'NACH', 'NAGE', 'NAGT', 'NAHT',
              'NAHM', 'NAHE', 'MUTS', 'MUND', 'MUMM', 'MSEC', 'MUOE', 'MUSE', 'MUTE',
              'MUSS', 'NAIV', 'NAME', 'NERO', 'NEPP', 'NEON', 'NERV', 'NERZ', 'NEST',
              'NESS', 'NEIN', 'NEID', 'NASA', 'NARR', 'NAPF', 'NASE', 'NASS', 'NAZI',
              'NATO', 'OKAY', 'OLAF', 'PIUS', 'PISA', 'PINS', 'PLAN', 'PLOT', 'POET',
              'PNEU', 'PLUS', 'PILZ', 'PILS', 'PEST', 'PERU', 'PERL', 'PFAD', 'PFAU',
              'PIKE', 'PHON', 'POLE', 'POLS', 'PUBS', 'PRAG', 'POTI', 'PUFF', 'PULK',
              'PUMA', 'PULT', 'PULS', 'POST', 'POSE', 'POOL', 'PONY', 'POMP', 'POPE',
              'POPO', 'PORT', 'PORE', 'PELZ', 'PELL', 'ORAL', 'OPUS', 'OPTI', 'ORTE',
              'ORTS', 'OTTO', 'OSZE', 'OSLO', 'OPER', 'OPEL', 'OLIV', 'OLGA', 'OLEG',
              'OMAS', 'OMEN', 'OPEC', 'OPAS', 'OVAL', 'OXID', 'PATE', 'PASS', 'PART',
              'PAUL', 'PEAK', 'PEIN', 'PECH', 'PARK', 'PAPI', 'OZON', 'OXYD', 'PAAR',
              'PAKT', 'PAPA', 'PANS', 'MPEG', 'MOST', 'LOKS', 'LOHN', 'LOGT', 'LORD',
              'LORE', 'LOTE', 'LOST', 'LOSE', 'LOGO', 'LOCH', 'LIVE', 'LITT', 'LIST',
              'LKWS', 'LOBE', 'LOBT', 'LOBS', 'LUFT', 'LUGE', 'MAAR', 'LUKE', 'LUGT',
              'LUGS', 'LUPE', 'LUST', 'LUTZ', 'LISP', 'LISA', 'LEID', 'LEIB', 'LEHM',
              'LEIH', 'LEIM', 'LEST', 'LESE', 'LENZ', 'LEGT', 'LEGE', 'LEBT', 'LEBE',
              'LEAR', 'LECH', 'LECK', 'LEER', 'LEDS', 'LGPL', 'LIDO', 'LIND', 'LIMA',
              'LILA', 'LINK', 'LINZ', 'LIRE', 'LIRA', 'LIGA', 'LIFT', 'LIED', 'LIEB',
              'LIDS', 'LIEF', 'LIEH', 'LIES', 'LIEO', 'MAAS', 'MACH', 'MING', 'MINE',
              'MIME', 'MINI', 'MIPS', 'MITI', 'MIST', 'MISS', 'MILZ', 'MILD', 'MICK',
              'MICH', 'METZ', 'MIDI', 'MIED', 'MIES', 'MIEF', 'MIXE', 'MIXT', 'MONT',
              'MOND', 'MOMO', 'MOOR', 'MOOS', 'MORD', 'MOPS', 'MOPP', 'MOLS', 'MOLL',
              'MODI', 'MODE', 'MOBS', 'MOFA', 'MOHN', 'MOLE', 'MOHR', 'MERZ', 'MERK',
              'MAMA', 'MALZ', 'MALT', 'MANN', 'MANZ', 'MAOT', 'MAOS', 'MAOE', 'MALO',
              'MALI', 'MAHL', 'MAGD', 'MADE', 'MAIL', 'MAIN', 'MALE', 'MAIS', 'MARC',
              'MARK', 'MEHL', 'MEER', 'MBIT', 'MEHR', 'MEIN', 'MEMO', 'MAYA', 'MAUT',
              'MARY', 'MARX', 'MARS', 'MAST', 'MATT', 'MAUS', 'MAUL', 'HAKT', 'HAKE',
              'BONS', 'BONN', 'BONI', 'BOOM', 'BOOT', 'BOTE', 'BOSS', 'BORD', 'BOJE',
              'BOHR', 'BLUT', 'BLOO', 'BLOG', 'BOAS', 'BOBS', 'BOGT', 'BOCK', 'BOXE',
              'BOXT', 'BUGS', 'BUDE', 'BUCH', 'BUHE', 'BUHT', 'BUND', 'BULL', 'BUKT',
              'BUBE', 'BRUT', 'BRAT', 'BOYS', 'BRAV', 'BREI', 'BROT', 'BRIE', 'BLEI',
              'BLAU', 'BEIN', 'BEIM', 'BEIL', 'BENS', 'BENZ', 'BERN', 'BERG', 'BEOS',
              'BEHR', 'BEET', 'BAUT', 'BAUS', 'BAUM', 'BEAS', 'BEBE', 'BECK', 'BEBT',
              'BERT', 'BETA', 'BISS', 'BIRG', 'BIOS', 'BIST', 'BITS', 'BIND', 'BILL',
              'BIAS', 'BETT', 'BETE', 'BIEG', 'BIER', 'BILD', 'BIET', 'BUNT', 'BUOE',
              'DEAL', 'DAZU', 'DAUM', 'DECK', 'DECT', 'DEMO', 'DELL', 'DEIN', 'DATO',
              'DASS', 'DAMM', 'DAME', 'DALI', 'DANK', 'DANN', 'DARM', 'DARF', 'DENK',
              'DENN', 'DILL', 'DIHK', 'DIES', 'DIMM', 'DING', 'DIVA', 'DITO', 'DIRK',
              'DIEB', 'DICK', 'DEUT', 'DERB', 'DEPP', 'DHCP', 'DICH', 'DIAS', 'DACH',
              'CHOR', 'CHIP', 'CHIC', 'CHUR', 'CITY', 'CLUB', 'CLOU', 'CLIP', 'CHEF',
              'CHAT', 'BYTE', 'BUSH', 'BURG', 'CAEN', 'CAFE', 'CENT', 'CAMP', 'CMOS',
              'COCA', 'CTRL', 'CSFR', 'CRUZ', 'COLT', 'COLA', 'CODE', 'COOL', 'COUP',
              'CREW', 'CPUS', 'BAUE', 'BAUD', 'AHLE', 'AGIO', 'AGIL', 'AHME', 'AHMT',
              'AHOI', 'AHNT', 'AHNE', 'AGFA', 'AFFE', 'ADAM', 'ADAC', 'ACTA', 'ADEL',
              'ADER', 'ADSL', 'ADLE', 'AIDS', 'AKKU', 'ALLS', 'ALLE', 'ALGE', 'ALSO',
              'ALTE', 'AMIS', 'AMEN', 'AMDS', 'ALFS', 'ALFA', 'AKTS', 'AKTE', 'AKNE',
              'AKUT', 'ALBA', 'ALEX', 'ALDI', 'ACPI', 'ACHT', 'AALE', 'AALS', 'AALT',
              'ABER', 'ABEL', 'AMME', 'AMOK', 'BACH', 'BABY', 'AZUR', 'AXEL', 'AVIV',
              'BACK', 'BADE', 'BARS', 'BARK', 'BARG', 'BART', 'BASE', 'BAST', 'BASS',
              'BASF', 'BARE', 'BANN', 'BALI', 'BALD', 'BAHN', 'BALL', 'BAND', 'BANK',
              'BANG', 'AUTO', 'AURA', 'ANSI', 'ANNO', 'ANNE', 'ANTI', 'AOEN', 'ARID',
              'ARGE', 'ARAL', 'ANNA', 'ANKE', 'AMTS', 'AMTE', 'AMOR', 'ANAL', 'ANDY',
              'ANJA', 'ANIS', 'ARIE', 'ARME', 'AUDI', 'AUCH', 'ATOM', 'AUEN', 'AUFS',
              'AULA', 'AUGE', 'ATME', 'ATEM', 'ARTE', 'ARNO', 'ARMS', 'ARZT', 'ASSE',
              'ASYL', 'ASTA', 'DNVP', 'DOCH', 'GABE', 'GABT', 'GALA', 'GAGS', 'GAGE',
              'FUOE', 'FUNK', 'FUND', 'FUOT', 'FURT', 'FURZ', 'GALT', 'GALV', 'GEBE',
              'GBIT', 'GAZE', 'GEBT', 'GECK', 'GEIG', 'GEHT', 'GEHE', 'GAUL', 'GATT',
              'GANZ', 'GANS', 'GANG', 'GARE', 'GARN', 'GAST', 'GASE', 'FUJI', 'FUHR',
              'FLAU', 'FLAK', 'FLOG', 'FLOH', 'FLUG', 'FLOP', 'FLOO', 'FIXT', 'FIXE',
              'FIES', 'FIEL', 'FICK', 'FILM', 'FILZ', 'FINK', 'FING', 'FLUR', 'FLUT',
              'FREI', 'FRAU', 'FRAO', 'FROH', 'FRON', 'FUGE', 'FROR', 'FRAG', 'FORM',
              'FORD', 'FOND', 'FORT', 'FOTO', 'FOUL', 'GEIL', 'GEIO', 'GUCK', 'GRUO',
              'GRUB', 'GURT', 'GURU', 'GUTS', 'GUTE', 'GUSS', 'GROO', 'GROG', 'GRAS',
              'GRAL', 'GRAF', 'GRAT', 'GRAU', 'GROB', 'GRAZ', 'GYSI', 'HABT', 'HABE',
              'HAAR', 'HAFT', 'HAHN', 'HAIS', 'HAIN', 'HAIE', 'HAAG', 'GRAD', 'GRAB',
              'GIBT', 'GERN', 'GERD', 'GIER', 'GIFT', 'GING', 'GINA', 'GILT', 'GENS',
              'GENF', 'GELD', 'GELB', 'GEIZ', 'GELE', 'GELS', 'GENE', 'GEMA', 'GIPS',
              'GIRO', 'GOTT', 'GOTE', 'GOSS', 'GOYA', 'GONG', 'GOLF', 'GLUT', 'GLAS',
              'GMBH', 'GNOM', 'GOLD', 'GNUS', 'FIBU', 'FIAT', 'EHRE', 'EHER', 'EHEN',
              'EHRT', 'EIBE', 'EIER', 'EIDE', 'EICH', 'EGOS', 'EGON', 'EFEU', 'EDLE',
              'EDER', 'EFTA', 'EGAL', 'EGGE', 'EGEL', 'EIES', 'EILE', 'ELFT', 'ELFE',
              'ELCH', 'ELIS', 'ELKE', 'EMIL', 'ELLE', 'ELKO', 'ELBE', 'ELBA', 'EINS',
              'EINE', 'EILT', 'EINT', 'EKEL', 'ELAN', 'EKLE', 'EDEN', 'EDEL', 'DRAN',
              'DOSE', 'DORT', 'DREH', 'DREI', 'DUFT', 'DUAL', 'DRIN', 'DORN', 'DORF',
              'DOKU', 'DOGE', 'DOCK', 'DOME', 'DOMS', 'DORA', 'DOOF', 'DUMM', 'DUNG',
              'ECHO', 'EBNE', 'EBER', 'ECHT', 'ECKE', 'ECUS', 'ECKT', 'EBEN', 'EBBE',
              'DUZE', 'DUTT', 'DUOS', 'DUZT', 'DVDS', 'EBAY', 'EADS', 'EMMA', 'ENBW',
              'FANS', 'FANG', 'FAND', 'FARM', 'FARN', 'FATA', 'FAST', 'FASS', 'FALL',
              'FALB', 'FADE', 'FACH', 'FAHL', 'FAHR', 'FAKT', 'FAIR', 'FAUL', 'FAUN',
              'FELD', 'FEIN', 'FEIL', 'FELL', 'FELS', 'FETT', 'FEST', 'FERN', 'FEIG',
              'FEHL', 'FCKW', 'FAXT', 'FAXE', 'FDGB', 'FEEN', 'FEGT', 'FEGE', 'EROS',
              'ERLE', 'ERGO', 'ERST', 'ERZE', 'ESSO', 'ESSE', 'ESEL', 'ERDE', 'ERBT',
              'ENGT', 'ENGE', 'ENDE', 'ENTE', 'EPEN', 'ERBE', 'EPOS', 'ESST', 'ETAT',
              'EXOT', 'EXIL', 'EWIG', 'EXPO', 'EVAS', 'EURO', 'ETWA', 'ETUI', 'ETON',
              'EUCH', 'EUER', 'EURE', 'EULE']


DICTIONARY_ = ['PIERR', 'IDLEE', 'NOSEE', 'SLEDK', 'SLEEK', 'REEKK' 'PINSS', 'IDOLL' 'AALEN', 'AALES', 'AALST', 'AALTE', 'AASES', 'ABART', 'ABBAT', 'ABBAU', 'ABBOG', 'ABELS', 'ABEND', 'ABGAB', 'ABGAS', 'ABHOB', 'ABKAM', 'ABLAG', 'ABMAO', 
'ABORT', 'ABRUF', 'ABSAH', 'ABSUD', 'ABTAT', 'ABTEI', 'ABTES', 'ABTUE', 'ABTUN', 'ABTUT', 'ABWEG', 'ABWOG', 'ABZOG', 
'ABZUG', 'ACHIM', 'ACHSE', 'ACHTE', 'ACKER', 'ACKRE', 'ACRYL', 'ADAMS', 'ADELE', 'ADELN', 'ADELS', 'ADELT', 'ADERN', 
'ADIEU', 'ADLER', 'ADLIG', 'ADOBE', 'ADOLF', 'ADRIA', 'ADRIG', 'AEROB', 'AFFEN', 'AFFIG', 'AFTER', 'AGAVE', 'AGENT', 
'AGFAS', 'AGILE', 'ARIEN', 'ARIER', 'ARMEE', 'ARMEM', 'ARMEN', 'ARMER', 'ARMES', 'ARMUT', 'ARNDT', 'ARNOS', 'AROMA', 
'AROSA', 'ARRAY', 'ARSCH', 'ARSEN', 'ARTEN', 'ARTET', 'ARTIG', 'ARTUS', 'ASCHE', 'ASCII', 'ASIAT', 'ASIEN', 'ASKET', 
'ASPIK', 'ASSEL', 'ASSEN', 'ASSES', 'ASTER', 'ASTES', 'ASYLS', 'ATARI', 'ATEMS', 'ATHEN', 'ATLAS', 'ATMEN', 'ATMET', 
'ATOLL', 'ATOME', 'ATOMS', 'AUDIS', 'AUGEN', 'AUGES', 'AUOEN', 'AUOER', 'AUREL', 'AUTOR', 'AUTOS', 'AXELS', 'AXIOM', 
'BOOMS', 'BOOMT', 'BOOTE', 'DIELE', 'DIENE', 'DIENT', 'DIESE', 
'DILDO', 'DILLS', 'DIMME', 'DIMMT', 'DINAR', 'DINGE', 'DINGS', 'DIODE', 'DIPOL', 'DIRKS', 'DIRNE', 'DIVAS', 'DIWAN', 
'DOCHT', 'DOCKS', 'DOGEN', 'DOGGE', 'DOGMA', 'DOHLE', 'DOLCH', 'DOLLY', 'DOMEN', 'DOMES', 'DONAU', 'DOOFE', 'DORAS', 
'DORFE', 'DORFS', 'DORIS', 'DORNS', 'DORRE', 'DORRT', 'DOSEN', 'DOSIS', 'DOVER', 'DRAHT', 'DRALL', 'DRAMA', 'DRANG', 
'DRAUF', 'DRECK', 'DREHE', 'DREHT', 'DREIN', 'DRESS', 'DRIFT', 'DRINK', 'DRITT', 'DROGE', 'DROHE', 'DROHT', 'DRUCK', 
'DUALE', 'DUBAI', 'DUBIO', 'DUCKE', 'DUCKT', 'DUDEN', 'DUELL', 'DUETT', 'DUFTE', 'DUFTS', 'DULDE', 'DUMAS', 'DUMME', 
'ERGAB', 'ERHOB', 'ERICH', 'ERIKA', 'ERKER', 'ERKOR', 
'ERLAG', 'ERLEN', 'ERNST', 'ERNTE', 'ERSTE', 'ERWIN', 'ERWOG', 'ERZEN', 'ERZES', 'ERZOG', 'ESCHE', 'ESELN', 'ESELS', 
'ESSAY', 'ESSEN', 'ESSER', 'ESSIG', 'ESSOS', 'ETAGE', 'ETATS', 'ETHIK', 'ETHOS', 'ETONS', 'ETWAS', 'EULEN', 'EULER', 
'EUPEN', 'EUREM', 'EUREN', 'EURER', 'EURES', 'EUROS', 'EUTER', 'EWIGE', 'EXAKT', 'EXCEL', 'EXILE', 'EXILS', 'EXPOS', 
'EXTRA', 'FABEL', 'FACHE', 'FACHS', 'FACHT', 'FACTO', 'FADEM', 'FADEN', 'FADER', 'FADES', 'FAHLE', 'FAHNE', 'FAHRE', 
'FAHRT', 'FAIRE', 'FAKTS', 'FALBE', 'FALKE', 'FALLE', 'FALLS', 'FALLT', 'FALTE', 'FAMOS', 'FANGE', 'FANGO', 'FANGS', 
'FANGT', 'FARBE', 'FARCE', 'FARNE', 'FARNS', 'FASAN', 'FASER', 'FASLE', 'FASSE', 'FASST', 'FASTE', 'FATAL', 'FATUM', 
'FAULE', 'FAULT', 'FAUNA', 'FAUNE', 'GIBST', 'GICHT', 'GIEOE', 'GIEOT', 'GIERE', 'GIERT', 'GIFTE', 'GIFTS', 'GILDE', 
'GINAS', 'GINGE', 'GINGT', 'GINKO', 'GIROS', 'GIZEH', 'GLANZ', 'GLATT', 'GLAUB', 'GLEIS', 'GLICH', 'GLIED', 'GLITT', 
'GNADE', 'GOLDA', 'GOLDS', 'GOLFS', 'GONGS', 'GORKI', 'GOSSE', 'GOSST', 'GOTEN', 'GOTHA', 'GOTIN', 'GOUDA', 'GOYAS', 
'GRABE', 'GRABS', 'GRABT', 'GRACE', 'GRADE', 'GRADS', 'GRALS', 'GRAMM', 'GRAPH', 'GRASE', 'GRAST', 'GRATE', 'GRATS', 
'GRAUE', 'GRAUT', 'GREIF', 'GREIS', 'GRELL', 'GRETE', 'GRIEO', 'GRIFF', 'GRILL', 'GRIMM', 'GRIPS', 'GROBE', 'GROGS', 
'GROLL', 'GROOE', 'GRUBE', 'GRUBT', 'GRUFT', 'GRUND', 'GUCKE', 'GUCKT', 'GUIDO', 'GUMMI', 'IHRER', 'IHRES', 'IKONE', 
'ILTIS', 'IMAGE', 'IMKER', 'IMKRE', 'IMMER', 'IMMUN', 'IMPFE', 'IMPFT', 'INDEM', 'INDER', 'INDES', 'INDEX', 'INDIO', 
'INDIZ', 'INDUS', 'INFAM', 'INFOS', 'INGOS', 'INNEN', 'INNIG', 'INSEL', 'INTEL', 'INTIM', 'INTUS', 'INUIT', 'IONEN', 
'IRDEN', 'IRREM', 'IRREN', 'IRRER', 'IRRES', 'IRRIG', 'IRRST', 'IRRTE', 'ISAAC', 'ISAAK', 'ISLAM', 'IVANS', 'KAABA', 
'KABEL', 'KABLE', 'KABUL', 'KADER', 'KADIS', 'KAFFS', 'KAFKA', 'KAHLE', 'KAHNS', 'KAIRO', 'KAKAO', 'KALBS', 'KALIF', 
'KALIS', 'KALKS', 'KALTE', 'KAMEL', 'KAMEN', 'KAMIN', 'KAMMS', 'KAMPF', 'KAMST', 'KANAL', 'KANNE', 'KANON', 'KANTE', 
'KANTS', 'KANUS', 'KAPPA', 'KAPPE', 'KAPPT', 'KARAT', 'KARGE', 'KARIN', 'KARLA', 'KARLS', 'KAROS', 'KARRE', 'KARRT', 
'KARTE', 'KASKO', 'KASSE', 'KASUS', 'KATER', 'KATIA', 'KATZE', 'KAUEN', 'KAUER', 'KAUFE', 'KAUFS', 'KAUFT', 'LITZE', 
'LLOYD', 'LOBBY', 'LOBEN', 'LOBES', 'LOBST', 'LOBTE', 'LOCHE', 'LOCHS', 'LOCHT', 'LOCKE', 'LOCKT', 'LODRE', 'LOGEN', 
'LOGGE', 'LOGGT', 'LOGIK', 'LOGIN', 'LOGIS', 'LOGOS', 'LOGST', 'LOHNE', 'LOHNS', 'LOHNT', 'LOIRE', 'LOKAL', 'LORDS', 
'LOREN', 'LOSEM', 'LOSEN', 'LOSER', 'MERCK', 'MERKE', 'MERKT', 'MESSE', 'MESST', 'METER', 
'MEUTE', 'MEYER', 'MIAMI', 'MIAUE', 'MIAUT', 'MICKS', 'MIDAS', 'MIEFS', 'MIENE', 'MIESE',
'SONNE', 'SONNT', 'SONOR', 'SONST', 'SONYS', 'SOOEN', 'SOOFT', 'SORBE', 'SORGE', 'SORGT', 'SORTE', 'SOUND', 'SOWIE', 
'SPALT', 'SPANN', 'SPANS', 'SPANT', 'SPAOE', 'SPAOT', 'SPARC', 'SPARE', 'SPART', 'SPATZ', 'SPECK', 'SPEER', 'SPEIE', 
'SPEIT', 'SPERR', 'SPEZI', 'SPIEL', 'SPIEN', 'SPIEO', 'SPIET', 'SPIKE', 'SPIND', 'SPINS', 'SPION', 'SPITZ', 'SPORE', 
'SPORN', 'SPORT', 'SPOTS', 'SPOTT', 'SPREE', 'SPREU', 'SPRIT', 'SPUKE', 'SPUKS', 'SPUKT', 'SPULE', 'SPULT', 'SPURT', 
'SPUTE', 'STAAT', 'STABS', 'STACH', 'STACK', 'STADT', 'STAHL', 'STAKT', 'STALL', 'STAMM', 'STAND', 'STANK', 'STARB', 
'STARE', 'STARK', 'STARR', 'STARS', 'START', 'STASI', 'STATT', 'STAUB', 'STAUE', 'STAUS', 'STAUT', 'STEAK', 'STEGE', 
'STEGS', 'STEHE', 'STEHT', 'STEIF', 'STEIG', 'STEIL', 'STEIN', 'STEIO', 'STELL', 'STERN', 'STETE', 'STETS', 'STEVE', 
'STICH', 'STIEG', 'STIEL', 'STIEO', 'STIER', 'STIFT', 'STILE', 'STILL', 'STILS', 'STIRB', 'STIRN', 'STOCK', 'STOFF', 
'STOLA', 'STOLZ', 'STOOE', 'STOOT', 'STOPP', 'STORY', 'STRAF', 'STROH', 'STROM', 'STUBE', 'STUCK', 'STUFE', 'SULZE', 
'SULZT', 'SUMMA', 'SUMME', 'SUMMT', 'SUMPF', 'SUPER', 'SUPPE', 'SURFE', 'SURFT', 'SURRE', 'SURRT', 'SUSES', 'SUSHI', 
'SVENS', 'SWAPO', 'SWING', 'SYRER', 'SZENE', 'TABAK', 'TABUS', 'TADEL', 'TADLE', 'TAFEL', 'TAFLE', 'TAFTS', 'TAGEN', 
'TAGES', 'TAGST', 'TAGTE', 'TAIGA', 'TAKEL', 'TAKLE', 'TAKTE', 'TAKTS', 'TALER', 'TALES', 'TALGS', 'TALKS', 'TALON', 
'TANDS', 'TANGE', 'TANGO', 'TANGS', 'TANJA', 'TANKE', 'TANKS', 'TANKT', 'TANNE', 'TANTE', 'TANZE', 'TANZT', 'TAPET', 
'TAPPE', 'TAPPT', 'TAPSE', 'TAPST', 'TARIF', 'TARNE', 'TARNT', 'TASSE', 'TASTE', 'TATAR', 'TATEN', 'TATET', 'TISCH', 
'TITAN', 'TITEL', 'TITLE', 'TITOS', 'TOAST', 'TOBEN', 'TOBST', 'TOBTE', 'TODES', 'TOFUS', 'TOGOS', 'TOKIO', 'TOLLE', 
'TOLLT', 'TONEN', 'TONES', 'TONNE', 'TOOLS', 'TOPAS', 'TOPFS', 'TOREN', 'TORFS', 'UNRAT', 'UNRUH', 'UNSER', 'UNSRE', 
'UNTAT', 'UNTEN', 'UNTER', 'UNZEN', 'URAHN', 'URALT', 'URANS', 'URBAN', 'URIGE', 'URINS', 'URNEN', 'USERS', 'WAAGE', 
'DEBIT', 'INANE', 'CUTUP', 'EROSE', 'RENTE', 'DICER', 'ENURE', 'BATON', 'INUST', 'TEPEE']

DICTIONARY_ = ['ABORTS', 'ABRATE', 'ABRAUM', 'ABREDE', 'ABREGE', 'ABREGT', 'ABRIEB', 'ABRIET', 'ABRISS', 'ABRUFE',
               'ABRUFS', 'ABRUFT', 'ABRUPT', 'ABSAGE', 'ABSAGT', 'ABSAHT', 'ABSANK', 'ABSATZ', 'ABSEHE', 'ABSEHT',
               'ABSTOO', 'ABSUDE', 'ABSURD', 'ABTEIL', 'ABTRAT', 'ABTRUG', 'ABTUST', 'ABWAHL', 'ABWARF', 'ABWEGE',
               'ABWEGS', 'ABWEHR', 'ABWICH', 'ABWIND', 'ABWOGT', 'ABWURF', 'ABZOGT', 'ABZUGS', 'ACETON', 'ACHIMS',
               'ACHSEL', 'ACHSEN', 'ACHSIG', 'ACHTEL', 'ACHTEM', 'ACHTEN', 'ACHTER', 'ACHTES', 'ACHTET', 'ACHTLE',
               'ACIDUM', 'CALLET', 'OPIATE', 'MIMBAR', 'PENILE', 'OCELOT', 'BOOTET', 'BORDEN', 'BORDES', 'BORGEN',
               'BORGST', 'BORGTE', 'BORKEN', 'BORKUM', 'BORSTE', 'BORTEN', 'BOSSEN', 'BOSSES', 'BOSTON', 'BOTANK',
               'BOTEST', 'BOUCLE', 'BOXEND', 'BOXERN', 'BOXERS', 'BOXEST', 'BOXTEN', 'BOXTET', 'BRACHT', 'BRAHMS',
               'BRANDE', 'BRANDS', 'BRANDT', 'BRATEN', 'BRATET', 'BRAUCH', 'BRAUEN', 'BRAUER', 'BRAUNE', 'BRAUSE',
               'BRAUST', 'BRAUTE', 'BRAVEM', 'BRAVEN', 'BRAVER', 'BRAVES', 'BRAVUR', 'BRECHE', 'BRECHT', 'CABRIO',
               'CACHES', 'CALVIN', 'CAMION', 'CAMPER', 'CAMPUS', 'CANNES', 'CANONS', 'CARDIN', 'CARLOS', 'CAROLA', 
               'CAROLS', 'CARUSO', 'CASINO', 'CASTRO', 'CATHYS', 'CELLOS', 'CENTER', 'CENTOS', 'CETERA', 'CEYLON', 
               'CHALET', 'CHANCE', 'CHANEL', 'CHARGE', 'CHARME', 'CHARTA', 'CHARTS', 'CHATEN', 'CHATET', 'CHECKS', 
               'EHRTET', 'EHRUNG', 'EICHEL', 
               'EICHEN', 'EICHST', 'EICHTE', 'EIFERE', 'EIFERN', 'EIFERS', 'EIFERT', 'EIFRIG', 'EIGELB', 'EIGENE', 
               'EIGENS', 'EIGNEN', 'EIGNER', 'EIGNET', 'EILAND', 'EILEND', 'EILGUT', 'EILIGE', 'EILTEN', 'EILTET', 
               'EILZUG', 'EIMERN', 'EIMERS', 'EINBAU', 'EINEHE', 'EINEND', 'EINGAB', 'EINHER', 'EINIGE', 'EINIGT', 
               'EINLUD', 'EINMAL', 'EINRAD', 'EINSAH', 'EINSAM', 'EINSEN', 'EINTEN', 'EINTET', 'EINZEL', 'EINZIG', 
               'EINZOG', 'EINZUG', 'EISENS', 'EISERN', 'EISIGE', 'EITERE', 'EITERN', 'EITERS', 'EITERT', 'EITLEM', 
               'EITLEN', 'EITLER', 'EITLES', 'EITRIG', 'EIWEIO', 'EKELIG', 'EKELND', 'EKELST', 'EKELTE', 'EKLIGE', 
               'EKZEME', 'EKZEMS', 'ELCHEN', 'ELCHES', 'ELEGIE', 'ELENDE', 'ELENDS', 'ELFMAL', 'ELFTEL', 'ELFTEM', 
               'ELFTEN', 'ELFTER', 'ELFTES', 'ELITEN', 'ELIZAS', 'ELSASS', 'ELSTER', 'ELTERN', 'EMANZE', 'EMBLEM', 
               'EMBRYO', 'EMDENS', 'EMILIA', 'EMIRAT', 'EMPORE', 'EMSIGE', 'ENDEND', 'ENDENS', 'ENDEST', 'ENDETE', 
               'ENDLOS', 'ENDUNG', 'ENGELN', 'ENGELS', 'ENGERE', 'ENGSTE', 'ENGTEN', 'ENGTET', 'ENKELN', 'ENKELS', 
               'ENORME', 'ENTBOT', 'ENTERE', 'ENTERN', 'ENTERT', 'ENTHOB', 'ENTKAM', 'ENTLUD', 'ENTZOG', 'ENTZUG', 
               'ENZIAN', 'ENZYME', 'ENZYMS', 'EPIKUR', 'EPILOG', 'EPISCH', 'EPOCHE', 'EPOXYD', 'EPSONS', 'EQUIPE', 
               'ERAHNE', 'ERAHNT', 'ERBAUE', 'ERBAUT', 'ERBEBE', 'ERBEBT', 'ERBEND', 'ERBENS', 'ERBGUT', 'ERBOST', 
               'ERBSEN', 'ERBTEN', 'ERBTET', 'ERDEND', 'ERDENS', 'ERDEST', 'ERDETE', 'ERDGAS', 'ERDIGE', 'ERDNAH', 
               'ERDUNG', 'EREILE', 'EREILT', 'EREMIT', 'ERERBT', 'ERFAND', 'ERFOLG', 'ERFROR', 'ERFUHR', 'ERFURT', 
               'ERGABT', 'ERGEBE', 'ERGEBT', 'ERGEHE', 'ERGEHT', 'ERGIBT', 'ERGING', 'ERGOSS', 'ERGUSS', 'ERHALT', 
               'ERHARD', 'ERHEBE', 'ERHEBT', 'ERHOBT', 'ERHOLE', 'ERHOLT', 'ERICHS', 'ERIKAS', 'ERKERN', 'ERKERS', 
               'ERKORT', 'ERLAGT', 'ERLASS', 'ERLEBE', 'ERLEBT', 'ERLEGE', 'ERLEGT', 'ERLIEF', 'ERLIEO', 'ERLITT', 
               'ERNEUT', 'ERNSTE', 'ERNTEN', 'ERNTET', 'EROBRE', 'EROGEN', 'EROTIK', 'ERRANG', 'ERRATA', 'ERRATE', 
               'ERREGE', 'ERREGT', 'ERRIET', 'ERSANN', 'ERSATZ', 'ERSEHE', 'ERSEHT', 'ERSTEM', 'ERSTEN', 'ERSTER', 
               'ERSTES', 'ERTRAG', 'ERTRUG', 'ERWARB', 'ERWERB', 'ERWIES', 'ERWINS', 'ERWIRB', 'ERWOGT', 'ERZOGT', 
               'ESCHEN', 'ESCHER', 'ESCUDO', 'ESELEI', 'ESKIMO', 'ESKUDO', 'ESSAYS', 'ESSBAR', 'ESSEND', 'ESSENS', 
               'ESSENZ', 'ESSERN', 'ESSERS', 'ESSIGS', 'ETAGEN', 'ETAPPE', 'ETWAIG', 'EUKLID', 'EULERS', 'EUNUCH', 
               'EUROPA', 'EUTERN', 'EUTERS', 'EWIGEM', 'EWIGEN', 'EWIGER', 'EWIGES', 'EXAKTE', 'EXAMEN', 'EXILEN', 
               'EXKURS', 'EXOGEN', 'EXOTEN', 'EXOTIN', 'EXPORT', 'EXPOSE', 'EXTERN', 'EXTRAS', 'EXTREM', 'EXZESS',
               'SERENE', 'COMPOS', 'APIECE', 'LIMNER', 'LABILE', 'ETALON', 'TERETE', 'GABELE', 'GABELN', 'GABELT', 
               'GABLER', 'GABLIG', 'GACKRE', 'GAFFEN', 'GAFFST', 'GAFFTE', 'GALANT', 'GALGEN', 'GALLEN', 'GALLIG', 
               'GALOPP', 'GALTEN', 'GALTET', 'GALTST', 'GANDHI', 'GANGES', 'GANOVE', 'GANZEM', 'GANZEN', 'GANZER', 
               'GANZES', 'GARAGE', 'GARANT', 'GARBEN', 'GARBOS', 'GARDEN', 'GARNEN', 'GARNES', 'GARTEN', 'GASSEN', 
               'GASTES', 'GASTOD', 'GATTEN', 'GATTER', 'GATTIN', 'GAUCHO', 'GAUKEL', 'GAUKLE', 'GAULLE', 'GAUMEN', 
               'GAUNER', 'GEAHNT', 'GEBART', 'GEBAUT', 'GEBEBT', 'GEBEIN', 'GEBELL', 'GEBEND', 'GEBENS', 'GEBERN', 
               'GEBERS', 'GEBETE', 'GEBETS', 'GEBIET', 'GEBISS', 'GEBOTE', 'GEBOTS', 'GEBOXT', 'GEBUNG', 'GEBURT', 
               'GECKEN', 'GEDECK', 'GEDIEH', 'GEDOPT', 'GEDULD', 'GEEHRT', 'GEEILT', 'GEEINT', 'GEERBT', 'GEFAHR', 
               'GEFAXT', 'GEFEGT', 'GEFEIT', 'GEFIEL', 'GEFIXT', 'GEFROR', 'GEGEND', 'GEGNER', 'GEHABE', 'GEHABT', 
               'GEHALT', 'GEHEGE', 'GEHEGT', 'GEHEIM', 'GEHEIO', 'GEHEND', 'GEHENS', 'GEHEUL', 'GEHIRN', 'GEHOLT', 
               'GEHUPE', 'GEHUPT', 'GEHWEG', 'GEIERN', 'GEIERS', 'GEIFER', 'GEIGEN', 'GEIGER', 'GEIGST', 'GEIGTE', 
               'GEILEM', 'GEILEN', 'GEILER', 'GEILES', 'GEILST', 'GEIOEL', 'GEIOEN', 'GEIOLE', 'GEIRRT', 'GEISEL', 
               'GEISHA', 'GEISTE', 'GEISTS', 'GEIZEN', 'GEIZES', 'GEIZIG', 'GEIZTE', 'GEJAGT', 'GEKAUT', 'GELABT', 
               'GELAGE', 'GELANG', 'GELASS', 'GELBEM', 'GELBEN', 'GELBER', 'GELBES', 'GELDER', 'GELDES', 'GELEBT', 
               'GELEES', 'GELEGT', 'GELEIS', 'GELEIT', 'GELENK', 'GELIND', 'GELLEN', 'GELLST', 'GELLTE', 'GELOBE', 
               'GUSSES', 'FABELN', 
               'FABIAN', 'FABRIK', 'FACHEM', 'FACHEN', 'FACHER', 'FACHES', 'FACHST', 'FACHTE', 'FACKEL', 'FACKLE', 
               'FADENS', 'FADERE', 'FADEST', 'FAHLEM', 'FAHLEN', 'FAHLER', 'FAHLES', 'FAHLST', 'FAHNDE', 'FAHNEN', 
               'FAHREN', 'FAHRER', 'FAHRIG', 'FAIBLE', 'FAIREM', 'FAIREN', 'FAIRER', 'FAIRES', 'FAKTEN', 'FAKTES', 
               'FAKTOR', 'FAKTUM', 'FALBEM', 'FALBEN', 'FALBER', 'FALBES', 'FALKEN', 'FALLEN', 'FALLES', 'FALSCH', 
               'FALTEN', 'FALTER', 'FALTET', 'FALTIG', 'FAMOSE', 'FANDEN', 'FANDET', 'FANDST', 'FANGEN', 'FANGES', 
               'FARBEN', 'FARBIG', 'FARMEN', 'FARMER', 'FARNEN', 'FARNES', 'FASANE', 'FASANS', 'FASELE', 'FASELN', 
               'FASELT', 'FASERN', 'FASRIG', 'FASSEN', 'FASSES', 'FASSTE', 'FASTEN', 'FASTET', 'FATALE', 'FATIMA', 
               'FATUMS', 'FAUCHE', 'FAUCHT', 'FAULEM', 'FAULEN', 'FAULER', 'FAULES', 'FAULIG', 'FAULST', 'FAULTE', 
               'FAUNEN', 'FAXEND', 'FAXEST', 'FAXTEN', 'FAXTET', 'FAZITE', 'FAZITS', 'FECHTE', 'FEDERE', 'FEDERN', 
               'FEDERT', 'FEDORA', 'FEGEND', 'FEGTEN', 'FEGTET', 'FEHDEN', 'FEHLEN', 'FEHLER', 'FEHLST', 'FEHLTE', 
               'FEIERE', 'FEIERN', 'FEIERT', 'FEIGEM', 'FEIGEN', 'FEIGER', 'FEIGES', 'FEIGST', 'FEILEN', 'FEILST', 
               'FEILTE', 'FEINDE', 'FEINDS', 'FEINEM', 'FEINEN', 'FEINER', 'FEINES', 'FEINST', 'FELDER', 'FELDES', 
               'FELGEN', 'FELLEN', 'FELSEN', 'FELSIG', 'FERIEN', 'FERKEL', 'FERMAT', 'FERMIS', 'FERNAB', 'FERNEM', 
               'FERNEN', 'FERNER', 'FERNES', 'FERNST', 'FERSEN', 'FERTIG', 'FESCHE', 'FESSEL', 'FESSLE', 'FESTEM', 
               'FESTEN', 'FESTER', 'FESTES', 'FETTEM', 'FETTEN', 'FETTER', 'FETTES', 'FETTIG', 'FETZEN', 'FETZIG', 
               'FEUCHT', 'FEUDAL', 'FEUERE', 'FEUERN', 'FEUERS', 'FEUERT', 'FEURIG', 'FIASKO', 'FIBELN', 'FICHTE', 
               'FICKEN', 'FICKER', 'FICKST', 'FICKTE', 'FIDELE', 'FIEBER', 'FIEBRE', 'FIELEN', 'FIELST', 'FIESEM', 
               'FIESEN', 'FIESER', 'FIESES', 'FIKTIV', 'FILETS', 'FILIUS', 'FILMEN', 'FILMES', 'FILMST', 'FILMTE', 
               'FILTER', 'FILTRE', 'FILZEN', 'FILZES', 'FILZIG', 'FILZTE', 'FIMMEL', 'FINALE', 'FINANZ', 'FINDEN', 
               'FINDER', 'FINDET', 'FINDIG', 'FINGEN', 'FINGER', 'FINGST', 'FINITE', 'FINKEN', 'FINNEN', 'FINNIN', 
               'FINTEN', 'FIRMEN', 'FIRSTE', 'FIRSTS', 'FISCHE', 'FISCHS', 'FISCHT', 'FISKUS', 'FISTEL', 'FITTEM', 
               'FITTEN', 'FITTER', 'FITTES', 'FIXEND', 'FIXERN', 'FIXERS', 'FIXEST', 'FIXTEN', 'FIXTET', 'FJORDE', 
               'FJORDS', 'FLACHE', 'FLACHS', 'FLACON', 'FLADEN', 'FLAGGE', 'FLAGGT', 'FLAKON', 'FLAMEN', 'FLAMME', 
               'FLAMMT', 'FLANKE', 'FLAUEM', 'FLAUEN', 'FLAUER', 'FLAUES', 'FLAUMS', 'FLAUST', 'FLAUTE', 'FLECKE', 
               'FLECKS', 'FLEGEL', 'FLEHEN', 'FLEHST', 'FLEHTE']

"""
T U N
A   U
T O T

T,N[]  O,U,A T,N , N,T[]
[],A  

B A
C

  H A U 
B A N D
A S S E
D E I N

H A U S
B A U M
E   D U
K G   M

H A U S
  L U X
F E R D
B O D

H O S E S
# # A # T
# H I K E 
A # L E E
L A S E R
E # # L #

B A R # I R
# S O N N E
H M # E N G
# A M I # L
G R U N D E 
# A S # U R
"""




DICTIONARY_ = ['HAU', 'BAND', 'ASSE', 'DEIN', 'BAD', 'HASE', 'ANSI', 'UDEN']
DICTIONARY_ = ['HAUS', 'LUX', 'FERD', 'BOD', 'FB', 'ALEO', 'UURD', 'SXD']
DICTIONARY_ = ['TUN', 'NUT', 'TAT', 'TOT']
DICTIONARY_ = ['BA', 'BC']
DICTIONARY_ = ['IN', 'IF', 'NUT', 'NO', 'FUN', 'TO']
DICTIONARY_ = ['HAUS', 'BANDE', 'AS', 'ER', 'DEINE', 'BADE', 'HASEN', 'AN', 'UDENR' 'SERE', 'ENSR', 'IS']
DICTIONARY_ = ['HOSES', 'LASER', 'SAILS', 'SHEET', 'STEER', 'HEEL', 'HIKE', 'KEEL', 'KNOT' 'LINE', 'AFT', 'ALE', 'EEL', 'LEE', 'TIE']
DICTIONARY_ = ['BAR', 'IR', 'SONNE', 'HM', 'ENG', 'AMI', 'GRUNDE', 'AS', 'UR', 'ASMARA', 'RO', 'MUS', 'NEIN', 'INN', 'DU', 'REGLER']


DICTIONARY = ['BRAUSE', 'RASA', 'ANONYM', 'SALATE',
               'BREZEL', 'NATION', 'ANHAND',
               'SOUL', 'ANSAGE', 'ALBEN', 'ORCA', 'INSEKT', 
               'REGATTA', 'BOLERO', 'RAMPE', 'MALEN', 
               'EIGELB', 'ALBEREI', 'SULTAN', 
               'ETAT', 'SPAT', 'APFEL', 'EIBE', 'PANGEA',
               'SOLE', 'LATERAL', 'TAKT', 'TEEN', 
               'GAGA', 'ASBEST', 'UHRWERK',
               'ADELIGER', 'UMTUN',
               'MIES', 'SEMINAR', 'FASELEI', 'SOLEI',
               'FLORA', 'GRILLEN', 'GEHEN', 'GROSSMACHT', 'OHNE',
               'KARO', 'BETEN', 'STAR', 'SELIG', 'LITER',
               'ZEILE', 'LEDIG', 'NEON', 'ANSEHEN', 'LUPINE', 
               'THRON', 'LIEBE', 'LIBERAL', 'OASE', 'SPULE', 'ISTER',
               'LOCKER', 'TRIEL', 'RAIN', 'PFAND', 'FRITZ',
               'GEWEBE', 'AZUBI', 'ANATHEM',
               'FRITZ', 'SEIFE', 'FAKTUR', 'PFARRER', 'FEGE',
               'FIGUR', 'KLUEVER', 'FEIERN', 'BACKOFEN', 'REISSER',
               'LEBHAFT']

DICTIONARY_ = ['BRAUSE', 'RASA', 'ANONYM', 'UHUS', 'SALATE',
               'DEN', 'LOS', 'BREZEL', 'ECK', 'NATION', 'ANHAND',
               'SOUL', 'ANSAGE', 'ALBEN', 'ORCA', 'INSEKT', 'DIEB',
               'REGATTA', 'BOLERO', 'RAMPE', 'MALEN', 'OFEN',
               'EIGELB', 'ALBEREI', 'EAN', 'SULTAN', 'AKTE', 'RATE',
               'ETAT', 'SPAT', 'APFEL', 'EIBE', 'PANGEA', 'ERN',
               'SOLE', 'BIS', 'LATERAL', 'TAKT', 'TEEN', 'OMA',
               'GAGA', 'SET', 'NON', 'RAPS', 'ASBEST', 'UHRWERK',
               'ADELIGER', 'MAGD', 'GR', 'DE', 'FLAU', 'OFT', 'UMTUN',
               'MIES', 'ROH', 'SEMINAR', 'FASELEI', 'EGO', 'SOLEI',
               'FLORA', 'GRILLEN', 'GEHEN', 'ERR', 'GROSSMACHT', 'OHNE',
               'KARO', 'BETEN', 'STAR', 'SELIG', 'LITER',
               'ZEILE', 'LEDIG', 'NEON', 'ANSEHEN', 'LUPINE', 'NEI',
               'THRON', 'LIEBE', 'LIBERAL', 'OASE', 'SPULE', 'ISTER',
               'LOCKER', 'TRIEL', 'DAS', 'RAIN', 'PFAND', 'AAS', 'FRITZ',
               'HUF', 'GEWEBE', 'MIS', 'FES', 'AZUBI', 'ANATHEM',
               'FRITZ', 'SEIFE', 'AUT', 'FAKTUR', 'PFARRER', 'FEGE',
               'FIGUR', 'KLUEVER', 'FEIERN', 'BACKOFEN', 'REISSER',
               'LEBHAFT']
