var regionCodes = {"karlshamn":"1082","karlskrona":"1080","olofström":"1060","ronneby":"1081","sölvesborg":"1083","ospecificerad arbetsort":" 9090","avesta":" 2084","borlänge":"2081","falun":"2080", "gagnef":"2026","hedemora":"2083","leksand":"2029","ludvika":"2085",
                "malung sälen":"2023","mora":"2062","orsa":"2034","rättvik":"2031","smedjebacken":"2061","säter":"2082","vansbro":"2021","älvdalen":"2039","gotland":"980","bollnäs":"2183","gävle":"2180","hofors":"2104","hudiksvall":"2184","ljusdal":"2161  ","nordanstig":"2132","ockelbo":"2101","ovanåker":"2121","sandviken":"2181","söderhamn":"2182","falkenberg":"1382","halmstad":"1380","hylte":"1315","kungsbacka":"1384","laholm":"1381","varberg":"1383","berg":"2326","bräcke":"2305","härjedalen":"2361","krokom":"2309","ragunda":"2303","strömsund":"2313","åre":"2321","östersund":"2380","aneby":"604","eksjö":"686","gislaved":"662","gnosjö":"617","habo":"643",
                "jönköping":"680","mullsjö":"642","nässjö":"682","sävsjö":"684","tranås":"687","vaggeryd":"665","vetlanda":"685","värnamo":"683","borgholm":"885","emmaboda":"862","hultsfred":"860","högsby":"821","kalmar":"880","mönsterås":"861","mörbylånga":"840","nybro":"881","oskarshamn":"882","torsås":"834","vimmerby":"884","västervik":"883","alvesta":"764","lessebo":"761","ljungby":"781","markaryd":"767","tingsryd":"763","uppvidinge":"760","växjö":"780","älmhult":"765","arjeplog":"2506","arvidsjaur":"2505","boden":"2582","gällivare":"2523","haparanda":"2583","jokkmokk":"2510","kalix":"2514","kiruna":"2584","luleå":"2580","pajala":"2521","piteå":"2581","älvsbyn":"2560","överkalix":"2513","övertorneå":"2518",
                "bjuv":"1260","bromölla":"1272","burlöv":"1231","båstad":"1278","eslöv":"1285","helsingborg":"1283","hässleholm":"1293","höganäs":"1284","hörby":"1266","höör":"1267","klippan":"1276","kristianstad":"1290","kävlinge":"1261","landskrona":"1282","lomma":"1262","lund":"1281","malmö":"1280","osby":"1273","perstorp":"1275","simrishamn":"1291","sjöbo":"1265","skurup":"1264","staffanstorp":"1230","svalöv":"1214","svedala":"1263","tomelilla":"1270","trelleborg":"1287","vellinge":"1233","ystad":"1286","åstorp":"1277","ängelholm":"1292","örkelljunga":"1257","östra-göinge":"1256","botkyrka":"127","danderyd":"162","ekerö":"125","haninge":"136","huddinge":"126","järfälla":"123",
                "lidingö":"186","nacka":"182","norrtälje":"188","nykvarn":"140","nynäshamn":"192","salem":"128","sigtuna":"191","sollentuna":"163","solna":"184","stockholm":"180","sundbyberg":"183","södertälje":"181","tyresö":"138","täby":"160","upplands väsby":"114","upplands-bro":"139","vallentuna":"115","vaxholm":"187","värmdö":"120","österåker":"117","eskilstuna":"484","flen":"482","gnesta":"461","katrineholm":"483","nyköping":"480","oxelösund":"481","strängnäs":"486","trosa":"488","vingåker":"428","enköping":"381","heby":"331","håbo":"305","knivsta":"330","tierp":"360","uppsala":"380","älvkarleby":"319","östhammar":"382","arvika":"1784","eda":"1730",
                "filipstad":"1782","forshaga":"1763","grums":"1764","hagfors":"1783","hammarö":"1761","karlstad":"1780","kil":"1715","kristinehamn":"1781","munkfors":"1762","storfors":"1760","sunne":"1766","säffle":"1785","torsby":"1737","årjäng":"1765","bjurholm":"2403","dorotea":"2425",
                "lycksele":"2481","malå":"2418","nordmaling":"2401","norsjö":"2417","robertsfors":"2409","skellefteå":"2482","sorsele":"2422","storuman":"2421","umeå":"2480",
                "vilhelmina":"2462","vindeln":"2404","vännäs":"2460","åsele":"2463","härnösand":"2280","kramfors":"2282","sollefteå":"2283","sundsvall":"2281","timrå":"2262","ånge":"2260","örnsköldsvik":"2284","arboga":"1984","fagersta":"1982","hallstahammar":"1961","kungsör":"1960","köping":"1983",
                "norberg":"1962","sala":"1981","skinnskatteberg":"1904","surahammar":"1907","västerås":"1980","ale":"1440","alingsås":"1489","bengtsfors":"1460","bollebygd":"1443","borås":"1490","dals-ed":"1438","essunga":"1445","falköping":"1499","färgelanda":"1439",
                "grästorp":"1444","gullspång":"1447","göteborg":"1480","götene":"1471","herrljunga":"1466","hjo":"1497","härryda":"1401","karlsborg":"1446","kungälv":"1482","lerum":"1441","lidköping":"1494","lilla edet":"1462","lysekil":"1484","mariestad":"1493","mark":"1463",
                "mellerud":"1461","munkedal":"1430","mölndal":"1481","orust":"1421","partille":"1402","skara":"1495","skövde":"1496","sotenäs":"1427","stenungsund":"1415","strömstad":"1486","svenljunga":"1465","tanum":"1435","tibro":"1472","tidaholm":"1498",
                "tjörn":"1419","tranemo":"1452","trollhättan":"1488","töreboda":"1473","uddevalla":"1485","ulricehamn":"1491","vara":"1470","vårgårda":"1442","vänersborg":"1487","åmål":"1492","öckerö":"1407","boxholm":"560","finspång":"562","kinda":"513","linköping":"580","mjölby":"586",
                "motala":"583","norrköping":"581","söderköping":"582","vadstena":"584","valdemarsvik":"563","ydre":"512","åtvidaberg":"561","ödeshög":"509" };

