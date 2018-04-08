'use strict';

var path = require('path');
var fs = require('fs');
var exec = require('child_process').exec;

exports.index = function (req, res) {
  var fieldName = req.param('fieldName');
  var fieldValue = req.param('fieldValue');

  var defaults = path.join(__dirname, '../../../..', 'config.json');
  var config = JSON.parse(fs.readFileSync(defaults, 'utf-8'));

  fieldValue = fieldValue.toString().toLowerCase();

  //cast to boolean if needed
  if (fieldValue == 'true') fieldValue = true;
  if (fieldValue == 'false') fieldValue = false;

  config['settings'][fieldName] = fieldValue;

  try {
    fs.writeFileSync(defaults, JSON.stringify(config));

    //if fieldName is DVR enable/disbale record.service
    if (fieldName == 'videoRecord') {
      exec('sudo systemctl ' + (fieldValue ? 'start' : 'stop') + ' record');
    }

    res.json({
      status: '1',
      reason: 'setting was saved successfully!'
    });
  } catch (err) {
    res.json({
      status: '0',
      reason: err
    });
  }
};
