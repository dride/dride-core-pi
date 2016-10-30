'use strict';



var validator = require('validator');


var config = require('../../config/environment');
var fileNames   = [];

// Get list of getPOLists
exports.index = function(req, res) {
	//const videoClipsFolder = config.videoClipsFolder;
	const videoClipsFolder = '../modules/video/clip/';
	const fs = require('fs');

    res.json({data: 
    				fs.readdirSync(videoClipsFolder)
    		});


};


