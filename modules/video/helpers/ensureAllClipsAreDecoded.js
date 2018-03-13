/*
 * This file will make sure all clips are decoded properly,
 * This script will run every minutes
 */
var fs = require('fs');
var record = require('./record');
var execSync = require('child_process').execSync;
var settingsHelper = require('../../settings/settings');

var state = '/home/Cardigan/state/app.json';
var dir = '/home/Cardigan/modules/video/';
var dirTmpClip = dir + 'tmp_clip';

//if app is connected skip the decoding
var isAppConnected = record.isAppOnline();

var settings = settingsHelper.getSettings();

if (isAppConnected && !isAppConnectedObj.connected) {
	fs.readdir(dirTmpClip, (err, files) => {
		if (err) {
			console.error('Could not list the directory.', err);
			process.exit(0);
		}
		let fielDetails = null;
		files.forEach((file, index) => {
			fileDetails = fs.statSync(dirTmpClip + '/' + file);

			var fileName = file.split('.').shift();

			//if the file is from the last minute ignore it
			if (Math.abs(new Date().getTime() - fileDetails.birthtimeMs) > 1000 * 65) {
				//repack h264 to mp4 container
				execSync(
					'avconv -framerate ' +
						(settings.resolution == '1080' ? 30 : 30) +
						' -i /home/Cardigan/modules/video/tmp_clip/' +
						fileName +
						'.h264 -c copy /home/Cardigan/modules/video/clip/' +
						fileDetails.birthtimeMs +
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
				record.saveThumbNail(fileDetails.birthtimeMs);
			}
		});
	});
}
