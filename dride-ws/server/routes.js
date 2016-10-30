/**
 * Main application routes
 */

'use strict';

var path = require('path');
var config = require('./config/environment');

var cors = require('cors')



module.exports = function(app) {

  app.use(cors());

  // Insert routes below
  app.use('/api/getClips', require('./api/getClips'));
  

};
