import pandas as pd
import plotly.graph_objects as go
import plotly.io as py
import geopy.distance

from shapely.geometry import LineString, mapping

WSSS_coordinates = ('012133N', '1035922E')

SG_FIR_coordinates = [
    ('082500N', '1163000E'), 
    ('025050N', '1091629E'), 
    ('045700N', '1081619E'), 
    ('050012N', '1080132E'), 
    ('045904N', '1075525E'), 
    ('045203N', '1074625E'), 
    ('043820N', '1073315E'), 
    ('041312N', '1071743E'), 
    ('033045N', '1055130E'), 
    ('031727N', '1052959E'), 
    ('031453N', '1052619E'), 
    ('025010N', '1051210E'), 
    ('024348N', '1050854E'), 
    ('023641N', '1051311E'), 
    ('021838N', '1052205E'), 
    ('011947N', '1044606E'), 
    ('012921N', '1043441E'), 
    ('011800N', '1043000E'), 
    ('011500N', '1040000E'), 
    ('010800N', '1034500E'), 
    ('011046N', '1034015E'), 
    ('011200N', '1033900E'), 
    ('011408N', '1033142E'), 
    ('011700N', '1033600E'), 
    ('012608N', '1034055E'), # National boundary of Singapore/Malaysia
    ('012730N', '1034326E'), # National boundary of Singapore/Malaysia
    ('012640N', '1034540E'), # National boundary of Singapore/Malaysia
    ('012832N', '1034809E'), # National boundary of Singapore/Malaysia
    ('012557N', '1035320E'), # National boundary of Singapore/Malaysia
    ('012513N', '1040006E'), # National boundary of Singapore/Malaysia
    ('012638N', '1040222E'), # National boundary of Singapore/Malaysia
    ('012421N', '1040528E'), # National boundary of Singapore/Malaysia
    ('012127N', '1040440E'), # National boundary of Singapore/Malaysia
    ('011937N', '1040551E'), # National boundary of Singapore/Malaysia
    ('012000N', '1042000E'), 
    ('023600N', '1044500E'), 
    ('034000N', '1034000E'), 
    ('045000N', '1034400E'), 
    ('064500N', '1024000E'), 
    ('070000N', '1030000E'), 
    ('070000N', '1080000E'), 
    ('103000N', '1140000E'), 
    ('082500N', '1163000E')
]

KL_FIR_vested1_coordinates = [
    ('023600N', '1044500E'),
    ('023200N', '1050000E'),
    ('060000N', '1050000E'), 
    ('060000N', '1030500E'), 
    ('045000N', '1034400E'), 
    ('034000N', '1034000E'), 
    ('023600N', '1044500E')
]

KL_FIR_vested2_coordinates = [
    ('023200N', '1050000E'),
    ('060000N', '1050000E'), 
    ('060000N', '1132000E'), 
    ('025050N', '1091629E'), 
    ('045700N', '1081619E'), 
    ('050012N', '1080132E'), 
    ('045904N', '1075525E'), 
    ('045203N', '1074625E'), 
    ('043820N', '1073315E'), 
    ('041312N', '1071743E'), 
    ('033045N', '1055130E'), 
    ('031727N', '1052959E'), 
    ('031453N', '1052619E'), 
    ('025010N', '1051210E'), 
    ('024348N', '1050854E'), 
    ('023641N', '1051311E'),
    ('022715N', '1051750E'),
    ('023200N', '1050000E'),
]

JARKARTA_FIR_delegated_coordinates = [
    ('031727N', '1052959E'),
    ('012450N', '1061648E'),
    ('001030N', '1045656E'),
    ('000000N', '1050340E'),
    ('000000N', '1044330E'),
    ('001113S', '1042205E'), # Arc of airspace
    ('001620S', '1035827E'), # Arc of airspace
    ('001458S', '1033419E'), # Arc of airspace
    ('000714S', '1031124E'), # Arc of airspace
    ('000618N', '1025123E'), # Arc of airspace
    ('002442N', '1023541E'), # Arc of airspace
    ('004636N', '1022528E'), # Arc of airspace
    ('011026N', '1022126E'), # Arc of airspace
    ('013430N', '1022353E'),
    ('011300N', '1033000E'),
    ('011408N', '1033142E'),
    ('011200N', '1033900E'),
    ('011046N', '1034015E'),
    ('010800N', '1034500E'),
    ('011500N', '1040000E'),
    ('011800N', '1043000E'),
    ('012921N', '1043441E'),
    ('011947N', '1044606E'),
    ('021838N', '1052205E'),
    ('023641N', '1051311E'),
    ('024348N', '1050854E'),
    ('025010N', '1051210E')
]

SG_JHR_airspace_complex_coordinates = [
    ('022600N', '1025605E'),
    ('022600N', '1043400E'),
    ('004300N', '1043400E'),
    ('004300N', '1025605E'),
    ('022600N', '1025605E')
]

