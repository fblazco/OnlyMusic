import { useEffect, useState } from 'react';
import { io } from 'socket.io-client';

const SOCKET_SERVER_URL = 'http://localhost:3000';

export const useWebSocket = () => {
  // Estado de la aplicación
  const [appState, setAppState] = useState({
    country: null,
    genre: null,
    music: null,
    rawPointer: { x: 0, y: 0 }
  });

  const [isConnected, setIsConnected] = useState(false);
  const [videoFrame, setVideoFrame] = useState(null);

  useEffect(() => {
    const socket = io(SOCKET_SERVER_URL);

    socket.on('connect', () => {
      console.log('🟢 Conectado al backend');
      setIsConnected(true);
    });

    socket.on('disconnect', () => {
      console.log('🔴 Desconectado del backend');
      setIsConnected(false);
    });

    // Estado enviado por el backend
    socket.on('app_state', (data) => {
      console.log('Estado recibido:', data);

      setAppState({
        country: data.country,
        genre: data.genre,
        music: data.music,
        rawPointer: data.pointer
      });
    });

    // Video enviado desde Python
    socket.on('video_frame', (frameData) => {
      setVideoFrame(frameData);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  return {
    appState,
    isConnected,
    videoFrame
  };
};