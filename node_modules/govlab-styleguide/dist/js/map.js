// Map II : Simplified bubble map

var width = 960,
height = 500,
active = d3.select(null);

// var projection = d3.geo.albersUsa()
// var projection = d3.geo.kavrayskiy7()
// var projection = d3.geo.equirectangular()
var projection = d3.geo.mercator()
.scale(150)
.translate([width / 2, height / 1.5]);

var path = d3.geo.path()
.projection(projection);

var svg = d3.select('.b-map').append('svg')
.attr('width', width)
.attr('height', height);

svg.append('rect')
.attr('class', 'background')
.attr('width', width)
.attr('height', height)
.on('click', reset);

var g = svg.append('g')
.style('stroke-width', '1.5px');

// create a shade based on array of rgb values and scalar
function shade(rgb, v) {
  for (var i in rgb) { rgb[i] = rgb[i]*v > 255 ? 255 : rgb[i]*v; }
    return rgb;
}

// set up regions based on the topojson geometry id of each country
var northAmerica = d3.set([
  124, 840
  ]);

// could not find:
// Tuvalu
var eastAsia = d3.set([
  16, 882, 104, 116, 585, 156, 598, 242, 608, 360, 296, 90, 408, 410, 764, 418,
  626, 458, 776, 584, 583, 548, 496, 704, 392, 36, 554, 540, 158
  ]);

var euCentralAsia = d3.set([
  8, 807, 51, 498, 31, 499, 112, 642, 70, 688, 100, 762, 268, 792, 398, 795, 804,
  417, 860, 643
  ]);

var latinAmerica = d3.set([
  84, 328, 68, 332, 76, 340, 170, 388, 188, 484, 192, 558, 212, 214, 591, 600, 218,
  604, 222, 662, 308, 670, 320, 740, 862, 32, 858, 152, 238
  ]);

var midEastNorthAfrica = d3.set([
  12, 434, 262, 504, 818, 760, 364, 788, 368, 400, 887, 422, 682, 512, 784, 634, 414
  ]);

var southAsia = d3.set([
  4, 462, 50, 524, 64, 586, 356, 144
  ]);

var subSaharanAfrica = d3.set([
  24, 450, 204, 454, 72, 466, 854, 478, 108, 480, 132, 508, 120, 516, 140, 562, 566,
  174, 646, 180, 678, 178, 686, 384, 694, 232, 706, 231, 710, 266, 728, 729, 270,
  288, 748, 226, 834, 624, 768, 404, 800, 426, 894, 430, 716, 148, 324, 732
  ]);

var westEurope = d3.set([
  304, 352, 752, 578, 246, 826, 372, 250, 724, 620, 56, 528, 276, 616, 203, 40, 380,
  300, 348, 703, 428, 233, 208, 756, 440, 191, 705
  ]);

