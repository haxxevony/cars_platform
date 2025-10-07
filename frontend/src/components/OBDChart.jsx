import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import API from '../services/api';

export default function OBDChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get('obd/chart/')
      .then(res => {
        const chartData = Object.entries(res.data).map(([key, value]) => ({
          severity: key,
          count: value
        }));
        setData(chartData);
      })
      .catch(err => console.error('Chart error:', err));
  }, []);

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <XAxis dataKey="severity" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="count" fill="#1976d2" />
      </BarChart>
    </ResponsiveContainer>
  );
}