waypoints_all = {
    'ABVIP': ('010008N', '1035032E'),
    'ABVON': ('012028N', '1035827E'),
    'ADNIK': ('011651N', '1035655E'),
    'ADPON': ('011203N', '1040514E'),
    # 'ADPON': ('010108N', '1035808E'),
    'AGROT': ('010108N', '1035808E'),
    'AGVAR': ('014719N', '1034145E'),
    'AKDAT': ('032923N', '1054917E'),
    'AKIPO': ('011356N', '1035542E'),
    'AKMET': ('015355N', '1034339E'),
    'AKMON': ('081254N', '1101306E'),
    'AKOMA': ('014522N', '1035443E'),
    'AKVOM': ('005620N', '1041514E'),
    'ANBUS': ('011554N', '1032100E'),
    'ANITO': ('001700S', '1045200E'),
    'ANUMA': ('011053N', '1035424E'),
    'APIPA': ('010618N', '1035228E'),
    'ARAMA': ('013654N', '1030712E'),
    'AROSO': ('020846N', '1032421E'),
    'ASISU': ('055906N', '1132046E'),
    'ASITI': ('004906N', '1035042E'),
    'ASOMI': ('010142N', '1040207E'),
    'ASUNA': ('005948N', '1030954E'),
    'ATLEX': ('010302N', '1033331E'),
    'ATLIR': ('011120N', '1035208E'),
    'ATPOM': ('002425N', '1052114E'),
    'ATRUM': ('013256N', '1040057E'),
    'AVLUB': ('003112S', '1042501E'),
    'AVPIV': ('011207N', '1035349E'),
    'BAVAL': ('004518N', '1040242E'),
    'BETBA': ('013302N', '1035331E'),
    'BIBVI': ('024336N', '1040618E'),
    'BIDAG': ('073101N', '1135544E'),
    'BIDUS': ('013554N', '1035755E'),
    'BIKTA': ('024337N', '1034308E'),
    'BIMOS': ('011512N', '1035815E'),
    'BIPOP': ('013122N', '1041018E'),
    'BISOV': ('004229N', '1025214E'),
    'BISUT': ('011218N', '1035701E'),
    'BITAM': ('010813N', '1040757E'),
    'BOBAG': ('010230N', '1032954E'),
    'BOBOB': ('022206N', '1070558E'),
    'BONSU': ('011928N', '1033710E'),
    'BOPVA': ('025303N', '1051349E'),
    'BUNTO': ('024200N', '1060000E'),
    'BUVAL': ('033622N', '1034341E'),
    'DAKIX': ('070854N', '1145054E'),
    'DAMOG': ('041225N', '1050014E'),
    'DODSO': ('012225N', '1061402E'),
    'DOLOX': ('044841N', '1052247E'),
    'DOVAN': ('011938N', '1041249E'),
    'DOVOL': ('033047N', '1034923E'),
    'DOWON': ('011957N', '1043048E'),
    'DUBOT': ('010846N', '1040103E'),
    'DUBSA': ('034901N', '1044540E'),
    'DUDIS': ('070000N', '1064836E'),
    'DUMUP': ('005430N', '1035516E'),
    'EGOLO': ('031934N', '1040047E'),
    'EGORA': ('013621N', '1040607E'),
    'ELALO': ('041240N', '1043329E'),
    'ELALU': ('013440N', '1040524E'),
    'ELBEB': ('012845N', '1040254E'),
    'ELBEX': ('013149N', '1040314E'),
    'ELGAP': ('012820N', '1040146E'),
    'ELGOR': ('033014N', '1054818E'),
    'ELMIN': ('012550N', '1040141E'),
    'EMRIX': ('012606N', '1041040E'),
    'EMSIB': ('005911N', '1035419E'),
    'EMSUX': ('024647N', '1051026E'),
    'EMTAP': ('011656N', '1035657E'),
    'ENLES': ('010932N', '1035350E'),
    'ENPUX': ('002859S', '1043434E'),
    'ENREP': ('045224N', '1041442E'),
    'ENSUN': ('012603N', '1040048E'),
    'ENVUM': ('011535N', '1040552E'),
    'ERVIV': ('010445N', '1041013E'),
    'ERVOT': ('011120N', '1035436E'),
    'ESBIT': ('012212N', '1040009E'),
    'ESBUM': ('045210N', '1042830E'),
    'ESLUX': ('011844N', '1035840E'),
    'ESPOB': ('070000N', '1053318E'),
    'EXOMO': ('010425N', '1040933E'),
    'GIXEM': ('004920N', '1042539E'),
    'GOTGA': ('012013N', '1044200E'),
    'GULGU': ('040141N', '1084242E'),
    'GULIB': ('041714N', '1110633E'),
    'GUMPU': ('013000N', '1034243E'),
    'GUNUD': ('011042N', '1050618E'),
    'GURES': ('002814N', '1043835E'),
    'GUTUP': ('045911N', '1075603E'),
    'HOSBA': ('011948N', '1042418E'),
    'IBASU': ('005751N', '1033410E'),
    'IBIVA': ('011351N', '1035637E'),
    'IBIXU': ('011621N', '1035740E'),
    'IDBUD': ('001454N', '1050139E'),
    'IDEMO': ('025431N', '1040603E'),
    'IDKIV': ('005652N', '1041333E'),
    'IDMAS': ('004900N', '1041848E'),
    'IDSEL': ('032432N', '1035544E'),
    'IDUNA': ('012306N', '1035934E'),
    'IDURO': ('012640N', '1040104E'),
    'IDVAS': ('012935N', '1040218E'),
    'IGARI': ('065612N', '1033506E'),
    'IGNON': ('010847N', '1041257E'),
    'IGOSI': ('005645N', '1040644E'),
    'IGULA': ('013232N', '1040333E'),
    'IGUTU': ('001331S', '1041857E'),
    'IKIRO': ('000849N', '1044420E'),
    'IKUKO': ('054512N', '1031324E'),
    'IKUMI': ('055338N', '1035509E'),
    'INVUB': ('002749N', '1051530E'),
    'IPDOL': ('045111N', '1035920E'),
    'IPNAK': ('013712N', '1040531E'),
    'IPRIX': ('070000N', '1040754E'),
    'IRPUG': ('005813N', '1040127E'),
    'IRSAB': ('024349N', '1054359E'),
    'IRTAD': ('010326N', '1041147E'),
    'ISDEB': ('024440N', '1063011E'),
    'ISGIL': ('004246N', '1031257E'),
    'ISNOM': ('010629N', '1035826E'),
    'JUNHA': ('005413N', '1043052E'),
    'KAKSA': ('011703N', '1035758E'),
    'KANLA': ('034556N', '1043606E'),
    'KARTO': ('011124N', '1053343E'),
    'KASPO': ('011507N', '1035709E'),
    'KETOD': ('031042N', '1040942E'),
    'KEXAS': ('011019N', '1044818E'),
    'KEXOL': ('043930N', '1040942E'),
    'KIBOL': ('025224N', '1042818E'),
    'KILOT': ('030217N', '1044023E'),
    'KIMER': ('011106N', '1035527E'),
    'KIRDA': ('000009N', '1045934E'),
    'LAGOT': ('071632N', '1113243E'),
    'LAGUS': ('011915N', '1035854E'),
    'LAPOL': ('012622N', '1034435E'),
    'LASIN': ('011538N', '1035722E'),
    'LAVAX': ('010950N', '1042714E'),
    'LAXOR': ('094937N', '1144829E'),
    'LEBIN': ('031438N', '1060604E'),
    'LEDOX': ('011642N', '1035651E'),
    'LEGOL': ('012053N', '1034723E'),
    'LELIB': ('012729N', '1032450E'),
    'LELON': ('011244N', '1035609E'),
    'LENDA': ('024124N', '1043932E'),
    'LEPNA': ('010648N', '1035339E'),
    'LETGO': ('011411N', '1035548E'),
    'LIDVA': ('010506N', '1035339E'),
    'LIGVU': ('034417N', '1061859E'),
    'LIPRO': ('025342N', '1051128E'),
    'LUSMO': ('033341N', '1065534E'),
    'LUXOL': ('011803N', '1035823E'),
    'MABAL': ('032826N', '1051236E'),
    'MABLI': ('041717N', '1061247E'),
    'MANIM': ('031430N', '1040554E'),
    'MASBO': ('020248N', '1025251E'),
    'MASNI': ('012037N', '1033746E'),
    'MELAS': ('070518N', '1080912E'),
    'MIBEL': ('012351N', '1020816E'),
    'MOLVO': ('012955N', '1040227E'),
    'MOXIB': ('012933N', '1040315E'),
    'MUMDU': ('010521N', '1042714E'),
    'MUMSO': ('034420N', '1053213E'),
    'NIVAM': ('023650N', '1040228E'),
    'NIXEB': ('013943N', '1061040E'),
    'NODIN': ('081100N', '1161142E'),
    'NOPAT': ('042313N', '1044756E'),
    'NUFFA': ('025341N', '1033829E'),
    'NYLON': ('013657N', '1040624E'),
    'OBDAB': ('031153N', '1040538E'),
    'OBDOS': ('002503N', '1065551E'),
    'OBGET': ('012307N', '1064531E'),
    'ODONO': ('063614N', '1030129E'),
    'OLKIT': ('045010N', '1115118E'),
    'OLMUT': ('030306N', '1053558E'),
    'OLNUB': ('011110N', '1035147E'),
    'OMDUD': ('005847N', '1035714E'),
    'OMKOM': ('013112N', '1035910E'),
    'OMLIV': ('025512N', '1062812E'),
    'OSERU': ('024450N', '1054334E'),
    'OTLAL': ('004209N', '1053052E'),
    'OTLON': ('030752N', '1042006E'),
    'PADLI': ('030918N', '1033133E'),
    'PALGA': ('011059N', '1034759E'),
    'PAMSI': ('010459N', '1034845E')
}

