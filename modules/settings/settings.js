var fs = require('fs');

var getSettings = () => {
	var config = fs.readFileSync('/home/core/config.json', 'utf-8');
	//recover from lost or currpoted config file
	if (!config) {
		var backupConfig = fs.readFileSync('/home/core/config.json', 'utf-8');
		fs.writeFileSync('/home/core/config.json', backupConfig);
		config = backupConfig;
	}

	return JSON.parse(config).settings;
};

module.exports = {
	getSettings: getSettings
};
