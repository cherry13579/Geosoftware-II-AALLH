mapboxgl.accessToken = 'pk.eyJ1IjoiY2hlcnJ5MTM1OSIsImEiOiJjam81bTRsbjIwOHZwM3ZvMWxoaXIzNzgxIn0.S75v2qYbBXUTvqIqXFQLfg';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/outdoors-v10',
    zoom: 4,
    center: [7.6261347, 51.9606649],
    attributionControl: false
});
map.addControl(new mapboxgl.AttributionControl(), 'top-left');

map.addControl(new MapboxGeocoder({
    accessToken: mapboxgl.accessToken
}));


map.on('load', function () {
    map.addSource('dem', {
        "type": "raster-dem",
        "url": "mapbox://mapbox.terrain-rgb"
    });
    map.addLayer({
        "id": "hillshading",
        "source": "dem",
        "type": "hillshade"
    }, 'waterway-river-canal-shadow');
});

map.addControl(new mapboxgl.GeolocateControl({
    positionOptions: {
        enableHighAccuracy: true
    },
    trackUserLocation: true
}));

map.on('click', function (e) {
    document.getElementById('info').innerHTML =
        // e.point is the x, y coordinates of the mousemove event relative
        // to the top-left corner of the map
        JSON.stringify(e.point) + '<br />' +
        // e.lngLat is the longitude, latitude geographical position of the event
        JSON.stringify(map.getBounds());
});

$(document).ready(function () {
    $("#bounds").click(function () {
        $("#resultDiv").hide();
        $("#info").text(JSON.stringify(map.getBounds()));
        sendToFlask(JSON.stringify(map.getBounds()));
    });
});

function sendToFlask(bbox) {
    $.ajax({
        type: 'POST',
        data: {
            'boundingbox': bbox
        },
        url: "/getCoordinates",
        success: function (data) {
            map.removeLayer('main');
            table = JSON.parse(data).table;
            bboxen = JSON.parse(data).bboxen;
            if (bboxen != null) {
                displayBboxen(bboxen);
            }

            $("#resultTable").html(table);
            $("#resultDiv").show();

            $([document.documentElement, document.body]).animate({
                scrollTop: $("#resultTable").offset().top
            }, 1000);
        },
        error: function (xhr) {
            console.log(xhr)
        }
    });
}

$(document).ajaxStart(function () {
    $("#overlay").show();
});

$(document).ajaxStop(function () {
    $("#overlay").hide();
});

$(document).ready(function () {
    $("#toBottom").click(function () {
        $([document.documentElement, document.body]).animate({
            scrollTop: $("#resultTable").offset().top
        }, 1000);
    });
});

$(document).ready(function () {
    $("#toTop").click(function () {
        $([document.documentElement, document.body]).animate({
            scrollTop: $("#bounds").offset().top
        }, 1000);
    });
});


function displayBboxen(listOfJsonBboxes) {
    listOfJsonBboxes.forEach(element => {
        let geoJson = {
            "type" : "FeatureCollection",
            "features" : [element]
        }

        console.log(geoJson)

        map.addSource("bbox", {
            type: "geojson",
            data: geoJson,
        })

        map.addLayer({
            id: 'main',
            type: 'fill',
            source: 'bbox',
            layout: {},
            paint: {
                'fill-color': getRandomColor(),
                'fill-opacity': 0.3
            }
        })

    });
}

function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }