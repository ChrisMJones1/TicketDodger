$(document).ready(function () {
    var DateTime = luxon.DateTime;
    var user_time = DateTime.local().setZone('America/Los_Angeles');
    var user_hour = user_time.hour;
    $("#time").html(user_time);

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
    
    var hide_risk = false;
    $("#risk-btn").on('click', risk_toggle);

    let searchParams = new URLSearchParams(window.location.search)
    $("#address").html(searchParams.get('placename'));
    var getresults = {
        y: searchParams.get('lat'),
        x: searchParams.get('long')
    }
    render_search(getresults);
    function render_search(result) {
        if(result.y >= 33.7030139 && result.y <= 34.7478410 && result.x <= -117.6972698 && result.x >= -118.9409686) {
            validsearch = true;
        } else {
            validsearch = false;
            $("#searchform__error").html("Whoops! This page is not a valid search, please return to the main page and try your Dodge again.");
            $("#error_display").show();
            return false;
        }

        if(validsearch === true){

            if(first_render === true) {
                first_render = false;

                map_611ae1ea252342b3a610c004d09e0358 = L.map(
                    "map_611ae1ea252342b3a610c004d09e0358",
                    {
                        crs: L.CRS.EPSG3857,
                        zoom: 18,
                        zoomControl: false,
                        preferCanvas: false,
                        // maxBounds: [[34.03336110903858, -118.24038889069691], [34.05336110903858, -118.26038889069691]],
                    }
                ).setView([result.y, result.x], 14);
                map_control = new L.Control.Zoom({ position: 'bottomright' }).addTo(map_611ae1ea252342b3a610c004d09e0358);
                L.marker([result.y, result.x]).addTo(map_611ae1ea252342b3a610c004d09e0358);


                // tile_layer_12702c5d484544a1afd7a770e13e3699 = L.tileLayer(
                //     "https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png",
                //     {
                //         "attribution": "\u0026copy; \u003ca href=\"http://www.openstreetmap.org/copyright\"\u003eOpenStreetMap\u003c/a\u003e contributors \u0026copy; \u003ca href=\"http://cartodb.com/attributions\"\u003eCartoDB\u003c/a\u003e, CartoDB \u003ca href =\"http://cartodb.com/attributions\"\u003eattributions\u003c/a\u003e",
                //         "detectRetina": false,
                //         "maxNativeZoom": 18,
                //         "maxZoom": 18,
                //         "minZoom": 0,
                //         "noWrap": false,
                //         "opacity": 1,
                //         "subdomains": "abc",
                //         "tms": false
                //     }
                // ).addTo(map_611ae1ea252342b3a610c004d09e0358);

                tile_layer_1 = L.tileLayer(
                    "https://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.{ext}",
                    {
                        "attribution": "\u0026copy; \u003ca href=\"http://www.openstreetmap.org/copyright\"\u003eOpenStreetMap\u003c/a\u003e contributors \u0026copy; \u003ca href=\"http://cartodb.com/attributions\"\u003eCartoDB\u003c/a\u003e, CartoDB \u003ca href =\"http://cartodb.com/attributions\"\u003eattributions\u003c/a\u003e",
                        "detectRetina": false,
                        "maxNativeZoom": 18,
                        "maxZoom": 18,
                        "minZoom": 0,
                        "noWrap": false,
                        "opacity": 1,
                        "subdomains": "abc",
                        "tms": false,
                        ext: 'jpg'
                    }
                ).addTo(map_611ae1ea252342b3a610c004d09e0358);
                tile_layer_2 = L.tileLayer(
                    "https://{s}.basemaps.cartocdn.com/light_only_labels/{z}/{x}/{y}{r}.png",
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

            if($("#time_choice").val() !== 'current')
            {
                user_hour = $("#time_choice").val();
            }

            $('#theme').on('change', theme_change);
            $.ajax({
                data : JSON.stringify({latlng: current_bounds, time: user_hour, centralpoint: result}),
                type : 'POST',
                dataType: "json",
                url : 'https://ticketdodger.herokuapp.com/search',
                success: function (data) {

                    var latlongs = data.latlongs;
                    // latlongs.forEach(function(entry) {
                    //     heat_map_9742ec1740444fea95c7fa38271f2180.addLatLng(entry);
                    // });
                    heat_map_9742ec1740444fea95c7fa38271f2180.setLatLngs(data.latlongs);
                    let risklevel = "There were " + data.count + " tickets given out <br> in this area at this time of day";
                    let risk_suggestion = "You will likely not get a ticket";
                    if(data.count >= 500)
                    {
                        // risklevel = "high";
                        risk_suggestion = "You will get a ticket, park elsewhere";
                    }
                    else if(data.count >= 100)
                    {
                        // risklevel = "medium";
                        risk_suggestion = "You will probably get a ticket, consider parking elsewhere";
                    }
                    else if(data.count >= 10)
                    {
                        // risklevel = "low";
                        risk_suggestion = "The risk of getting a ticket here is low";
                    }
                    $("#level").html(risklevel);
                    $("#risk_suggestion").html(risk_suggestion);
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

    function theme_change()
    {
        switch (this.value) {
            case 'watercolor':
                tile_layer_1.setUrl('https://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.{ext}');
                tile_layer_2.setUrl('https://{s}.basemaps.cartocdn.com/light_only_labels/{z}/{x}/{y}{r}.png');
                break;

            case 'dark':
                tile_layer_1.setUrl('https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png');
                tile_layer_2.setUrl('');
                break;

            case 'light':
                tile_layer_1.setUrl('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
                tile_layer_2.setUrl('');
                break;
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

            if($("#time_choice").val() !== 'current')
            {
                user_hour = $("#time_choice").val();
            }


            //Put in override here if condition for selecting a time instead

            update_cache = L.latLngBounds(northeast, southwest);
            // console.log(JSON.stringify(current_bounds));
            $.ajax({
                data : JSON.stringify({latlng: current_bounds, cache: current_cache, time: user_hour}),
                type : 'POST',
                dataType: "json",
                url : 'https://ticketdodger.herokuapp.com/map',
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
    $('#time_choice').on('change', refresh_time);
    function refresh_time() {
        render_search(getresults);
    }
    function risk_toggle() {
        // let offset = $('#risk_container').width() - $('#btn-box').width();
        if(hide_risk === false)
        {
            $('#risk_container').animate({left: '-85vw', right: '85vw'}, 500, function() {$('#risk_container').clearQueue(); hide_risk = true;});
        }
        else
        {
            $('#risk_container').animate({left: '0', right: '0'}, 500, function() {$('#risk_container').clearQueue(); hide_risk = false;});
        }
        
    }
});
