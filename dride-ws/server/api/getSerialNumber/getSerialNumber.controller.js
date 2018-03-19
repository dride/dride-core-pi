'use strict';

var exec = require('child_process').exec;

// Get list of getSerialNumbers
exports.index = function(req, res) {
	var cmd = "cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2";

	exec(cmd, function(error, stdout, stderr) {
		// command output is in stdout
		res.json({ serial: stdout.replace(/(\n|\r)+$/, '') });
	});
};
