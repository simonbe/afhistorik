var width = 500,
    height = 500;

var svg = d3.select('#areaMap').append('svg')
    .attr('width', '100%')//width)
    .attr('height', '100%')//height);

d3.select('#areaMap').on('resize',mapResize);

var active = d3.select(null);

var subunits = [];
var centered;

var projection = d3.geoMercator()
      .scale(1)
      .translate([0, 0]);
var path = d3.geoPath().projection(projection);

svg.append("rect")
    .attr("class","background")
    .attr("width", width)
    .attr("height", height)
    .on("click", clicked);

var gMap = svg.append('g')
        .style('stroke-width','1.5px');

//d3.json('sverige.json',  function(data) {//'js/sverige.topojson', function(data) {

//d3.json('http://172.16.200.111/sverige.json',  function(data) {//'js/sverige.topojson', function(data) {

setTimeout(function() {
  subunits = topojson.feature(dataSverige, dataSverige.objects.sverige);

  for(var i=0;i<subunits.features.length;i++)
  {
    subunits.features[i].color = "steelblue";
  }

  var counties = dataSverige.objects.sverige.geometries;
  var color =  d3.scaleOrdinal(d3.schemeCategory20);//d3.scale.category20();

  var offsetX = 50,
      offsetY = 190;

  var b = path.bounds(topojson.merge(dataSverige, counties)),
      s = 3 / Math.max((b[1][0] - b[0][0]) / width, (b[1][1] - b[0][1]) / height),
      t = [(width - s * (b[1][0] + b[0][0])) / 2 + offsetX, (height - s * (b[1][1] + b[0][1])) / 2 + offsetY];

  projection.scale(s).translate(t);

  gMap.selectAll('.munic')
      .data(subunits.features)
    .enter().append('path')
      //.attr('class', 'county')//function(d) { return 'munic munic--' + d.properties.KNKOD; })
      .attr('id','kommun')
      .attr('d', path)
      .style("fill", function(d,i) { return subunits.features[i].color; })//function(d,i) {  return color(i); });//.style("fill", function(d, i) { return color(d.color = d3.max(neighbors[i], function(n) { return countries[n].color; }) + 1 | 0); });
      .on('click',clicked)
      //.on('dblclick',dblClicked);

  gMap.selectAll('.munic')
      .data(subunits.features)
      .enter().append('text')
      .attr('class','place-label')
      .attr('transform', function(d,i) { return "translate(" + path.centroid(d) +")"; })
      .attr('dy','.05em')
      .style('font-size','1px')
      .style('visibility','hidden')//.append('svg:title')
      .text(function(d,i) { return d.properties.KNNAMN; });
},50)

//});

function clicked(d)
{
  if(active.node() === this) // return mapReset();//selectAndUse(d);
  {
    active.classed('active',false);
    active = d3.select(this).classed('active',true);

    var bounds = path.bounds(d),
      dx = bounds[1][0] - bounds[0][0],
      dy = bounds[1][1] - bounds[0][1],
      x = (bounds[0][0] + bounds[1][0]) / 2,
      y = (bounds[0][1] + bounds[1][1]) / 2,
      scale = .4 / Math.max(dx / width, dy / height),
      translate = [width / 2 - scale * x, height / 2 - scale * y];

      // Call prompt handling
      updatePrompt(d.properties.KNKOD);

      gMap.transition().duration(750).selectAll('text')
          .style('visibility',function(d2) { if(d2 === d) return 'visible'; else return 'hidden';} )
          .style('font-size', 14/scale + 'px');

      gMap.transition()
        .duration(750)
        .style('stroke-width', 1.5 / scale + 'px')
        .attr('transform','translate(' + translate + ')scale(' + scale +')')
    }
    else {
      active.classed('active',false);
      active = d3.select(this).classed('active',true);

      var bounds = path.bounds(d),
      dx = bounds[1][0] - bounds[0][0],
      dy = bounds[1][1] - bounds[0][1],
      x = (bounds[0][0] + bounds[1][0]) / 2,
      y = (bounds[0][1] + bounds[1][1]) / 2,
      scale = .4 / Math.max(dx / width, dy / height),
      translate = [width / 2 - scale * x, height / 2 - scale * y];

      gMap.transition().duration(750).selectAll('text')
      .style('visibility',function(d2) { if(d2 === d) return 'visible'; else return 'hidden';} )
      .style('font-size', 14/scale + 'px');

      gMap.transition()
      .duration(750)
      .style('stroke-width', 1.5 / scale + 'px')
      .attr('transform','translate(' + translate + ')scale(' + scale +')')
    }
}

