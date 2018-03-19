'use strict';

var path = require('path'),
	fs = require('fs'),
	ini = require('ini'),
	rimraf = require('rimraf');

var fileNames = [];

// Get list of getPOLists
exports.index = function(req, res) {
	//delete clip, thumb & gps file
	var p1 = new Promise((resolve, reject) => {
		try {
			rimraf('/dride/clip/', () => {
				fs.mkdirSync('/dride/clip');
				resolve();
			});
		} catch (err) {
			reject(err);
		}
	});
	var p2 = new Promise((resolve, reject) => {
		try {
			rimraf('/dride/thumb/', () => {
				fs.mkdirSync('/dride/thumb');
				resolve();
			});
		} catch (err) {
			reject(err);
		}
	});
	//   var p3 = new Promise((resolve, reject) => {
	//     try {
	//       rimraf("/dride/gps/", () => {
	// 		fs.mkdirSync("/dride/gps");
	//         resolve();
	//       });
	//     } catch (err) {
	//       reject();
	//     }
	//   });

	// add p3 for GPS
	Promise.all([p1, p2])
		.then(values => {
			res.json({
				status: 1
			});
		})
		.catch(error => {
			res.json({
				status: 0,
				error: error
			});
		});
};
