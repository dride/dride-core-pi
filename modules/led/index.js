var exec = require('child_process').exec;

module.exports = {
	welcome: function() {
		exec('sudo ./bin/test');
	},
	error: function() {
		exec('sudo ./bin/test');
	},
	isPaired: function() {
		exec('sudo ./bin/test');
	}
};
