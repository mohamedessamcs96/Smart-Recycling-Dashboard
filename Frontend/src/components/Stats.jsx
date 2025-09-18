import React, { useEffect, useState } from "react";
import axios from "axios";

// Chart.js + React wrapper
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

// Register needed Chart.js components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function Stats() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    axios
      .get("http://localhost:8000/stats")
      .then((res) => setStats(res.data))
      .catch((err) => console.error("Stats fetch failed:", err));
  }, []);

  if (!stats) return null;

  // Overall chart (accept/reject)
  const overallData = {
    labels: ["Accepted", "Rejected"],
    datasets: [
      {
        label: "Items",
        data: [stats.accept, stats.reject],
        backgroundColor: ["#34d399", "#f87171"], // green & red
        borderRadius: 8,
      },
    ],
  };

  // By Type chart
  const typeData = {
    labels: Object.keys(stats.by_type || {}),
    datasets: [
      {
        label: "By Type",
        data: Object.values(stats.by_type || {}),
        backgroundColor: "#60a5fa", // blue
        borderRadius: 8,
      },
    ],
  };

  // By Brand chart
  const brandData = {
    labels: Object.keys(stats.by_brand || {}),
    datasets: [
      {
        label: "By Brand",
        data: Object.values(stats.by_brand || {}),
        backgroundColor: "#fbbf24", // amber
        borderRadius: 8,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { display: false },
      title: {
        display: true,
        color: "#064420",
        font: { size: 16, weight: "bold" },
      },
    },
    scales: {
      x: {
        ticks: { color: "#064420", font: { weight: "600" } },
        grid: { display: false },
      },
      y: {
        beginAtZero: true,
        ticks: { color: "#064420" },
        grid: { color: "rgba(0,0,0,0.05)" },
      },
    },
  };

  return (
    <div className="stats-column">
      {/* Overall */}
      <section className="card">
        <h2>📊 Recycling Stats</h2>
        <Bar data={overallData} options={{ ...options, plugins: { ...options.plugins, title: { ...options.plugins.title, text: "Accepted vs Rejected" } } }} />
      </section>

      {/* By Type */}
      <section className="card">
        <h3>By Type</h3>
        <ul>
          {Object.entries(stats.by_type || {}).map(([k, v]) => (
            <li key={k}>
              {k}: {v}
            </li>
          ))}
        </ul>
        <Bar data={typeData} options={{ ...options, plugins: { ...options.plugins, title: { ...options.plugins.title, text: "Items by Type" } } }} />
      </section>

      {/* By Brand */}
      <section className="card">
        <h3>By Brand</h3>
        <ul>
          {Object.entries(stats.by_brand || {}).map(([k, v]) => (
            <li key={k}>
              {k}: {v}
            </li>
          ))}
        </ul>
        <Bar data={brandData} options={{ ...options, plugins: { ...options.plugins, title: { ...options.plugins.title, text: "Items by Brand" } } }} />
      </section>
    </div>
  );
}
