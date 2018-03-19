'use strict';

var should = require('should');
var chai = require('chai');
var expect = chai.expect;
var app = require('../../app');
var request = require('supertest');
var fs = require('fs');
var path = require('path');

describe('GET /api/getSettings', function() {
	this.timeout(5000);

	it('should respond with settings object', function(done) {
		request(app)
			.get('/api/getSettings')
			.expect(200)
			.expect('Content-Type', /json/)
			.end(function(err, res) {
				if (err) return done(err);

				var configFromFile = JSON.parse(fs.readFileSync('./config.json', 'utf-8'));

				expect(res.body).to.deep.equal(configFromFile);

				done();
			});
	});
});
