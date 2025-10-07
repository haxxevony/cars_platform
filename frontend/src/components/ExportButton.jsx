import React from 'react';
import { Button } from '@mui/material';

export default function ExportButton() {
  const handleExport = () => {
    window.open('http://127.0.0.1:8000/api/obd/export/', '_blank');
  };

  return (
    <Button variant="outlined" onClick={handleExport}>
      Export Diagnostics CSV
    </Button>
  );
}
