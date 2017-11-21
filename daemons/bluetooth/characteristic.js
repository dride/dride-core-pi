var util = require('util');
var spawn = require("child_process").spawn;
var fs = require("fs");

var bleno = require('bleno');

var BlenoCharacteristic = bleno.Characteristic;

var exec = require('child_process').exec;


var gpio = require('rpi-gpio');
gpio.setup(29, gpio.DIR_IN, gpio.EDGE_BOTH);

var ex = null;

var buttonStream = function () {
  buttonStream.super_.call(this, {
    uuid: '5678',
    properties: ['read', 'write', 'notify'],
    value: null
  });

  this._value = new Buffer(0);
  this._interval = null;
  this._updateValueCallback = null;
};

util.inherits(buttonStream, BlenoCharacteristic);

buttonStream.prototype.onReadRequest = function (offset, callback) {
  callback(this.RESULT_SUCCESS, this._value);
};



buttonStream.prototype.onSubscribe = function (maxValueSize, updateValueCallback) {
  ex = updateValueCallback
}

gpio.on('change', function (channel, value) {

  if (value) {
  	var currentTimeStamp = parseInt(new Date().getTime() / 1000).toString();

    // save currentTimestamp in the db
    var savedVideosPath = '/home/Cardigan/modules/video/savedVideos.json'
    fs.appendFile(savedVideosPath, ',' + currentTimeStamp, function (err) {
      if (err) throw err;
      console.log('Saved!');
     });

	// push videoId to app
	if (ex){
		var process = spawn('python',["/home/Cardigan/modules/indicators/python/states/standalone.py", "buttonPress"]);

		var data = new Buffer(Buffer.byteLength(currentTimeStamp, 'utf8') + 2);

		data.writeUInt32LE(currentTimeStamp, 0);

		console.log('NotifyOnlyCharacteristic update value: ' + currentTimeStamp);
		ex(data);
	}else{
		var process = spawn('python',["/home/Cardigan/modules/indicators/python/states/standalone.py", "buttonPressOffline"]);
	}

  }

});
buttonStream.prototype.onUnsubscribe = function () {
  this._updateValueCallback = null;
  ex = null
};


buttonStream.prototype.stringToBytes = function (string) {
  var array = new Uint8Array(string.length);
  for (var i = 0, l = string.length; i < l; i++) {
    array[i] = string.charCodeAt(i);
  }
  return array.buffer;
};

buttonStream.prototype.bytesToString = function (buffer) {
  return String.fromCharCode.apply(null, new Uint8Array(buffer));
};



module.exports = buttonStream;