function dblClicked(d)
{
  /*if(active.node() === this)
  {
   return mapReset();
 }*/

  active.classed('active',false);
  active = d3.select(this).classed('active',true);

  var bounds = path.bounds(d),
    dx = bounds[1][0] - bounds[0][0],
    dy = bounds[1][1] - bounds[0][1],
    x = (bounds[0][0] + bounds[1][0]) / 2,
    y = (bounds[0][1] + bounds[1][1]) / 2,
    scale = .4 / Math.max(dx / width, dy / height),
    translate = [width / 2 - scale * x, height / 2 - scale * y];

  gMap.transition().duration(750).selectAll('text')
      .style('visibility',function(d2) { if(d2 === d) return 'visible'; else return 'hidden';} )
      .style('font-size', 14/scale + 'px');

  gMap.transition()
    .duration(750)
    .style('stroke-width', 1.5 / scale + 'px')
    .attr('transform','translate(' + translate + ')scale(' + scale +')')

  // Call prompt handling
  updatePrompt(d.properties.KNKOD);
}

function mapReset()
{
  active.classed('active',false);
  active = d3.select(null);
  gMap.transition()
    .duration(750)
    .style('stroke-width','1.5px')
    .attr('transform','');
}

// called when input includes region
function mapZoom(codes)
{
  console.log('map zoom')

  // only zoom in if a single region
  if(codes && codes.length == 1)
  {
    var selected = null;
    for(var i=0;i<subunits.features.length;i++)
    {
      if(subunits.features[i].properties.KNKOD == codes[0])
      {
        selected = subunits.features[i];
      }
    }

    var bounds = path.bounds(selected),
      dx = bounds[1][0] - bounds[0][0],
      dy = bounds[1][1] - bounds[0][1],
      x = (bounds[0][0] + bounds[1][0]) / 2,
      y = (bounds[0][1] + bounds[1][1]) / 2,
      scale = .4 / Math.max(dx / width, dy / height),
      translate = [width / 2 - scale * x, height / 2 - scale * y];

    gMap.transition().duration(750).selectAll('text')
        .style('visibility',function(d2) { if(d2 === codes[0]) return 'visible'; else return 'hidden';} )
        .style('font-size', 14/scale + 'px');
    gMap.transition()
        .duration(750)
        .style('stroke-width', 1.5 / scale + 'px')
        .attr('transform','translate(' + translate + ')scale(' + scale +')')
  }
}

function mapResize()
{
  console.log('map resize')
}

/*
var x,y,k;
if(d && centered!=d)
{
  var centroid = path.centroid(d);
  x = centroid[0];
  y = centroid[1];
  k = 4;
  centered = d;
  // centered.properties.KNKOD ger uppdaterad data
}
else {
  x = width/2;
  y = height/2;
  k = 1;
  centered = null;
}

//  d3.selectAll("path")
//    .classed("active", centered && function(d) { return d === centered; });

svg.transition().duration(750).selectAll('text')
  .style('visibility',function(d) { if(d === centered) return 'visible'; else return 'hidden';} );

svg.transition().duration(750)
  .attr("transform","translate(" + width/2 + "," + height/2 + ")scale(" + k + ")translate(" + -x + "," + -y + ")")
  //.style("stroke-width", 1.5 / k + "px");
*/

