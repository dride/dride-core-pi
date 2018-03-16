/*
 * This file will clean old clips if we reach 95% of free storage
 * This will not take into consideration locked clips
 */
var fs = require('fs');
var disk = require('diskusage');

var dir = '/dride/';
var dirVideo = dir + 'clip/';
var videoModuleDir = '/home/core/modules/video/';

disk.check('/', (err, info) => {
	if (err) {
		console.log(err);
		process.exit(0);
	} else {
		var freeSpace = info.free * 100 / info.total;
		//console.log('freeSpace: ', freeSpace);

		//if we got less than 15% let's cleanup
		if (freeSpace < 15) {
			//load EMR clips
			var savedVideos = fs.readFileSync(videoModuleDir + 'savedVideos.json', 'utf8');
			var EMRvideos = JSON.parse(savedVideos ? savedVideos : []);

			fs.readdir(dirVideo, (err, files) => {
				if (err) {
					console.error('Could not list the directory.', err);
					process.exit(0);
				}

				files.sort((filea, fileb) => {
					return filea.time < fileb.time;
				});
				var count = 0;
				files.forEach((file, index) => {
					fileName = file.split('.').shift();

					if (!isEMR(EMRvideos, fileName) && fileName) {
						try {
							fs.unlinkSync(dirVideo + fileName + '.mp4');
						} catch (e) {
							console.log(e);
						}
						try {
							fs.unlinkSync(dir + 'thumb/' + fileName + '.jpg');
						} catch (e) {
							console.log(e);
						}
						count++;
					}
					console.log(count);
					if (count > 5) {
						process.exit();
					}
				});
			});
		}
	}
});

function isEMR(EMRvideos, fileName) {
	for (var i = 0; i < EMRvideos.length; i++) {
		if (EMRvideos[i].key === fileName) {
			return true;
		}
	}
	return false;
}
