'use strict';

var express = require('express');
var controller = require('./updateFirmware.controller');

var router = express.Router();

var multer = require('multer');
var storage = multer.diskStorage({
	destination: function(req, file, cb) {
		cb(null, '/home/core/firmware');
	},
	filename: function(req, file, cb) {
		cb(null, 'latest.zip');
	}
});

var upload = multer({ storage: storage, mimetype: 'application/zip' });

router.post('/', upload.single('file'), function(req, res) {
	controller.index(req, res);
});

module.exports = router;
