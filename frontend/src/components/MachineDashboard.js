// src/components/MachineDashboard.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MachineChart from './MachineChart';

const MachineDashboard = () => {
  const [measurements, setMeasurements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMeasurements = async () => {
      try {
        // Use the environment variable set in Docker Compose (REACT_APP_API_URL)
        const baseURL = process.env.REACT_APP_API_URL || '';
        // Specify the machine name as required by the backend endpoint
        const machineName = "DrillingMachine";
        // Call the endpoint with the machine_name query parameter
        const response = await axios.get(`${baseURL}/api/machine-data?machine_name=${machineName}`);
        // The backend is expected to return an object like { data: [...] }
        setMeasurements(response.data.data);
      } catch (err) {
        console.error("Error fetching measurements:", err);
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchMeasurements();
  }, []);

  if (loading) return <div>Loading machine data...</div>;
  if (error) return <div>Error loading machine data: {error.message}</div>;

  // Group measurements by topic so that each chart shows one topic's data.
  const groupedData = measurements.reduce((acc, measurement) => {
    const topic = measurement.topic;
    if (!acc[topic]) {
      acc[topic] = [];
    }
    acc[topic].push(measurement);
    return acc;
  }, {});

  return (
    <div style={dashboardStyle}>
      {Object.entries(groupedData).map(([topic, data]) => (
        <div key={topic} style={chartContainerStyle}>
          <MachineChart topic={topic} measurements={data} />
        </div>
      ))}
    </div>
  );
};

// Simple grid layout styles
const dashboardStyle = {
  display: 'grid',
  gridTemplateColumns: '1fr 1fr',
  gap: '20px',
  padding: '20px',
};

const chartContainerStyle = {
  border: '1px solid #ccc',
  borderRadius: '8px',
  padding: '10px',
  backgroundColor: '#fff',
};

export default MachineDashboard;
