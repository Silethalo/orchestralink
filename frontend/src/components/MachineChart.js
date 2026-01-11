// src/components/MachineChart.js

import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const MachineChart = ({ topic, measurements }) => {
  // Sort measurements by timestamp to ensure the chart is drawn correctly
  const sortedMeasurements = measurements.slice().sort(
    (a, b) => new Date(a.timestamp) - new Date(b.timestamp)
  );

  const labels = sortedMeasurements.map((m) =>
    new Date(m.timestamp).toLocaleTimeString()
  );
  const dataPoints = sortedMeasurements.map((m) => m.value);

  // Retrieve the unit from the first measurement (assuming all values for a topic share the same unit)
  const unit = sortedMeasurements[0]?.unit || '';

  const data = {
    labels,
    datasets: [
      {
        label: `${topic} (${unit})`,
        data: dataPoints,
        fill: false,
        backgroundColor: 'rgba(75,192,192,0.4)',
        borderColor: 'rgba(75,192,192,1)',
        tension: 0.1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: {
        display: true,
        text: `${topic} Data`,
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Time',
        },
      },
      y: {
        title: {
          display: true,
          text: `Value (${unit})`,
        },
      },
    },
  };

  return <Line data={data} options={options} />;
};

export default MachineChart;
