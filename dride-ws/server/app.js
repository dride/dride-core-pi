/**
 * Main application file
 */

'use strict';

// Set default node environment to development
process.env.NODE_ENV = process.env.NODE_ENV || 'development';

var express = require('express');
var config = require('./config/environment.js');

// Setup server
var app = express();

var server = require('http').createServer(app);
require('./routes')(app);

// Start server
server.listen(config.port, config.ip, function() {
	console.log('Express server listening on %d, in %s mode', config.port, app.get('env'));
});

app.use('/', express.static(__dirname));

// Expose app
exports = module.exports = app;
