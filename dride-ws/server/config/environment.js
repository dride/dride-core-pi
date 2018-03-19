'use strict';

module.exports = {
	// Server IP
	ip: process.env.OPENSHIFT_NODEJS_IP || process.env.IP || undefined,

	// Server port
	port: 9000
};
