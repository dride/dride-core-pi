var RaspiCam = require('raspicam');
var settingsHelper = require('../../settings/settings');
var exec = require('child_process').exec;
var execSync = require('child_process').execSync;
var fs = require('fs');
var path = require('path');
var spawn = require('child_process').spawn;
var led = require('../../led/index');

var dir = '/dride/';
var dirTmpClip = dir + 'tmp_clip/';
var firstFired = false;
var recordClip = interval => {
	console.log('recordClip');
	return new Promise((resolve, reject) => {
		var settings = settingsHelper.getSettings();

		switch (settings.resolution) {
			case '1080':
				var videoQuality = {
					width: 1920,
					height: 1080,
					fps: 25
				};
				break;
			case '720':
				var videoQuality = {
					width: 1280,
					height: 720,
					fps: 25
				};
				break;
			default:
				var videoQuality = {
					width: 1280,
					height: 720,
					fps: 25
				};
		}

		var camera = new RaspiCam({
			mode: 'video',
			output: '/dride/tmp_clip/%d.h264',
			framerate: videoQuality.fps,
			timeout: 0,
			segment: interval,
			width: videoQuality.width,
			height: videoQuality.height,
			rotation: settings.flipVideo ? 180 : 0,
			log: d => {
				//detect camera error and put steady red LED
				//mmal: main: Failed to create camera component
				if (d.indexOf('mmal: main: Failed to create camera component') > 0) {
					setTimeout(() => {
						led.error();
						process.exit(0);
					}, 3000);
				}
			}
		});
		//listen for the "read" event triggered when each new video is saved
		camera.on('read', (err, timestamp, fileName) => {
			//do stuff
			fileName = fileName.split('.').shift();

			if (firstFired) {
				prevFileName = findPrevClipFileName(fileName);
				if (prevFileName && fs.existsSync(dirTmpClip + prevFileName + '.h264')) {
					//repack h264 to mp4 container
					encodeAndAddThumb(prevFileName, videoQuality.fps);
				}
			} else {
				firstFired = true;
			}
		});
		camera.start();
	});
};

var saveThumbNail = fielName => {
	//save thumb
	execSync(
		'avconv -ss 00:00:00 -i /dride/clip/' +
			fielName +
			'.mp4 -vframes 1 -q:v 15 -s 640x480 /dride/thumb/' +
			fielName +
			'.jpg -y'
	);
};

var findPrevClipFileName = currentFileName => {
	var prevFileName = null;
	var file = null;

	files = fs.readdirSync(dirTmpClip);
	for (var i in files.sort()) {
		file = files[i];
		if (file.split('.').shift() === currentFileName) {
			return prevFileName ? prevFileName.split('.').shift() : null;
		}
		prevFileName = file;
	}

	return null;
};

var encodeAndAddThumb = (fileName, fps, birthtimeMs) => {
	//repack h264 to mp4 container
	fileName = fileName.split('.').shift();
	fileDetails = fs.statSync(dirTmpClip + fileName + '.h264');

	execSync(
		'avconv -framerate ' + fps + ' -i /dride/tmp_clip/' + fileName + '.h264 -c copy /dride/clip/' + fileName + '.mp4 -y'
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
	saveThumbNail(fileName);
};

module.exports = {
	recordClip: recordClip,
	saveThumbNail: saveThumbNail,
	encodeAndAddThumb: encodeAndAddThumb
};