function getMaxCountysMultiples(countyData,usePerCapita)
{
  // Note: we are assuming the codes/counts come in the same order for each county data

  // init

  //countyData = countyData[0].values.percapita

  //var koder = countyData['Kommunkod']
  //var counts = countyData['CountsPerCapita']

  var countyData0 = countyData[0].values.total;
  if(usePerCapita)
    countyData0 = countyData[0].values.percapita;

  var koder = Object.keys(countyData0);
  var counts = Object.keys(countyData0).map(function(key){
    return countyData0[key];
  });

  //var koder = countyData[0].values['Kommunkod']
  //var counts = countyData[0].values['CountsPerCapita']

  var maxCounts = []
  var maxIndexes = [];

  for(var i=0;i<koder.length;i++)
  {
    maxCounts[i] = counts[i];
    maxIndexes[i] = 0;
  }

  for(var i=0;i<countyData.length;i++)
  {
    //koder = countyData[i].values['Kommunkod']
    if(usePerCapita)
      counts = countyData[i].values.percapita;//['CountsPerCapita']
    else {
        counts = countyData[i].values.total;
      }

    for(var j=0;j<koder.length;j++)
    {
      if(counts[koder[j]] > maxCounts[j])
      {
        maxCounts[j] = counts[koder[j]]
        maxIndexes[j] = i;
      }
    }
  }

  return maxIndexes;
}

function updateMap(countyData,usePerCapita)
{
  // different behaviour if it is one input or if we are comparing several

  if(countyData.length == 1) // only one input - show demand of this across country
  {
    if(usePerCapita)
      countyData = countyData[0].values.percapita;
    else
      countyData = countyData[0].values.total;

    //var koder = countyData['Kommunkod']
    //var counts = countyData['CountsPerCapita']
    var koder = Object.keys(countyData);
    var counts = Object.keys(countyData).map(function(key){
    return countyData[key];
    });


    var minCounts = Math.min.apply(Math,counts);
    var maxCounts = Math.max.apply(Math,counts);

    var colorScale = d3.scaleLinear()
    .range(['white','steelblue','red'])
    .domain([minCounts,maxCounts/2,maxCounts])
    //.range(['white','steelblue','red'])
    //.domain([minCounts,maxCounts/2,maxCounts])

    // fix mismatch between API and topojson
    for(var i=0;i<koder.length;i++)
    {
      if(koder[i].length == 3)
      koder[i] = "0" + koder[i]
    }

    for(var i=0;i<subunits.features.length;i++)
    {
      /*var index = koder.indexOf(subunits.features[i].properties.KNKOD)
      if(index>-1)
      {
        subunits.features[i].color = colorScale(counts[index-1]);
      }
      else {
        subunits.features[i].color = "steelblue";//"steelblue";
      }*/
      var knkod = subunits.features[i].properties.KNKOD;
      if(koder.indexOf(knkod) > -1)
      {
        subunits.features[i].color = colorScale(countyData[knkod])
      }
      else {
        subunits.features[i].color = "white";//"steelblue";
      }
    }

    //  var svg = d3.select("body").transition();
    gMap.selectAll('path')
    .style('stroke', 'black')
    .style('stroke-width', '0.1')
    .style("fill", function(d,i) { return subunits.features[i].color; });
  }
  else {
    // comparing several inputs, showing top one in each part

    // foreach kommunkod, determine the top index
    //countyData = countyData[0].values.percapita

    //var koder = countyData['Kommunkod']
    //var counts = countyData['CountsPerCapita']

    var countyData0 =countyData[0].values.total
    if(usePerCapita)
      countyData0 =countyData[0].values.percapita


    var koder = Object.keys(countyData0);
    var counts = Object.keys(countyData0).map(function(key){
    return countyData0[key];
    });

    //var koder = countyData[0].values['Kommunkod']
    var maxIndexes = getMaxCountysMultiples(countyData,usePerCapita)

    var minCounts = 0;//Math.min.apply(Math,counts);
    var maxCounts = Math.max.apply(Math,maxIndexes);//Math.max.apply(Math,counts);

    var colorScale = d3.scale.sqrt()
    .range(['steelblue','yellow','red'])//.range(['steelblue','green','red'])
    .domain([minCounts,maxCounts/2,maxCounts])

    // fix mismatch between API and topojson
    for(var i=0;i<koder.length;i++)
    {
      if(koder[i].length == 3)
      koder[i] = "0" + koder[i]
    }

    for(var i=0;i<subunits.features.length;i++)
    {
      var index = koder.indexOf(subunits.features[i].properties.KNKOD)
      if(index>-1){
        subunits.features[i].color = colorScale(maxIndexes[index-1]);
      }
      else {
        subunits.features[i].color = "white";
      }
    }

    //  var svg = d3.select("body").transition();
    gMap.selectAll('path')
    .style("fill", function(d,i) { return subunits.features[i].color; });
  }
}
