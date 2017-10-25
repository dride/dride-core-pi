var util = require('util');

var bleno = require('bleno');

var BlenoCharacteristic = bleno.Characteristic;

var exec = require('child_process').exec;


var gpio = require('rpi-gpio');
gpio.setup(29, gpio.DIR_IN, gpio.EDGE_BOTH);


var buttonStream = function() {
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

buttonStream.prototype.onReadRequest = function(offset, callback) {


  console.log('buttonStream - onReadRequest: value = ' + this._value.toString('hex'));


  callback(this.RESULT_SUCCESS, this._value);
};




buttonStream.prototype.onSubscribe = function(maxValueSize, updateValueCallback) {
  console.log('buttonStream - onSubscribe');
  var subObj = this;
  gpio.on('change', function(channel, value) {

    if (value){
        // push videoId to app
        console.log('hey!')
        
        subObj._updateValueCallback = updateValueCallback;

        subObj.shareVideoId();


    } 




  });



};

buttonStream.prototype.onUnsubscribe = function() {
  console.log('buttonStream - onUnsubscribe');


  this._updateValueCallback = null;
};

buttonStream.prototype.shareVideoId = function() {
    var videoId = '15055545036';
    console.log(videoId);
    this._value.write(videoId);
    // this._isinsane
    this._updateValueCallback(this._value);
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
