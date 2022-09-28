```bash
docker-compose up -d
```

Default channel: `signal`

```bash
curl --location --request POST '127.0.0.1:8088/api/message/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "bla-bla-bla": "asdasdassd",
    "type": "connect"
}'
```

```javascript
var Centrifuge = require("centrifuge")
var jwt = require('jsonwebtoken');
var token = jwt.sign({ sub: 'dalongdemo'}, '05f0842d-c302-4036-a19f-6ac263b9f620');
const centrifuge = new Centrifuge('ws://127.0.0.1:8089/connection/websocket');
centrifuge.setToken(token)
centrifuge.subscribe("signal", function(message) {
    console.log(message);
});
centrifuge.connect();
```
