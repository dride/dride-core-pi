/*
 * This file will clean old clips if we reach 95% of free storage
 * This will not take into consideration locked clips
 */
var fs = require('fs');
var disk = require('diskusage');

var dir = '/home/Cardigan/modules/video/';
var dirVideo = dir + 'clip/';

disk.check('/', function (err, info) {
  if (err) {
    console.log(err);
    process.exit(0);
  } else {
    var freeSpace = info.free * 100 / info.total;

    //if we got less than 10% let's cleanup
    if (freeSpace < 10) {

      fs.readdir(dirVideo, function (err, files) {
        if (err) {
          console.error("Could not list the directory.", err);
          process.exit(0);
        }

        files.sort(function (filea, fileb) {
          return filea.time < fileb.time;
        });

        files.forEach(function (file, index) {
          if (index > 2) return;
          fileName = file.split('.').shift()
          try {
            fs.unlinkSync(dirVideo + fileName + '.mp4');
          } catch (err) {
			console.warn(err)
          }
          try {
            fs.unlinkSync(dir + 'thumb/' + fileName + '.jpg');
          } catch (err) {
			console.warn(err)
          }
        })

      })

    }
  }
});
