/*
 * This file will make sure all clips are decoded properly,
 * This script will run every minutes
 */
var fs = require('fs');
var record = require('./record');
var execSync = require('child_process').execSync;

var state = '/home/Cardigan/state/app.json';
var dir = '/home/Cardigan/modules/video/';
var dirTmpClip = dir + 'tmp_clip';

//if app is connected skip the decoding
var isAppConnected = record.isAppOnline();
var used = false;
if (isAppConnected && !isAppConnectedObj.connected) {
	fs.readdir(dirTmpClip, function(err, files) {
		if (err) {
			console.error('Could not list the directory.', err);
			process.exit(0);
		}

		files.forEach(function(file, index) {
			var fileName = file.split('.').shift();

			if (used) return;

			//if the file is from the last minute ignore it
			if (Math.abs(new Date().getTime() - fileName) > 1000 * 65) {
				//repack h264 to mp4 container
				execSync(
					'avconv -framerate 24 -i /home/Cardigan/modules/video/tmp_clip/' +
						fileName +
						'.h264 -c copy /home/Cardigan/modules/video/clip/' +
						fileName +
						'.mp4 -y'
				);
				//remove tmp file
				if (fs.existsSync(dir + 'tmp_clip/' + fileName + '.h264')) {
					fs.unlinkSync(dir + 'tmp_clip/' + fileName + '.h264');
				}
				record.saveThumbNail(fileName).then(
					done => {
						used = true;
						resolve();
					},
					err => {
						console.log(err);
						reject(err);
					}
				);
			}
		});
	});
}
