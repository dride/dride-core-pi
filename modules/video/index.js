var record = require('./helpers/record');
var settingsHelper = require('../settings/settings');
var verifyCamera = require('./helpers/verifyCamera');
var spawn = require('child_process').spawn;
var fs = require('fs');

var settings = settingsHelper.getSettings();
var interval = settings.clipLength * 60 * 1000;
if (settings.videoRecord) {
	//make sure we have the camera connected, If not notify with an error LED,
	if (!verifyCamera.verifyCamera()) {
		spawn('python', ['/home/core/modules/indicators/python/states/standalone.py', 'error']);
	} else {
		record.recordClip(new Date().getTime(), interval);
	}
}
