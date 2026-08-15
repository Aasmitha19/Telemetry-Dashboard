import React, { useEffect, useState } from 'react';

const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

export default function App() {
  const [backendStatus, setBackendStatus] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchStatus() {
      try {
        const response = await fetch(`${backendUrl}/status`);
        if (!response.ok) {
          throw new Error(`Backend returned ${response.status}`);
        }
        const data = await response.json();
        setBackendStatus(data);
      } catch (err) {
        setError(err.message);
      }
    }

    fetchStatus();
  }, []);

  return (
    <main style={{ fontFamily: 'Arial, sans-serif', padding: '2rem', maxWidth: '1000px', margin: '0 auto' }}>
      <h1>VisionEdge</h1>
      <p>Live object detection dashboard will appear here.</p>

      <div style={{ display: 'grid', gap: '1rem', gridTemplateColumns: 'minmax(320px, 1fr) minmax(320px, 1fr)', alignItems: 'start' }}>
        <section style={{ border: '1px solid #ddd', borderRadius: '12px', padding: '1rem' }}>
          <h2>Live preview</h2>
          <div style={{ marginBottom: '1rem', minHeight: '240px', background: '#f7f7f7', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <img
              src={`${backendUrl}/video_feed`}
              alt="Live camera preview"
              style={{ maxWidth: '100%', borderRadius: '8px' }}
              onError={() => setError('Unable to load live stream. Is the backend running?')}
            />
          </div>
          <p style={{ margin: 0, color: '#555' }}>
            Press <strong>q</strong> in the backend window to stop the stream.
          </p>
        </section>

        <section style={{ border: '1px solid #ddd', borderRadius: '12px', padding: '1rem' }}>
          <h2>Backend status</h2>
          {error ? (
            <p style={{ color: 'red' }}>{error}</p>
          ) : backendStatus ? (
            <div>
              <p><strong>Backend:</strong> {backendStatus.backend}</p>
              <p><strong>Backend ready:</strong> {String(backendStatus.backend_ready)}</p>
              <p><strong>Camera source:</strong> {backendStatus.camera_source}</p>
              <p><strong>Model path:</strong> {backendStatus.model_path ?? 'Not found'}</p>
              <p><strong>Model loaded:</strong> {String(backendStatus.model_loaded)}</p>
              {!backendStatus.model_loaded && (
                <p style={{ color: '#b04', marginTop: '0.75rem' }}>
                  No local model file was found. The backend will attempt to load the default YOLO model name, but detection will only work if the model can be downloaded or the file is present.
                </p>
              )}
              <p><strong>Video feed:</strong> <a href={`${backendUrl}/video_feed`} target="_blank" rel="noreferrer">Open stream</a></p>
              <p><strong>Detections API:</strong> <a href={`${backendUrl}/detections`} target="_blank" rel="noreferrer">Open JSON</a></p>
            </div>
          ) : (
            <p>Loading backend info…</p>
          )}
        </section>
      </div>
    </main>
  );
}
