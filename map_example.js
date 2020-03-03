$(document).ready(function () {
    var OpenStreetMapProvider = window.GeoSearch.OpenStreetMapProvider;
    var DateTime = luxon.DateTime;
    var user_time = DateTime.local().setZone('America/Los_Angeles');
    var user_hour = user_time.hour;

        var loading = false;
        var new_max = false;
        var delay;
        var new_heatmap;
        var update_cache;
        var map_611ae1ea252342b3a610c004d09e0358;
        var max_south;
        var max_north;
        var max_west;
        var max_east;
        var current_cache;
        var current_bounds;
    var tile_layer_12702c5d484544a1afd7a770e13e3699;
    var heat_map_9742ec1740444fea95c7fa38271f2180;
    var address_input;
    var first_render = true;
    var validsearch;




        $("#searchform__submitbutton").click(search);

        function search() {
            address_input = $("#search_input").val();

            // import
            // import { OpenStreetMapProvider } from 'leaflet-geosearch';

            // setup
            const provider = new OpenStreetMapProvider();

            // search
            provider.search({ query: address_input }).then(function(result) {
                // address_input = result;
                // result = JSON.parse(result);
                result = result[0];
                result.x = parseFloat(result.x);
                result.y = parseFloat(result.y);
                render_search(result);
            })
        }

        function render_search(result) {
            if(result.y >= 33.7030139 && result.y <= 34.7478410 && result.x <= -117.6972698 && result.x >= -118.9409686) {
                validsearch = true;
            } else {
                validsearch = false;
                $("#searchform__error").innerHTML = "Error finding address / address out of range"
                return;
            }

            if(validsearch === true){

                if(first_render === true) {
                    first_render = false;
                    $("#map_611ae1ea252342b3a610c004d09e0358").fadeIn();
                    $("#splash__toggle").fadeOut();

                    map_611ae1ea252342b3a610c004d09e0358 = L.map(
                        "map_611ae1ea252342b3a610c004d09e0358",
                        {
                            crs: L.CRS.EPSG3857,
                            zoom: 18,
                            zoomControl: true,
                            preferCanvas: false,
                            // maxBounds: [[34.03336110903858, -118.24038889069691], [34.05336110903858, -118.26038889069691]],
                        }
                    ).setView([result.y, result.x], 14);


                    tile_layer_12702c5d484544a1afd7a770e13e3699 = L.tileLayer(
                        "https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png",
                        {
                            "attribution": "\u0026copy; \u003ca href=\"http://www.openstreetmap.org/copyright\"\u003eOpenStreetMap\u003c/a\u003e contributors \u0026copy; \u003ca href=\"http://cartodb.com/attributions\"\u003eCartoDB\u003c/a\u003e, CartoDB \u003ca href =\"http://cartodb.com/attributions\"\u003eattributions\u003c/a\u003e",
                            "detectRetina": false,
                            "maxNativeZoom": 18,
                            "maxZoom": 18,
                            "minZoom": 0,
                            "noWrap": false,
                            "opacity": 1,
                            "subdomains": "abc",
                            "tms": false
                        }
                    ).addTo(map_611ae1ea252342b3a610c004d09e0358);

                    var latlngs = [];
                    heat_map_9742ec1740444fea95c7fa38271f2180 = L.heatLayer(
                        latlngs,
                        {"blur": 18, "max": 1.0, "maxOpacity": 0.8, "maxZoom": 18, "minOpacity": 0.2, "radius": 10}
                    ).addTo(map_611ae1ea252342b3a610c004d09e0358);
                }
                else {
                    map_611ae1ea252342b3a610c004d09e0358.setView([result.y, result.x], 14);

                }
                    current_bounds = map_611ae1ea252342b3a610c004d09e0358.getBounds();
                user_time = DateTime.local().setZone('America/Los_Angeles');
                user_hour = user_time.hour;
                    $.ajax({
                        data : JSON.stringify({latlng: current_bounds, time: user_hour}),
                        type : 'POST',
                        dataType: "json",
                        url : '/search',
                        success: function (data) {

                            var latlongs = data.latlongs;
                            // latlongs.forEach(function(entry) {
                            //     heat_map_9742ec1740444fea95c7fa38271f2180.addLatLng(entry);
                            // });
                            heat_map_9742ec1740444fea95c7fa38271f2180.setLatLngs(data.latlongs);
                            current_cache = current_bounds;
                        }});

                    current_cache = map_611ae1ea252342b3a610c004d09e0358.getBounds();
                    max_north = current_cache._northEast.lat;
                    max_south = current_cache._southWest.lat;
                    max_east = current_cache._northEast.lng;
                    max_west = current_cache._southWest.lng;

// map_611ae1ea252342b3a610c004d09e0358.maxBounds([[34.034367839694845, -118.23953329151861], [34.05239832548047, -118.23958491234966]]);
                    map_611ae1ea252342b3a610c004d09e0358.on('moveend', mapdelay);
                }


        }


    function mapdelay() {
        clearTimeout(delay);
        delay = setTimeout(maprefresh, 1000);
    }
        function maprefresh( event ) {
            current_bounds = map_611ae1ea252342b3a610c004d09e0358.getBounds();
            if(current_bounds._southWest.lat < max_south) {
                max_south = current_bounds._southWest.lat;
                new_max = true;
            }
            if(current_bounds._southWest.lng < max_west) {
                max_west = current_bounds._southWest.lng;
                new_max = true;
            }
            if(current_bounds._northEast.lat > max_north) {
                max_north = current_bounds._northEast.lat;
                new_max = true;
            }
            if(current_bounds._northEast.lng > max_east) {
                max_east = current_bounds._northEast.lng;
                new_max = true;
            }
            if(loading === false && new_max === true) {
                loading = true;
                new_max = false;
                var northeast = L.latLng(max_north, max_east);
                var southwest = L.latLng(max_south, max_west);
                // current_cache = {"_southWest":{"lat":33.60546961227188,"lng":-121.85485839843751},"_northEast":{"lat":34.492975402501536}
                user_time = DateTime.local().setZone('America/Los_Angeles');
                user_hour = user_time.hour;
                //Put in override here if condition for selecting a time instead

                update_cache = L.latLngBounds(northeast, southwest);
                // console.log(JSON.stringify(current_bounds));
                $.ajax({
                    data : JSON.stringify({latlng: current_bounds, cache: current_cache, time: user_hour}),
                    type : 'POST',
                    dataType: "json",
                    url : '/map',
                    success: function (data) {
                        // new_heatmap = JSON.parse(data);
                        // new_heatmap = data;
                        var latlongs = data.latlongs;
                        latlongs.forEach(function(entry) {
                            heat_map_9742ec1740444fea95c7fa38271f2180.addLatLng(entry);
                        });
                        //heat_map_9742ec1740444fea95c7fa38271f2180.setLatLngs(data.latlongs);
                        current_cache = update_cache;
                        loading = false;
                    }
                })
            }
            // console.log(map_611ae1ea252342b3a610c004d09e0358.getBounds());

                // .done(function (data) {
                //     // new_heatmap = JSON.parse(data);
                //     console.log(data);
                //     new_heatmap = data;
                //     heat_map_9742ec1740444fea95c7fa38271f2180.setLatLngs(new_heatmap.latlongs);
                // });
            // event.preventDefault();
        }
});
