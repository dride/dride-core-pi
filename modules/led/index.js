var execSync = require('child_process').execSync;

module.exports = {
	welcome: function() {
		execSync('sudo  ' + __dirname + '/bin/main welcome', {
			stdio: 'inherit'
		});
	},
	error: function() {
		execSync('sudo  ' + __dirname + '/bin/main error', {
			stdio: 'inherit'
		});
	},
	isPaired: function() {
		execSync('sudo  ' + __dirname + '/bin/main isPaired', {
			stdio: 'inherit'
		});
	},
	pending: function() {
		execSync('sudo  ' + __dirname + '/bin/main pending', {
			stdio: 'inherit'
		});
	}
};
