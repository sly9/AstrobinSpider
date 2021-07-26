// image filename => image data
let images = {}
    // pyongc id => target details
let topTargets = {}

async function loadData() {
    const [imagesJSON, topTargetsJSON] = await Promise.all([
        fetch('images.json'),
        fetch('top_targets.json'),
    ]);
    images = await imagesJSON.json();
    topTargets = await topTargetsJSON.json();
    //console.log(images)
    //console.log(topTargets)

    drawMarker(100);

}

let currentTargets = [];

let currentTargetID = null;

function drawMarker(n) {
    currentTargets = moreFrequentThanXTimesTargets(n);
    console.log(currentTargets);
    var pointStyle = {
        stroke: "#f0f",
        width: 3,
        fill: "rgba(255, 204, 255, 0.4)"
    };

    var currentPointStyle = {
        stroke: "#f00",
        width: 5,
        fill: "rgba(255, 204, 255, 1)"
    };

    var textStyle = {
        fill: "#f0f",
        font: "bold 15px Helvetica, Arial, sans-serif",
        align: "left",
        baseline: "bottom"
    };
    Celestial.add({
        type: "raw",
        callback: function(error, json) {
            console.log('first callback');
            Celestial.redraw();
        },

        redraw: function() {

            var m = Celestial.metrics(), // Get the current map size in pixels
                // empty quadtree, will be used for proximity check
                quadtree = d3.geom.quadtree().extent([
                    [-1, -1],
                    [m.width + 1, m.height + 1]
                ])([]);

            Object.values(currentTargets).forEach(target => {
                // [RA, DEC] in degrees
                let coordinatesDegree = target.coordinates['radians coords'].map(x => x * 180 / Math.PI);


                if (Celestial.clip(coordinatesDegree)) {
                    // get point coordinates
                    var pt = Celestial.mapProjection(coordinatesDegree);
                    // object radius in pixel, could be varable depending on e.g. dimension or magnitude 

                    // Fake radius
                    //var r = Math.pow(20 - prop.mag, 0.7); // replace 20 with dimmest magnitude in the data
                    let r = Math.pow(Math.sqrt(target.astrobin_filenames.length), 0.7);

                    // draw on canvas
                    //  Set object styles fill color, line color & width etc.
                    if (target.id == currentTargetID) {
                        Celestial.setStyle(currentPointStyle);
                    } else {
                        Celestial.setStyle(pointStyle);
                    }


                    // Start the drawing path
                    Celestial.context.beginPath();
                    // Thats a circle in html5 canvas
                    Celestial.context.arc(pt[0], pt[1], r, 0, 2 * Math.PI);
                    // Finish the drawing path
                    Celestial.context.closePath();
                    // Draw a line along the path with the prevoiusly set stroke color and line width      
                    Celestial.context.stroke();
                    // Fill the object path with the prevoiusly set fill color
                    Celestial.context.fill();

                    // Set text styles       
                    Celestial.setTextStyle(textStyle);
                    // and draw text on canvas
                    //Celestial.context.fillText(target.name, pt[0] + r - 1, pt[1] - r + 1);
                }
            });
        }
    });

    Celestial.redraw();
}

function getClickPosition(e) {
    var map = document.getElementById('celestial-map');
    var x = e.offsetX;
    var y = e.offsetY;
    var inv = Celestial.mapProjection.invert([x, y]);
    if (inv === undefined || isNaN(inv[0]))
        return;

    let closestTarget = closestTargetAt(inv[0], inv[1]);
    console.log('clicking at: ', inv, closestTarget);
    selectTarget(closestTarget);
    // update slider show
}

function selectTarget(target) {
    if (!target) return;

    currentTargetID = target.id;

    updateInfo(target);
    updateSlider(target);
}

function updateInfo(target) {
    $('#name').text(target.name);
    $('#type').text(target.type);
    $('#ra').text(target.coordinates['right ascension']);
    $('#dec').text(target.coordinates.declination);

    let otherName = '';
    if (target['other identifiers']['common names']) otherName += target['other identifiers']['common names'] + ', ';
    if (target['other identifiers'].messier) otherName += target['other identifiers'].messier + ', ';
    $('#other_name').text(otherName)
}

function updateSlider(target) {
    let relatedImages = astroBinImagesByID(target.id);
    console.log(relatedImages);
    relatedImages.sort(() => Math.random() - 0.5)


    let sliderContainer = $('.slider')
    sliderContainer.empty();
    let html = ['<ul class="lightSlider" id="lightSlider">']

    let len = relatedImages.length > 20 ? 20 : relatedImages.length;
    for (let i = 0; i < len; i++) {
        let img = relatedImages[i];
        if (img.hash) {
            html.push(`<li data-thumb="${img.url_thumb}"><a target="_blank" href="https://astrobin.com/${img.hash}/"><img src="${img.url_regular}" /></a></li>`)
        } else {
            html.push(`<li data-thumb="${img.url_thumb}"><a target="_blank" href="https://astrobin.com/${img.id}/"><img src="${img.url_regular}" /></a></li>`)
        }
    }

    html.push('</ul>');
    sliderContainer.html(html.join(''));
    $('#lightSlider').lightSlider({
        gallery: true,
        item: 1,
        loop: true,
        slideMargin: 0,
        thumbItem: 9
    });

}


window.addEventListener('DOMContentLoaded', (event) => {
    console.log('DOM fully loaded and parsed');
    loadData();
    document.getElementById('celestial-map').addEventListener('click', getClickPosition, false);
    $('#lightSlider').lightSlider({
        gallery: true,
        item: 1,
        loop: true,
        slideMargin: 0,
        thumbItem: 9
    });
});

function astroBinImagesByID(id) {
    let targetDetails = topTargets[id];
    let filenames = targetDetails['astrobin_filenames'];
    return filenames.map(x => images[x]);
}

function moreFrequentThanXTimesTargets(x) {
    let result = {};
    Object.entries(topTargets).forEach(entry => {
        let value = entry[1];
        if (parseInt(value['count']) >= x) {
            result[entry[0]] = entry[1];
        }
    });
    return result;
}

function distance(ra0, dec0, ra1, dec1) {
    return Math.sqrt(Math.pow(ra0 - ra1, 2) + Math.pow(dec0 - dec1, 2));
}

function closestTargetAt(ra, dec) {
    if (ra < 0) ra = ra + 360;

    let answer = null;
    let bestDistance = Number.MAX_VALUE;
    for (let key in currentTargets) {
        let target = currentTargets[key];
        let coordinatesDegree = target.coordinates['radians coords'].map(x => x * 180 / Math.PI);
        let d = distance(ra, dec, coordinatesDegree[0], coordinatesDegree[1]);

        if (d < bestDistance) {
            bestDistance = d;
            answer = target;
        }
    }

    let answerCoords = answer.coordinates['radians coords'].map(x => x * 180 / Math.PI);

    if (bestDistance > 5) {
        //     console.log('The best answer I found is at: ', answer, answerCoords, ' but its too far', bestDistance);
        return null;
    } else {
        //       console.log('The best answer I found is: ', answer, answerCoords, ' pretty close: ', bestDistance);
    }
    currentTargetID = answer.id;
    Celestial.redraw();
    return answer;
}