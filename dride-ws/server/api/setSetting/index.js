'use strict';

var express = require('express');
var controller = require('./setSetting.controller');

var router = express.Router();


;



router.get('/', function(req, res){


 	controller.index(req, res)


 	
});

module.exports = router;