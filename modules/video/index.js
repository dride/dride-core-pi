
var record = require('./helpers/record')
var spawn = require("child_process").spawn;

var interval = 60*1000

record.recordClip(new Date().getTime(), interval);

setInterval(_=>{
	console.log('start..')
	record.recordClip(new Date().getTime(), interval);
}, interval + 1500)
 