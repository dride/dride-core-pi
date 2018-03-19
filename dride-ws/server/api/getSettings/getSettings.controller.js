'use strict';

// Return the settings object from /config.json in JSON format

var path = require('path');
var fs = require('fs');
var fileNames = [];

// Get list of getPOLists
exports.index = function(req, res) {
	var defaults = path.join(__dirname, '../../../..', 'config.json');
	var config = JSON.parse(fs.readFileSync(defaults, 'utf-8'));

	res.json(config);
};
