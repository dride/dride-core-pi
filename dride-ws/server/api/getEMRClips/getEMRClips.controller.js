'use strict';

var path = require('path');
var validator = require('validator');
var fs = require('fs');

var fileNames = [];

// Get list of getPOLists
exports.index = function(req, res) {
	var savedVideos = '/home/core/modules/video/savedVideos.json';
	if (fs.existsSync(savedVideos)) {
		var EMRvideos = fs.readFileSync(savedVideos, 'utf8');

		try {
			EMRvideos = JSON.parse(EMRvideos);
		} catch (e) {
			EMRvideos = [];
		}
		for (var i = 0; i < EMRvideos.length; i++) {
			EMRvideos[i].timestamp = EMRvideos[i].key;
			EMRvideos[i].clip = '/clip/' + EMRvideos[i].key + '.mp4';
			EMRvideos[i].thumb = '/thumb/' + EMRvideos[i].key + '.jpg';
		}

		res.json({
			data: EMRvideos
		});
	} else {
		res.json({
			data: []
		});
	}
};
