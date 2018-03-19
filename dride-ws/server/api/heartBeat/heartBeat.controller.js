'use strict';
var fs = require('fs');

// return 1 to indicate device is connected.
// mark state as app connected
exports.index = function(req, res) {
	var state = './state/app.json';
	fs.writeFileSync(
		state,
		JSON.stringify({
			connected: true,
			dte: new Date().getTime()
		}),
		err => {
			if (err) throw err;
		}
	);

	res.json({ status: 1 });
};
