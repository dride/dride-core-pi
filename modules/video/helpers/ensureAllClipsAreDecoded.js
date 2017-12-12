/*
 * This file will make sure all clips are decoded properly,
 * This script will run once on boot
 */
var fs = require('fs');
var record = require('./record')
var execSync = require('child_process').execSync;

var dir = '/home/Cardigan/modules/video/';
var dirTmpClip = dir + 'tmp_clip';


fs.readdir(dirTmpClip, function (err, files) {
	if (err) {
		console.error("Could not list the directory.", err);
		process.exit(0);
	}


	files.forEach(function (file, index) {
	  //repack h264 to mp4 container
	  var timestamp = file.split('.').shift();
	  execSync('MP4Box -add  '+dir+'tmp_clip/' + timestamp + '.h264 '+dir+'clip/' + timestamp + '.mp4');
	  //remove tmp file
	  fs.unlinkSync(dir+'tmp_clip/' + timestamp + '.h264');
	  record.saveThumbNail(timestamp).then(
		  done => resolve(),
		  err => {
			  console.log(err)
			  reject(err)
			}
	  )
	})

})

