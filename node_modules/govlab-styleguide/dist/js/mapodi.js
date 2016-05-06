// Map II : Simplified bubble map (ODI version)

var mobileOnly = '(max-width: 767px)'

// disable the map on mobile (ie replace with something else)
if (window.matchMedia(mobileOnly).matches) {

  console.log('Mobile, map disabled');

} else { // desktop
  var width = 900,
  height = 400,
  active = d3.select(null);

  var projection = d3.geo.mercator()
  .scale(120)
  .translate([width / 2, height / 1.5]);

  var path = d3.geo.path()
  .projection(projection);

  var svg = d3.select('.map').append('svg')
  .attr('width', width)
  .attr('height', height);

  svg.append('rect')
  .attr('class', 'background')
  .attr('width', width)
  .attr('height', height);

  var g = svg.append('g')
  .style('stroke-width', '1.5px');

// create a shade based on array of rgb values and scalar
function shade(rgb, v) {
  for (var i in rgb) { rgb[i] = rgb[i]*v > 255 ? 255 : rgb[i]*v; }
    return rgb;
}

// set up regions based on the topojson geometry id of each country
// var northAmerica = d3.set([
//   124, 840
//   ]);

// var eastAsia = d3.set([
//   16, 882, 104, 116, 585, 156, 598, 242, 608, 360, 296, 90, 408, 410, 764, 418,
//   626, 458, 776, 584, 583, 548, 496, 704, 392, 36, 554, 540, 158
//   ]);

// var euCentralAsia = d3.set([
//   8, 807, 51, 498, 31, 499, 112, 642, 70, 688, 100, 762, 268, 792, 398, 795, 804,
//   417, 860, 643, 703
//   ]);

// var latinAmerica = d3.set([
//   84, 328, 68, 332, 76, 340, 170, 388, 188, 484, 192, 558, 212, 214, 591, 600, 218,
//   604, 222, 662, 308, 670, 320, 740, 862, 32, 858, 152, 238
//   ]);

// var midEastNorthAfrica = d3.set([
//   12, 434, 262, 504, 818, 760, 364, 788, 368, 400, 887, 422, 682, 512, 784, 634, 414
//   ]);

// var southAsia = d3.set([
//   4, 462, 50, 524, 64, 586, 356, 144
//   ]);

// var subSaharanAfrica = d3.set([
//   24, 450, 204, 454, 72, 466, 854, 478, 108, 480, 132, 508, 120, 516, 140, 562, 566,
//   174, 646, 180, 678, 178, 686, 384, 694, 232, 706, 231, 710, 266, 728, 729, 270,
//   288, 748, 226, 834, 624, 768, 404, 800, 426, 894, 430, 716, 148, 324, 732
//   ]);

// var westEurope = d3.set([
//   304, 352, 752, 578, 246, 826, 372, 250, 724, 620, 56, 528, 276, 616, 203, 40, 380,
//   300, 348, 428, 233, 208, 756, 440, 191, 705
//   ]);

// var verboseNames = {
//   'northAmerica'        : 'North America',
//   'eastAsia'            : 'East Asia & Pacific',
//   'euCentralAsia'       : 'East Europe & Central Asia',
//   'latinAmerica'        : 'Latin America & Caribbean',
//   'midEastNorthAfrica'  : 'Middle East & North Africa',
//   'southAsia'           : 'South Asia',
//   'subSaharanAfrica'    : 'Sub-Saharan Africa',
//   'westEurope'          : 'West Europe'
// }

var regions =
{
  'af' : {
    'name' : 'Africa',
    'geometries'  : [12, 24, 204, 72, 854, 108, 120, 132, 140, 148, 174, 178, 180, 262, 818,
                    226, 232, 231, 266, 270, 288, 324, 624, 384, 404, 426, 430, 434, 450,
                    454, 466, 478, 480, 504, 508, 516, 562, 566, 646, 678, 686, 690, 694,
                    706, 710, 728, 729, 748, 834, 768, 788, 800, 894, 716],
    'translate'   : {x: 1, y: .9}
  },
  'as' : {
    'name' : 'Asia',
    'geometries'  : [4, 48, 50, 64, 96, 116, 104, 156, 626, 86, 360, 364, 368, 376, 392, 400,
                    398, 408, 410, 414, 417, 418, 422, 458, 462, 496, 524, 512, 586, 608,
                    634, 643, 682, 702, 144, 760, 762, 764, 792, 795, 784, 860, 704, 887],
    'translate'   : {x: 1.5, y: 1}
  },
  'eu' : {
    'name' : 'Europe',
    'geometries'  : [8, 20, 51, 40, 31, 112, 56, 70, 100, 191, 196, 203, 208, 233, 246, 250,
                    268, 276, 300, 348, 352, 372, 380, 428, 438, 440, 442, 807, 470, 498, 492,
                    499, 528, 578, 616, 620, 642, 674, 688, 703, 705, 724, 752, 756, 804, 826,
                    336, 304, 352],
    'translate'   : {x: 1, y: 1}
  },
  'na' : {
    'name' : 'North America',
    'geometries'  : [28, 44, 52, 84, 124, 188, 192, 212, 214, 222, 308, 320, 332, 340, 388, 484,
                    558, 591, 659, 662, 670, 780, 840],
    'translate'   : {x: .5, y: 1.5}
  },
  'oc' : {
    'name' : 'Oceania',
    'geometries'  : [36, 242, 296, 584, 583, 520, 554, 585, 598, 882, 90, 776, 548],
    'translate'   : {x: 1.6, y: 1}
  },
  'sa' : {
    'name' : 'South America',
    'geometries'  : [32, 68, 76, 152, 170, 218, 328, 600, 604, 740, 858, 862],
    'translate'   : {x: 1.1, y: .9}
  }
}


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

  // add regions
  for (var r in regions) {
    g.append('path')
    .datum(topojson.merge(world, world.objects.countries.geometries.filter( function(d, i) { return d3.set(regions[r].geometries).has(d.id); })))
    .attr('class', 'region')
    .attr('id', r)
    .attr('d', path)
    .on("click", clicked)
    .on("mouseover", highlight)
    .on("mouseout", deHighlight);
  }

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
  var scale = 60; // multiplier for bubbles size curve
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
    var region = g.select('#' + d.location.replace(/\s+/g, '-')).datum();
    var b = path.bounds(region),
    x = (b[0][0] + b[1][0]) / 2,
    y = (b[0][1] + b[1][1]) / 2;

    // manual adjustments
    // (i.e. some of the bounding boxes don't make visual sense, so just
    // adjust those manually)
      console.log(d.location);
      console.log(regions);
    if (d.location in regions) {
      x *= regions[d.location].translate.x;
      y *= regions[d.location].translate.y;
    }
    // if (d.location === 'northAmerica') {
    //   x *= .5;
    //   y *= 1.5;
    // } else if (d.location === 'euCentralAsia') {
    //   x *= 1.35;
    //   y *= 1.5;
    // } else if (d.location === 'eastAsia') {
    //   x *= 1.6;
    //   y *= .9;
    // } else if (d.location === 'latinAmerica') {
    //   x *= 1.2;
    //   y *= .95;
    // } else if (d.location === 'westEurope') {
    //   x *= .95;
    //   y *= .95;
    // } else if (d.location === 'subSaharanAfrica') {
    //   x *= 1.05;
    //   y *= .9;
    // } else if (d.location === 'midEastNorthAfrica') {
    //   x *= 1.05;
    //   y *= .9;
    // }

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
    var scale = 3; // multiplier for shade curve
    var c = counts[d.location.replace(/\s+/g, '-')].count;
    var v = (Math.log(c + 1)/Math.log(base))*scale/max;
    v = v > 1 ? 1 : v;

    return d3.rgb.apply(null, shade([0, 138, 179], v));
  })
  .attr('id', function(d, i) {
    return '_bubble_' + d.location.replace(/\s+/g, '-');
  })
  .on("click", clicked)
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
  .on("click", clicked)
  .on("mouseover", highlight)
  .on("mouseout", deHighlight);

  // no one needs you antarctica
  g.select('#Antarctica').remove();
}

