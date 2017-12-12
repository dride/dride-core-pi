var RaspiCam = require("raspicam");
var execSync = require('child_process').execSync;
var fs = require('fs');

var recordClip = (timestamp, interval) => {
  return new Promise((resolve, reject) => {

    if (!/^\d+$/.test(timestamp)) {
      reject('Err: input issues, Who are you?');
      return;
    }

    var camera = new RaspiCam({
      mode: "video",
      output: "./tmp_clip/" + timestamp + ".h264",
      framerate: 30,
      timeout: interval,
      width: 1280,
      height: 720,
      log: function () {}
    })

    camera.start();

    camera.on("exit", (ts) => {
      //repack h264 to mp4 container
      execSync('MP4Box -add  tmp_clip/' + timestamp + '.h264 clip/' + timestamp + '.mp4');
      //remove tmp file
      fs.unlinkSync('tmp_clip/' + timestamp + '.h264');
      saveThumbNail(timestamp).then(
        done => resolve(),
        err => {
          console.log(err)
          reject(err)
        }
      )

    });


  });




}

var saveThumbNail = (timestamp) => {
	
  return new Promise((resolve, reject) => {

		//add watermark
		execSync('avconv -y  -i /home/Cardigan/modules/video/clip/' + timestamp + '.mp4 -f mjpeg -vframes 1 -ss 1 /home/Cardigan/modules/video/thumb/' + timestamp + '.jpg')

  })
}

module.exports = {
	recordClip: recordClip,
	saveThumbNail: saveThumbNail
}
