'use strict';

var path = require('path'),
	fs = require('fs');

exports.index = function(req, res) {
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
