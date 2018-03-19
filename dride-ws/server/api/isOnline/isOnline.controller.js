'use strict';
var fs = require('fs');

// return 1 to indicate device is connected.
exports.index = function(req, res) {
	res.json({ status: 1 });
};
