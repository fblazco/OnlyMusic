const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const cors = require('cors');
const setupSockets = require('./sockets/index');

const app = express();
app.use(cors());

// Creamos el servidor HTTP y lo montamos con Socket.IO
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: "*", 
    methods: ["GET", "POST"]
  }
});

// Inicializamos la lógica de sockets
setupSockets(io);

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`🧠 Cerebro backend escuchando en el puerto ${PORT}`);
});