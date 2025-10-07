import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import axios from 'axios';
import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer
} from 'recharts';

// 🔐 Login Component
function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://127.0.0.1:8000/api/auth/token/', {
        username,
        password
      });

      const { access, refresh } = res.data;
      localStorage.setItem('token', access);
      localStorage.setItem('refresh', refresh);

      const payload = JSON.parse(atob(access.split('.')[1]));
      localStorage.setItem('role', payload.role || 'guest');

      navigate('/dashboard');
    } catch (err) {
      alert('Login failed');
    }
  };

  return (
    <form onSubmit={handleLogin} style={{ padding: '2rem' }}>
      <h2>Login</h2>
      <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} required /><br /><br />
      <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required /><br /><br />
      <button type="submit">Login</button>
    </form>
  );
}

// 📊 Dashboard Component
function Dashboard() {
  const [metadata, setMetadata] = useState([]);
  const [sensorData, setSensorData] = useState([]);
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');

  useEffect(() => {
    if (token) {
      axios.get('http://127.0.0.1:8000/metadata/', {
        headers: { Authorization: `Bearer ${token}` }
      }).then(res => setMetadata(res.data));

      axios.get('http://127.0.0.1:8000/sensor-chart/', {
        headers: { Authorization: `Bearer ${token}` }
      }).then(res => setSensorData(res.data));
    }
  }, [token]);

  const handleExport = (type) => {
    const url = `http://127.0.0.1:8000/export/${type}/?token=${token}`;
    window.open(url, '_blank');
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Welcome, {role}</h2>

      <h3>Vehicle Metadata</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={metadata}>
          <XAxis dataKey="year" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="make" stroke="#8884d8" />
        </LineChart>
      </ResponsiveContainer>

      <h3>Sensor Readings</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={sensorData}>
          <XAxis dataKey="timestamp" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="value" stroke="#82ca9d" />
        </LineChart>
      </ResponsiveContainer>

      <br />
      <button onClick={() => handleExport('csv')}>📤 Export CSV</button>
      <button onClick={() => handleExport('pdf')} style={{ marginLeft: '1rem' }}>🧾 Export PDF</button>
    </div>
  );
}

// 🧭 App Router
function App() {
  const token = localStorage.getItem('token');
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={token ? <Dashboard /> : <Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;