STAR_SID_waypoints = {
    'ABVIP': ('010008N', '1035032E'),
    'ADPON': ('011203N', '1040514E'),
    # 'ADPON': ('010108N', '1035808E'),
    'AGROT': ('010108N', '1035808E'),
    'AGVAR': ('014719N', '1034145E'),
    'AKMET': ('015355N', '1034339E'),
    'AKOMA': ('014522N', '1035443E'),
    'ALFA' : ('013033N', '1034942E'),
    'ANITO': ('001700S', '1045200E'),
    'ARAMA': ('013654N', '1030712E'),
    'AROSO': ('020846N', '1032421E'),
    'ASITI': ('004906N', '1035042E'),
    'ASOMI': ('010142N', '1040207E'),
    'ASUNA': ('005948N', '1030954E'),
    'ATLEX': ('010302N', '1033331E'),
    'ATRUM': ('013256N', '1040057E'),
    'BETBA': ('013302N', '1035331E'),
    'BIBVI': ('024336N', '1040618E'),
    'BIDUS': ('013554N', '1035755E'),
    'BIPOP': ('013122N', '1041018E'),
    'BISOV': ('004229N', '1025214E'),
    'BITAM': ('010813N', '1040757E'),
    'BOBAG': ('010230N', '1032954E'),
    'BOKIP': ('010421N', '1034353E'),
    'BTM'  : ('010813N', '1040758E'),
    'DODSO': ('012225N', '1061402E'),
    'DOVAN': ('011938N', '1041249E'),
    'DUBOT': ('010846N', '1040103E'),
    'DUMUP': ('005430N', '1035516E'),
    'ELALO': ('041240N', '1043329E'),
    'EMRIX': ('012606N', '1041040E'),
    'ERVIV': ('010445N', '1041013E'),
    'GIXEM': ('004920N', '1042539E'),
    'GOTGA': ('012013N', '1044200E'),
    'GUMPU': ('013000N', '1034243E'),
    'GUNUD': ('011042N', '1050618E'),
    'GURES': ('002814N', '1043835E'),
    'HOSBA': ('011948N', '1042418E'),
    'IBASU': ('005751N', '1033410E'),
    'IBIVA': ('011351N', '1035637E'),
    'IBIXU': ('011621N', '1035740E'),
    'IDBUD': ('001454N', '1050139E'),
    'IDKIV': ('005652N', '1041333E'),
    'IGNON': ('010847N', '1041257E'),
    'IGOSI': ('005645N', '1040644E'),
    'IKIRO': ('000849N', '1044420E'),
    'ISGIL': ('004246N', '1031257E'),
    'ISNOM': ('010629N', '1035826E'),
    'KANLA': ('034556N', '1043606E'),
    'KARTO': ('011124N', '1053343E'),
    'KEXAS': ('011019N', '1044818E'),
    'KILOT': ('030217N', '1044023E'),
    'KIRDA': ('000009N', '1045934E'),
    'LAMA' : ('013150N', '1035850E'), #Added from ENR 3.6 holding list
    'LAVAX': ('010950N', '1042714E'),
    'LEDOX': ('011642N', '1035651E'),
    'LELIB': ('012729N', '1032450E'),
    'LETGO': ('011411N', '1035548E'),
    'MABAL': ('032826N', '1051236E'),
    'MASBO': ('020248N', '1025251E'),
    'MIBEL': ('012351N', '1020816E'),
    'MOLVO': ('012955N', '1040227E'),
    'MOXIB': ('012933N', '1040315E'),
    'MUMDU': ('010521N', '1042714E'),
    'NYLON': ('013657N', '1040624E'),
    'PALGA': ('011059N', '1034759E'),
    'PAMSI': ('010459N', '1034845E'),
    'PASPU': ('015915N', '1040618E'),
    'PIBAP': ('023023N', '1040618E'),
    'POSUB': ('012725N', '1040748E'),
    'POVEB': ('011344N', '1040130E'),
    'PU'   : ('012524N', '1035600E'),
    'REMES': ('004342N', '1035735E'),
    'REPOV': ('001623N', '1040300E'),
    'RWY 02R DER': ('012122N', '1040051E'),
    'RWY 02C DER': ('012145N', '1035957E'),
    'RWY 02L DER': ('012305N', '1035933E'),
    'RWY 20C DER': ('011942N', '1035905E'),
    'RWY 20R DER': ('012047N', '1035835E'),
    'RWY 20L DER': ('011919N', '1035959E'),
    'SABKA': ('015051N', '1031713E'),
    'SALRU': ('011701N', '1040802E'),
    'SAMKO': ('010530N', '1035255E'),
    'SANAT': ('010749N', '1035930E'),
    'SEBVO': ('011259N', '1044028E'),
    'SJ'   : ('011321N', '1035115E'),
    'SINJON': ('011321N', '1035115E'),
    'SURGA': ('003657S', '1063119E'),
    'TAROS': ('004200N', '1021612E'),
    'TEBUN': ('011455N', '1031557E'),
    'TOMAN': ('012147N', '1054717E'),
    'TUSPI': ('003301N', '1040959E'), #Added from ENR 3.6 holding list
    'UGEBO': ('003813N', '1052432E'),
    'UKIBO': ('011758N', '1035924E'),
    'UPTEL': ('005925N', '1040730E'),
    'VAMPO': ('005833N', '1032525E'),
    'VANBU': ('010643N', '1042740E'),
    'VASTI': ('004320N', '1043406E'),
    'VEBMA': ('012030N', '1045332E'),
    'VEXEL': ('005904N', '1034254E'),
    'VIBOG': ('004310N', '1034302E'),
    'VIGUD': ('011328N', '1035730E'),
    'VIMAL': ('010942N', '1042353E'),
    'VIRET': ('003940N', '1043511E'),
    'VMR'  : ('022318N', '1035218E'),
    'VOVOS': ('011123N', '1032651E'),
    'VTK'  : ('012455N', '1040120E'),
    'TEKONG' : ('012455N', '1040120E')
}

