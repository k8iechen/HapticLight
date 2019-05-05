const fs = require('fs');
const nitori = require('@google/maps').createClient({
  key: 'no stealerino key',
  Promise: Promise
});

function getRoute() {
  var orig = 'University of Waterloo';
  var dest = 'University of Toronto';
  var request = {
    origin: orig,
    destination: dest,
    alternatives: false,
    mode: 'walking',
    units: 'metric'
  };

  nitori.directions(request, function(err, data) {
    result = JSON.stringify(data.routes[0].legs[0].steps);
    console.log(result)
    fs.writeFile("./directions.json", result, (err) => console.error);
  });
}

getRoute();
