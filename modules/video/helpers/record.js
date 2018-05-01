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
					//if app is connected skip the decoding
					var isAppConnected = isAppOnline();

					//repack h264 to mp4 container
					//if app connected dont run encode, It will be later picked up by the ensureAllClipsAreDecoded service.
					if (!isAppConnectedObj.connected || isAppConnectedObj.clicked) {
						encodeAndAddThumb(prevFileName, settings.resolution);
					}
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
	fileName = fileName.split('.').shift();
	fileDetails = fs.statSync(dirTmpClip + fileName + '.h264');

	execSync(
		'avconv -framerate ' +
			(resolution == '1080' ? 30 : 30) +
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
	saveThumbNail(fileName);
};

module.exports = {
	recordClip: recordClip,
	saveThumbNail: saveThumbNail,
	isAppOnline: isAppOnline,
	encodeAndAddThumb: encodeAndAddThumb
};
