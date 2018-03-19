'use strict';

var express = require('express');
var controller = require('./indicator.controller');

var router = express.Router();


;



router.get('/:action', function(req, res){


 	controller.index(req, res)


 	
});

module.exports = router;