// this allows us to process multiple data sources in a single function using d3, e.g. instead of just d3.json()
queue()
.defer(d3.json, 'static/js/world.json')
.defer(d3.json, 'static/js/studies.json')
.defer(d3.tsv, 'static/js/world-country-names.tsv')
.await(ready);

function highlight(d) {
  var region = this.id.replace(/_bubble_|_text_/, '');
  var bubble = this.id.replace(/^(?!_bubble_|_text_)|_text_/, '_bubble_');
  d3.selectAll('.node').classed('fade', true);
  d3.select('.map-caption').text(regions[region].name);
  d3.select('.map-caption').classed('default', false);
  d3.select('#' + region).classed('active', true);
  d3.select('#' + bubble).classed('active', true);
  zoomBubble('#' + bubble, 1.4);
  // console.log('in', this.id); // debug
}

function deHighlight(d) {
  var region = '#' + this.id.replace(/_bubble_|_text_/, '');
  var bubble = '#' + this.id.replace(/^(?!_bubble_|_text_)|_text_/, '_bubble_');
  d3.selectAll('.node').classed('fade', false);
  d3.select('.map-caption').text('Select a Region');
  d3.select('.map-caption').classed('default', true);
  d3.select(region).classed('active', false);
  d3.select(bubble).classed('active', false);
  zoomBubble(bubble, -1);
  // console.log('out', this.id); // debug
}

var intervals = {};
function zoomBubble(elem, zoom) {
  if (d3.select(elem)[0][0] === null) { return -1; }

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
  var region = this.id.replace(/_bubble_|_text_/, '');
  d3.selectAll('.region').classed('selected', false);
  d3.select('#' + region).classed('selected', true);
  filterBy ('region-' + region);
}

}
