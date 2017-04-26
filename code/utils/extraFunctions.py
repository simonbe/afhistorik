# -*- coding: utf-8 -*-
#from pyspark.sql.functions import *
import utils.trendStatistics as trendStatistics
import csv
import collections

def GetAllYears():
    result = []
    for i in range(2006,2017,1):
        result.append(str(i))
    return result

kommunTillId =  {"karlshamn":"1082","karlskrona":"1080","olofström":"1060","ronneby":"1081","sölvesborg":"1083","ospecificerad arbetsort":"9090","avesta":"2084","borlänge":"2081","falun":"2080", "gagnef":"2026","hedemora":"2083","leksand":"2029","ludvika":"2085",
                "malung-sälen":"2023","mora":"2062","orsa":"2034","rättvik":"2031","smedjebacken":"2061","säter":"2082","vansbro":"2021","älvdalen":"2039","gotland":"980","bollnäs":"2183","gävle":"2180","hofors":"2104","hudiksvall":"2184","ljusdal":"2161","nordanstig":"2132","ockelbo":"2101","ovanåker":"2121","sandviken":"2181","söderhamn":"2182","falkenberg":"1382","halmstad":"1380","hylte":"1315","kungsbacka":"1384","laholm":"1381","varberg":"1383","berg":"2326","bräcke":"2305","härjedalen":"2361","krokom":"2309","ragunda":"2303","strömsund":"2313","åre":"2321","östersund":"2380","aneby":"604","eksjö":"686","gislaved":"662","gnosjö":"617","habo":"643","jönköping":"680","mullsjö":"642","nässjö":"682","sävsjö":"684","tranås":"687","vaggeryd":"665","vetlanda":"685","värnamo":"683","borgholm":"885","emmaboda":"862","hultsfred":"860","högsby":"821","kalmar":"880","mönsterås":"861","mörbylånga":"840","nybro":"881","oskarshamn":"882","torsås":"834","vimmerby":"884","västervik":"883","alvesta":"764","lessebo":"761","ljungby":"781","markaryd":"767","tingsryd":"763","uppvidinge":"760","växjö":"780","älmhult":"765","arjeplog":"2506","arvidsjaur":"2505","boden":"2582","gällivare":"2523","haparanda":"2583","jokkmokk":"2510","kalix":"2514","kiruna":"2584","luleå":"2580","pajala":"2521","piteå":"2581","älvsbyn":"2560","överkalix":"2513","övertorneå":"2518","bjuv":"1260","bromölla":"1272","burlöv":"1231","båstad":"1278","eslöv":"1285","helsingborg":"1283","hässleholm":"1293","höganäs":"1284","hörby":"1266","höör":"1267","klippan":"1276","kristianstad":"1290","kävlinge":"1261","landskrona":"1282","lomma":"1262","lund":"1281","malmö":"1280","osby":"1273","perstorp":"1275","simrishamn":"1291","sjöbo":"1265","skurup":"1264","staffanstorp":"1230","svalöv":"1214","svedala":"1263","tomelilla":"1270","trelleborg":"1287","vellinge":"1233","ystad":"1286","åstorp":"1277","ängelholm":"1292","örkelljunga":"1257","östra-göinge":"1256","botkyrka":"127","danderyd":"162","ekerö":"125","haninge":"136","huddinge":"126","järfälla":"123","lidingö":"186","nacka":"182","norrtälje":"188","nykvarn":"140","nynäshamn":"192","salem":"128","sigtuna":"191","sollentuna":"163","solna":"184","stockholm":"180","sundbyberg":"183","södertälje":"181","tyresö":"138","täby":"160","upplands väsby":"114","upplands-bro":"139","vallentuna":"115","vaxholm":"187","värmdö":"120","österåker":"117","eskilstuna":"484","flen":"482","gnesta":"461","katrineholm":"483","nyköping":"480","oxelösund":"481","strängnäs":"486","trosa":"488","vingåker":"428","enköping":"381","heby":"331","håbo":"305","knivsta":"330","tierp":"360","uppsala":"380","älvkarleby":"319","östhammar":"382","arvika":"1784","eda":"1730",
                "filipstad":"1782","forshaga":"1763","grums":"1764","hagfors":"1783","hammarö":"1761","karlstad":"1780","kil":"1715","kristinehamn":"1781","munkfors":"1762","storfors":"1760","sunne":"1766","säffle":"1785","torsby":"1737","årjäng":"1765","bjurholm":"2403","dorotea":"2425","lycksele":"2481","malå":"2418","nordmaling":"2401","norsjö":"2417","robertsfors":"2409","skellefteå":"2482","sorsele":"2422","storuman":"2421","umeå":"2480",
                "vilhelmina":"2462","vindeln":"2404","vännäs":"2460","åsele":"2463","härnösand":"2280","kramfors":"2282","sollefteå":"2283","sundsvall":"2281","timrå":"2262","ånge":"2260","örnsköldsvik":"2284","arboga":"1984","fagersta":"1982","hallstahammar":"1961","kungsör":"1960","köping":"1983","norberg":"1962","sala":"1981","skinnskatteberg":"1904","surahammar":"1907","västerås":"1980","ale":"1440","alingsås":"1489","bengtsfors":"1460","bollebygd":"1443","borås":"1490","dals-ed":"1438","essunga":"1445","falköping":"1499","färgelanda":"1439","grästorp":"1444","gullspång":"1447","göteborg":"1480","götene":"1471","herrljunga":"1466","hjo":"1497","härryda":"1401","karlsborg":"1446","kungälv":"1482","lerum":"1441","lidköping":"1494","lilla edet":"1462","lysekil":"1484","mariestad":"1493","mark":"1463","mellerud":"1461","munkedal":"1430","mölndal":"1481","orust":"1421","partille":"1402","skara":"1495","skövde":"1496","sotenäs":"1427","stenungsund":"1415","strömstad":"1486","svenljunga":"1465","tanum":"1435","tibro":"1472","tidaholm":"1498","tjörn":"1419","tranemo":"1452","trollhättan":"1488","töreboda":"1473","uddevalla":"1485","ulricehamn":"1491","vara":"1470","vårgårda":"1442","vänersborg":"1487","åmål":"1492","öckerö":"1407","boxholm":"560","finspång":"562","kinda":"513","linköping":"580","mjölby":"586",
                "motala":"583","norrköping":"581","söderköping":"582","vadstena":"584","valdemarsvik":"563","ydre":"512","åtvidaberg":"561","ödeshög":"509"}

for k in kommunTillId.keys():
    if len(kommunTillId[k])<4:
        kommunTillId[k] = '0' + kommunTillId[k]

#kommunTillId = map(lambda x: x if len(x[1])>3 else {x[0]:'0'+x[1]},kommunTillId) # convert e.g. 180 to 0180

#kommunTillId=  {"karlshamn":1082,"karlskrona":1080,"olofström":1060,"ronneby":1081,"sölvesborg":1083,"ospecificerad arbetsort": 9090,"avesta": 2084,"borlänge":2081,"falun":2080, "gagnef":2026,"hedemora":2083,"leksand":2029,"ludvika":2085,
#                "malung-sälen":2023,"mora":2062,"orsa":2034,"rättvik":2031,"smedjebacken":2061,"säter":2082,"vansbro":2021,"älvdalen":2039,"gotland":980,"bollnäs":2183,"gävle":2180,"hofors":2104,"hudiksvall":2184,"ljusdal":2161  ,"nordanstig":2132,"ockelbo":2101,"ovanåker":2121,"sandviken":2181,"söderhamn":2182,"falkenberg":1382,"halmstad":1380,"hylte":1315,"kungsbacka":1384,"laholm":1381,"varberg":1383,"berg":2326,"bräcke":2305,"härjedalen":2361,"krokom":2309,"ragunda":2303,"strömsund":2313,"åre":2321,"östersund":2380,"aneby":604,"eksjö":686,"gislaved":662,"gnosjö":617,"habo":643,"jönköping":680,"mullsjö":642,"nässjö":682,"sävsjö":684,"tranås":687,"vaggeryd":665,"vetlanda":685,"värnamo":683,"borgholm":885,"emmaboda":862,"hultsfred":860,"högsby":821,"kalmar":880,"mönsterås":861,"mörbylånga":840,"nybro":881,"oskarshamn":882,"torsås":834,"vimmerby":884,"västervik":883,"alvesta":764,"lessebo":761,"ljungby":781,"markaryd":767,"tingsryd":763,"uppvidinge":760,"växjö":780,"älmhult":765,"arjeplog":2506,"arvidsjaur":2505,"boden":2582,"gällivare":2523,"haparanda":2583,"jokkmokk":2510,"kalix":2514,"kiruna":2584,"luleå":2580,"pajala":2521,"piteå":2581,"älvsbyn":2560,"överkalix":2513,"övertorneå":2518,"bjuv":1260,"bromölla":1272,"burlöv":1231,"båstad":1278,"eslöv":1285,"helsingborg":1283,"hässleholm":1293,"höganäs":1284,"hörby":1266,"höör":1267,"klippan":1276,"kristianstad":1290,"kävlinge":1261,"landskrona":1282,"lomma":1262,"lund":1281,"malmö":1280,"osby":1273,"perstorp":1275,"simrishamn":1291,"sjöbo":1265,"skurup":1264,"staffanstorp":1230,"svalöv":1214,"svedala":1263,"tomelilla":1270,"trelleborg":1287,"vellinge":1233,"ystad":1286,"åstorp":1277,"ängelholm":1292,"örkelljunga":1257,"östra-göinge":1256,"botkyrka":127,"danderyd":162,"ekerö":125,"haninge":136,"huddinge":126,"järfälla":123,"lidingö":186,"nacka":182,"norrtälje":188,"nykvarn":140,"nynäshamn":192,"salem":128,"sigtuna":191,"sollentuna":163,"solna":184,"stockholm":180,"sundbyberg":183,"södertälje":181,"tyresö":138,"täby":160,"upplands väsby":114,"upplands-bro":139,"vallentuna":115,"vaxholm":187,"värmdö":120,"österåker":117,"eskilstuna":484,"flen":482,"gnesta":461,"katrineholm":483,"nyköping":480,"oxelösund":481,"strängnäs":486,"trosa":488,"vingåker":428,"enköping":381,"heby":331,"håbo":305,"knivsta":330,"tierp":360,"uppsala":380,"älvkarleby":319,"östhammar":382,"arvika":1784,"eda":1730,
#                "filipstad":1782,"forshaga":1763,"grums":1764,"hagfors":1783,"hammarö":1761,"karlstad":1780,"kil":1715,"kristinehamn":1781,"munkfors":1762,"storfors":1760,"sunne":1766,"säffle":1785,"torsby":1737,"årjäng":1765,"bjurholm":2403,"dorotea":2425,"lycksele":2481,"malå":2418,"nordmaling":2401,"norsjö":2417,"robertsfors":2409,"skellefteå":2482,"sorsele":2422,"storuman":2421,"umeå":2480,
#                "vilhelmina":2462,"vindeln":2404,"vännäs":2460,"åsele":2463,"härnösand":2280,"kramfors":2282,"sollefteå":2283,"sundsvall":2281,"timrå":2262,"ånge":2260,"örnsköldsvik":2284,"arboga":1984,"fagersta":1982,"hallstahammar":1961,"kungsör":1960,"köping":1983,"norberg":1962,"sala":1981,"skinnskatteberg":1904,"surahammar":1907,"västerås":1980,"ale":1440,"alingsås":1489,"bengtsfors":1460,"bollebygd":1443,"borås":1490,"dals-ed":1438,"essunga":1445,"falköping":1499,"färgelanda":1439,"grästorp":1444,"gullspång":1447,"göteborg":1480,"götene":1471,"herrljunga":1466,"hjo":1497,"härryda":1401,"karlsborg":1446,"kungälv":1482,"lerum":1441,"lidköping":1494,"lilla edet":1462,"lysekil":1484,"mariestad":1493,"mark":1463,"mellerud":1461,"munkedal":1430,"mölndal":1481,"orust":1421,"partille":1402,"skara":1495,"skövde":1496,"sotenäs":1427,"stenungsund":1415,"strömstad":1486,"svenljunga":1465,"tanum":1435,"tibro":1472,"tidaholm":1498,"tjörn":1419,"tranemo":1452,"trollhättan":1488,"töreboda":1473,"uddevalla":1485,"ulricehamn":1491,"vara":1470,"vårgårda":1442,"vänersborg":1487,"åmål":1492,"öckerö":1407,"boxholm":560,"finspång":562,"kinda":513,"linköping":580,"mjölby":586,
#                "motala":583,"norrköping":581,"söderköping":582,"vadstena":584,"valdemarsvik":563,"ydre":512,"åtvidaberg":561,"ödeshög":509 }

