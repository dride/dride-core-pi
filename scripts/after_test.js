var fs = require('fs');
var path = require('path');

//set state to false
var state = path.join(__dirname, '../state/app.json');
fs.writeFileSync(
	state,
	JSON.stringify({
		connected: false
	})
);
