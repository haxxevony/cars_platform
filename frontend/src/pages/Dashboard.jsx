import { useEffect, useState } from 'react';
import API from '../services/api';
import {
  LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

export default function Dashboard() {
  const [user, setUser] = useState(null);
  const [metadata, setMetadata] = useState({ makes: [], models: [], years: [] });
  const [selected, setSelected] = useState({ make: '', model: '', year: '' });
  const [fuseBox, setFuseBox] = useState([]);
  const [sensorData, setSensorData] = useState([]);

  useEffect(() => {
    API.get('users/')
      .then((res) => setUser(res.data[0]))
      .catch((err) => console.error('User fetch error:', err));

    API.get('metadata/')
      .then((res) => setMetadata(res.data))
      .catch((err) => console.error('Metadata fetch error:', err));

    API.get('sensor-chart/')
      .then((res) => setSensorData(res.data))
      .catch((err) => console.error('Sensor chart fetch error:', err));
  }, []);

  const handleSelect = (field) => (e) => {
    setSelected((prev) => ({ ...prev, [field]: e.target.value }));
  };

  const fetchFuseBox = async () => {
    try {
      const res = await API.get('fusebox/', {
        params: {
          make: selected.make,
          model: selected.model,
          year: selected.year
        }
      });
      setFuseBox(res.data);
    } catch (err) {
      console.error('FuseBox fetch error:', err);
    }
  };

  const handleExport = (type) => {
    const token = localStorage.getItem('token');
    const url = `http://127.0.0.1:8000/api/export/${type}/?token=${token}`;
    window.open(url, '_blank');
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '900px', margin: 'auto' }}>
      <h2>Welcome to the Dashboard</h2>
      {user ? (
        <p>Logged in as: <strong>{user.username}</strong></p>
      ) : (
        <p>Loading user info...</p>
      )}

      <div style={{ marginTop: '2rem' }}>
        <h3>Select Vehicle</h3>

        <div style={{ marginBottom: '1rem' }}>
          <label>Make:</label>
          <select value={selected.make} onChange={handleSelect('make')} style={{ width: '100%', padding: '0.5rem' }}>
            <option value="">Select Make</option>
            {metadata.makes.map((make) => (
              <option key={make} value={make}>{make}</option>
            ))}
          </select>
        </div>

        <div style={{ marginBottom: '1rem' }}>
          <label>Model:</label>
          <select value={selected.model} onChange={handleSelect('model')} style={{ width: '100%', padding: '0.5rem' }}>
            <option value="">Select Model</option>
            {metadata.models.map((model) => (
              <option key={model} value={model}>{model}</option>
            ))}
          </select>
        </div>

        <div style={{ marginBottom: '1rem' }}>
          <label>Year:</label>
          <select value={selected.year} onChange={handleSelect('year')} style={{ width: '100%', padding: '0.5rem' }}>
            <option value="">Select Year</option>
            {metadata.years.map((year) => (
              <option key={year} value={year}>{year}</option>
            ))}
          </select>
        </div>

        <button onClick={fetchFuseBox} disabled={!selected.make || !selected.model || !selected.year}>
          Lookup Fuse Box
        </button>

        {fuseBox.length > 0 && (
          <div style={{ marginTop: '2rem' }}>
            <h4>Fuse Box Results</h4>
            {fuseBox.map((item, index) => (
              <div key={index} style={{ marginBottom: '1rem', padding: '1rem', border: '1px solid #ccc' }}>
                <p><strong>Location:</strong> {item.location}</p>
                {item.diagram_url && (
                  <p>
                    <strong>Diagram:</strong>{' '}
                    <a href={item.diagram_url} target="_blank" rel="noopener noreferrer">
                      View Diagram
                    </a>
                  </p>
                )}
                {item.notes && <p><strong>Notes:</strong> {item.notes}</p>}
              </div>
            ))}
          </div>
        )}
      </div>

      {sensorData.length > 0 && (
        <div style={{ marginTop: '3rem' }}>
          <h3>Sensor Data Chart</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={sensorData}>
              <XAxis dataKey="timestamp" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="value" stroke="#8884d8" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      <div style={{ marginTop: '3rem', display: 'flex', gap: '1rem' }}>
        <button onClick={() => handleExport('csv')}>
          Download CSV
        </button>
        <button onClick={() => handleExport('pdf')}>
          Download PDF
        </button>
      </div>
    </div>
  );
}
