'use strict';

var path = require('path'),
	fs = require('fs'),
	in_array = require('in_array'),
	spawn = require('child_process').spawn;
var led = require('../../../../modules/led/index');

var fileNames = [];

// control indicators
exports.index = function(req, res) {
	var availableActions = ['isPaired', 'pending', 'welcome'];
	var action = req.param('action');

	if (in_array(action, availableActions)) {
		led[action]();
		res.json({
			status: '1'
		});
	} else {
		res.json({
			error: 'Unknown action'
		});
	}
};
