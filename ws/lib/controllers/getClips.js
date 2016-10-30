'use strict';

var service = require('../services/example-service');

/**
 * Initialise endpoint
 *
 * @param router
 */
module.exports = function(router) {

  /**
   * Example Collection
   */
  router.get('/', function(req, res, next) {

    service.getExamples({}, function(err, items) {
      if (err) return next(err);

      res.cacheControl({ maxAge: 10});
      res.json(items);
    });
  });
};
