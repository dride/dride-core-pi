/*
 * This file will make sure all clips are decoded properly,
 * This script will run every minutes
 */
var fs = require('fs');
var record = require('./record');
var execSync = require('child_process').execSync;
var settingsHelper = require('../../settings/settings');

var dir = '/dride/';
var dirTmpClip = dir + 'tmp_clip';

/**
 * TODO:!!
 * Make sure we're decoding the right clip!
 */

var settings = settingsHelper.getSettings();
fs.readdir(dirTmpClip, (err, files) => {
	if (err) {
		console.error('Could not list the directory.', err);
		process.exit(0);
	}
	for (var index = 0; index < files.length; index++) {
		file = files[index];
		fileDetails = fs.statSync(dirTmpClip + '/' + file);

		//remove empty files
		if (!fileDetails.size) {
			fs.unlinkSync(dirTmpClip + '/' + file);
			continue;
		}
		var fileName = file.split('.').shift();

		//if the file is from the last minute ignore it
		if (Math.floor(Date.now() / 1000) - parseInt(fileName) > 120) {
			//repack h264 to mp4 container
			execSync(
				'avconv -framerate ' +
					(settings.resolution == '1080' ? 30 : 30) +
					' -i /dride/tmp_clip/' +
					fileName +
					'.h264 -c copy /dride/clip/' +
					fileName +
					'.mp4 -y'
			);

			//remove tmp file
			if (fs.existsSync(dir + 'tmp_clip/' + fileName + '.h264')) {
				try {
					fs.unlinkSync(dir + 'tmp_clip/' + fileName + '.h264');
				} catch (err) {
					//throw err
					console.error(error);
				}
			}
			// Manual encoding will add .m to the file name, this will allow us to avoid conflict with button press events
			record.saveThumbNail(fileName);
			break;
		}
	}
});
