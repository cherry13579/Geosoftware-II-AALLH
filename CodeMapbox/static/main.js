mapboxgl.accessToken = 'pk.eyJ1IjoiY2hlcnJ5MTM1OSIsImEiOiJjam81bTRsbjIwOHZwM3ZvMWxoaXIzNzgxIn0.S75v2qYbBXUTvqIqXFQLfg';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/outdoors-v10',
    zoom: 4,
    center: [7.6261347, 51.9606649]
});

map.on('load', function () {
    map.addSource('dem', {
        "type": "raster-dem",
        "url": "mapbox://mapbox.terrain-rgb"
    });
    map.addLayer({
        "id": "hillshading",
        "source": "dem",
        "type": "hillshade"
        // insert below waterway-river-canal-shadow;
        // where hillshading sits in the Mapbox Outdoors style
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


// function sendToFlask(bbox) {
//     $.post( "/getCoordinates", {
//         'boundingbox': bbox 
//     });
// }

function sendToFlask(bbox) {
    $.ajax({
        type: 'POST',
        data: {
            'boundingbox': bbox
        },
        url: "/getCoordinates",
        success: function (data) {
            table = JSON.parse(data).table
            console.log(table)
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