#kommunTillId = map(lambda x: x if len(x)>3 else '0'+x,kommunTillId) # convert e.g. 180 to 0180

idTillKommun = {}

# municipality populations as of december 2015
# used to calculate per capita results
kommunTillPopulationdec2015 = { "botkyrka":89425,"danderyd":32421,"ekerö":26984,"haninge":83866,"huddinge":105311,"järfälla":72429,"lidingö":46302,"nacka":97986,"norrtälje":58669,"nykvarn":10192,"nynäshamn":27500,"salem":16426,"sigtuna":44786,
"sollentuna":70251,"solna":76158,"stockholm":923516,"sundbyberg":46110,"södertälje":93202,"tyresö":46177,"täby":68281,"upplandsväsby":42661,"upplands-bro":25789,"vallentuna":32380,"vaxholm":11380,
"värmdö":41107,"österåker":42130,"enköping":41893,"heby":13594,"håbo":20279,"knivsta":16869,"tierp":20547,"uppsala":210126,"älvkarleby":9293,"östhammar":21563,"eskilstuna":102065,"flen":16440,
"gnesta":10649,"katrineholm":33462,"nyköping":54262,"oxelösund":11701,"strängnäs":34102,"trosa":12078,"vingåker":8953,"boxholm":5328,"finspång":21199,"kinda":9795,"linköping":152966,"mjölby":26602,
"motala":42903,"norrköping":137035,"söderköping":14240,"vadstena":7407,"valdemarsvik":7747,"ydre":3658,"åtvidaberg":11545,"ödeshög":5236,"aneby":6537,"eksjö":16790,"gislaved":29272,"gnosjö":9514,
"habo":11314,"jönköping":133310,"mullsjö":7157,"nässjö":30451,"sävsjö":11228,"tranås":18546,"vaggeryd":13372,"vetlanda":26873,"värnamo":33473,"alvesta":19581,"lessebo":8516,"ljungby":27638,
"markaryd":9779,"tingsryd":12260,"uppvidinge":9319,"växjö":88108,"älmhult":16168,"borgholm":10681,"emmaboda":9090,"hultsfred":13919,"högsby":5857,"kalmar":65704,"mönsterås":13144,"mörbylånga":14669,
"nybro":19754,"oskarshamn":26450,"torsås":6943,"vimmerby":15419,"västervik":36049,"gotland":57391,"karlshamn":31846,"karlskrona":65380,"olofström":13170,"ronneby":28697,"sölvesborg":17160,"bjuv":14962,
"bromölla":12513,"burlöv":17430,"båstad":14373,"eslöv":32438,"helsingborg":137909,"hässleholm":51048,"höganäs":25610,"hörby":15020,"höör":15970,"klippan":16917,"kristianstad":82510,"kävlinge":30104,
"landskrona":43961,"lomma":23324,"lund":116834,"malmö":322574,"osby":12954,"perstorp":7211,"simrishamn":19065,"sjöbo":18514,"skurup":15149,"staffanstorp":23119,"svalöv":13655,"svedala":20462,
"tomelilla":13132,"trelleborg":43359,"vellinge":34667,"ystad":28985,"åstorp":15193,"ängelholm":40732,"örkelljunga":9831,"östragöinge":14102,"falkenberg":42949,"halmstad":96952,"hylte":10514,"kungsbacka":79144,
"laholm":24195,"varberg":61030,"ale":28862,"alingsås":39602,"bengtsfors":9626,"bollebygd":8799,"borås":108488,"dals-ed":4799,"essunga":5590,"falköping":32511,"färgelanda":6495,"grästorp":5644,"gullspång":5229,
"göteborg":548190,"götene":13160,"herrljunga":9349,"hjo":8983,"härryda":36651,"karlsborg":6764,"kungälv":42730,"lerum":40181,"lidköping":39009,"lillaedet":13178,"lysekil":14464,"mariestad":24043,
"mark":33906,"mellerud":9169,"munkedal":10205,"mölndal":63340,"orust":15010,"partille":36977,"skara":18711,"skövde":53555,"sotenäs":9006,"stenungsund":25508,"strömstad":12854,"svenljunga":10506,
"tanum":12455,"tibro":10980,"tidaholm":12669,"tjörn":15315,"tranemo":11619,"trollhättan":57092,"töreboda":9293,"uddevalla":54180,"ulricehamn":23494,"vara":15662,"vårgårda":11165,"vänersborg":38381,
"åmål":12601,"öckerö":12682,"arvika":25841,"eda":8505,"filipstad":10625,"forshaga":11379,"grums":8945,"hagfors":11824,"hammarö":15420,"karlstad":89245,"kil":11802,"kristinehamn":24270,"munkfors":3663,
"storfors":4032,"sunne":13208,"säffle":15366,"torsby":11910,"årjäng":9869,"askersund":11151,"degerfors":9543,"hallsberg":15509,"hällefors":7032,"karlskoga":30283,"kumla":21154,"laxå":5656,"lekeberg":7492,
"lindesberg":23562,"ljusnarsberg":4928,"nora":10502,"örebro":144200,"arboga":13858,"fagersta":13286,"hallstahammar":15645,"kungsör":8343,"köping":25557,"norberg":5803,"sala":22109,"skinnskatteberg":4472,
"surahammar":9985,"västerås":145218,"avesta":22781,"borlänge":50988,"falun":57062,"gagnef":10079,"hedemora":15235,"leksand":15326,"ludvika":26362,"malung-sälen":10036,"mora":20101,"orsa":6750,
"rättvik":10759,"smedjebacken":10790,"säter":11009,"vansbro":6715,"älvdalen":7035,"bollnäs":26594,"gävle":98877,"hofors":9435,"hudiksvall":36975,"ljusdal":19027,"nordanstig":9490,"ockelbo":5849,
"ovanåker":11469,"sandviken":38314,"söderhamn":25785,"härnösand":25066,"kramfors":18359,"sollefteå":19783,"sundsvall":97633,"timrå":17987,"ånge":9493,"örnsköldsvik":55576,"berg":7032,"bräcke":6455,
"härjedalen":10262,"krokom":14785,"ragunda":5387,"strömsund":11712,"åre":10677,"östersund":61066,"bjurholm":2453,"dorotea":2740,"lycksele":12177,"malå":3109,"nordmaling":7060,"norsjö":4176,"robertsfors":6771,
"skellefteå":72031,"sorsele":2516,"storuman":5943,"umeå":120777,"vilhelmina":6829,"vindeln":5371,"vännäs":8593,"åsele":2832,"arjeplog":2887,"arvidsjaur":6471,"boden":27913,"gällivare":18123,
"haparanda":9831,"jokkmokk":5072,"kalix":16248,"kiruna":23178,"luleå":76088,"pajala":6193,"piteå":41548,"älvsbyn":8183,"överkalix":3395,"övertorneå":4603 }

