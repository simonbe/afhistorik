var colorsMix = ['steelblue','red','green','black','yellow','gray']

var orderMonths = { '01':'jan', '02': 'feb', '03': 'mar', '04': 'apr', '05': 'maj',
'06':'jun', '07':'jul','08':'aug','09':'sep','10':'okt','11':'nov','12':'dec'};
var monthsOrder = ['01','02','03','04','05','06','07','08','09','10','11','12'];//['jan','feb','mar','apr','maj','jun','jul','aug','sep','okt','nov','dec']

function convertToMonthHistogram(months,counts)
{
  var converted = [];
  var histogram = {};

  for(var i=0;i<counts.length;i++)
  {
    var parts = months[i].split('-'); // of form '2010-06'
    var d = parts[1] // only use month part
    if(d in histogram)
      histogram[d] = histogram[d] + counts[i];
    else {
      histogram[d] = counts[i];
    }
  }

  // normalize
  var tot = 0;
  for(var key in histogram)
  {
    tot = tot + histogram[key]
  }

  // return translated and ordered
  for(var i=0;i<monthsOrder.length;i++)
  {
    converted.push({ x:orderMonths[monthsOrder[i]], y:(histogram[monthsOrder[i]]/tot)})
  }

  return converted;
}

// Set the dimensions of the canvas / graph
var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 400 - margin.left - margin.right,
    height = 200 - margin.top - margin.bottom;

    var xBar = d3.scaleBand().range([0, width], .1)//d3.scaleOrdinal()
        //.rangeRoundBands([0, width], .1);

    var yBar = d3.scaleLinear()
        .range([height, 0]);

    var xAxisBar = d3.axisBottom(xBar)//d3.svg.axis()
        //.scale(xBar)
        //.orient("bottom");

    var yAxisBar = d3.axisLeft(yBar).ticks(10,"%")//d3.svg.axis()
        //.scale(yBar)
        //.orient("left")
        //.ticks(10, "%");

    var svgbar = d3.select("#area3").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Adds the svg canvas
//  var barChart1Data = [{x:'Jan', y:10}, {x:'Feb', y:20}, {x:'Mar', y:20}];//convertToDate(['2003-01','2005','2010'],[1,4,9])//[ { x: '2003-01', y: 1 }, { x: '2004-07', y: 4}, { x: '2005-10', y:9 } , { x: '2006-02', y:16 } ]


  svgbar.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        //.call(xAxisBar);

  svgbar.append("g")
              .attr("class", "y axis")
          //    .call(yAxisBar)
            /*.append("text")
              .attr("transform", "rotate(-90)")
              .attr("y", 6)
              .attr("dy", ".71em")
              .style("text-anchor", "end")
              .text("Procent");*/

              svgbar.append('text')
                      .attr('class','x axis')//.attr('class','title')
                      .attr('x',width/2)
                      .attr('y',0-(margin.top/2))
                      .attr('text-anchor','middle')
                      .text('Fördelning')


function updateBarChart1(data)
{
    var totData = [];
    var barChart1Data = []; // temp variable

    for(var i=0;i<data.length;i++)
    {
      var months = data[i].values['Month']
      var counts = data[i].values['Counts']
      var dataConv = convertToMonthHistogram(months,counts);
      if(i==0)
        barChart1Data = dataConv;
      totData.push(dataConv);
    }

    // Scale the range of the data again
    xBar.domain(barChart1Data.map( function(d) { return d.x; }));
    yBar.domain([0,0.2]);//[0, d3.max(barChart1Data, function(d) { return d.y; })]);

    // Select the section we want to apply our changes to
    //var svg = d3.select("#area3");
/*    xAxisBar = d3.svg.axis()
        .scale(xBar)
        .orient("bottom")
        .ticks(12);

    yAxisBar = d3.svg.axis()
        .scale(yBar)
        .orient("left")
        .ticks(10, "%");
*/

  svgbar.selectAll("rect").data([]).exit()
  .transition()
  .duration(300)
  .attr('y',yBar(0))
  .attr('height',height - yBar(0))
  .remove()

    svgbar.transition().select(".x.axis") // change the x axis
    .duration(300)
    .call(xAxisBar);
    svgbar.transition().select(".y.axis") // change the y axis
    .duration(300)
    .call(yAxisBar);

    var bars = svgbar.selectAll('.bar').data(totData, function(d) { return d; })
    var layer = svgbar.selectAll(".bar")
    .data(totData)
  .enter().append("g")
    .attr("class", "layer")
    .style("fill", function(d, i) { return 'steelblue'; });

    /*svgbar.transition()
      .duration(300)
      .attr('y',yBar(0))
      .attr('height',height - yBar(0))*/
      layer.selectAll("bar")
      .data(function(d) { return d; }).remove()
      //.remove()
    layer.selectAll(".rectClass").data([]).remove()

    var rect0 = layer.selectAll("bar")
    .data(function(d) { return d; })
  .enter().append("rect")
    .attr('class','rectClass')
    .attr("x", function(d) { return xBar(d.x); })
    .attr("y", height)
    .attr("width", xBar.bandwidth())//.rangeBand())
    .attr("height", 0);

    /*rect.transition()
    .delay(function(d, i) { return i * 10; })
    .attr("y", function(d) { return yBar(d.y); })
    .attr("height", function(d) { return yBar(d.y0) - y(d.y0 + d.y); });*/
    var n=totData.length;

    rect0.transition()
    .delay(function(d, i) { return i * 1; })
    .attr("x", function(d, i, j) { var l1 = xBar(d.x) + xBar.bandwidth() / n * i; return l1/2;})//.rangeBand() / n * j; })
    .attr("y", function(d) { return yBar(d.y) })
    .attr("width", xBar.bandwidth() / n - 5)//.rangeBand() / n)
    .attr("height", 0);

    rect0.transition()
    .delay(function(d, i) { return i * 10; })
    .attr("x", function(d, i, j) { return (xBar(d.x) + xBar.bandwidth() / n * i)/2;})//.rangeBand() / n * j; })
    .attr("y", function(d) { return yBar(d.y) })
    .attr("width", xBar.bandwidth() / n - 5)//.rangeBand() / n)
    .style('fill',function(d,i,j) { return colorsMix[j]; })
    .attr("height", function(d) { return height - yBar(d.y); });

    /*var rect = bars//.selectAll(".bar")
    //.data(function(d) { return d; })
    .enter().append("rect")
    .attr("x", function(d) { return xBar(d.x); })
    .attr("y", height)
    .attr("width", xBar.rangeBand())
    .attr("height", 0);*/


    /*bars.exit()
      .transition()
      .duration(300)
      .attr('y',yBar(0))
      .attr('height',height - yBar(0))
      .remove()

    bars.enter().append('rect')
    .attr('class','bar')
    .attr('y',yBar(0))
    .attr('height', height - yBar(0))

    bars.transition()
      .duration(300)
      .attr('x',function(d) { return xBar(d.x)})
      .attr('width', xBar.rangeBand())
      .attr('y', function(d) { return yBar(d.y)})
      .attr('height', function(d) { return height - yBar(d.y)})*/
/*    svg.transition().select('bar')
    .duration(750)
    .attr("x", function(d) { return xBar(d.x); })
      .attr('y', function(d) { return yBar(d.y)})
      .attr('height', function(d) { return height - yBar(d.y)})
*/
}
