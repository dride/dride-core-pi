'use strict';

var should = require('should');
var app = require('../../app');
var request = require('supertest');

describe('GET /api/getSerialNumber', function() {
	it('should return a serail number', function(done) {
		request(app)
			.get('/api/getSerialNumber')
			.expect(200)
			.expect('Content-Type', /json/)
			.end(function(err, res) {
				if (err) return done(err);
				res.body.should.be.instanceof(Object);
				done();
			});
	});
});
