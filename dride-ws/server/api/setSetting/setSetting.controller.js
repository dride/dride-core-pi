'use strict';

// Return the settings object from /defaults.cfg in JSON format

var path = require("path");

var iniparser = require('iniparser');


var config = require('../../config/environment');
var fileNames   = [];

var fieldName = req.param('fieldName');
var fieldValue = req.param('fieldValue');

// Get list of getPOLists
exports.index = function(req, res) {

	var defaults = path.join(__dirname, '../../../..', 'defaults.cfg');
	iniparser.parse(defaults, function(err,data){
		
	    res.json(data);
	});

	   


};


