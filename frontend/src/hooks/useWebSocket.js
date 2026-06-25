import { useEffect, useState } from 'react';
import { io } from 'socket.io-client';

const SOCKET_SERVER_URL = 'http://localhost:3000';

export const useWebSocket = () => {
  // 1. Todos los estados ADENTRO de la función
  const [appState, setAppState] = useState({
    country: null,
    genre: null,
    rawPointer: { x: 0, y: 0 }
  });
  const [isConnected, setIsConnected] = useState(false);
  const [videoFrame, setVideoFrame] = useState(null);

  useEffect(() => {
    const socket = io(SOCKET_SERVER_URL);

    socket.on('connect', () => setIsConnected(true));
    socket.on('disconnect', () => setIsConnected(false));

    // Escuchamos el estado ya procesado por el backend
    socket.on('app_state', (data) => {
      setAppState({
        country: data.country,
        genre: data.genre,
        rawPointer: data.pointer
      });
    });

    // Escuchamos el frame de video
    socket.on('video_frame', (frameData) => {
      setVideoFrame(frameData);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  return { appState, isConnected, videoFrame };
};