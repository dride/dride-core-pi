var record = require('./helpers/record');
var settingsHelper = require('../settings/settings');
var verifyCamera = require('./helpers/verifyCamera');
var led = require('../led/index');
var fs = require('fs');

var settings = settingsHelper.getSettings();
var interval = settings.clipLength * 60 * 1000;

if (settings.videoRecord) {
	//make sure we have the camera connected, If not notify with an error LED,
	if (!verifyCamera.verifyCamera()) {
		led.error();
	} else {
		record.recordClip(interval);
	}
}
