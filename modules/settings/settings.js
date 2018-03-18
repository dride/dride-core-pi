var fs = require('fs');
const path = require('path');

var getSettings = () => {
	var config = fs.readFileSync(path.join(__dirname, '../../config.json'), 'utf-8');
	//recover from lost or currpoted config file
	if (!config) {
		var backupConfig = fs.readFileSync(path.join(__dirname, '../../config.backup'), 'utf-8');
		fs.writeFileSync(path.join(__dirname, '../../config.json'), backupConfig);
		config = backupConfig;
	}

	return JSON.parse(config).settings;
};

module.exports = {
	getSettings: getSettings
};
