'use strict';

const settings = require('../settings');
const expect = require('chai').expect;
const fs = require('fs');
const path = require('path');

describe('Settings', () => {
	it('should return settings object', () => {
		var configFromFile = JSON.parse(fs.readFileSync(path.join(__dirname, '../../../config.json'), 'utf-8'));

		expect(settings.getSettings()).to.deep.equal(configFromFile.settings);
	});
});