STARs = {
    'ARAMA1A': ['ARAMA', 'BOBAG', 'BOKIP', 'SAMKO'],
    'ARAMA1B': ['ARAMA', 'BOBAG', 'SAMKO', 'BITAM', 'DOVAN', 'BIPOP'],
    'ASUNA2A': ['ASUNA', 'VAMPO', 'IBASU', 'VEXEL', 'SAMKO'],
    'ASUNA2B': ['ASUNA', 'VAMPO', 'IBASU', 'VEXEL', 'ABVIP', 'AGROT', 'BITAM', 'DOVAN', 'BIPOP'],
    'ELALO1A': ['ELALO', 'KANLA', 'KILOT', 'PIBAP', 'PASPU', 'NYLON', 'POSUB', 'SANAT'],
    'ELALO1B': ['ELALO', 'KANLA', 'KILOT', 'PIBAP', 'PASPU', 'NYLON'],
    'KARTO2A': ['TOMAN', 'KARTO', 'GUNUD', 'KEXAS', 'VIMAL', 'IGNON', 'SANAT'],
    'KARTO2B': ['TOMAN', 'KARTO', 'GUNUD', 'KEXAS', 'LAVAX', 'DOVAN', 'BIPOP'],
    'LEBAR2A': ['PASPU', 'PU', 'SINJON', 'PALGA', 'PAMSI', 'SAMKO'],
    'LEBAR3B': ['REMES', 'SINJON', 'PU', 'BETBA', 'BIDUS'],
    'LELIB3B': ['ARAMA', 'LELIB', 'GUMPU', 'ALFA', 'BIDUS'],
    'MABAL2A': ['MABAL', 'KILOT', 'PIBAP', 'PASPU', 'NYLON', 'POSUB', 'SANAT'],
    'MABAL2B': ['MABAL', 'KILOT', 'PIBAP', 'PASPU', 'NYLON'],
    'REPOV2A': ['REPOV', 'REMES', 'DUMUP', 'SAMKO'],
    'REPOV2B': ['REPOV', 'REMES', 'BITAM', 'DOVAN', 'BIPOP'],
    'TEBUN1A': ['TEBUN', 'VAMPO', 'IBASU', 'VEXEL', 'SAMKO'],
    'TEBUN1B': ['TEBUN', 'VAMPO', 'IBASU', 'VEXEL', 'ABVIP', 'AGROT', 'BITAM', 'DOVAN', 'BIPOP'],
    'UGEBO1A': ['UGEBO', 'GUNUD', 'KEXAS', 'VIMAL', 'IGNON', 'SANAT'],
    'UGEBO1B': ['UGEBO', 'GUNUD', 'KEXAS', 'LAVAX', 'DOVAN', 'BIPOP'],
}