// this allows us to process multiple data sources in a single function using d3, e.g. instead of just d3.json()
queue()
.defer(d3.json, 'js/world.json')
.defer(d3.json, 'js/studies.json')
.defer(d3.tsv, 'js/world-country-names.tsv')
.await(ready);
function ready(error, world, studies, names) {
  if (error) throw error;

  // get country names from topojson
  var countries = topojson.feature(world, world.objects.countries).features;
  countries = countries.filter(function(d) {
    return names.some(function(n) {
      if (d.id == n.id) return d.name = n.name;
    });
  }).sort(function(a, b) {
    return a.name.localeCompare(b.name);
  });

  // draw map
  // g.selectAll('path')
  // .data(countries)
  // .enter()
  // .enter().append('path')
  // .attr('d', path)
  // .attr('class', 'feature')
  // .attr('id', function(d, i) {
  //   // console.log (countries[i].name.replace(/\s+/g, '-'), d.id);
  //   return countries[i].name.replace(/\s+/g, '-');
  // })
  // .on('click', clicked);

  // add the countries from topojson i think this is faster in terms of drawing edges
  // g.append('path')
  // .datum(topojson.mesh(world, world.objects.countries, function(a, b) { return a !== b; }))
  // .attr('class', 'country')
  // .attr('d', path);

  // add regions
  g.append('path')
  .datum(topojson.merge(world, world.objects.countries.geometries.filter( function(d, i) { return northAmerica.has(d.id); })))
  .attr('class', 'region')
  .attr('id', 'northAmerica')
  .attr('d', path)
  .on("mouseover", highlight)
  .on("mouseout", deHighlight);

  g.append('path')
  .datum(topojson.merge(world, world.objects.countries.geometries.filter( function(d, i) { return eastAsia.has(d.id); })))
  .attr('class', 'region')
  .attr('id', 'eastAsia')
  .attr('d', path)
  .on("mouseover", highlight)
  .on("mouseout", deHighlight);

  g.append('path')
  .datum(topojson.merge(world, world.objects.countries.geometries.filter( function(d, i) { return euCentralAsia.has(d.id); })))
  .attr('class', 'region')
  .attr('id', 'euCentralAsia')
  .attr('d', path)
  .on("mouseover", highlight)
  .on("mouseout", deHighlight);

  g.append('path')
  .datum(topojson.merge(world, world.objects.countries.geometries.filter( function(d, i) { return latinAmerica.has(d.id); })))
  .attr('class', 'region')
  .attr('id', 'latinAmerica')
  .attr('d', path)
  .on("mouseover", highlight)
  .on("mouseout", deHighlight);

  g.append('path')
  .datum(topojson.merge(world, world.objects.countries.geometries.filter( function(d, i) { return midEastNorthAfrica.has(d.id); })))
  .attr('class', 'region')
  .attr('id', 'midEastNorthAfrica')
  .attr('d', path)
  .on("mouseover", highlight)
  .on("mouseout", deHighlight);

  g.append('path')
  .datum(topojson.merge(world, world.objects.countries.geometries.filter( function(d, i) { return southAsia.has(d.id); })))
  .attr('class', 'region')
  .attr('id', 'southAsia')
  .attr('d', path)
  .on("mouseover", highlight)
  .on("mouseout", deHighlight);

  g.append('path')
  .datum(topojson.merge(world, world.objects.countries.geometries.filter( function(d, i) { return subSaharanAfrica.has(d.id); })))
  .attr('class', 'region')
  .attr('id', 'subSaharanAfrica')
  .attr('d', path)
  .on("mouseover", highlight)
  .on("mouseout", deHighlight);

  g.append('path')
  .datum(topojson.merge(world, world.objects.countries.geometries.filter( function(d, i) { return westEurope.has(d.id); })))
  .attr('class', 'region')
  .attr('id', 'westEurope')
  .attr('d', path)
  .on("mouseover", highlight)
  .on("mouseout", deHighlight);

  // draw bubbles
  var s = studies.children; // quick shorthand copy because we still need the original structure with children for pack layout later

  // count up totals in data categories and flag data duplicates for later filtering
  var counts = {}; // object for counting totals in the provided data, could possibly be merged into studies obj
  for (var i in s) {
    var l = s[i].location.replace(/\s+/g, '-');
    if (!(l in counts)) {
      counts[l] = {};
    }
    if ('count' in counts[l]) {
      counts[l].count++;
      studies.children[i].duplicate = true;
    } else {
      counts[l].count = 1;
    }
  }

  // assign a size value to each datum based on the count
  var base = 4; // log base for bubbles size curve
  var scale = 80; // multiplier for bubbles size curve
  for (var i in studies.children) {
    var l = s[i].location.replace(/\s+/g, '-');
    studies.children[i].size = (Math.log(counts[l].count + 1)/Math.log(base))*scale;
  }

  var node = svg.selectAll('svg')
  .data(studies.children)
  .enter().append('g')
  .filter(function(d) { return !d.duplicate; })
  .attr('class', function(d, i) {
    return 'node';
  })
  .attr('transform', function(d, i) {
    // var country = g.select('#' + d.location.replace(/\s+/g, '-')).datum();
    // var b = path.bounds(country),
    // x = (b[0][0] + b[1][0]) / 2,
    // y = (b[0][1] + b[1][1]) / 2;
    // if (d.location === 'United States') {
    //   // Translate the coords manually for USA
    //   // This is a workaround to deal with the fact that the bounding box of
    //   // USA expands to the entire width of the map due to Alaska's islands
    //   x = x/2.15;
    //   y = y*1.25;
    // }

    var region = g.select('#' + d.location.replace(/\s+/g, '-')).datum();
    var b = path.bounds(region),
    x = (b[0][0] + b[1][0]) / 2,
    y = (b[0][1] + b[1][1]) / 2;

    // manual adjustments
    // (i.e. some of the bounding boxes don't make visual sense, so just
    // adjust those manually)
    if (d.location === 'northAmerica') {
      x *= .45;
      y *= 1.7;
    } else if (d.location === 'euCentralAsia') {
      x *= 1.5;
      y *= 1.5;
    } else if (d.location === 'eastAsia') {
      x *= 1.7;
      y *= .9;
    } else if (d.location === 'latinAmerica') {
      x *= 1.2;
      y *= .95;
    } else if (d.location === 'westEurope') {
      x *= .95;
      y *= .95;
    } else if (d.location === 'subSaharanAfrica') {
      x *= 1.05;
      y *= .9;
    } else if (d.location === 'midEastNorthAfrica') {
      x *= 1.05;
      y *= .9;
    }

    return 'translate(' + x + ',' + y + ')';
  });

  node.append('circle')
  .attr('r', function(d) {
    return d.size/2; // ie size is a diameter for layout purposes
  })
  .style('fill', function(d) {
    // strip out just the count numbers and put into a flat array, then find the max
    var countsarr = [];
    for (var i in counts) { countsarr.push(counts[i].count); }
      var max = Math.max.apply(null, countsarr);

    // calculate the value of the shade (logarithmic)
    var base = 2; // log base for shade curve
    var scale = 2; // multiplier for shade curve
    var c = counts[d.location.replace(/\s+/g, '-')].count;
    var v = (Math.log(c + 1)/Math.log(base))*scale/max;
    v = v > 1 ? 1 : v;

    return d3.rgb.apply(null, shade([0, 138, 179], v));
  })
  .attr('id', function(d, i) {
    return '_bubble_' + d.location.replace(/\s+/g, '-');
  })
  .on("mouseover", highlight)
  .on("mouseout", deHighlight);

  node.append('text')
  .attr('dy', '.3em')
  .style('text-anchor', 'middle')
  .text(function(d) {
    var t =
    // d.location + ' ' +
    counts[d.location.replace(/\s+/g, '-')].count;
    return t;
  })
  .attr('id', function(d, i) {
    return '_text_' + d.location.replace(/\s+/g, '-');
  })
  .on("mouseover", highlight)
  .on("mouseout", deHighlight);

  // no one needs you antarctica
  g.select('#Antarctica').remove();
}

