
function updateView(usePerCapita) {
  var inputText = $('#inputText').val()
  if(inputText == "")
    inputText = "och"

  // analytics
  ga('send', 'event', 'input', 'search', inputText);

  // Convert back region texts to region codes
  var res = convertRegionText2Codes(inputText.toLowerCase());
  var mapSelected = false;
  if(res[0] == true) { // has been changed
    inputText = res[1];
    var codes = res[2];
    // zoom in to municipality
    mapZoom(codes);
    mapSelected = true;
  }
  else {
    // zoom out map just in case
    mapReset();
  }

  inputText = inputText.toLowerCase();

  var encodedText = encodeURI(inputText).replace(/\(/g, "%28").replace(/\)/g, "%29");
  var adr = 'http://13.74.12.222:8080/realtime1/' + encodedText; //'http://172.16.200.111:8080/realtime1/' + encodedText;//'http://172.22.72.134:8080/realtime1/' + encodedText;//'http://localhost:8080/realtime1/' + encodedText; //'http://172.22.73.98:8080/realtime1/' + encodedText;//'http://localhost:8080/realtime1/' + encodedText;

  $.getJSON(adr,function(data) {
    var keys = Object.keys(data)
    //var objData = data[keys[1]]
    var jsonData = JSON.stringify(data)
    $('#outputKeys').val(keys)
    $('#outputData').val(jsonData)

    var dataMonths = [];
    var dataKommunkoder = [];
    var dataKommunkoder2 = [];
    var dataOccupations = [];
    var dataEmployers = [];

    for(var i=0;i<keys.length;i++)
    {
      if(keys[i]!='retrieval_time') // skip timing debug data
      {
        dataMonths.unshift({ key: keys[i], values: data[keys[i]]['months'] }); // unshift adds to beginning of array (push to the end)
        dataKommunkoder.unshift({ key: keys[i], values: data[keys[i]]['kommunkoder'] });
        dataKommunkoder2.unshift({ key: keys[i], values: { percapita: data[keys[i]]['kommunkoder_percapita'], total: data[keys[i]]['kommunkoder_total'] }});
        dataOccupations.unshift({ key: keys[i], values: data[keys[i]]['occupations'] });
        dataEmployers.unshift({ key: keys[i], values: data[keys[i]]['employers'] });
      }
    }

    updateLineChart1(dataMonths)

    //if(mapSelected == true)

    updateBarChart1(dataMonths);//data[inputText]['months'])
    updateHorizChart1(dataOccupations,true);//data[inputText]['occupations'],true)
    updateHorizchart22(dataEmployers,true);//data[inputText]['occupations'],true)
    updateHorizchart22(dataEmployers,true);//data[inputText]['occupations'],true)
    updateMap(dataKommunkoder2,usePerCapita);//data[inputText]['kommunkoder'])

    populateNewExamples();
  });
}
