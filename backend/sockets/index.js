const { processVisionData } = require('../services/mapper');

function setupSockets(io) {
  io.on('connection', (socket) => {
    console.log(`🔌 Nueva conexión frontend/vision: ${socket.id}`);

    // Escucha los datos matemáticos que vienen desde Python
    socket.on('vision_data', (data) => {
      const { x, y } = data.pointer;
      const genreId = data.genreId;

      // Procesamos los datos crudos a través de nuestro servicio
      const appState = processVisionData(x, y, genreId);

      // Emitimos el estado ya procesado hacia React
      io.emit('app_state', appState);
    });

    // NUEVO: Escucha el frame de video en Base64 y lo retransmite a la web
    socket.on('video_frame', (base64Image) => {
      // broadcast emite a todos los clientes conectados EXCEPTO al que envió el mensaje
      socket.broadcast.emit('video_frame', base64Image);
    });

    socket.on('disconnect', () => {
      console.log(`❌ Se desconectó: ${socket.id}`);
    });
  });
}

module.exports = setupSockets;