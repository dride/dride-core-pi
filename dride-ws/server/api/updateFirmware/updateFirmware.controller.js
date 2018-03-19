'use strict';

var path = require('path'),
	fs = require('fs'),
	mv = require('mv'),
	https = require('https'),
	request = require('request'),
	AdmZip = require('adm-zip'),
	rmdir = require('rmdir'),
	fileUpload = require('express-fileupload');

var fileNames = [];

/*
 *   receive a zip with the new firmware and updates the files.
 */
exports.index = function(req, res) {
	// console.log(req.file.path);

	if (!req.file.path) {
		res.send('{"status": "0", "info": "firmware upload failed"}');
		return;
	}

	//path to zip of firmware
	var fileDir = req.file.path;

	// reading archives
	var zip = new AdmZip(fileDir);
	var zipEntries = zip.getEntries(); // an array of ZipEntry records

	zip.extractAllTo('/home/core', true);

	res.send('{"status": "1"}');

	require('child_process').exec('sudo /sbin/shutdown -r now', function(msg) {
		console.log(msg);
	});
};
