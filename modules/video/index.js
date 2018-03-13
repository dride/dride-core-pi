var record = require('./helpers/record');
var settingsHelper = require('../settings/settings');
var verifyCamera = require('./helpers/verifyCamera');
var spawn = require('child_process').spawn;
var fs = require('fs');

var settings = settingsHelper.getSettings();
var interval = settings.clipLength * 30 * 1000;
console.log(interval);
if (settings.videoRecord) {
	//make sure we have the camera connected, If not notify with an error LED,
	if (!verifyCamera.verifyCamera()) {
		spawn('python', ['/home/Cardigan/modules/indicators/python/states/standalone.py', 'error']);
	} else {
		record.recordClip(new Date().getTime(), interval);
	}
}