yrkeIdTillYrkesbenamning = {}

def GenerateIdToKommun():
    for key in kommunTillId.keys():
        idTillKommun[str(kommunTillId[key])] = key

def GetKommunTillId(namn):
    if namn in kommunTillId:
        return kommunTillId[namn]
    else:
        return -1

def GetIdTillKommun(id):
    if id in idTillKommun:
        return idTillKommun[id]
    else:
        return -1

def GetAllKommunKoder():
    if len(idTillKommun) == 0:
        GenerateIdToKommun()

    return idTillKommun.keys()

def GetAllKommunNamn():
    return kommunTillId.keys()

def GetAllOccupations():
    # only keeping the top X most common

    result = ['Personlig assistent','Säljare','Lärare i förskola/Förskollärare','Hemförsäljare','Telefonförsäljare','Lärare i grundskolans senare år','Kock/Kokerska','Innesäljare',
              'Utesäljare','Systemutvecklare/Programmerare','Lärare i grundskolans tidigare år','Ekonomiassistent','Undersköterska','Redovisningsekonom','Administrativ assistent',
              'Sjuksköterska, grundutbildad','Demonstratör','Servitör/Servitris','Socialsekreterare','Lärare i gymnasiet - kärnämnen','Lärare i fritidshem/Fritidspedagog','Restaurangbiträde',
              'Förskollärare','Sjuksköterska, medicin och kirurgi','Försäljare, fackhandel','Städare/Lokalvårdare','Saknas','Barnskötare','Kundtjänstmedarbetare','Butikssäljare, fackhandel','IT-konsult',
              'Lagerarbetare','Specialpedagog','Barnflicka/Barnvakt','Receptionist, telefonist','Account manager','Helpdesktekniker/Supporttekniker','Grundskollärare 4-9','Lärare i gymnasiet - yrkesämnen',
              'Distriktssköterska','Specialistläkare','Kontorist','Försäljare, dagligvaror','Inköpare','Truckförare','Frisör','Programmerare','Arbetsterapeut','Psykolog','Lärare i praktiska och estetiska ämnen',
              'Sjuksköterska, psykiatrisk vård','Torg- och marknadsförsäljare','IT-tekniker/Datatekniker','Elevassistent','Lastbilsförare','Taxiförare/Taxichaufför','Butiksdemonstratör','Controller','Distributionsförare',
              'Ordermottagare','Hembiträde','Sjuksköterska, äldreomsorg och -vård/geriatrik','Träarbetare/Snickare','Försäljningschef','Handläggare/Utredare, offentlig förvaltning','Tandsköterska','Löneadministratör','Ekonomichef']

    res2 = []
    for r in result:
        res2.append(r)#r.decode('utf-8'))

    return res2

