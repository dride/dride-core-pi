const fs = require('fs-extra');
var path = require('path');
var archiver = require('archiver');
var uploadHelper = require('./helpers/uploadZip');

const filterFunc = (src, dest) => {
	//dont copy node_modules
	if (src.indexOf('node_modules') > -1) {
		return false;
	}

	//dont copy tests
	if (src.indexOf('test') > -1) {
		return false;
	}
	//dont copy keys
	if (src.indexOf('keys') > -1) {
		return false;
	}
	//dont copy filename starting with a .
	if (
		!src
			.split('/')
			.pop()
			.split('.')[0]
	) {
		return false;
	}

	return true;
};
const fileName = 'dride_' + new Date().getTime();
fs.copy('../dride-core/', '/tmp/' + fileName, { filter: filterFunc }, err => {
	if (err) return console.error(err);

	//TODO: read version form config.json
	packageJson = JSON.parse(fs.readFileSync('./package.json', 'utf8'));
	var currentVersion = packageJson.version;

	var output = fs.createWriteStream('scripts/build/latest.zip');
	var archive = archiver('zip');

	output.on('close', function() {
		console.log('Zip done...');

		//upload to S3
		uploadHelper.uploadZip('scripts/build/latest.zip', 'latest');
		uploadHelper.uploadZip('scripts/build/latest.zip', currentVersion);
	});

	archive.on('error', function(err) {
		throw err;
	});

	// pipe archive data to the file
	archive.pipe(output);
	archive.directory('/tmp/' + fileName, 'core');

	archive.finalize();
});
