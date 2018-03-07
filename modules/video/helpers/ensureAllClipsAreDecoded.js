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

if (isAppConnected && !isAppConnectedObj.connected) {
	fs.readdir(dirTmpClip, function(err, files) {
		if (err) {
			console.error('Could not list the directory.', err);
			process.exit(0);
		}

		files.forEach(function(file, index) {
			var fileName = file.split('.').shift();

			//if the file is from the last minute ignore it
			if (Math.abs(new Date().getTime() - fileName) > 1000 * 65) {
				//repack h264 to mp4 container
				execSync(
					'avconv -framerate 24 -i /home/Cardigan/modules/video/tmp_clip/' +
						timestamp +
						'.h264 -c copy /home/Cardigan/modules/video/clip/' +
						timestamp +
						'.mp4'
				);
				//remove tmp file
				if (fs.existsSync(dir + 'tmp_clip/' + timestamp + '.h264')) {
					fs.unlinkSync(dir + 'tmp_clip/' + timestamp + '.h264');
				}
				record.saveThumbNail(fileName).then(
					done => resolve(),
					err => {
						console.log(err);
						reject(err);
					}
				);
				return;
			} else {
				console.log('skip, too new..', new Date().getTime() - fileName);
			}
		});
	});
}
