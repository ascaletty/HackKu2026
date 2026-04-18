
var map = L.map('map').setView([51.505, -0.09], 13);




L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map);

function sendData() {
  var addy1 = document.getElementById('addy1').value;
  var addy2 = document.getElementById('addy2').value;
  console.log("sending post request")
  $.ajax({
                url: '/form',
                type: 'POST',
                data: { 'addy1': addy1,
                        'addy2': addy2},
                success: function(response) {
                  L.marker(response[0]).addTo(map)
                  L.marker(response[1]).addTo(map)
                  console.log(response[2])
                  var polyline= L.polyline(response[2], {color: 'red'}).addTo(map);
                  map.fitBounds(polyline.getBounds());
                  // map.fitBounds([response[0], response[1]])

                },
                error: function(error) {
                    console.log(error);
                }
            });

}
