'use strict';

var should = require('should');
var app = require('../../app');
var request = require('supertest');

describe('GET /api/isOnline', function() {
	it('should respond 1 if device is connected', function(done) {
		request(app)
			.get('/api/heartBeat')
			.expect(200)
			.expect('Content-Type', /json/)
			.end(function(err, res) {
				if (err) return done(err);
				res.body.should.have.property('status').and.equal(1);
				done();
			});
	});
});
