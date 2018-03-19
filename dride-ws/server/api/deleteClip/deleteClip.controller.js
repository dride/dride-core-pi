'use strict';

var path = require('path'),
	fs = require('fs');
var fileNames = [];

exports.index = function(req, res) {
	//TODO: Validate the input type's
	var videoId = req.param('videoId');
	var error = [];
	//delete clip, thumb & gps file
	var videoPath = '/dride/';
	var videoModulePath = '/home/core/modules/video/';
	try {
		fs.unlinkSync(videoPath + 'clip/' + videoId + '.mp4');
	} catch (err) {
		error.push(err);
	}

	try {
		fs.unlinkSync(videoPath + 'thumb/' + videoId + '.jpg');
	} catch (err) {
		error.push(err);
	}

	try {
		fs.unlinkSync(videoPath + 'gps/' + videoId + '.json');
	} catch (err) {
		error.push(err);
	}

	//remove video from savedVideos.json
	var savedVideosPath = videoModulePath + 'savedVideos.json';
	var EMRvideos = JSON.parse(fs.readFileSync(savedVideosPath, 'utf8'));
	for (var i = 0; i < EMRvideos.length; i++) {
		if (EMRvideos[i].key == videoId) {
			EMRvideos.splice(i, 1);
		}
	}
	fs.writeFileSync(savedVideosPath, JSON.stringify(EMRvideos));

	res.json({
		status: '1',
		error: error
	});
};
