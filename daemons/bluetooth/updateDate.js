var util = require('util');

var bleno = require('bleno');

var BlenoCharacteristic = bleno.Characteristic;

var exec = require('child_process').exec;

var updateDate = function() {
	updateDate.super_.call(this, {
		uuid: '9997',
		properties: ['read', 'write'],
		value: null
	});

	this._value = new Buffer(0);
	this._interval = null;
	this._updateValueCallback = null;
};

util.inherits(updateDate, BlenoCharacteristic);

updateDate.prototype.onWriteRequest = function(data, offset, withoutResponse, callback) {
	console.log('write!');
	this._value = data;

	if (this._value.toString().length == 10) {
		var cmd = "sudo date -s '@" + this._value.toString() + "'";
		exec(cmd, function(error, stdout, stderr) {
			var RTCcmd = 'sudo hwclock -w';
			exec(RTCcmd, function(error, stdout, stderr) {
				console.log('HW clock updated!');
			});
		});
	}

	console.log('EchoCharacteristic - onWriteRequest: value = ' + this._value.toString());

	if (this._updateValueCallback) {
		console.log('EchoCharacteristic - onWriteRequest: notifying');

		this._updateValueCallback(this._value);
	}

	callback(this.RESULT_SUCCESS);
};

updateDate.prototype.stringToBytes = function(string) {
	var array = new Uint8Array(string.length);
	for (var i = 0, l = string.length; i < l; i++) {
		array[i] = string.charCodeAt(i);
	}
	return array.buffer;
};

updateDate.prototype.bytesToString = function(buffer) {
	return String.fromCharCode.apply(null, new Uint8Array(buffer));
};

module.exports = updateDate;
