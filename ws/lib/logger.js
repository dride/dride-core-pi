'use strict';

var bunyan = require('bunyan');
var config = require('konfig')({ path: 'config' });

var options = { name: config.app.microservice.server.name || 'microservice' };

if (config.app.log && config.app.log.path) {
  options.streams = [
    { type: 'rotating-file', path: config.app.log.path }
  ];
}

var log = bunyan.createLogger(options);

module.exports = log;
