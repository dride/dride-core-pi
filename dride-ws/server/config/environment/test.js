'use strict';

var request = require('supertest');

// Test specific configuration
// ===========================
module.exports = {
  testAccount: {
  	phoneNumber: '0524624657',
  	uid: '6b76b170-79ae-11e6-bd53-f76c7247d4cd',
  	token: getFreshToken('0524624657')
  },
  testAccount2: {
    phoneNumber: '0500000000',
    uid: '57a3a940-79af-11e6-a0f6-b10df89c7ea2',
    token: getFreshToken('0500000000')
  },
  testPO: {
    id: null
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

function getFreshToken(phone){

  if (phone == "0524624657")
    return 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjBhZDkxNzYzN2IzNjUzZTBjNjdlMGVhYWY0YTRlZTk1YjMxZTJkNGQifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vbWVnby1lMTUwNyIsImFkbWluIjp0cnVlLCJwaG9uZSI6IjA1MjQ2MjQ2NTciLCJhdWQiOiJtZWdvLWUxNTA3IiwiYXV0aF90aW1lIjoxNDczNzc3MjE4LCJ1c2VyX2lkIjoiNzlmOGU2YjAtNzliNy0xMWU2LWExZTYtZWQxOTU5MTlkNmNmIiwic3ViIjoiNzlmOGU2YjAtNzliNy0xMWU2LWExZTYtZWQxOTU5MTlkNmNmIiwiaWF0IjoxNDczNzc3NDE0LCJleHAiOjE0NzM3ODEwMTQsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnt9LCJzaWduX2luX3Byb3ZpZGVyIjoiY3VzdG9tIn19.VrTZJ1ccd35nDCB-5-qElCkHHkiBMB4FwUsba55htYzB3lpXM0jOnPtn0mDGUkqBmQmOxuG9inNqKNQolCmNv4FcaH0wsPR_L4gt0jgCY6pNVyU9GsW1_NM7Jb_T5fr9DGOr6T_mLHHeWSlC1p2alRGVgM92NeRS0InemCLCzJ-4h9Jly_iRwwT87YrRT71Xg9cDbpaQ6zNW_IvjqbeFsyAtN5gvlfQwMjdFcF1euJt--yX1ojjxHyEznInb1RFHnl8hJx9eX7t8UgO3QG0mRR_ef2UTNDEXFeXYUBZB8LvUU8dCWwfmxMjaJtf9TgrEwJDgJwXKD2U8f5yMwe1lgg';
  else
    return 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJjbGFpbXMiOnsiYWRtaW4iOmZhbHNlLCJwaG9uZSI6IjA1MDAwMDAwMDAifSwidWlkIjoiNTdhM2E5NDAtNzlhZi0xMWU2LWEwZjYtYjEwZGY4OWM3ZWEyIiwiaWF0IjoxNDczNzcwNzIzLCJleHAiOjE0NzM3NzQzMjMsImF1ZCI6Imh0dHBzOi8vaWRlbnRpdHl0b29sa2l0Lmdvb2dsZWFwaXMuY29tL2dvb2dsZS5pZGVudGl0eS5pZGVudGl0eXRvb2xraXQudjEuSWRlbnRpdHlUb29sa2l0IiwiaXNzIjoiZmlyZWJhc2VAbWVnby1lMTUwNy5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsInN1YiI6ImZpcmViYXNlQG1lZ28tZTE1MDcuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20ifQ.VncTrKp_dOvqoZfg624DcNjVeWLLGiHvrbDVK6E7zF6vFpDSpl6SFHJ4Kkh7PsXelRR7Eh9hy00LSfsIbX_wYGgvZlh6I6JInMwidgh8kgXx5CqHLgx2Jt50I9KVa8YZMDBEFOjro38X6KCX5c7PFcOYsaso_xrPA4vIHUUZa8tgJLBbZsfIVCLbiVjqHis28_Q36vjcNNPkXSqwWmMjMPc7w0ENE8cQqLyeePjmmbpuGfxH5D5d4r0CAdzMBKLizB_J8BzJTsb3xbgmMkTvlyjbuzyoEYYKY_Dj8lQ797QT9NtgkKvP6uDTEPBKefqKO0Ufwb6TTsco1j5TiTYQvg';
}
