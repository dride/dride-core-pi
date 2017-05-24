var util = require('util');

var bleno = require('bleno');

var BlenoCharacteristic = bleno.Characteristic;

var Gpio = require('onoff').Gpio,
  button = new Gpio(23, 'in', 'both');

var CountCharacteristic = function() {
  CountCharacteristic.super_.call(this, {
    uuid: '5678',
    properties: ['read', 'write', 'notify'],
    value: null
  });

  this._value = new Buffer([17,0,0,0]);
  this._interval = null;
  this._updateValueCallback = null;
};

util.inherits(CountCharacteristic, BlenoCharacteristic);

CountCharacteristic.prototype.onReadRequest = function(offset, callback) {
  console.log('CountCharacteristic - onReadRequest: value = ' + this._value.toString('hex'));

  callback(this.RESULT_SUCCESS, this._value);
};

CountCharacteristic.prototype.onSubscribe = function(maxValueSize, updateValueCallback) {
  console.log('CountCharacteristic - onSubscribe');
  var subObj = this;
  button.watch(function (err, value) {
    if (err) {
      throw err;
    }
    if (value == 1){
        // push videoId to app
        console.log('hey!')
        
        subObj._updateValueCallback = updateValueCallback;

        subObj.increment();


    } 

  });



};

CountCharacteristic.prototype.onUnsubscribe = function() {
  console.log('CountCharacteristic - onUnsubscribe');


  this._updateValueCallback = null;
};

CountCharacteristic.prototype.increment = function() {
    var videoId = '15055545036';
    console.log(videoId);
    this._value.write(videoId);
    // this._isinsane
    this._updateValueCallback(this._value);
};



CountCharacteristic.prototype.stringToBytes = function(string) {
   var array = new Uint8Array(string.length);
   for (var i = 0, l = string.length; i < l; i++) {
       array[i] = string.charCodeAt(i);
    }
    return array.buffer;
};



module.exports = CountCharacteristic;
