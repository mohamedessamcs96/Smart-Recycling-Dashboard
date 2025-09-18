// App.jsx
import React, { useState, useEffect } from "react";
import Feed from "./components/Feed";
import Upload from "./components/Upload";
import Filters from "./components/Filters";
import Stats from "./components/Stats"; // chart component
import axios from "axios";
import "./App.css";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function App() {
  const [filters, setFilters] = useState({});
  const [reloadKey, setReloadKey] = useState(0);
  const [stats, setStats] = useState({
    by_type: {},
    by_brand: {},
    accept: 0,
    reject: 0,
  });

  const fetchStats = async () => {
    try {
      const r = await axios.get(`${API}/stats`);
      setStats(r.data);
    } catch (e) {
      console.error("fetchStats", e);
    }
  };

  useEffect(() => {
    fetchStats();
    const t = setInterval(fetchStats, 3000);
    return () => clearInterval(t);
  }, []);

  return (
    <div className="app-container">
      <h1 className="app-title"> Smart Recycling Dashboard</h1>

      {/* Upload + Filters */}
      <div className="controls">
        <Upload onDone={() => setReloadKey((k) => k + 1)} />
        <Filters onChange={setFilters} />
      </div>

      {/* Dashboard */}
      <div className="feed-wrapper">
        {/* Live Feed */}
        <div className="feed-grid">
          <Feed key={reloadKey} filters={filters} />
        </div>

        {/* Stats sidebar */}
        <aside className="feed-stats">
          <h2> Stats</h2>
          <Stats stats={stats} />
        </aside>
      </div>
    </div>
  );
}
