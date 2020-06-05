//  Map all points delivery


mapboxgl.accessToken = 'pk.eyJ1Ijoib2RpbGVsZWNsZXJjc2l0ZSIsImEiOiJjazZjMDJtNGEwZ3F2M2tvdnNncnkxNXRxIn0.c7i8XUNby5CQwhdrsG3r0A';
var map = new mapboxgl.Map({
    container: 'map-livraison',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [-1.249550, 44.651470], //longitude, latitude
    zoom: 11,
});


var geojson = {
    type: 'FeatureCollection',
    features: [{
        type: 'Feature',
        geometry: {
            type: 'Point',
            coordinates: [-1.2409519, 44.6750527,]
        },
        properties: {
            title: 'Location - Bateau',
            description: 'Livraison directement chez votre loueur de bateau'
        }
    },
    {
        type: 'Feature',
        geometry: {
            type: 'Point',
            coordinates: [-1.2461412, 44.6459416]
        },
        properties: {
            title: 'Parking Club de voile',
            description: 'Ecole de voile'
        }
    },
    {
        type: 'Feature',
        geometry: {
            type: 'Point',
            coordinates: [-1.238413, 44.6603032]
        },
        properties: {
            title: 'Plage des américains',
            description: 'Livraison bateau corps mort'
        }
    }
    ]
};

var geojson_apero = {
    type: 'FeatureCollection',
    features: [{
        type: 'Feature',
        geometry: {
            type: 'Point',
            coordinates: [-1.2427271, 44.6482281]
        },
        properties: {
            title: 'Apero',
            description: 'Corps mort'
        }
    }]
};





map.on('load', function () {
    map.addSource('maine', {
        'type': 'geojson',
        'data': {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [
                            [
                                [-1.2370777, 44.6604727],
                                [-1.238966, 44.6666385],
                                [-1.238966, 44.6679814],
                                [-1.2373352, 44.6680425],
                                [-1.2359619, 44.6637083],
                                [-1.2350178, 44.6610222],
                                [-1.2369061, 44.6605338]
                            ]
                        ]
                    }, properties: {
                        title: 'Plage des américains',
                        description: 'Livraison bateau corps mort'
                    }

                }, {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [
                            [
                                [-1.2370348, 44.6572675],
                                [-1.2371635, 44.6585344],
                                [-1.2360048, 44.6586717],
                                [-1.2356615, 44.6572981],
                                [-1.2370348, 44.6572675]
                            ]
                        ]
                    },
                    properties: {
                        title: 'Plage des américains',
                        description: 'Livraison bateau corps mort'
                    }

                },
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [
                            [
                                [-1.2291384, 44.696237],
                                [-1.2311983, 44.6933389],
                                [-1.2299538, 44.6927897],
                                [-1.2277222, 44.6956574],
                                [-1.2291384, 44.6961455]
                            ]
                        ]
                    },
                    properties: {
                        title: 'Plage des américains',
                        description: 'Livraison bateau corps mort'
                    }

                },
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [
                            [
                                [-1.2309837, 44.6896473],
                                [-1.2290955, 44.6889151],
                                [-1.2327862, 44.6837892],
                                [-1.2346745, 44.6838502],
                                [-1.2311554, 44.6895253]
                            ]
                        ]
                    },
                    properties: {
                        title: 'Plage des américains',
                        description: 'Livraison bateau corps mort'
                    }

                },
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [
                            [
                                [-1.2367344, 44.6786628],
                                [-1.2372494, 44.6754891],
                                [-1.2353611, 44.6750619],
                                [-1.2345028, 44.6778694],
                                [-1.2365627, 44.6786628],
                            ]
                        ]
                    },
                    properties: {
                        title: 'Plage des américains',
                        description: 'Livraison bateau corps mort'
                    }

                },

            ]



        },

    });

    map.addLayer({
        'id': 'maine',
        'type': 'fill',
        'source': 'maine',
        'layout': {},
        'paint': {
            'fill-color': 'green',
            'fill-opacity': 0.6
        }
    });

    map.addLayer({
        'id': 'zone5',
        'type': 'fill',
        'source': 'maine',
        'layout': {},
        'paint': {
            'fill-color': 'green',
            'fill-opacity': 0.6
        }
    });

    map.addLayer({
        'id': 'zone5a',
        'type': 'fill',
        'source': 'maine',
        'layout': {},
        'paint': {
            'fill-color': 'green',
            'fill-opacity': 0.6
        }
    });
    map.addLayer({
        'id': 'zone6',
        'type': 'fill',
        'source': 'maine',
        'layout': {},
        'paint': {
            'fill-color': 'green',
            'fill-opacity': 0.6
        }
    });
    map.addLayer({
        'id': 'zone7',
        'type': 'fill',
        'source': 'maine',
        'layout': {},
        'paint': {
            'fill-color': 'green',
            'fill-opacity': 0.6
        }
    });
});

map.on('click', 'Feature', function (e) {
    var coordinates = e.features[0].geometry.coordinates.slice();
    var description = e.features[0].properties.description;

    // Ensure that if the map is zoomed out such that multiple
    // copies of the feature are visible, the popup appears
    // over the copy being pointed to.
    while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
        coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
    }

    new mapboxgl.Popup()
        .setLngLat(coordinates)
        .setHTML(description)
        .addTo(map);
});

// add markers to map
geojson.features.forEach(function (marker) {

    // create a HTML element for each feature
    var el = document.createElement('div');
    el.className = 'marker';

    // make a marker for each feature and add to the map
    new mapboxgl.Marker(el)
        .setLngLat(marker.geometry.coordinates)
        .setPopup(new mapboxgl.Popup({ offset: 25 }) // add popups
            .setHTML('<h3>' + marker.properties.title + '</h3><p>' + marker.properties.description + '</p>'))
        .addTo(map);
});

geojson_apero.features.forEach(function (marker) {

    // create a HTML element for each feature
    var el = document.createElement('div');
    el.className = 'marker-apero';

    // make a marker for each feature and add to the map
    new mapboxgl.Marker(el)
        .setLngLat(marker.geometry.coordinates)
        .setPopup(new mapboxgl.Popup({ offset: 25 }) // add popups
            .setHTML('<h3>' + marker.properties.title + '</h3><p>' + marker.properties.description + '</p>'))
        .addTo(map);
});