SIDs = {
    'ANITO7A': ['MOXIB','EMRIX','HOSBA','VANBU', 'VIRET', 'GURES', 'IKIRO', 'ANITO'],
    'ANITO8B': ['IBIXU', 'IBIVA','ISNOM','ASOMI','UPTEL', 'IDKIV','GIXEM','VASTI','VIRET','GURES','IKIRO','ANITO'],
    'ANITO1C': ['HOSBA','VANBU','VIRET','GURES','IKIRO','ANITO'],
    'ANITO1D': ['UKIBO', 'ISNOM', 'ASOMI', 'UPTEL', 'IDKIV', 'GIXEM', 'VASTI', 'VIRET', 'GURES', 'IKIRO', 'ANITO'],
    'ANITO7E': ['MOLVO', 'EMRIX', 'HOSBA', 'VANBU', 'VIRET', 'GURES', 'IKIRO', 'ANITO'],
    'ANITO8F': ['LEDOX','LETGO', 'ISNOM', 'ASOMI', 'UPTEL', 'IDKIV', 'GIXEM', 'VASTI', 'VIRET', 'GURES', 'IKIRO', 'ANITO'],
    'AROSO3A': ['MOXIB','AKOMA','AKMET','AROSO'],
    'AROSO5B': ['IBIXU', 'IBIVA', 'DUBOT','ADPON','SALRU','TEKONG','AKOMA','AKMET','AROSO'],
    'AROSO1C': ['AKOMA','AKMET','AROSO'],
    'AROSO1D': ['UKIBO','POVEB','ADPON','SALRU','TEKONG','AKOMA','AKMET','AROSO'],
    'AROSO3E': ['MOLVO','ATRUM','AKOMA','AKMET','AROSO'],
    'AROSO5F': ['LEDOX', 'LETGO', 'DUBOT','ADPON','SALRU','TEKONG','AKOMA','AKMET','AROSO'],
    'DODSO1A': ['MOXIB','EMRIX', 'HOSBA', 'VEBMA', 'TOMAN', 'DODSO'],
    'DODSO1B': ['IBIXU', 'IBIVA','DUBOT', 'ERVIV','MUMDU','SEBVO', 'GOTGA','VEBMA', 'TOMAN', 'DODSO'],
    'DODSO1C': ['HOSBA', 'VEBMA', 'TOMAN', 'DODSO'],
    'DODSO1D': ['UKIBO','DUBOT', 'ERVIV','MUMDU','SEBVO', 'GOTGA','VEBMA', 'TOMAN', 'DODSO'],
    'DODSO1E': ['MOLVO','EMRIX', 'HOSBA', 'VEBMA', 'TOMAN', 'DODSO'],
    'DODSO1F': ['LEDOX', 'LETGO', 'DUBOT', 'ERVIV','MUMDU','SEBVO', 'GOTGA','VEBMA', 'TOMAN', 'DODSO'],
    'IDBUD1A': ['MOXIB','EMRIX','HOSBA','VANBU','VIRET','GURES','IDBUD'],
    'IDBUD1B': ['IBIXU','IBIVA','ISNOM','ASOMI','UPTEL','IDKIV','GIXEM','VASTI','VIRET','GURES','IDBUD'],
    'IDBUD1C': ['HOSBA','VANBU','VIRET','GURES','IDBUD'],
    'IDBUD1D': ['UKIBO', 'ISNOM', 'ASOMI', 'UPTEL', 'IDKIV', 'GIXEM', 'VASTI', 'VIRET', 'GURES', 'IDBUD'],
    'IDBUD1E': ['MOLVO', 'EMRIX', 'HOSBA', 'VANBU', 'VIRET', 'GURES', 'IDBUD'],
    'IDBUD1F': ['LEDOX','LETGO', 'ISNOM', 'ASOMI', 'UPTEL', 'IDKIV', 'GIXEM', 'VASTI', 'VIRET', 'GURES', 'IDBUD'],
    'KIRDA1A': ['MOXIB','EMRIX','HOSBA','VANBU', 'VIRET', 'GURES', 'IKIRO', 'KIRDA'],
    'KIRDA1B': ['IBIXU', 'IBIVA','ISNOM','ASOMI','UPTEL', 'IDKIV','GIXEM','VASTI','VIRET','GURES','IKIRO','KIRDA'],
    'KIRDA1C': ['HOSBA','VANBU','VIRET','GURES','IKIRO','KIRDA'],
    'KIRDA1D': ['UKIBO', 'ISNOM', 'ASOMI', 'UPTEL', 'IDKIV', 'GIXEM', 'VASTI', 'VIRET', 'GURES', 'IKIRO', 'KIRDA'],
    'KIRDA1E': ['MOLVO', 'EMRIX', 'HOSBA', 'VANBU', 'VIRET', 'GURES', 'IKIRO', 'KIRDA'],
    'KIRDA1F': ['LEDOX','LETGO', 'ISNOM', 'ASOMI', 'UPTEL', 'IDKIV', 'GIXEM', 'VASTI', 'VIRET', 'GURES', 'IKIRO', 'KIRDA'],
    'MASBO3A': ['MOXIB','AKOMA','AGVAR','SABKA','MASBO'],
    'MASBO5B': ['IBIXU', 'IBIVA', 'DUBOT','ADPON','SALRU','TEKONG','AKOMA','AGVAR','SABKA','MASBO'],
    'MASBO1C': ['AKOMA','AGVAR','SABKA','MASBO'],
    'MASBO1D': ['UKIBO','POVEB','ADPON','SALRU','TEKONG','AKOMA','AGVAR','SABKA','MASBO'],
    'MASBO3E': ['MOLVO','ATRUM','AKOMA','AGVAR','SABKA','MASBO'],
    'MASBO5F': ['LEDOX', 'LETGO', 'DUBOT','ADPON','SALRU','TEKONG','AKOMA','AGVAR','SABKA','MASBO'],
    'VMR6A': ['MOXIB','AKOMA','VMR'],
    'VMR9B': ['IBIXU', 'IBIVA', 'DUBOT','ADPON','SALRU','TEKONG','AKOMA','VMR'],
    'VMR1C': ['AKOMA','VMR'],
    'VMR1D': ['UKIBO','POVEB','ADPON','SALRU','TEKONG','AKOMA','VMR'],
    'VMR6E': ['MOLVO','ATRUM','AKOMA','VMR'],
    'VMR9F': ['LEDOX', 'LETGO', 'DUBOT','ADPON','SALRU','TEKONG','AKOMA','VMR'],
    'MIBEL1A': ['MOXIB','EMRIX','HOSBA','VANBU', 'IGOSI','ASITI','VIBOG','ISGIL','BISOV','MIBEL'],
    'MIBEL1B': ['IBIXU', 'IBIVA','SAMKO','VIBOG','ISGIL','BISOV','MIBEL'],
    'MIBEL1C': ['HOSBA','VANBU','IGOSI','ASITI','VIBOG','ISGIL','BISOV','MIBEL'],
    'MIBEL1D': ['UKIBO', 'VIGUD', 'SAMKO','VIBOG','ISGIL','BISOV','MIBEL'],
    'MIBEL1E': ['MOLVO', 'EMRIX', 'HOSBA', 'VANBU', 'IGOSI','ASITI','VIBOG','ISGIL','BISOV','TAROS'],
    'MIBEL1F': ['LEDOX','LETGO', 'SAMKO','VIBOG','ISGIL','BISOV','TAROS'],
    'TAROS1A': ['MOXIB','EMRIX','HOSBA','VANBU', 'IGOSI','ASITI','VIBOG','ISGIL','BISOV','TAROS'],
    'TAROS1B': ['IBIXU', 'IBIVA','SAMKO','VIBOG','ISGIL','BISOV','TAROS'],
    'TAROS1C': ['HOSBA','VANBU','IGOSI','ASITI','VIBOG','ISGIL','BISOV','TAROS'],
    'TAROS1D': ['UKIBO', 'VIGUD', 'SAMKO','VIBOG','ISGIL','BISOV','TAROS'],
    'TAROS1E': ['MOLVO', 'EMRIX', 'HOSBA', 'VANBU', 'IGOSI','ASITI','VIBOG','ISGIL','BISOV','TAROS'],
    'TAROS1F': ['LEDOX','LETGO', 'SAMKO','VIBOG','ISGIL','BISOV','TAROS'],
    'TOMAN3A': ['MOXIB','EMRIX','HOSBA','VEBMA','TOMAN'],
    'TOMAN5B': ['IBIXU', 'IBIVA','DUBOT','ERVIV','MUMDU','SEBVO','GOTGA','VEBMA','TOMAN'],
    'TOMAN1C': ['HOSBA','VEBMA','TOMAN'],
    'TOMAN1D': ['UKIBO', 'DUBOT','ERVIV','MUMDU','SEBVO','GOTGA','VEBMA','TOMAN'],
    'TOMAN3E': ['MOLVO', 'EMRIX', 'HOSBA', 'VEBMA','TOMAN'],
    'TOMAN5F': ['LEDOX','LETGO', 'DUBOT','ERVIV','MUMDU','SEBVO','GOTGA','VEBMA','TOMAN'],
    'VOVOSL1B': ['IBIXU', 'IBIVA','SAMKO','BOKIP','ATLEX','VOVOS'],
    'VOVOS1D': ['UKIBO', 'VIGUD', 'SAMKO','BOKIP','ATLEX','VOVOS'],
    'VOVOS1F': ['LEDOX','LETGO', 'SAMKO','BOKIP','ATLEX','VOVOS'],
}

holding_pts_app = ['BOBAG', 'HOSBA', 'KEXAS','LAMA', 'NYLON','REMES','SAMKO','SINJON','TUSPI','VAMPO']
holding_pts_acc = ['ELALO','KARTO','KILOT','MABAL','REPOV','UGEBO']                   

