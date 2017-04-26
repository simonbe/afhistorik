
/*function addToData(totData)
{
  var outData = [];
  var combCounts = []

  for(var i=0;i<totData.length;i++)
  {

  }
}*/

function convertToDate(months,counts)
{
  var converted = [];

  for(var i=0;i<months.length;i++)
  {
    var parts = months[i].split('-');
    var d = new Date(parts[0], parts[1]-1, 0);
    converted.push({ x:d, y:counts[i]})
  }

  return converted;
}

var color = d3.scaleOrdinal(d3.schemeCategory10);//schemeCategory10;
var colorsMix = ['steelblue','red','green','black','yellow','gray']

// Set the dimensions of the canvas / graph
var margin = {top: 30, right: 20, bottom: 30, left: 50},
    width = 400 - margin.left - margin.right,
    height = 250 - margin.top - margin.bottom;

var svg0 = d3.select('#area1').append('svg')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
    .append('g')
    .attr('transform','translate(' + margin.left + ',' + margin.top + ')');

// Set the ranges
var x = d3.scaleTime().range([0, width]); //d3.scale.linear().range([0, width]);//
var y = d3.scaleLinear().range([height, 0]);

// Define the axes
var xAxis = d3.axisBottom(x).ticks(10)//d3.svg.axis().scale(x)
    //.orient("bottom").ticks(10);

var yAxis = d3.axisLeft(y).ticks(10)//d3.svg.axis().scale(y)
    //.orient("left").ticks(10);

// Define the line
var line = d3.line()
    .x(function(d) { return x(d.x); })
    .y(function(d) { return y(d.y); });

    svg0.append("rect")
    .attr("width", "100%")
    .attr("height", "100%")
    .attr("fill", "white");

function addLineChart1(combinedData)
{
  lineChart1Data = combinedData[0].values;
  var svg = d3.select("body").transition();
  var totYMax = -1;

  combinedData.forEach(function(d, i) {
      var m = d3.max(d.values, function(d2) { return d2.y; })
      if(m>totYMax)
        totYMax = m;
  });

  x.domain(d3.extent(lineChart1Data, function(d) { return d.x; }));
  //y.domain([0, d3.max(lineChart1Data, function(d) { return d.y; })]);
  y.domain([0, totYMax]);

// if no axis exists, create one
if (svg0.selectAll(".x.axis")._groups[0].length < 1)//svg0.selectAll(".x.axis")[0].length < 1 )
{
  svg0.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg0.append('text')
          .attr('class','x axis')//.attr('class','title')
          .attr('x',width/2)
          .attr('y',0-(margin.top/2))
          .attr('text-anchor','middle')
          .text('Annonser per månad')
// otherwise, update the axis
} else {
  svg0.selectAll(".x.axis").transition().duration(750).call(xAxis)
}

if (svg0.selectAll(".y.axis")._groups[0].length < 1) //svg0.selectAll(".y.axis")[0].length < 1 ) {
{
  svg0.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Antal");
// otherwise, update the axis
} else {
  svg0.selectAll(".y.axis").transition().duration(750).call(yAxis)
}

svg0.selectAll('.lineLegend').remove()

if(combinedData.length == 1 && svg0.selectAll(".line")._groups[0].length == 1)//svg0.selectAll(".line")[0].length == 1) // do transition if only one line
{
  combinedData.forEach(function(d, i) {
      var lines = svg.select(".line")   // change the line
      lines.duration(750)
      .attr("d", line(d.values))
      .style('stroke','steelblue');
  });
}
else
{
  // remove and add new path(s)
  svg0.selectAll(".line").remove();
  combinedData.forEach(function(d, i) {
      var dTemp = svg0.append("path")
      //.data(combinedData)
      .attr("class", "line")
      .attr("d", line(d.values))
      .style('stroke',function(){
        return colorsMix[i];
        //return '#'+Math.floor(Math.random()*16777215).toString(16);
      })

      if(combinedData.length != 1)
      {

        combinedData.forEach(function(d,i){
          svg0.append('text')
        //.attr('transform',function(d2) { return "translate(" + x(d2.value.x) + "," + y(d2.value.y) + ")";})
          .attr('class','lineLegend')
          .attr('x',margin.left/2 +5)
          .attr('y',0-(margin.top/2)+i*12+25)
          .attr('text-anchor','start')
          .attr('fill',colorsMix[i])
          .text(d.key)//.attr('y', y(d.values[d.values.length-1] ).text('XYZ');
        })
      }

      //.attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.temperature) + ")"; })
      //.attr("x", 3)
      //.attr("dy", ".35em")
      // also add legends and change colors if multiple
    });
}
}

var lineChart1Data = convertToDate(['2003-01','2005-02','2010-10'],[1,4,9])//[ { x: '2003-01', y: 1 }, { x: '2004-07', y: 4}, { x: '2005-10', y:9 } , { x: '2006-02', y:16 } ]
var lineChart2Data = convertToDate(['2002-01','2005-02','2010-10'],[1,7,3])
var combinedData = [ { key: "1", values: lineChart1Data } ];//, { key:"2" , values: lineChart2Data } ];

addLineChart1(combinedData);

function updateLineChart1(data)
{
  var combinedData = [];

  if(data.length>1) {
    for(var i=0;i<data.length;i++)
    {
      var months = data[i].values['Month']
      var counts = data[i].values['Counts']
      lineChart1Data = convertToDate(months,counts);
      combinedData.push({ key: data[i].key, values: lineChart1Data });
    }
  } else {
    var months = data[0].values['Month']
    var counts = data[0].values['Counts']
    lineChart1Data = convertToDate(months,counts);
    combinedData = [ { key: data[0].key, values: lineChart1Data } ];
  }

  addLineChart1(combinedData);

  return;
  // Differently updated if single or multiple values
  // A) single values

  if(data.length == 1)
  {
    data = data[0]
    var months = data['Month']
    var counts = data['Counts']

    lineChart1Data = convertToDate(months,counts);

    // Scale the range of the data again
    x.domain(d3.extent(lineChart1Data, function(d) { return d.x; }));
    y.domain([0, d3.max(lineChart1Data, function(d) { return d.y; })]);

    // Select the section we want to apply our changes to
    var svg = d3.select("body").transition();

    // Make the changes
    svg.select(".line")   // change the line
    .duration(750)
    .attr("d", line(lineChart1Data));
    svg.select(".x.axis") // change the x axis
    .duration(750)
    .call(xAxis);
    svg.select(".y.axis") // change the y axis
    .duration(750)
    .call(yAxis);
  }

  // B) multiple values: need to add legends, changed transition
  else if(data.length>1)
  {
    var months = data['Month']
    var counts = data['Counts']

    lineChart1Data = convertToDate(months,counts);

    // Scale the range of the data again
    x.domain(d3.extent(lineChart1Data, function(d) { return d.x; }));
    y.domain([0, d3.max(lineChart1Data, function(d) { return d.y; })]);

    // Select the section we want to apply our changes to
    var svg = d3.select("body").transition();

    // Make the changes
    svg.select(".line")   // change the line
    .duration(750)
    .attr("d", line(lineChart1Data));
    svg.select(".x.axis") // change the x axis
    .duration(750)
    .call(xAxis);
    svg.select(".y.axis") // change the y axis
    .duration(750)
    .call(yAxis);
  }
}
