import { useWebSocket } from './hooks/useWebSocket';
import './App.css';

function App() {
  const { appState, isConnected, videoFrame } = useWebSocket();

  return (
    <div className="container">
      <header>
        <h1>Instalación InfoVis 🎧</h1>
        <div className={`status ${isConnected ? 'online' : 'offline'}`}>
          Backend: {isConnected ? 'Conectado 🟢' : 'Desconectado 🔴'}
        </div>
      </header>

      <main className="dashboard">
        {/* Cámara en Vivo */}
        <section className="camera-feed" style={{ marginBottom: '20px' }}>
          <h2>Cámara en Vivo 📷</h2>
          {videoFrame ? (
            <img 
              src={`data:image/jpeg;base64,${videoFrame}`} 
              alt="Feed de visión" 
              style={{ width: '100%', maxWidth: '640px', borderRadius: '8px', border: '2px solid #555' }}
            />
          ) : (
            <div style={{ height: '360px', maxWidth: '640px', backgroundColor: '#222', color: '#aaa', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '8px', border: '2px dashed #444' }}>
              Esperando señal de video desde Python...
            </div>
          )}
        </section>

        {/* Tarjetas de Datos */}
        <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
          <section className="card" style={{ flex: '1', minWidth: '250px', padding: '20px', backgroundColor: '#1e1e1e', borderRadius: '8px' }}>
            <h2>País Seleccionado</h2>
            <p className="value" style={{ fontSize: '1.5em', fontWeight: 'bold', color: '#4CAF50' }}>
              {appState.country ? appState.country : "Buscando..."}
            </p>
          </section>

          <section className="card" style={{ flex: '1', minWidth: '250px', padding: '20px', backgroundColor: '#1e1e1e', borderRadius: '8px' }}>
            <h2>Género Musical</h2>
            <p className="value" style={{ fontSize: '1.5em', fontWeight: 'bold', color: '#2196F3' }}>
              {appState.genre ? appState.genre : "Ningún disco detectado"}
            </p>
          </section>
        </div>
      </main>

      <footer className="debug-info" style={{ marginTop: '40px', padding: '10px', borderTop: '1px solid #333', fontSize: '0.9em', color: '#888' }}>
        <p>Debug Visión ➔ X: {appState.rawPointer?.x?.toFixed(2)} | Y: {appState.rawPointer?.y?.toFixed(2)}</p>
      </footer>
    </div>
  );
}

export default App;