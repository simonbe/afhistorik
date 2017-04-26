var data = {
  labels: [
    'Ingen databehörighet'
  ],
  series: [
    {
      label: 'XX',
      values: [100]
    },]
};

var chart2Width      = 220,
    barHeight        = 20,
    groupHeight      = barHeight * 1;//data.series.length,
    gapBetweenGroups = 2,
    spaceForLabels   = 200,
    spaceForLegend   = 150,
    yOffsetBars = 20;

// Zip the series data together (first values, second values, etc.)
var zippedData = [];
for (var i=0; i<data.labels.length; i++) {
  for (var j=0; j<data.series.length; j++) {
    zippedData.push(data.series[j].values[i]);
  }
}

// Color scale
var color = d3.scaleOrdinal(d3.schemeCategory20);//schemeCategory20;
var chart2Height = 200;//barHeight * zippedData.length + gapBetweenGroups * data.labels.length;

var xBar3 = d3.scaleLinear()
    .domain([0, d3.max(zippedData)])
    .range([0, chart2Width]);

var yBar3 = d3.scaleLinear()
    .range([chart2Height + gapBetweenGroups, 0]);

var yAxisBar3 = d3.axisLeft(yBar3).tickFormat('').tickSize(0)//d3.svg.axis()
    //.scale(yBar3)
    //.tickFormat('')
    //.tickSize(0)
    //.orient("left");

// Specify the chart2 area and dimensions
var chart2 = d3.select(".chart2")
    .attr("width", spaceForLabels + chart2Width + spaceForLegend)
    .attr("height", chart2Height);

    function orderEmployers(occupations,counts)
    {
      var maxNr = 6;
      data = {}

      // sort occupations by the count numbers
      var list = []
      for(var i=0;i<occupations.length;i++)
      {
        list.push({'occ': occupations[i], 'count': counts[i]})
      }

      list.sort(function(a,b){
        return ((a.count>b.count)? -1 : ((a.count == b.count)? 0 : 1));
      })

      for(var k=0;k<list.length;k++)
      {
        occupations[k] = list[k].occ;
        counts[k] = list[k].count;
      }

      // return them using correct format
      labels = [];
      series = [];
      var singleData = [];

      for(var i=0;i<maxNr;i++)
      {
        labels.push(occupations[i])
        singleData.push(counts[i]);
      }

      series.push({label:'Arbetsgivare',values: singleData});
      data = { labels: labels, series: series};

      return data;
    }

    function updateHorizchart22(data,useReal)
    {
      if(data[0])
      {
        var occupations = data[0].values['Employers']
        var counts = data[0].values['Counts']
        data = orderEmployers(occupations,counts)

        var zippedData = [];
        for (var i=0; i<data.labels.length; i++) {
          for (var j=0; j<data.series.length; j++) {
            zippedData.push(data.series[j].values[i]);
          }
        }
        // Scale the range of the data again

        var xBar3 = d3.scaleLinear()
        .domain([0, d3.max(zippedData)])
        .range([0, chart2Width]);

        var yBar3 = d3.scaleLinear()
        .range([chart2Height + gapBetweenGroups, 0]);

        // Create bars
        var Bar3 = chart2.selectAll("g")
        .data(zippedData);

        Bar3.exit()
        //  .transition()
        //  .duration(300)
        //  .attr('y',yBar3(0))
        //  .attr('height',barHeight - yBar3(0))
        .remove()

        Bar3.enter().append("g")
        .attr("transform", function(d, i) {
          return "translate(" + spaceForLabels + "," +  (i * barHeight + gapBetweenGroups * (0.5 + Math.floor(i/data.series.length))) + ")";
        })

        Bar3.select('#labelTexts').remove()

        Bar3.append("rect")
        .attr("width", "100%")
        .attr("height", "100%")
        .attr("fill", "white");

        Bar3.append("text")
        .attr('id','labelTexts')
        .attr("class", "label")
        .attr("x", function(d) { return - 10; })
        .attr("y", groupHeight / 2)
        .attr("dy", ".35em")
        .text(function(d,i) {
          if (i % data.series.length === 0)
          return data.labels[Math.floor(i/data.series.length)];
          else
          return ""});

          // Create rectangles of the correct width
          Bar3.select('#idRects').remove()
          Bar3.append("rect")
          .attr('id','idRects')
          .attr("fill", function(d,i) { return "indianred"; })//color(i % data.series.length); })
          //.attr("class", "bar")
          .attr("width", xBar3)
          .attr("height", barHeight - 1);

          // Add text label in bar
          Bar3.append("text")
          .attr("x", function(d) { return xBar3(d) - 3; })
          .attr("y", barHeight / 2)
          .attr("fill", "red")
          .attr("dy", ".35em")
          .text(function(d) { return d; });

          // Draw labels
          chart2.append("g")
          .attr("class", "y axis")
          .attr("transform", "translate(" + spaceForLabels + ", " + -gapBetweenGroups/2 + ")")
          .call(yAxisBar3);

          // Draw legend
          var legendRectSize = 18,
          legendSpacing  = 4;

          var legend = chart2.selectAll('.legend')
          .data(data.series);

          legend.exit().remove();
          legend.enter()
          .append('g')
          .attr('transform', function (d, i) {
            var height = legendRectSize + legendSpacing;
            var offset = 0;//-gapBetweenGroups/2 - 100;
            var horz = spaceForLabels + chart2Width + 40 - legendRectSize - 150;
            var vert = i * height - offset;
            return 'translate(' + horz + ',' + vert + ')';
          });

          /*legend.append('rect')
          .attr('width', legendRectSize)
          .attr('height', legendRectSize)
          .style('fill', function (d, i) { return "indianred";}) //color(i); })
          .style('stroke', function (d, i) { return "indianred";}) //color(i); });

          legend.append('text')
          .attr('class', 'legend')
          .attr('x', legendRectSize + legendSpacing)
          .attr('y', legendRectSize - legendSpacing)
          .text(function (d) { return d.label; });
          */
        }
      }

updateHorizchart22(data,false);
