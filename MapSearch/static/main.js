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

var draw = new MapboxDraw({
    displayControlsDefault: false,
    controls: {
        polygon: true,
        trash: true
    }
});
map.addControl(draw);


map.on('draw.create', function() {
    console.log(draw.getAll());
});
// map.on('draw.delete', updateArea);
map.on('draw.update', function() {
    console.log(draw.getAll());
});



$(document).ready(function () {
    $("#bounds").click(function () {
        $("#resultDiv").hide();
        // $("#info").text(JSON.stringify(map.getBounds()));
        sendToFlask(JSON.stringify(map.getBounds()));
    });
});

$(document).ready(function () {
    $("#polygon").click(function () {
        $("#resultDiv").hide();
        // $("#info").text(JSON.stringify(map.getBounds()));
        sendToFlask(JSON.stringify(draw.getAll()));
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
            try {
                map.removeLayer('main');
                map.removeSource('main');
            } catch (error) {
                console.log("")
            }
            table = JSON.parse(data).table;
            bboxen = JSON.parse(data).bboxen;
            if (bboxen != null) {
                displayBboxen(bboxen);
            }

            $("#resultTable").html(table);
            $("#resultDiv").show();

            $([document.documentElement, document.body]).animate({
                scrollTop: $("#bounds").offset().top
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
        element.properties.color = getRandomColor();
    });

    let geoJsonData = {
        "type": "FeatureCollection",
        "features": listOfJsonBboxes
    }
    // console.log(geoJsonData);

    map.addLayer({
        id: 'main',
        type: 'fill',
        source: {
            type: 'geojson',
            data: geoJsonData,
        },
        layout: {},
        paint: {
            'fill-opacity': 0.4,
            'fill-color': ["get", "color"],
            'fill-outline-color': 'black',
        }
    });


    var popup = new mapboxgl.Popup({
        closeButton: false,
        closeOnClick: false
    });

    map.on('click', 'main', function (e) {
        popup.remove();
        popup.setLngLat(e.lngLat)
            .setHTML(e.features[0].properties.ID)
            .addTo(map);
    });

    // Change the cursor to a pointer when the mouse is over the states layer.
    map.on('mouseenter', 'main', function (e) {
        map.getCanvas().style.cursor = 'pointer';
    });

    // Change it back to a pointer when it leaves.
    map.on('mouseleave', 'main', function () {
        map.getCanvas().style.cursor = '';
        popup.remove();
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