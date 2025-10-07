import React, { useEffect, useState } from 'react';
import { FormControl, InputLabel, Select, MenuItem } from '@mui/material';
import API from '../services/api';

export default function VehicleDropdown() {
  const [vehicles, setVehicles] = useState([]);
  const [selected, setSelected] = useState('');

  useEffect(() => {
    API.get('vehicles/dropdown/')
      .then(res => setVehicles(res.data))
      .catch(err => console.error('Dropdown error:', err));
  }, []);

  return (
    <FormControl fullWidth>
      <InputLabel>Select Vehicle</InputLabel>
      <Select value={selected} onChange={(e) => setSelected(e.target.value)}>
        {vehicles.map(v => (
          <MenuItem key={v.id} value={v.id}>
            {v.make} {v.model} ({v.year})
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}