var allCodes = [];
var allRegions = [];
var codeRegions = {};

for(var k in regionCodes)
{
  regionCodes[k] = regionCodes[k].trim();
  // correct e.g. 180 -> 0180 (change on backend)
  if(regionCodes[k].length<4)
    regionCodes[k] = '0' + regionCodes[k];
  allCodes.push(regionCodes[k]); // (!) do not convert to string
  codeRegions[regionCodes[k]] = k;
  allRegions.push(k);
}

String.prototype.capitalizeFirstLetter = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

function isSubStringInList(substring,list)
{
  for(var i=0;i<list.length;i++)
    if(list[i].indexOf(substring)>-1)
      return true;

  return false;
}

// replaces all occurances in input string with corresponding codes
// slow, could change to trie (as in autocomplete)
function convertRegionText2Codes(input)
{
  var replacements = [];
  var changed = false;
  var codes = [];

  for(var i=0;i<allRegions.length;i++)
  {
    if(input.indexOf(allRegions[i])>-1)
    {
      // add to replace array
      // check it is not subpart of another one
      if(isSubStringInList(allRegions[i],replacements) == false)
        replacements.push(allRegions[i]);
      changed = true;
    }
  }

  // do all replacements
  for(var i=0;i<replacements.length;i++)
  {
    input = input.replace(replacements[i], regionCodes[replacements[i]]);
    codes.push(regionCodes[replacements[i]]);
  }

  return [changed,input,codes];
}

function convertRegionCodes2Text(input)
{
  var replacements = []
  input = input.trim()

  for(var i=0;i<allCodes.length;i++)
  {
    if(input.indexOf(allCodes[i])>-1)
    {
      // add to replace array
      replacements.push(allCodes[i]);
    }
  }

  // do all replacements
  for(var i=0;i<replacements.length;i++)
  {
    input = input.replace(replacements[i], codeRegions[replacements[i]].capitalizeFirstLetter());
  }

  return input;
}

function convertRegionCode2Text(code)
{
  if(code in codeRegions)
    return codeRegions[code].capitalizeFirstLetter();
  else
    return "";
}

function convertRegionText2Code(text)
{
  if(text.toLowerCase() in regionCodes)
    return regionCodes[text.toLowerCase()];
  else
    return "";
}

function resetRegionsText(input)
{
  var replacements = []
  var sList = input.split(' ')

  for(var j=0;j<sList.length;j++)
  {
    for(var i=0;i<allRegions.length;i++)
    {
      if(sList[j] == allRegions[i])
      {
        // add to replace array
        replacements.push(allRegions[i]);
      }
    }
  }

  // do all replacements
  for(var i=0;i<replacements.length;i++)
  {
    input = input.replace(replacements[i], "");
  }

  return input;
}

// OLD
function resetRegions(current)
{
  var sList = current.split(' ')
  for(var i=0;i<sList.length;i++)
  {
    if(allCodes.indexOf(sList[i])>-1)
    {
      sList[i] = ''
    }
  }

  var res = "";
  for(var i in sList)
    if(sList[i]!='')
      res = res + " " + sList[i];

  return res;
}

function updatePrompt(region)
{
//  if(region[0] == '0')
//    region = region.slice(1,region.length);

  // get current command
  var current = $('#inputText').val()

  // replace region if already specified
  current = resetRegionsText(current.toLowerCase());
  current = current.trim();

  var regionText = convertRegionCode2Text(region);

  // also convert region code to text
  current = current + " " + regionText;//region;
  current = current.trim();

  $('#inputText').val(current)
  updateView();
}
