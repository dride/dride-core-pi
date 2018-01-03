var util = require('util');
var spawn = require("child_process").spawn;
var fs = require("fs");

var bleno = require('bleno');

var BlenoCharacteristic = bleno.Characteristic;


var videoReady = function () {
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

videoReady.prototype.onReadRequest = function (offset, callback) {
  callback(this.RESULT_SUCCESS, this._value);
};



videoReady.prototype.onSubscribe = function (maxValueSize, updateValueCallback) {
  console.log('videoReady: onSubscribe ')
  videoReady.prototype.ex = updateValueCallback
}

videoReady.startListner = () => {

  spawn('python', ["/home/Cardigan/modules/indicators/python/states/standalone.py", "isDownloading"]);

  console.log('videoReady: wating for video.. ')
  var w = fs.watch('/home/Cardigan/modules/video/thumb/', (listner, filename) => {
	  console.log(listner, filename)
		setTimeout(() => {
			spawn('python', ["/home/Cardigan/modules/indicators/python/states/standalone.py", "done"]);

			filename = filename.replace('.jpg', '')
			var data = new Buffer.from(filename, 'utf8');
			data.write(filename);

			videoReady.prototype.ex(data);
			console.log('videoReady: videoId sent!')
		}, 1000 * 10);

		w.close();
		return;
	
  });

}



videoReady.prototype.onUnsubscribe = function () {
  this._updateValueCallback = null;
  ex = null
};


videoReady.prototype.stringToBytes = function (string) {
  var array = new Uint8Array(string.length);
  for (var i = 0, l = string.length; i < l; i++) {
    array[i] = string.charCodeAt(i);
  }
  return array.buffer;
};

videoReady.prototype.bytesToString = function (buffer) {
  return String.fromCharCode.apply(null, new Uint8Array(buffer));
};



module.exports = videoReady;
