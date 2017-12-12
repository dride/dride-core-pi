
var record = require('./helpers/record')

var interval = 60*1000

record.recordClip(new Date().getTime(), interval);

setInterval(_=>{
	console.log('start..')
	record.recordClip(new Date().getTime(), interval);
}, interval)
