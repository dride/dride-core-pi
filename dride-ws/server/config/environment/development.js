'use strict';

// Development specific configuration
// ==================================
module.exports = {
  seedDB: false,
  testAccount: {
  	phoneNumber: '0524624657',
  	uid: '0524624657'
  },
  firebase: {
  	databaseURL: "https://mego-e1507.firebaseio.com",
  	serviceAccount: {
					  "type": "service_account",
					  "project_id": "mego-e1507",
					  "private_key_id": "6c7376ab12aadf830badecbb26bfd12f3333cdbb",
					  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDH4QGE2Nvt97U7\np/YgOuuG5kXL6MIDbYAQjIY9hzE5KegH8Ykpb0e0E/pRwK7rovB92FU9+ZQmhVzn\nwi1KUZrVikeNrnGz+Qlg/NPf9PBdIe4bNnlg9twt9RA4RLev9hN8aJD2SMCzw11O\nW06tqWmFWFWE+D1L6W7sBtKkFB7Unizh9mHk0V47JwUs9LeDBd4iIb1b6f8Zhq9r\nzkgPk9zHQ9h+yHvkjxluxCfbEEL/ktKXZjmA8B9Rnpuq6oxHgWXqTvyjXt2XJ5C4\nWofZC1twVTNqD63TX1NSuD3FVnEhtyWQvwkLGL/3i/iax+WUia6dNOjt/rk661Za\nvcYh03xnAgMBAAECggEANMM8t2jXhZXiDYFlA1UKX23h9tXWgTkimTu/I/bQE5rw\nWUh1QK7TasHrTjFi+2jjuxSkS9vaM+D4iWVEt12bVctO4COweCXBSAz1kSUDXlJa\nnGxg1ivUK32JbpEVPCnlMu4Xdiv2Un2737dSqZ0S8dRDnvo4lBVm5n9Wk2GMUeuH\ngz2TrR07HmLnCnys/88hO/X4+XhEkUhQtNB/FzpuVQn4eQXCJXaiqtJ4xXun3XQN\nrR93gV7VVOpTJ97S/qfzwXstEXRIoea6Q8cwHbyHyCKuXP5AZZtA9q0aRrE/PwrN\nFc/AZVbEFU51I4bp2APxh0n7Q6tdf0Lms0BePJNnQQKBgQDzvHDP/WYS452qokJi\nsr9cA9C1Sdr2/x7zlQwWWjIwe3IYWxUHuzkg3LI5nOz8QpvBZHt8tMC5IHDANnIv\nLutHi6P6WDgrE1AJ341r5cLJ+eJRn4TtIT0kazwme5IXnvd6auGjbch+pvme2gVg\naPcC3JpURyq/uKjicjbabMe2HwKBgQDR76Rdevfeb8ZbtH1N0meFclHn0eCnt7ie\nOhAXMfSe3iJnuS8ObJCgiEll/H0qyKB75wR55lAXeN09Byy8E0ZaXjXVLk4ljKu5\nHzd5/aHdVdt+iHnc32tsX/duLubFHYCRvvqawG0PW06Kfyz77DZeo17wE7M5ktO8\nrls3R6MguQKBgGUi2kTTxtkrra6yKY2+0fyicKXpAXzgG73DKQLVZmILtyo4ER/m\nJixmp2WUohmCohK7WSpD7nxi46Y+cV72vxYu8Vnd5WCqYNnX81zEN/GLSMfJw2SK\nGE7WWF03hUVb5yDa3MntsfYr3wR1PynkJCsB0uAJr8liHGHqNqyn2q7NAoGAMCO3\nmQf9lrAi2ByHLzU0L9GLHpFt5oemegHudqMp6NQfJ5G7TJ9wep9F1XEUcp8WzdKn\noBxD+V3pvXjLtUTmOQqpZXz8xnd/WS/jVMHoQAzUDCvXZeKFi5Bl+IoguMqPFNyq\nMpo1Z/QUCoYnFo2P2hu0RXD/BBC7JOUGXaK7sWECgYEAmXg3eyvHt1gDvc1lqp9A\nCVXAIb1ro9q/yHj5v2OAOLsR+gOBDUwJ0ZCRsh5WCy66leXfSKBhvQaeOnvz8ZuI\nlnzJW/Fw9UECvWZnJHA9Ryr8pa29NdeUmfk/VbjeoyC+/kD33U2SduJqrqk/vQG0\nkcWBA5wO6t6OYv2vLuqMcZ8=\n-----END PRIVATE KEY-----\n",
					  "client_email": "firebase@mego-e1507.iam.gserviceaccount.com",
					  "client_id": "116242813295369134167",
					  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
					  "token_uri": "https://accounts.google.com/o/oauth2/token",
					  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
					  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase%40mego-e1507.iam.gserviceaccount.com"
					}
  },
  mixpanel: {
    token: 'e5a185f6cf4395045c0a097d5a0d9052'
  }
};