def parse_coordinates(coordinates):
    latitudes = []
    longitudes = []
    for lat_str, lon_str in coordinates:
        lat_deg = float(lat_str[:2]) + float(lat_str[2:4]) / 60 + float(lat_str[4:6]) / 3600
        lon_deg = float(lon_str[:3]) + float(lon_str[3:5]) / 60 + float(lon_str[5:7]) / 3600
        if lat_str.endswith('S'):
            lat_deg *= -1
        if lon_str.endswith('W'):
            lon_deg *= -1
        latitudes.append(lat_deg)
        longitudes.append(lon_deg)
    return latitudes, longitudes

# Convert coordinates to decimal and prepare lists for plotting
lat, lon = parse_coordinates(list(waypoints_all.values()))
names = list(waypoints_all.keys())

# Create DataFrame
df = pd.DataFrame({
    'lat': lat,
    'lon': lon,
    'name': names,
})

# Create scatter plot
fig = go.Figure(go.Scattermapbox(
    lon = df['lon'],
    lat = df['lat'],
    mode = 'markers',
    marker = dict(size = 8, opacity = 0.8, color = 'blue'),
    text = df['name'],
    name= 'Waypoints',
    hovertemplate = 'Waypoint: %{text}<br>Coordinates: %{lat}, %{lon}<extra></extra>',
))

# Convert coordinates to decimal and prepare lists for plotting
STAR_SID_lat, STAR_SID_lon = parse_coordinates(list(STAR_SID_waypoints.values()))
STAR_SID_names = list(STAR_SID_waypoints.keys())

# Create DataFrame
STAR_SID_df = pd.DataFrame({
    'lat': STAR_SID_lat,
    'lon': STAR_SID_lon,
    'name': STAR_SID_names,
})

# Create scatter plot
fig.add_trace(go.Scattermapbox(
    lon = STAR_SID_df['lon'],
    lat = STAR_SID_df['lat'],
    mode = 'markers',
    marker = dict(size = 8, opacity = 0.8, color = 'blue'),
    text = STAR_SID_df['name'],
    showlegend = False,
    hovertemplate = 'Waypoint: %{text}<br>Coordinates: %{lat}, %{lon}<extra></extra>',
))


# Create LineString for Singapore FIR
SG_FIR_latitudes, SG_FIR_longitudes = parse_coordinates(SG_FIR_coordinates)
fir_line = LineString(zip(SG_FIR_longitudes, SG_FIR_latitudes))

# Add Singapore FIR to plot
fig.add_trace(go.Scattermapbox(
    lon=[point[0] for point in fir_line.coords],
    lat=[point[1] for point in fir_line.coords],
    mode='lines',
    line=dict(width=2, color='black'),
    name='Singapore FIR',
))

KL_FIR_vested1_latitudes, KL_FIR_vested1_longitudes = parse_coordinates(KL_FIR_vested1_coordinates)
my_1_line = LineString(zip(KL_FIR_vested1_longitudes, KL_FIR_vested1_latitudes))

fig.add_trace(go.Scattermapbox(
    lon=[point[0] for point in my_1_line.coords],
    lat=[point[1] for point in my_1_line.coords],
    mode='lines',
    line=dict(width=1, color='black'), 
    name='Malaysia Responsibility Area 1',
    showlegend= False
))

KL_FIR_vested2_latitudes, KL_FIR_vested2_longitudes = parse_coordinates(KL_FIR_vested2_coordinates)
my_2_line = LineString(zip(KL_FIR_vested2_longitudes, KL_FIR_vested2_latitudes))

fig.add_trace(go.Scattermapbox(
    lon = [point[0] for point in my_2_line.coords],
    lat = [point[1] for point in my_2_line.coords],
    mode = 'lines',
    line = dict(width = 1, color = 'black'),
    name = 'Malaysia Responsibility Area 2',
    showlegend = False
))

JARKARTA_FIR_delegated_latitudes, JARKARTA_FIR_delegated_longitudes = parse_coordinates(JARKARTA_FIR_delegated_coordinates)
jarkarta_line = LineString(zip(JARKARTA_FIR_delegated_longitudes, JARKARTA_FIR_delegated_latitudes))

fig.add_trace(go.Scattermapbox(
    lon = [point[0] for point in jarkarta_line.coords],
    lat = [point[1] for point in jarkarta_line.coords],
    mode = 'lines',
    line = dict(width = 1, color = 'black'),
    name = 'Jakarta delegated FIR',
    showlegend = False
))

# Add dummy trace for legend
fig.add_trace(go.Scattermapbox(
    lon=[None],
    lat=[None],
    mode='lines',
    line=dict(width=2, color='blue'),
    name='STAR procedures',
))

STARs_A = {k:v for k,v in STARs.items() if k[-1] == 'A'}

for star, waypoints in STARs_A.items():
    latitudes = []
    longitudes = []
    hover_text = []
    waypoints_str = '--> '.join(waypoints)
    for waypoint in waypoints:
        coord = STAR_SID_waypoints[waypoint]
        lat, lon  = parse_coordinates([coord])
        latitudes.append(lat[0])
        longitudes.append(lon[0])
        hover_text.append(f'Waypoint: {waypoint}<br>Coordinates: {lat[0]}, {lon[0]}<br>STAR: {star}<br>{waypoints_str}') 
    # Add route to plot
    fig.add_trace(go.Scattermapbox(
        lon=longitudes,
        lat=latitudes,
        mode='lines',
        line=dict(width=2, color='blue'),
        name=star,
        legendgroup=  'STARs for Runway 02L/C/R',
        hovertemplate='%{hovertext}<extra></extra>',
        hovertext=hover_text, 
        showlegend = False,
    ))

STARs_B = {k:v for k,v in STARs.items() if k[-1] == 'B'}

for star, waypoints in STARs_B.items():
    latitudes = []
    longitudes = []
    hover_text = []
    waypoints_str = '--> '.join(waypoints)
    for waypoint in waypoints:
        coord = STAR_SID_waypoints[waypoint]
        lat, lon  = parse_coordinates([coord])
        latitudes.append(lat[0])
        longitudes.append(lon[0])
        hover_text.append(f'Waypoint: {waypoint}<br>Coordinates: {lat[0]}, {lon[0]}<br>STAR: {star}<br>{waypoints_str}') 
    # Add route to plot
    fig.add_trace(go.Scattermapbox(
        lon=longitudes,
        lat=latitudes,
        mode='lines',
        line=dict(width=2, color='blue'),
        name=star,
        legendgroup=  'STARs for Runway 20L/C/R',
        hovertemplate='%{hovertext}<extra></extra>',
        hovertext=hover_text, 
        showlegend = False,
    ))

# Add dummy trace for legend
fig.add_trace(go.Scattermapbox(
    lon=[None],
    lat=[None],
    mode='lines',
    line=dict(width=2, color='purple'),
    name='SID procedures',
))

