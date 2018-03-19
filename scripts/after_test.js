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
//update config.json with latest verison
//read version form config.json
packageJson = JSON.parse(fs.readFileSync('./package.json', 'utf8'));

config = JSON.parse(fs.readFileSync('./config.json', 'utf8'));
config.version = packageJson.version;

fs.writeFileSync('./config.json', JSON.stringify(config));

//set backup config to state dir
fs.createReadStream('./config.json').pipe(fs.createWriteStream('./state/config.backup.json'));

//update state app.json
fs.writeFileSync('./state/app.json', JSON.stringify({ connected: false }));
