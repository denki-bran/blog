'use strict';
import express from 'express';
const app = express();
let port = 3000;
app.get('/', function (req, res) {
    res.send('Hello World!');
});

app.listen(port, () => {
    console.log('Server start:', port);
});

