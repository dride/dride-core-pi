var util = require('util');
var spawn = require("child_process").spawn;
var fs = require("fs");

var videoReady = require('./videoReady');

var bleno = require('bleno');

var BlenoCharacteristic = bleno.Characteristic;

var gpio = require('rpi-gpio');
gpio.setup(16, gpio.DIR_IN, gpio.EDGE_BOTH);

var ex = null;

var buttonStream = function () {
  buttonStream.super_.call(this, {
    uuid: '5678',
    properties: ['read', 'write', 'notify']
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
  console.log('buttonStream: onSubscribe ')
  ex = updateValueCallback
  spawn('python',["/home/Cardigan/modules/indicators/python/states/standalone.py", "isPaired"]);
}

gpio.on('change', function (channel, value) {

  if (value) {
  	var currentTimeStamp = (new Date().getTime()).toString();

    // save currentTimestamp in the db
    var savedVideosPath = '/home/Cardigan/modules/video/savedVideos.json'
    fs.appendFile(savedVideosPath, ',' + currentTimeStamp, function (err) {
      if (err) throw err;
      console.log('Saved!');
     });

	// push videoId to app
	if (ex){
		spawn('python',["/home/Cardigan/modules/indicators/python/states/standalone.py", "buttonPress"]);

		var data = new Buffer.from(currentTimeStamp, 'utf8')

		data.write(currentTimeStamp);

		ex(data);

		videoReady.startListner()

	}else{
		spawn('python',["/home/Cardigan/modules/indicators/python/states/standalone.py", "buttonPressOffline"]);
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
