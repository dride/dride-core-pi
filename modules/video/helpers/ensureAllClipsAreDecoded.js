var RaspiCam = require('raspicam');
var exec = require('child_process').exec;
var execSync = require('child_process').execSync;
var fs = require('fs');
var spawn = require('child_process').spawn;

var recordClip = (timestamp, interval) => {
	return new Promise((resolve, reject) => {
		var settings = JSON.parse(fs.readFileSync('/home/Cardigan/config.json', 'utf-8'));

		switch (settings.videoQuality) {
			case '1080':
				var videoQuality = {
					width: 1920,
					height: 1080
				};
				break;
			case '720':
				var videoQuality = {
					width: 1280,
					height: 720
				};
				break;
			default:
				var videoQuality = {
					width: 1280,
					height: 720
				};
		}

		if (!/^\d+$/.test(timestamp)) {
			reject('Err: input issues, Who are you?');
			return;
		}
		var camera = new RaspiCam({
			mode: 'video',
			output: '/home/Cardigan/modules/video/tmp_clip/' + timestamp + '.h264',
			framerate: 25,
			timeout: interval,
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

		camera.on('exit', ts => {
			var dir = '/home/Cardigan/modules/video/';
			//repack h264 to mp4 container
			var isAppConnected = isAppOnline();
			if (isAppConnected && !isAppConnectedObj.connected) {
				//repack h264 to mp4 container
				execSync(
					'avconv -framerate 24 -i ' +
						dir +
						'tmp_clip/' +
						timestamp +
						'.h264 -c copy ' +
						dir +
						'clip/' +
						timestamp +
						'.mp4'
				);

				//remove tmp file

				if (fs.existsSync(dir + 'tmp_clip/' + timestamp + '.h264')) {
					fs.unlinkSync(dir + 'tmp_clip/' + timestamp + '.h264');
				}

				saveThumbNail(timestamp).then(
					done => resolve(),
					err => {
						console.log(err);
						reject(err);
					}
				);
			}
		});
	});
};

var saveThumbNail = fielName => {
	return new Promise((resolve, reject) => {
		//save thumb
		exec(
			'avconv -ss 00:00:00 -i /home/Cardigan/modules/video/clip/' +
				fielName +
				'.mp4 -vframes 1 -q:v 2 /home/Cardigan/modules/video/thumb/' +
				fielName +
				'.jpg',
			() => {
				resolve();
			}
		);
	});
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