# runways = ['02C','20C','02R','20L','02L','20R']
SIDs_A = {k:v for k,v in SIDs.items() if k[-1] == 'A'}

for SID, waypoints in SIDs_A.items():
    latitudes = []
    longitudes = []
    hover_text = []
    waypoints_str = '--> '.join(waypoints)
    for waypoint in waypoints:
        coord = STAR_SID_waypoints[waypoint]
        lat, lon  = parse_coordinates([coord])
        latitudes.append(lat[0])
        longitudes.append(lon[0])
        hover_text.append(f'Waypoint: {waypoint}<br>Coordinates: {lat[0]}, {lon[0]}<br>SID: {SID}<br>{waypoints_str}') 
    # Add route to plot
    fig.add_trace(go.Scattermapbox(
        lon=longitudes,
        lat=latitudes,
        mode='lines',
        line=dict(width=2, color='purple'),
        name=SID,
        legendgroup=  'SIDs for Runway 02C',
        hovertemplate='%{hovertext}<extra></extra>',
        hovertext=hover_text,
        showlegend = False,
    ))

SIDs_B = {k:v for k,v in SIDs.items() if k[-1] == 'B'}

for SID, waypoints in SIDs_B.items():
    latitudes = []
    longitudes = []
    hover_text = []
    waypoints_str = '--> '.join(waypoints)
    for waypoint in waypoints:
        coord = STAR_SID_waypoints[waypoint]
        lat, lon  = parse_coordinates([coord])
        latitudes.append(lat[0])
        longitudes.append(lon[0])
        hover_text.append(f'Waypoint: {waypoint}<br>Coordinates: {lat[0]}, {lon[0]}<br>SID: {SID}<br>{waypoints_str}') 
    # Add route to plot
    fig.add_trace(go.Scattermapbox(
        lon=longitudes,
        lat=latitudes,
        mode='lines',
        line=dict(width=2, color='purple'),
        name=SID,
        legendgroup=  'SIDs for Runway 20C',
        hovertemplate='%{hovertext}<extra></extra>',
        hovertext=hover_text,
        showlegend = False,
    ))

SIDs_C = {k:v for k,v in SIDs.items() if k[-1] == 'C'}

for SID, waypoints in SIDs_C.items():
    latitudes = []
    longitudes = []
    hover_text = []
    waypoints_str = '--> '.join(waypoints)
    for waypoint in waypoints:
        coord = STAR_SID_waypoints[waypoint]
        lat, lon  = parse_coordinates([coord])
        latitudes.append(lat[0])
        longitudes.append(lon[0])
        hover_text.append(f'Waypoint: {waypoint}<br>Coordinates: {lat[0]}, {lon[0]}<br>SID: {SID}<br>{waypoints_str}')   
    # Add route to plot
    fig.add_trace(go.Scattermapbox(
        lon=longitudes,
        lat=latitudes,
        mode='lines',
        line=dict(width=2, color='purple'),
        name=SID,
        legendgroup=  'SIDs for Runway 02R',
        hovertemplate='%{hovertext}<extra></extra>',
        hovertext=hover_text,
        showlegend = False,
    ))

SIDs_D = {k:v for k,v in SIDs.items() if k[-1] == 'D'}

for SID, waypoints in SIDs_D.items():
    latitudes = []
    longitudes = []
    hover_text = []
    waypoints_str = '--> '.join(waypoints)
    for waypoint in waypoints:
        coord = STAR_SID_waypoints[waypoint]
        lat, lon  = parse_coordinates([coord])
        latitudes.append(lat[0])
        longitudes.append(lon[0])
        hover_text.append(f'Waypoint: {waypoint}<br>Coordinates: {lat[0]}, {lon[0]}<br>SID: {SID}<br>{waypoints_str}')   
    # Add route to plot
    fig.add_trace(go.Scattermapbox(
        lon=longitudes,
        lat=latitudes,
        mode='lines',
        line=dict(width=2, color='purple'),
        name=SID,
        legendgroup=  'SIDs for Runway 20L',
        hovertemplate='%{hovertext}<extra></extra>',
        hovertext=hover_text,
        showlegend = False,
    ))

SIDs_E = {k:v for k,v in SIDs.items() if k[-1] == 'E'}

for SID, waypoints in SIDs_E.items():
    latitudes = []
    longitudes = []
    hover_text = []
    waypoints_str = '--> '.join(waypoints)
    for waypoint in waypoints:
        coord = STAR_SID_waypoints[waypoint]
        lat, lon  = parse_coordinates([coord])
        latitudes.append(lat[0])
        longitudes.append(lon[0])
        hover_text.append(f'Waypoint: {waypoint}<br>Coordinates: {lat[0]}, {lon[0]}<br>SID: {SID}<br>{waypoints_str}')
    # Add route to plot
    fig.add_trace(go.Scattermapbox(
        lon=longitudes,
        lat=latitudes,
        mode='lines',
        line=dict(width=2, color='purple'),
        name=SID,
        legendgroup=  'SIDs for Runway 02L',
        hovertemplate='%{hovertext}<extra></extra>',
        hovertext=hover_text,
        showlegend = False,
    ))

SIDs_F = {k:v for k,v in SIDs.items() if k[-1] == 'F'}

for SID, waypoints in SIDs_F.items():
    latitudes = []
    longitudes = []
    hover_text = []
    waypoints_str = '--> '.join(waypoints)
    for waypoint in waypoints:
        coord = STAR_SID_waypoints[waypoint]
        lat, lon  = parse_coordinates([coord])
        latitudes.append(lat[0])
        longitudes.append(lon[0])        
        hover_text.append(f'Waypoint: {waypoint}<br>Coordinates: {lat[0]}, {lon[0]}<br>SID: {SID}<br>{waypoints_str}')
    # Add route to plot
    fig.add_trace(go.Scattermapbox(
        lon=longitudes,
        lat=latitudes,
        mode='lines',
        line=dict(width=2, color='purple'),
        name=SID,
        legendgroup='SIDs for Runway 20R',
        hovertemplate='%{hovertext}<extra></extra>',
        hovertext=hover_text,
        showlegend=False,
    ))


center = (parse_coordinates([WSSS_coordinates])[0][0], parse_coordinates([WSSS_coordinates])[1][0])
# Generate points on the circle
circle_lats = []
circle_lons = []
for bearing in range(0, 360):
    point = geopy.distance.great_circle(nautical=40).destination(center, bearing)
    circle_lats.append(point.latitude)
    circle_lons.append(point.longitude)

# Add the circle to the plot
fig.add_trace(go.Scattermapbox(
    lon=circle_lons + [circle_lons[0]],
    lat=circle_lats + [circle_lats[0]],
    mode='lines',
    line=dict(width=2, color='red'),
    name='40NM Circle',
))

