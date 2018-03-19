'use strict';

var path = require("path");

var fs = require('fs')
  


// return 1 to indicate device is connected.
exports.index = function(req, res) {

	var currentFrame = path.join(__dirname, '../../../../modules/settings', 'road.jpg');

    res.sendFile(currentFrame);

};
