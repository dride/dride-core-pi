var util = require('util');
var spawn = require('child_process').spawn;
var fs = require('fs');

var bleno = require('bleno');

var BlenoCharacteristic = bleno.Characteristic;

var videoReady = function() {
	videoReady.super_.call(this, {
		uuid: '6655',
		properties: ['read', 'write', 'notify']
	});

	this._value = new Buffer(0);
	this._interval = null;
	this._updateValueCallback = null;
};

util.inherits(videoReady, BlenoCharacteristic);

videoReady.prototype.ex = null;

videoReady.prototype.onReadRequest = function(offset, callback) {
	callback(this.RESULT_SUCCESS, this._value);
};

videoReady.prototype.onSubscribe = function(maxValueSize, updateValueCallback) {
	console.log('videoReady: onSubscribe ');
	videoReady.prototype.ex = updateValueCallback;
};

videoReady.startListner = clickTimeStamp => {
	console.log('videoReady: wating for video.. ');
	var w = fs.watch('/dride/thumb/', (listner, filename) => {
		/**
		 * We might get unwated encoded video clips during the watch period, So we filter them so we will get the clip we need.
		 */
		if (filename < clickTimeStamp || filename - clickTimeStamp > 60) {
			return;
		}

		filename = filename.replace('.jpg', '');

		// save currentTimestamp in the db
		var emrVideos = JSON.parse(fs.readFileSync('/home/core/modules/video/savedVideos.json', 'utf8'));
		if (!emrVideos) {
			emrVideos = [];
		}

		//make sure this was not published before
		found = false;
		for (var i = 0; i < emrVideos.length; i++) {
			if (emrVideos[i].key == filename || Math.abs(parseInt(emrVideos[i].key) - parseInt(filename)) < 5000) {
				found = true;
				break;
			}
		}

		if (!found) {
			emrVideos.push({
				key: filename,
				cue: clickTimeStamp
			});
		}

		fs.writeFileSync('/home/core/modules/video/savedVideos.json', JSON.stringify(emrVideos));

		var state = '/home/core/state/app.json';
		fs.writeFile(
			state,
			JSON.stringify({
				connected: false
			}),
			err => {
				if (err) throw err;
			}
		);

		setTimeout(() => {
			//TODO: clear all indicator light
			var data = new Buffer.from(filename, 'utf8');
			data.write(filename);

			if (videoReady.prototype.ex) {
				videoReady.prototype.ex(data);
			}
			console.log('videoReady: videoId sent!');
		}, 1000 * 10);

		w.close();
		return;
	});
};

videoReady.prototype.onUnsubscribe = function() {
	this._updateValueCallback = null;
	ex = null;
};

videoReady.prototype.stringToBytes = function(string) {
	var array = new Uint8Array(string.length);
	for (var i = 0, l = string.length; i < l; i++) {
		array[i] = string.charCodeAt(i);
	}
	return array.buffer;
};

videoReady.prototype.bytesToString = function(buffer) {
	return String.fromCharCode.apply(null, new Uint8Array(buffer));
};

module.exports = videoReady;
