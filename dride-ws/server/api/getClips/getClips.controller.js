'use strict';

var path = require('path');
var validator = require('validator');

// Get list of getPOLists
exports.index = function (req, res) {
  var videoClipsFolder = '/dride/thumb/';
  var fs = require('fs');

  var clipsObj = [];

  var files = fs.readdirSync(videoClipsFolder);
  for (var i in files) {
    if (files[i] == '.DS_Store' || files[i] == '.gitignore') continue;

    files[i] = files[i].split('.')[0];

    clipsObj.push({
      key: files[i],
      clip: '/clip/' + files[i] + '.mp4',
      thumb: '/thumb/' + files[i] + '.jpg',
      timestamp: files[i]
    });
  }

  res.json({
    data: clipsObj
  });
};
