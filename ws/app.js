'use strict';

/*
 * Dependencies
 */
var log     = require('./lib/logger');
var config  = require('konfig')({ path: 'config' });
var express = require('express');
var micro   = require('express-microservice-starter');

var app  = express();

app.use(micro({
  discoverable: true,
  controllersPath: 'lib/controllers',
  monitorsPath: 'lib/monitors'
}));

app.listen(process.env.PORT || config.app.server.port, function onListen() {
  log.info('Initialised ' + config.app.microservice.server.name);
});

module.exports = app;
