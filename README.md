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
var token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MiJ9.RXpppb6_o9lArotr7zSVC_muwlMAtUAxw9kfFX83nWg';
const centrifuge = new Centrifuge('ws://127.0.0.1:8089/connection/websocket');
centrifuge.setToken(token)
centrifuge.subscribe("signal", function(message) {
    console.log(message);
});
centrifuge.connect();
```
