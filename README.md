# cityglow api


## twilio config

### logic

functions and assets > services

#### /main

```
exports.handler = function(context, event, callback) {
  let twiml = new Twilio.twiml.VoiceResponse();
  twiml.dial({timeout: 15, action: '/vapi', method: 'POST'}, '+16192189260');
  return callback(null, twiml);
};
```

#### /vapi

```
exports.handler = function(context, event, callback) {
  let twiml = new Twilio.twiml.VoiceResponse();
  twiml.dial({timeout: 5, action: '/message', method: 'POST'}, '+15313009677');
  twiml.hangup();

  return callback(null, twiml);
};
```

#### /message

```
exports.handler = function(context, event, callback) {
  let twiml = new Twilio.twiml.VoiceResponse();
  twiml.dial('+16192189260'); // if vapi ai not available, return to original phone and let it go to voice message
  return callback(null, twiml);
};
```

### active phone numbers

configure to use webhook, .. , function

### twilML app (deprecated??)

Voice Configuration > Request URL

https://medspa-test-3053.twil.io/main

replace with URL assigned under services


## vapi 

### setup

1. create assistant
2. assign number to assistant
3. set up server URL

### local


1. forward calls

ngrok http 4242

https://eccf5589f22d.ngrok-free.app -> http://localhost:424
^ enter this as server URL in vapi messages under assistant config


vapi listen --forward-to localhost:8000/calls/vapi-webhook/

## elevenlabs

1. settings > post-call webhook
2. agent > anaylsis > data collection (name)
