'use strict';
const expect = require('chai').expect;
var record = require('../../helpers/record');
var path = require('path');
var fs = require('fs');

describe('Video', () => {
	describe('helpers', () => {
		describe('record', () => {
			it('should return false when app is NOT connected', () => {
				expect(record.isAppOnline().connected).to.be.false;
			});
			it('should return true when app is connected', () => {
				var state = path.join(__dirname, '../../../../state/app.json');
				fs.writeFileSync(
					state,
					JSON.stringify({
						connected: true
					})
				);

				expect(record.isAppOnline().connected).to.be.true;
			});

			it('should return true when app is connected for less then 60 seconds', () => {
				var state = path.join(__dirname, '../../../../state/app.json');
				fs.writeFileSync(
					state,
					JSON.stringify({
						connected: true,
						dte: new Date().getTime()
					})
				);

				expect(record.isAppOnline().connected).to.be.true;
			});

			it('should return false when app is not connected for longer then 60 seconds', () => {
				var state = path.join(__dirname, '../../../../state/app.json');
				fs.writeFileSync(
					state,
					JSON.stringify({
						connected: true,
						dte: new Date().getTime() - 2 * 60 * 1000
					})
				);

				expect(record.isAppOnline().connected).to.be.false;
			});

			it('should return false after app was idle for too long', () => {
				expect(record.isAppOnline().connected).to.be.false;
			});
		});
	});
});
