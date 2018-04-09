var util = require('util');
var spawn = require('child_process').spawn;
var fs = require('fs');

var videoReady = require('./videoReady');

var bleno = require('bleno');

var BlenoCharacteristic = bleno.Characteristic;

var gpio = require('rpi-gpio');
gpio.setup(16, gpio.DIR_IN, gpio.EDGE_BOTH);

var ex = null;

var buttonStream = function() {
	buttonStream.super_.call(this, {
		uuid: '5678',
		properties: ['read', 'write', 'notify']
	});

	this._value = new Buffer(0);
	this._interval = null;
	this._updateValueCallback = null;
};

util.inherits(buttonStream, BlenoCharacteristic);

buttonStream.prototype.onReadRequest = function(offset, callback) {
	callback(this.RESULT_SUCCESS, this._value);
};

buttonStream.prototype.onSubscribe = function(maxValueSize, updateValueCallback) {
	console.log('buttonStream: onSubscribe ');
	ex = updateValueCallback;
	spawn('python', ['/home/core/modules/indicators/python/states/standalone.py', 'isPaired']);
};

gpio.on('change', function(channel, value) {
	if (value) {
		var currentTimeStamp = new Date().getTime().toString();
		videoReady.startListner(currentTimeStamp);
		spawn('python', ['/home/core/modules/indicators/python/states/standalone.py', 'welcome']);

		if (ex) {
			//update state that we need to encode video no matter what
			var state = '/home/core/state/app.json';
			fs.writeFile(
				state,
				JSON.stringify({
					connected: true,
					dte: new Date().getTime() + 120 * 1000,
					clicked: true
				}),
				err => {
					if (err) throw err;
				}
			);

			var data = new Buffer.from(currentTimeStamp, 'utf8');

			data.write(currentTimeStamp);

			ex(data);
		}
	}
});

buttonStream.prototype.onUnsubscribe = function() {
	this._updateValueCallback = null;
	ex = null;
};

buttonStream.prototype.stringToBytes = function(string) {
	var array = new Uint8Array(string.length);
	for (var i = 0, l = string.length; i < l; i++) {
		array[i] = string.charCodeAt(i);
	}
	return array.buffer;
};

buttonStream.prototype.bytesToString = function(buffer) {
	return String.fromCharCode.apply(null, new Uint8Array(buffer));
};

module.exports = buttonStream;
