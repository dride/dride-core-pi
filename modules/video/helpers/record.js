var RaspiCam = require("raspicam");
var exec = require('child_process').exec;
var fs = require('fs');

var recordClip = (timestamp, interval) => {
  return new Promise((resolve, reject) => {

    if (!/^\d+$/.test(timestamp)) {
      reject('Err: input issues, Who are you?');
      return;
    }
    var camera = new RaspiCam({
      mode: "video",
      output: "/home/Cardigan/modules/video/tmp_clip/" + timestamp + ".h264",
      framerate: 30,
      timeout: interval,
      width: 1280,
      height: 720,
      log: function () {}
    })

    camera.start();

    camera.on("exit", (ts) => {
      //repack h264 to mp4 container
      exec('MP4Box -add  /home/Cardigan/modules/video/tmp_clip/' + timestamp + '.h264 /home/Cardigan/modules/video/clip/' + timestamp + '.mp4', (e, stdout, stderr)=> {
		//remove tmp file
		fs.unlink('/home/Cardigan/modules/video/tmp_clip/' + timestamp + '.h264');
		saveThumbNail(timestamp).then(
			done => resolve(),
			err => {
			console.log(err)
			reject(err)
			}
		)
	  });


    });


  });




}

var saveThumbNail = (timestamp) => {
  return new Promise((resolve, reject) => {
		//add watermark
		exec('avconv -y  -i /home/Cardigan/modules/video/clip/' + timestamp + '.mp4 -f mjpeg -vframes 1 -ss 1 /home/Cardigan/modules/video/thumb/' + timestamp + '.jpg')
  })
}

module.exports = {
	recordClip: recordClip,
	saveThumbNail: saveThumbNail
}
