var AWS = require('aws-sdk');
var fs = require('fs');

module.exports = {
	uploadZip: function(src, destFileName) {
		keys = JSON.parse(fs.readFileSync('./keys/aws.json', 'utf8'));
		AWS.config.update({
			accessKeyId: keys.accessKeyId,
			secretAccessKey: keys.secretAccessKey
		});
		// Read in the file, convert it to base64, store to S3
		fs.readFile(src, function(err, data) {
			if (err) {
				throw err;
			}

			var base64data = new Buffer(data, 'binary');

			var s3 = new AWS.S3();
			s3.putObject(
				{
					Bucket: 'dride/releases/dride',
					Key: destFileName + '.zip',
					Body: base64data,
					ACL: 'public-read'
				},
				function(resp) {
					console.log(arguments);
					console.log('Successfully uploaded package.');
				}
			);
		});
	}
};
