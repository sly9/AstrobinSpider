function useRealLocation() {
    if (!navigator.geolocation) {
        console.log('your browser doesnt support geolocation, change it');
        return;
    }
    navigator.geolocation.getCurrentPosition((position) => {
        console.log(position.coords);
        latitudeWrapper.value = position.coords.latitude;
        longitudeWrapper.value = position.coords.longitude;
        Celestial.location([position.coords.latitude, position.coords.longitude])

    });
}

function updateLocation() {
    Celestial.location([parseFloat(latitudeWrapper.value), parseFloat(longitudeWrapper.value)])
}

// from target with 5+ counts , to the max. 100 numbers in it.
let percentiles = [5];

function calculatePercentiles() {
    let counts = Object.values(topTargets).map(t => t.count).filter(t => { return t > 5 }).sort((x, y) => { return parseInt(x) - parseInt(y) });
    //for (let i = 0; i < 16; i++) {
    //    percentiles.push(counts[parseInt(counts.length * (i / 20))]);
    //}

    for (let i = 0; i < 100; i++) {
        percentiles.push(counts[parseInt(counts.length * (i / 100))]);
    }
}