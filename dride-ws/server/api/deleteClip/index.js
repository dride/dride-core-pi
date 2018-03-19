'use strict';

var express = require('express');
var controller = require('./deleteClip.controller');

var router = express.Router();


;



router.get('/:videoId', function(req, res){


 	controller.index(req, res)


 	
});

module.exports = router;