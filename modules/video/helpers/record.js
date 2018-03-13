var RaspiCam = require('raspicam');
var settingsHelper = require('../../settings/settings');
var exec = require('child_process').exec;
var execSync = require('child_process').execSync;
var fs = require('fs');
var spawn = require('child_process').spawn;

var recordClip = (timestamp, interval) => {
	return new Promise((resolve, reject) => {
		var settings = settingsHelper.getSettings();

		switch (settings.resolution) {
			case '1080':
				var videoQuality = {
					width: 1920,
					height: 1080,
					fps: 30
				};
				break;
			case '720':
				var videoQuality = {
					width: 1280,
					height: 720,
					fps: 30
				};
				break;
			default:
				var videoQuality = {
					width: 1280,
					height: 720,
					fps: 30
				};
		}

		console.log('sett', videoQuality);

		if (!/^\d+$/.test(timestamp)) {
			reject('Err: input issues, Who are you?');
			return;
		}
		var camera = new RaspiCam({
			mode: 'video',
			output: '/home/Cardigan/modules/video/tmp_clip/%d.h264',
			framerate: videoQuality.fps,
			timeout: 0,
			segment: 10000,
			width: videoQuality.width,
			height: videoQuality.height,
			rotation: settings.flipVideo ? 180 : 0,
			log: function(d) {
				//detect camera error and put steady red LED
				//mmal: main: Failed to create camera component
				if (d.indexOf('mmal: main: Failed to create camera component') > 0) {
					setTimeout(() => {
						spawn('python', ['/home/Cardigan/modules/indicators/python/states/standalone.py', 'error']);
						process.exit(0);
					}, 3000);
				}
			}
		});

		camera.start();
	});
};

var saveThumbNail = fielName => {
	//save thumb
	execSync(
		'avconv -ss 00:00:00 -i /home/Cardigan/modules/video/clip/' +
			fielName +
			'.mp4 -vframes 1 -q:v 2 -s 640x480 /home/Cardigan/modules/video/thumb/' +
			fielName +
			'.jpg'
	);
};

var isAppOnline = () => {
	var state = '/home/Cardigan/state/app.json';

	//if app is connected skip the decoding
	var isAppConnected = fs.readFileSync(state, 'utf8');
	if (!isAppConnected) {
		isAppConnected = {
			connected: false
		};
	} else {
		try {
			isAppConnectedObj = JSON.parse(fs.readFileSync(state, 'utf8'));
		} catch (error) {
			if (error) throw error;
		}
	}

	if (
		isAppConnectedObj &&
		isAppConnectedObj.dte &&
		Math.abs(new Date().getTime() - isAppConnectedObj.dte) > 1000 * 60
	) {
		fs.writeFile(
			state,
			JSON.stringify({
				connected: false
			})
		);
		isAppConnectedObj.connected = false;
	}
	return isAppConnectedObj;
};

module.exports = {
	recordClip: recordClip,
	saveThumbNail: saveThumbNail,
	isAppOnline: isAppOnline
};
