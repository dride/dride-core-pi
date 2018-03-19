// 'use strict';

// process.env.NODE_ENV = 'test';

// var should = require('should');
// var app = require('../../app');
// var request = require('supertest');
// var fs = require('fs');
// var path = require('path');

// describe('deleteAllClips', () => {
// 	//copy clips to /dride/*
// 	beforeEach(done => {
// 		fs.copyFileSync(
// 			path.join(__dirname, '../../../..', 'tests/data/1521390239070.jpg'),
// 			path.join(__dirname, '../../../..', 'dride/thumb/1521390239070.jpg')
// 		);
// 		fs.copyFileSync(
// 			path.join(__dirname, '../../../..', 'tests/data/1521390239070.mp4'),
// 			path.join(__dirname, '../../../..', 'dride/clip/1521390239070.mp4')
// 		);
// 		done();
// 	});

// 	describe('GET /api/deleteAllClips', function() {
// 		it('should remove all clips in /dride/clip & thumbs in /dride/thumb', function(done) {
// 			request(app)
// 				.get('/api/deleteAllClips')
// 				.expect(200)
// 				.expect('Content-Type', /json/)
// 				.end(function(err, res) {
// 					if (err) return done(err);
// 					res.body.should.have.property('status').and.equal(1);
// 					done();
// 				});
// 		});
// 	});
// });
