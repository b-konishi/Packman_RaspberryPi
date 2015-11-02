var WebSocketServer = require('ws').Server,
    wss = new WebSocketServer({port: 8080}),
    fs = require("fs");
wss.on('connection', function(ws) {
  ws.on('message', function(message) {
  //  console.log('%s', message);
    fs.writeFileSync("../sample.txt", message);
    /*if (message.length) {
      ws.send('comed');
    }*/

  });
});
