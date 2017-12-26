var bleno = require('bleno');

var BlenoPrimaryService = bleno.PrimaryService;

console.log('bleno - echo');

var buttonStream = require('./characteristic');
var videoReady = require('./videoReady');
var updateDate = require('./updateDate');

console.log('start');

bleno.on('stateChange', function(state) {
  console.log('on -> stateChange: ' + state);

  if (state === 'poweredOn') {
    bleno.startAdvertising('dride', ['1234']);
  } else {
    bleno.stopAdvertising();
  }
});

bleno.on('advertisingStart', function(error) {
  console.log('on -> advertisingStart: ' + (error ? 'error ' + error : 'success'));

  if (!error) {
    bleno.setServices([
      new BlenoPrimaryService({
        uuid: '1234',
        characteristics: [
		  new buttonStream(),
		  new videoReady()
        ]
	  }),
      new BlenoPrimaryService({
        uuid: '7787',
        characteristics: [
          new updateDate()
        ]
      })

    ]);




  }
});

