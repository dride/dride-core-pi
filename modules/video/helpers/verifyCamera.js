var execSync = require('child_process').execSync;

module.exports.verifyCamera = () => {
	var res = execSync('/opt/vc/bin/vcgencmd get_camera');
	return res.toString().indexOf('supported=1 detected=1') >= 0 ? true : false;
};