def GetAllMonths():

    result = []
    for y in GetAllYears():

        for i in range(1,13,1):
            m = y + "-"
            if i<10:
                m = m + "0"
            m=m+str(i)
            result.append(m)

    return result

def GetYrkeData(allData,yrke,nameYrken):

    # Stop words
    stopWords = []
    removeStopWords = False

    if removeStopWords == True:

        with open('C:/Projects/Trend/commonWordsSorted_1k_filtered_unicode_manual.txt', 'rb') as csvfile:
            raw = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in raw:
                stopWords.append(row[0])#row[0].decode('utf-8'))
                #stopWords.append(row[0].replace('\\',''))

        # only keep top X
        stopWords[580:] = []
        print('stopwords length: ' + str(len(stopWords)))
    # end Stop words

    yrkesbenamningCount = allData.groupBy(nameYrken).count()#"YRKESBENAMNING").count()
    yrkeList = yrkesbenamningCount.select(nameYrken)

    yrkeRestNamn = yrke

    # get all words for yrke Rest
    if(yrkeRestNamn is not ''):
        dRest = allData.filter(allData[nameYrken] == yrkeRestNamn)
    else:
        dRest = allData

    allBeskrRest = dRest.select("PLATSBESKRIVNING")
    allBeskrRest.cache()
    allBeskrRest.count()

    uniFreqRest = trendStatistics.getUnigramFreqs(allBeskrRest,stopWords).collect() #getUnigramFreqs(allBeskrRest,stopWords).collect()
    bgFreqRest = []#getBigramFreqs(allBeskrRest,stopWords).collect()

    return [uniFreqRest,bgFreqRest]

