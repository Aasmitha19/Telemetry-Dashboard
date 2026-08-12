import { useEffect, useState } from "react";
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";
import "./App.css"; // We will create this file next for styling

function App() {
  const [metrics, setMetrics] = useState(null);
  const [history, setHistory] = useState([]); // Stores data over time for the graph

  useEffect(() => {
    const fetchData = () => {
      fetch("http://localhost:8000/metrics")
        .then((response) => response.json())
        .then((data) => {
          setMetrics(data);
          
          // Append new data to history, keeping only the last 10 readings for a smooth graph
          setHistory((prevHistory) => {
            const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
            const updatedHistory = [...prevHistory, { ...data, time: timestamp }];
            if (updatedHistory.length > 10) {
              return updatedHistory.slice(1); // Drop the oldest point
            }
            return updatedHistory;
          });
        })
        .catch((error) => {
          console.error("API Error:", error);
        });
    };

    fetchData(); // Fetch immediately on load
    const interval = setInterval(fetchData, 2000); // AUTOMATIC UPDATE EVERY 2 SECONDS

    return () => clearInterval(interval); // Clean up timer on exit
  }, []);

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Telemetry Dashboard</h1>
        <div className="pipeline-status">
          <span className="status-dot"></span> Pipeline Running
        </div>
      </header>

      {metrics && (
        <>
          {/* METRIC CARDS LAYOUT */}
          <div className="metrics-grid">
            <div className="metric-card fps-card">
              <h3>FPS</h3>
              <p className="metric-value">{metrics.fps}</p>
            </div>
            <div className="metric-card gpu-card">
              <h3>GPU Usage</h3>
              <p className="metric-value">{metrics.gpu_usage}%</p>
            </div>
            <div className="metric-card memory-card">
              <h3>GPU Memory</h3>
              <p className="metric-value">{metrics.gpu_memory} GB</p>
            </div>
            <div className="metric-card decoder-card">
              <h3>Decoder Usage</h3>
              <p className="metric-value">{metrics.decoder_usage}%</p>
            </div>
          </div>

          {/* GRAPHS USING RECHARTS */}
          <div className="graph-container">
            <h2>Live Performance Trends</h2>
            <div style={{ width: "100%", height: 300 }}>
              <ResponsiveContainer>
                <LineChart data={history} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                  <XAxis dataKey="time" stroke="#aaa" />
                  <YAxis stroke="#aaa" />
                  <Tooltip contentStyle={{ backgroundColor: "#222", border: "1px solid #444" }} />
                  <Legend />
                  <Line type="monotone" dataKey="fps" stroke="#4caf50" strokeWidth={3} name="FPS" activeDot={{ r: 8 }} />
                  <Line type="monotone" dataKey="gpu_usage" stroke="#2196f3" strokeWidth={3} name="GPU Usage (%)" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </>
      )}
      {!metrics && <p className="loading-text">Connecting to telemetry server...</p>}
    </div>
  );
}

export default App;