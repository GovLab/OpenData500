// Map I : World map with color coded bubbles based on categories

var width = 960,
height = 500,
active = d3.select(null);

// var projection = d3.geo.albersUsa()
var projection = d3.geo.mercator()
// var projection = d3.geo.kavrayskiy7()
// var projection = d3.geo.equirectangular()
.scale(150)
.translate([width / 2, height / 1.5]);

var path = d3.geo.path()
.projection(projection);

var svg = d3.select('.b-pack-map').append('svg')
.attr('width', width)
.attr('height', height);

svg.append('rect')
.attr('class', 'background')
.attr('width', width)
.attr('height', height)
.on('click', reset);

var g = svg.append('g')
.style('stroke-width', '1.5px');


// d3.json('/js/us.json', function(error, us) {
//   if (error) throw error;

//   g.selectAll('path')
//       .data(topojson.feature(us, us.objects.states).features)
//     .enter().append('path')
//       .attr('d', path)
//       .attr('class', 'feature')
//       .on('click', clicked);

//   g.append('path')
//       .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a !== b; }))
//       .attr('class', 'mesh')
//       .attr('d', path);
// });

function shade(rgb, v) {
  for (var i in rgb) { rgb[i] = rgb[i]*v > 255 ? 255 : rgb[i]*v; }
    return rgb;
}

queue()
.defer(d3.json, 'js/world.json')
.defer(d3.json, 'js/studies2.json')
.defer(d3.tsv, 'js/world-country-names.tsv')
.await(ready);

function ready(error, world, studies, names) {
  if (error) throw error;


  // get country names
  var countries = topojson.feature(world, world.objects.countries).features;
  countries = countries.filter(function(d) {
    return names.some(function(n) {
      if (d.id == n.id) return d.name = n.name;
    });
  }).sort(function(a, b) {
    return a.name.localeCompare(b.name);
  });

  // draw map
  g.selectAll('path')
  .data(countries)
  .enter().append('path')
  .attr('d', path)
  .attr('class', 'feature')
  .attr('id', function(d, i) { return countries[i].name.replace(' ', '-'); })
  .on('click', clicked);

  // g.append('path')
  // .datum(topojson.mesh(world, world.objects.countries, function(a, b) { return a !== b; }))
  // .attr('class', 'mesh')
  // .attr('d', path);

  // draw bubbles
  var s = studies.children;
  var counts = {};

  for (var i in s) {
    var loc = s[i].location.replace(' ', '-');
    if (!(s[i].impact in counts)) {
      counts[s[i].impact] = {};
    }
    if (loc in counts[s[i].impact]) {
      counts[s[i].impact][loc]['count']++;
      if (counts[s[i].impact][loc]['count'] > 1) {
        studies.children[i].duplicate = true;
      }
    } else {
      counts[s[i].impact][loc] = {'count' : 1, 'dup' : 0};
    }
  }

  // console.log(s);

  var diameter = 120; // diameter of container circles to pack bubbles into
  var base = 4; // log base for bubbles size curve
  var scale = 80; // multiplier for bubbles size curve

  for (var i in studies.children) {
    var l = s[i].location.replace(' ', '-');
    studies.children[i].size = (Math.log(counts[s[i].impact][l]['count'] + 1)/Math.log(base))*scale;
  }

  var pack = d3.layout.pack()
  .size([diameter, diameter])
  .value(function(d) {
    return d.size;
  });

  var dup = 0;

  var node = svg.selectAll('svg')
  .data(pack(studies).filter(function(d) { return !d.children && !d.duplicate; }))
  .enter().append('g')
  .attr('class', function(d, i) {
    // var l = d.location.replace(' ', '-');
    // if (counts[d.impact][l]['dup']) { counts[d.impact][l]['dup']--; return 'remove'; }
    return 'node';
  })
  .attr('transform', function(d, i) {
    console.log (g.select('#' + d.location.replace(' ', '-')).datum());
    var country = g.select('#' + d.location.replace(' ', '-')).datum();
    var b = path.bounds(country),
    x = (b[0][0] + b[1][0]) / 2,
    y = (b[0][1] + b[1][1]) / 2;
    if (d.location === 'United States') {
      // Translate the coords manually for USA
      // This is a workaround to deal with the fact that the bounding box of
      // USA expands to the entire width of the map due to Alaska's islands
      x = x/2.15;
      y = y*1.25;
    }

    x = (d.x-diameter/2)+x;
    y = (d.y-diameter/2)+y;

    return 'translate(' + x + ',' + y + ')';
  });

  node.append('title')
  .text(function(d) { return d.title; });

  node.append('circle')
  .attr('r', function(d) {
    return d.size/2;
  })
  .style('fill', function(d) {
    var countsarr = [];
    for (var i in counts[d.impact]) { countsarr.push(counts[d.impact][i]['count']); }
      var max = Math.max.apply(null, countsarr);
    var lighten = 1.8;
    var c = counts[d.impact][d.location.replace(' ', '-')]['count']*lighten;
    var s = (c > max ? max : c)/max;
    // var s = 1;
    var blue = [0, 138, 179];
    var orange = [238, 91, 67];
    var yellow = [194, 195, 59];
    var fuchsia = [173, 0, 84];
    if (d.impact === 'government') {
      return d3.rgb.apply(null, shade(blue, s));
    } else if (d.impact === 'citizens') {
      return d3.rgb.apply(null, shade(orange, s));
    } else if (d.impact === 'opportunity') {
      return d3.rgb.apply(null, shade(yellow, s));
    } else if (d.impact === 'problems') {
      return d3.rgb.apply(null, shade(fuchsia, s));
    }
    return d3.rgb(128, 128, 128);
  });

  node.append('text')
  .attr('dy', '.3em')
  .style('text-anchor', 'middle')
  .text(function(d) { return counts[d.impact][d.location.replace(' ', '-')]['count']; });


  g.select('#Antarctica').remove();
}

function clicked(d) {
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

  // g.transition()
  //     .duration(750)
  //     .style('stroke-width', 1.5 / scale + 'px');
  //     .attr('transform', 'translate(' + translate + ')scale(' + scale + ')');
    }

    function reset() {
      active.classed('active', false);
      active = d3.select(null);

      g.transition()
      .duration(750)
      .style('stroke-width', '1.5px')
      .attr('transform', '');
    }