def removeLastCharacters(word):
    if word.endswith('.') or word.endswith(',') or word.endswith('?'):
        return word[:-1]
    else:
        return word

def getUnigramFreqs(beskr,stopWords):
    unigrams = beskr.map(lambda x: str(x).lower().split(' ')) \
        .flatMap(lambda x: [(removeLastCharacters(x[i]),1) for i in range(0,len(x))])
    freq_unigrams = unigrams.reduceByKey(lambda x,y:x+y) \
        .map(lambda x:(x[1],x[0])) \
        .sortByKey(False)

    return freq_unigrams

def distanceSparseVectors(cols1, cols2):
    return len(set(cols1).intersection(cols2))

def ConvertToDate(strDate):
    if strDate:
        return time.strptime(strDate, "%Y-%m-%d").date()
    else:
        return time.strptime("1900-01-01", "%Y-%m-%d").date()

def WithinDates(date,startDate,endDate):
    if startDate <= date <= endDate:
        return True
    else:
        return False

def GetAllTextWrtDates(allData,startDate,endDate):
    #newData = allData.filter(lambda x: True if WithinDates(ConvertToDate(x.PUBLICERAD_FROM.encode('utf-8')),startDate,endDate) else False).map(lambda x: x.PLATSBESKRIVNING.encode('utf-8').split(' '))
    #newData = allData.filter(to_date(allData['PUBLICERAD_FROM'])).gt(startDate)
    #a=allData.filter(allData['PUBLICERAD_FROM']=='2013-02-02')
    a=allData.filter(to_date(allData['FORSTA_PUBLICERINGSDATUM']) > startDate)
    a=a.filter(to_date(a['FORSTA_PUBLICERINGSDATUM']) < endDate)
    #(x.PUBLICERAD_FROM.encode('utf-8')),startDate,endDate) else False).map(lambda x: x.PLATSBESKRIVNING.encode('utf-8').split(' '))
    return a

def GetKommunIdsPopulation(kommunIds,correspondingData):
    # completely unneccessary need for this conversion, change to only id on backend (!)
    res = [0]*len(kommunIds)
    i = 0

    for i in range(0,len(correspondingData),1):
        id = kommunIds[i]
        data = correspondingData[i]
        if id in idTillKommun:
            namn = idTillKommun[id]
            pop = GetKommunNamnPopulation(namn)
            if pop == 0:
                res[i] = 0
            else:
                res[i] = float(data)/pop
        else:
            res[i] = 0

    return res

def GetKommunNamnPopulation(kommunNamn):
    if kommunNamn in kommunTillPopulationdec2015:
        return kommunTillPopulationdec2015[kommunNamn]
    else:
        return 0

def SortedHistogram(c,topNrs):
    #d = dict((x,c.count(x)) for x in c)
    cnt = collections.Counter(c)
    tops = cnt.most_common(topNrs)
    # return unzipped
    return zip(*tops)