function highlight(d) {
  var region = '#' + this.id.replace(/_bubble_|_text_/, '');
  var bubble = '#' + this.id.replace(/^(?!_bubble_|_text_)|_text_/, '_bubble_');
  d3.selectAll('.node').classed('fade', true);
  d3.select(region).classed('active', true);
  d3.select(bubble).classed('active', true);
  zoomBubble(bubble, 1.4);
  // console.log('in', this.id); // debug
}

function deHighlight(d) {
  var region = '#' + this.id.replace(/_bubble_|_text_/, '');
  var bubble = '#' + this.id.replace(/^(?!_bubble_|_text_)|_text_/, '_bubble_');
  d3.selectAll('.node').classed('fade', false);
  d3.select(region).classed('active', false);
  d3.select(bubble).classed('active', false);
  zoomBubble(bubble, -1);
  // console.log('out', this.id); // debug
}

var intervals = {};
function zoomBubble(elem, zoom) {
  var
  frames = 100,
  e = d3.select(elem),
  r = Number(e.attr('r')),
  eid = e.attr('id'),
  x = 0
  ;

  var defaultSize = e.datum().size/2;

  function frame() {
    if (zoom > 0) {
      // e.attr('r', defaultSize*(1+(x/frames)*(zoom-1)));
      e.attr('r', r+(zoom*defaultSize-r)*(x/frames));
      x++;

      if (x >= frames) {
        clearInterval(id);
      }
    } else { // reset to original size
      e.attr('r', r-(r-defaultSize)*(x/frames));
      x++;

      if (x >= frames) {
        clearInterval(id);
      }
    }
  }

  if (eid in intervals && intervals[eid] > 0) {
    clearInterval(intervals[eid]);
  }
  var id = setInterval(frame, 1);
  intervals[eid] = id;

  return id;
}

function clicked(d) {
  console.log(this.id, d.id);
  if (active.node() === this) return reset();
  active.classed('active', false);
  active = d3.select(this).classed('active', true);

  var bounds = path.bounds(d),
  dx = bounds[1][0] - bounds[0][0],
  dy = bounds[1][1] - bounds[0][1],
  x = (bounds[0][0] + bounds[1][0]) / 2,
  y = (bounds[0][1] + bounds[1][1]) / 2,
  scale = .9 / Math.max(dx / width, dy / height),
  translate = [width / 2 - scale * x, height / 2 - scale * y];
}

function reset() {
  active.classed('active', false);
  active = d3.select(null);

  g.transition()
  .duration(750)
  .style('stroke-width', '1.5px')
  .attr('transform', '');
}
