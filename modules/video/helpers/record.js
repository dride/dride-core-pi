var RaspiCam = require('raspicam');
var settingsHelper = require('../../settings/settings');
var exec = require('child_process').exec;
var execSync = require('child_process').execSync;
var fs = require('fs');
var path = require('path');
var spawn = require('child_process').spawn;

var dir = '/dride/';
var dirTmpClip = dir + 'tmp_clip/';

var recordClip = (timestamp, interval) => {
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

		if (!/^\d+$/.test(timestamp)) {
			reject('Err: input issues, Who are you?');
			return;
		}
		var camera = new RaspiCam({
			mode: 'video',
			output: '/dride/tmp_clip/' + timestamp + '_%d.h264',
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
						spawn('python', ['/home/core/modules/indicators/python/states/standalone.py', 'error']);
						process.exit(0);
					}, 3000);
				}
			}
		});
		//listen for the "read" event triggered when each new video is saved
		camera.on('read', (err, timestamp, filename) => {
			//do stuff
			const serialNumber = parseInt(filename.match(/[0-9]+/g)[1], 10);
			if (serialNumber > 1) {
				if (
					fs.existsSync(
						dirTmpClip + filename.match(/[0-9]+/g)[0].toString() + '_' + (serialNumber - 1).toString() + '.h264'
					)
				) {
					//if app is connected skip the decoding
					var isAppConnected = isAppOnline();

					//repack h264 to mp4 container
					//if app connected dont run encode, It will be later picked up by the ensureAllClipsAreDecoded service.
					if (!isAppConnectedObj.connected || isAppConnectedObj.clicked) {
						encodeAndAddThumb(
							filename.match(/[0-9]+/g)[0].toString() + '_' + (serialNumber - 1).toString(),
							settings.resolution
						);
					}
				}
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

var isAppOnline = () => {
	var state = path.join(__dirname, '../../../state/app.json');

	//if app is connected skip the decoding
	var isAppConnected = fs.readFileSync(state, 'utf8');

	try {
		isAppConnectedObj = JSON.parse(fs.readFileSync(state, 'utf8'));
	} catch (error) {
		isAppConnectedObj = {
			connected: false,
			wasEmpty: true
		};
	}
	if (isAppConnectedObj.dte && new Date().getTime() - isAppConnectedObj.dte > 1000 * 60) {
		fs.writeFileSync(
			state,
			JSON.stringify({
				connected: false
			})
		);
		isAppConnectedObj.connected = false;
	} else if (isAppConnectedObj.wasEmpty) {
		fs.writeFileSync(
			state,
			JSON.stringify({
				connected: false
			})
		);
	}
	return isAppConnectedObj;
};

var encodeAndAddThumb = (fileName, resolution, birthtimeMs) => {
	//repack h264 to mp4 container

	fileDetails = fs.statSync(dirTmpClip + fileName + '.h264');

	execSync(
		'avconv -framerate ' +
			(resolution == '1080' ? 30 : 30) +
			' -i /dride/tmp_clip/' +
			fileName +
			'.h264 -c copy /dride/clip/' +
			Math.floor(fileDetails.birthtimeMs) +
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
	saveThumbNail(Math.floor(fileDetails.birthtimeMs));
};

module.exports = {
	recordClip: recordClip,
	saveThumbNail: saveThumbNail,
	isAppOnline: isAppOnline,
	encodeAndAddThumb: encodeAndAddThumb
};
