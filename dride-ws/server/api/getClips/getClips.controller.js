'use strict';



var validator = require('validator');


var config = require('../../config/environment');
var fileNames   = [];

// Get list of getPOLists
exports.index = function(req, res) {
	//const videoClipsFolder = config.videoClipsFolder;

	const videoClipsFolder = '../../modules/video/clip/';
	const fs = require('fs');

	var files = fs.readdirSync(videoClipsFolder);
	for (var i in files) {

	  console.log('Model Loaded: ' + files[i]);
	  if (files[i] == '.DS_Store' || files[i] == '.gitignore')
	  	continue;

	  files[i] = (files[i].split('.'))[0]

	  fileNames.push(files[i]);
	}


    res.json({data: 
    				fileNames
    		});


};