# Add dummy trace for legend
fig.add_trace(go.Scattermapbox(
    lon=[None],
    lat=[None],
    mode='markers',
    line=dict(width=2, color='yellow'),
    name='Holding Points',
))

# Add waypoints for holding_pts_app
for waypoint in holding_pts_app:
    coord = STAR_SID_waypoints[waypoint]
    lat, lon  = parse_coordinates([coord])
    fig.add_trace(go.Scattermapbox(
        lon=[lon[0]],
        lat=[lat[0]],
        mode='markers',
        marker=dict(size=10, color='yellow'),
        name=waypoint,
        text=[f'Waypoint: {waypoint}<br>Coordinates: {lat[0]}, {lon[0]}'],
        showlegend= False
    ))

# Add waypoints for holding_pts_acc
for waypoint in holding_pts_acc:
    coord = STAR_SID_waypoints[waypoint]
    lat, lon  = parse_coordinates([coord])
    fig.add_trace(go.Scattermapbox(
        lon=[lon[0]],
        lat=[lat[0]],
        mode='markers',
        marker=dict(size=10, color='yellow'),
        name=waypoint,
        text=[f'Waypoint: {waypoint}<br>Coordinates: {lat[0]}, {lon[0]}'],
        showlegend=False
    ))




# Combine waypoint and FIR coordinates
all_lats = SG_FIR_latitudes
all_lons = SG_FIR_longitudes

# Calculate the center of the map view
center_lat = (min(all_lats) + max(all_lats)) / 2
center_lon = (min(all_lons) + max(all_lons)) / 2

# Set mapbox style and center
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox=dict(
        center=dict(lat=center_lat, lon=center_lon),
        zoom=6,
    ),
    autosize=False,
    width = 2000,
    height = 1300,
    margin={"r":0,"t":0,"l":0,"b":0},
    legend=dict(
    orientation="h",
    yanchor="top",
    y=1,
    xanchor="right",
    x=1
    ),
    updatemenus=[
    dict(
        type="buttons",
        direction="right",
        buttons=list([
            dict(
                args=[{"visible": [True] + [True]+ [True]*4 + [True] + [True]*len(STARs_A) + [True]*len(STARs_B)+ [True]+ [True] *len(SIDs)+ [True] + [True]+ [True]*len(holding_pts_app) + [True]*len(holding_pts_acc)}],
                label="Show All",
                method="update"
            ),
            dict(
                args=[{"visible": [True] + [True]+ [False]*4 + [False]+ [False]*len(STARs)+ [False]+ [False]* len(SIDs)+ [False]+ [True] + [True]*len(holding_pts_app) + [True]*len(holding_pts_acc)}],
                label="Show Waypoints Only",
                method="update"
            ),
            dict(
                args=[{"visible": [False] + [False]+ [True]*4 + [False]+ [False]*len(STARs)+ [False]+ [False] *len(SIDs)+ [True]+ [False] + [False]*len(holding_pts_app) + [False]*len(holding_pts_acc)}],
                label="Show Singapore FIR Only",
                method="update"
            ),
            dict(
                args=[{"visible": [False] + [False]+ [False]*4 + [True]+ [True]*len(STARs)+ [True]+ [True]* len(SIDs)+ [True]+ [True] + [True]*len(holding_pts_app) + [True]*len(holding_pts_acc)}],
                label="Show STARs and SIDs only",
                method="update"
            ),
        ]),
        pad={"r": 10, "t": 5},
        showactive=True,
        x=0.1,
        xanchor="left",
        y=1.09,
        yanchor="top"
        ),
    dict(
        type="buttons",
        direction="right",
        buttons=list([
            dict(
                args = [{"visible": [False] + [False]+ [False]*4 + [True]+ [True]*len(STARs_A) + [True]*len(STARs_B)+ [False]+ [False] *len(SIDs)+ [True]+ [True] + [True]*len(holding_pts_app) + [True]*len(holding_pts_acc)}],
                label = "Show STARs Only",
                method = "update"
            ),
            dict(
                args = [{"visible": [False] + [False]+ [False]*4 + [True]+ [True]*len(STARs_A) + [False]*len(STARs_B)+ [False]+ [False] *len(SIDs)+ [True]+ [True] + [True]*len(holding_pts_app) + [True]*len(holding_pts_acc)}],
                label = "Show STARs for Runway 02L/C/R Only",
                method = "update"
            ),
            dict(
                args = [{"visible": [False] + [False]+ [False]*4 + [True]+ [False]*len(STARs_A) + [True]*len(STARs_B)+ [False]+ [False] *len(SIDs)+ [True]+ [True] + [True]*len(holding_pts_app) + [True]*len(holding_pts_acc)}],
                label = "Show STARs for Runway 20L/C/R Only",
                method = "update"
            )
        ]),
        pad={"r": 10, "t": 5},
        showactive=True,
        x=0.1,
        xanchor="left",
        y=1.06,
        yanchor="top"
    ),
    dict(
        type="buttons",
        direction="right",
        buttons=list([
            dict(
                args = [{"visible": [False] + [False]+ [False]*4 + [False]+ [False]*len(STARs)+ [True] + [True] *len(SIDs)+ [True]+ [True] + [True]*len(holding_pts_app) + [True]*len(holding_pts_acc)}],
                label = "Show SIDs Only",
                method = "update"
            ),
            dict(
                args = [{"visible": [False] + [False]+ [False]*4 + [False]+ [False]*len(STARs)+ [True]+ [True]* len(SIDs_A)+ [False]* len(SIDs_B)+[True]* len(SIDs_C)+ [False]* len(SIDs_D)+ [True]* len(SIDs_E)+ [False]* len(SIDs_F) + [True]+ [True] + [True]*len(holding_pts_app) + [True]*len(holding_pts_acc)}],
                label = "Show SIDs for Runway 02L/C/R Only",
                method = "update"
            ),
            dict(
                args = [{"visible": [False] + [False]+ [False]*4 + [False]+ [False]*len(STARs)+ [True]+ [False]* len(SIDs_A)+ [True]* len(SIDs_B)+[False]* len(SIDs_C)+ [True]* len(SIDs_D)+ [False]*len(SIDs_E)+ [True]* len(SIDs_F)+ [True]+ [True] + [True]*len(holding_pts_app) + [True]*len(holding_pts_acc)}],
                label = "Show SIDs for Runway 20L/C/R Only",
                method = "update"
            )
        ]),
        pad={"r": 10, "t": 5},
        showactive=True,
        x=0.1,
        xanchor="left",
        y=1.03,
        yanchor="top"
    )
    ]
)

fig.show()

# Save the figure
py.write_html(fig, 'Singapore_FIR.html')