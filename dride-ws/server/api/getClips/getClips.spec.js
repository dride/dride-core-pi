'use strict';

var should = require('should');
var app = require('../../app');
var request = require('supertest');

var config = require('../../config/environment');

describe('GET /api/PO/getPOList', function() {
  
  this.timeout(5000);

  // it('should respond with POObject', function(done) {
  //   request(app)
  //     .get('/api/PO/getPOList?byCity=5')
  //     .set('token', config.testAccount.token)
  //     .expect(200)
  //     .expect('Content-Type', /json/)
  //     .end(function(err, res) {
  //       if (err) return done(err);
  //       res.body.should.have.property('status').and.equal(1);
  //       res.body.should.have.property('POObject');
  //       done();
  //     });
  // });

  // it('should respond with nothing found', function(done) {
  //   request(app)
  //     .get('/api/PO/getPOList?byCity=')
  //     .set('token', config.testAccount.token)
  //     .expect(200)
  //     .expect('Content-Type', /json/)
  //     .end(function(err, res) {
  //       if (err) return done(err);
  //       res.body.should.have.property('status').and.equal(0);
  //       done();
  //     });
  // });


});