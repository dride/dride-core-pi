('use strict');

var path = require('path');
var validator = require('validator');
var execSync = require('child_process').execSync;

// will set live mode on or off
exports.index = function(req, res) {
	var mode = req.param('mode');

	if (mode == 1) {
		//stop record
		execSync('sudo systemctl stop record');
		//start record
		execSync('sudo systemctl start live');
	} else {
		//stop livestream
		execSync('sudo systemctl stop live');
		//start record
		execSync('sudo systemctl start record');
	}

	res.json({
		data: 1
	});
};
