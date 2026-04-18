 
function sendData() {
            var value = document.getElementById('input').value;
            $.ajax({
                url: '/form',
                type: 'POST',
                data: { 'data': value },
                success: function(response) {
                    var map = L.map('map').setView([response.lo, response.la], 13);
              L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                  maxZoom: 19,
                  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
              }).addTo(map);

                },
                error: function(error) {
                    console.log(error);
                }
            });
        }

