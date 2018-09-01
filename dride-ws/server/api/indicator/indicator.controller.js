'use strict';

var in_array = require('in_array');
var led = require('../../../../modules/led/index');

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
