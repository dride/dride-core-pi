'use strict';

// Return the settings object from /defaults.cfg in JSON format

var path = require("path"),
	fs = require('fs'),
   	ini = require('ini')


var config = require('../../config/environment');
var fileNames   = [];


// Get list of getPOLists
exports.index = function(req, res) {


	//TODO: Validate the input type's

	var CategoryName = req.param('CategoryName');
	var fieldName = req.param('fieldName');
	var fieldValue = req.param('fieldValue');

	var defaults = path.join(__dirname, '../../../..', 'defaults.cfg');
	var config = ini.parse(fs.readFileSync(defaults, 'utf-8'))
	  
	config[CategoryName][fieldName] = fieldValue;

	try {
	    fs.writeFileSync(defaults, ini.stringify(config));
	    res.json({ "status": "1", "reason": "setting was saved successfully!" });
	} catch (err) {
	    res.json({ "status": "0", "reason": err });
	}


};


