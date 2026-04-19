
var map = L.map('map').setView([51.505, -0.09], 13);




L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map);

const outputElem = document.querySelector("#output");

if (typeof HTMLGeolocationElement === "function") {
  const geo = document.querySelector("geolocation");
  geo.addEventListener("location", () => {
    if (geo.position) {
      map.setView([geo.position.coords.latitude, geo.position.coords.longitude])
      console.log(geo.position)
    } else if (geo.error) {
      outputElem.textContent += `${geo.error.message}, `;
      console.log("fail")
    }
  });
} else {
  const fallback = document.querySelector("#fallback");
  fallback.addEventListener("click", () => {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        map.setView([position.coords.latitude, position.coords.longitude])
        outputElem.textContent += `(${position.coords.latitude}, ${position.coords.longitude}), `;
      },
      (error) => {
        console.log(error)
        outputElem.textContent += `${error.message}, `;
      },
    );
  });
}

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

function getColor(temp) {
  const min = 0;
  const max = 100;

  const t = Math.max(0, Math.min(1, (temp - min) / (max - min)));

  const r = Math.round(255 * t);
  const b = Math.round(255 * (1 - t));

  return `rgb(${r}, 100, ${b})`;
}
