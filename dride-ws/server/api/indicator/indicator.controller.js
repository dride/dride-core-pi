'use strict';

var path = require('path'),
	fs = require('fs'),
	in_array = require('in_array'),
	spawn = require('child_process').spawn;
var fileNames = [];

// control indicators
exports.index = function(req, res) {
	var availableActions = [
		'isWaiting',
		'isDownloading',
		'isPaired',
		'needToPair',
		'needToLogin',
		'uploadSuccessfully',
		'done'
	];
	var action = req.param('action');

	if (in_array(action, availableActions)) {
		var indicatorScriptPath = '/home/core/modules/indicators/python/states/standalone.py';
		if (fs.existsSync(indicatorScriptPath)) {
			spawn('python', [indicatorScriptPath, action]);
			res.json({
				status: '1'
			});
		} else {
			res.json({
				error: 'Indicator module is not available'
			});
		}
	} else {
		res.json({
			error: 'Unknown action'
		});
	}
};
