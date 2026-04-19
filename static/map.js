
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
function getTemp(i, tempByIndex) {
  if (tempByIndex[i] !== undefined) return tempByIndex[i];

  // fallback: search backward
  for (let j = i; j >= 0; j--) {
    if (tempByIndex[j] !== undefined) return tempByIndex[j];
  }

  // fallback forward
  for (let j = i; j < 10000; j++) {
    if (tempByIndex[j] !== undefined) return tempByIndex[j];
  }

  return 0; // final fallback
}
function sendData() {
  var addy1 = document.getElementById('addy1').value;
  var addy2 = document.getElementById('addy2').value;
  console.log("sending post request")
  $.ajax({
                url: '/form',
                type: 'POST',
                data: { 'addy1': addy1,
                        'addy2': addy2
                        },
                success: function(response) {
                  L.marker(response[0]).addTo(map)
                  L.marker(response[1]).addTo(map)
                  var coords = response[2];
                  console.log(coords)
                  var temp_time_dict = response[3];

                  const indexes = Object.keys(temp_time_dict)
                    .map(Number)
                    .sort((a, b) => a - b);
                  const overview= {};
                  Object.keys(temp_time_dict).forEach(k => {
                    const entry = Object.values(temp_time_dict[k])[0];
                      overview[Number(k)] = [entry.temperature, entry.windSpeed, entry.shortForecast];
                 });

                  const tempByIndex = {};
                  console.log(overview)
                  const temp=overview[Object.keys(overview)[0]][0]
                  const windSpeed= overview[Object.keys(overview)[0]][1]

                  const shortForecast= overview[Object.keys(overview)[0]][2]
                  document.getElementById("startw").textContent= "Temperature is " + temp+ "F, with wind speed "+ windSpeed+ ", and " +shortForecast+ " forecast";

                  Object.keys(temp_time_dict).forEach(k => {
                    const entry = Object.values(temp_time_dict[k])[0];
                      tempByIndex[Number(k)] = entry.temperature;
                 });
                  const temps = Object.values(temp_time_dict).map(obj => {
                      const entry = Object.values(obj)[0];
                      return entry.temperature;
                    });

                  const minTemp = Math.min(...temps);
                  const maxTemp = Math.max(...temps);
                  for (let i = 0; i < coords.length - 1; i++) {
                      const start = coords[i];
                      const end = coords[i + 1];

                      const temp = getTemp(i, tempByIndex)
                      console.log(temp)
                      console.log(start)

                      console.log(end)

                      const segment = [
                        [start[0], start[1]],
                        [end[0], end[1]]
                      ];

                      L.polyline(segment, {
                        color: getColor(temp),
                      }).addTo(map);
                    }

                  // for (let i = 0; i < indexes.length - 1; i++) {
                  //   const startIdx = indexes[i];
                  //   console.log(startIdx)
                  //   const endIdx = indexes[i + 1];
                  //
                  //   console.log(endIdx)
                  //   const start = coords[startIdx];
                  //   const end = coords[endIdx];
                  //   console.log(start)
                  //
                  //   console.log(end)
                  //
                  //   const temp = Object.values(temp_time_dict[startIdx])[0].temperature;
                  //
                  //   const segment = [
                  //     [start[0], start[1]],
                  //     [end[0], end[1]]
                  //   ];
                  //
                  //   L.polyline(segment, {
                  //     color: getColor(temp),
                  //   }).addTo(map);
                  // }
                  map.fitBounds([response[0], response[1]])
                },
                error: function(error) {
                    console.log(error);
                }
            });

}

function rgbToHex(r, g, b) {
  return "#" + [r, g, b]
    .map(x => x.toString(16).padStart(2, "0"))
    .join("");
}
function getColor(temp) {
  const min = 30;
  const max = 50;

  const t = Math.max(0, Math.min(1, (temp - min) / (max - min)));

  const r = Math.round(255 * t);
  const b = Math.round(255 * (1 - t));

  return `rgb(${r}, 100, ${b})`;
}
