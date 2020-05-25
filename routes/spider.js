const express = require('express');
const router = express.Router();
const Fetch = require("node-fetch");


// http://astrobin.com/api/v1/imageoftheday/?limit=20&api_key=aa2a70c0dd02cffeaa4e475eee1f4cbf6ef37cb6&api_secret=939d21c3c67dc7b4abd9ec69bc873f71bdb00242


/* GET home page. */
router.get('/', async function (req, res, next) {
    const response = await Fetch('http://astrobin.com/api/v1/imageoftheday/?limit=20&api_key=aa2a70c0dd02cffeaa4e475eee1f4cbf6ef37cb6&api_secret=939d21c3c67dc7b4abd9ec69bc873f71bdb00242&format=json');
    const json = await response.json();
    //res.write(`Parsed ${json['meta']['limit']} images. Click on the link for the next 20`);
    //res.end(json['meta']['next']);
    res.render('spider', json);
});

module.exports = router;
