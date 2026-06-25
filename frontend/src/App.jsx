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

        {/* Cámara */}
        <section className="camera-feed" style={{ marginBottom: '20px' }}>
          <h2>Cámara en Vivo 📷</h2>

          {videoFrame ? (
            <img
              src={`data:image/jpeg;base64,${videoFrame}`}
              alt="Feed de visión"
              style={{
                width: '100%',
                maxWidth: '640px',
                borderRadius: '8px',
                border: '2px solid #555'
              }}
            />
          ) : (
            <div
              style={{
                height: '360px',
                maxWidth: '640px',
                backgroundColor: '#222',
                color: '#aaa',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                borderRadius: '8px',
                border: '2px dashed #444'
              }}
            >
              Esperando señal de video desde Python...
            </div>
          )}
        </section>

        {/* País + Género */}
        <div
          style={{
            display: 'flex',
            gap: '20px',
            flexWrap: 'wrap',
            marginBottom: '20px'
          }}
        >
          <section
            className="card"
            style={{
              flex: '1',
              minWidth: '250px',
              padding: '20px',
              backgroundColor: '#1e1e1e',
              borderRadius: '8px'
            }}
          >
            <h2>País Seleccionado</h2>

            <p
              className="value"
              style={{
                fontSize: '1.5em',
                fontWeight: 'bold',
                color: '#4CAF50'
              }}
            >
              {appState.country || "Buscando..."}
            </p>
          </section>

          <section
            className="card"
            style={{
              flex: '1',
              minWidth: '250px',
              padding: '20px',
              backgroundColor: '#1e1e1e',
              borderRadius: '8px'
            }}
          >
            <h2>Género Musical</h2>

            <p
              className="value"
              style={{
                fontSize: '1.5em',
                fontWeight: 'bold',
                color: '#2196F3'
              }}
            >
              {appState.genre || "Ningún disco detectado"}
            </p>
          </section>
        </div>

        {/* Información Musical */}
        <section
          className="card"
          style={{
            padding: '20px',
            backgroundColor: '#1e1e1e',
            borderRadius: '8px'
          }}
        >
          {appState.music ? (
            <>
              <h2>
                Top 10 de {appState.genre} en {appState.country}
              </h2>

              <p style={{ marginBottom: '10px' }}>
                <strong>Total Streams:</strong>{' '}
                {appState.music.total_streams.toLocaleString()}
              </p>

              {appState.music.is_mock && (
                <p style={{ color: '#ff9800' }}>
                  ⚠ Datos simulados
                </p>
              )}

              <table
                style={{
                  width: '100%',
                  borderCollapse: 'collapse',
                  marginTop: '20px'
                }}
              >
                <thead>
                  <tr style={{ borderBottom: '1px solid #555' }}>
                    <th style={{ textAlign: 'left', padding: '8px' }}>#</th>
                    <th style={{ textAlign: 'left', padding: '8px' }}>Canción</th>
                    <th style={{ textAlign: 'left', padding: '8px' }}>Artista</th>
                    <th style={{ textAlign: 'right', padding: '8px' }}>Streams</th>
                  </tr>
                </thead>

                <tbody>
                  {appState.music.top_10?.map((song, index) => (
                    <tr key={index} style={{ borderBottom: '1px solid #333' }}>
                      <td style={{ padding: '8px' }}>{index + 1}</td>

                      <td style={{ padding: '8px' }}>
                        {song.name}
                      </td>

                      <td style={{ padding: '8px' }}>
                        {song.artist}
                      </td>

                      <td
                        style={{
                          padding: '8px',
                          textAlign: 'right'
                        }}
                      >
                        {song.streams.toLocaleString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
          ) : (
            <>
              <h2>Información Musical</h2>

              <p style={{ color: '#999' }}>
                Selecciona un país y un género para visualizar el Top 10 de canciones.
              </p>
            </>
          )}
        </section>
      </main>

      <footer
        className="debug-info"
        style={{
          marginTop: '40px',
          padding: '10px',
          borderTop: '1px solid #333',
          fontSize: '0.9em',
          color: '#888'
        }}
      >
        <p>
          Debug Visión ➔ X: {appState.rawPointer?.x?.toFixed(2)} | Y:{' '}
          {appState.rawPointer?.y?.toFixed(2)}
        </p>
      </footer>
    </div>
  );
}

export default App;