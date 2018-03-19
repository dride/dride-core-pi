'use strict';

var should = require('should');
var app = require('../../app');
var request = require('supertest');
var fs = require('fs');

describe('GET /api/heartBeat', function() {
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
	it('should update app state after heartBeat', function(done) {
		request(app)
			.get('/api/heartBeat')
			.expect(200)
			.expect('Content-Type', /json/)
			.end(function(err, res) {
				if (err) return done(err);
				res.body.should.have.property('status').and.equal(1);

				var state = JSON.parse(fs.readFileSync('./state/app.json', 'utf8'));

				state.connected.should.be.true;

				done();
			});
	});
});
