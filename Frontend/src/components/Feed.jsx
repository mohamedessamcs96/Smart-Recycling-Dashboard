// Feed.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import ItemModal from "./ItemModal";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function Feed({ filters }) {
  const [items, setItems] = useState([]);
  const [selectedId, setSelectedId] = useState(null);

  const fetchItems = async () => {
    try {
      const res = await axios.get(`${API}/items`, { params: filters });
      setItems(res.data);
    } catch (e) {
      console.error("fetchItems", e);
    }
  };

  useEffect(() => {
    fetchItems();
    const t = setInterval(fetchItems, 3000);
    return () => clearInterval(t);
  }, [filters]);

  return (
    <section className="feed-main">
      <h2>♻️ Live Feed</h2>
      <div className="feed-grid">
        {items.map((it) => (
          <div
            key={it.id}
            className="feed-item"
            onClick={() => setSelectedId(it.id)}
          >
            <img src={`${API}${it.image_path}`} alt={it.type} />
            <p>
              <strong>{it.type}</strong> / {it.brand}
            </p>
            <p>{(it.confidence * 100).toFixed(0)}%</p>
            <span className={`badge ${it.decision.toLowerCase()}`}>
              {it.decision}
            </span>
          </div>
        ))}
      </div>

      {selectedId && (
        <ItemModal id={selectedId} onClose={() => setSelectedId(null)} />
      )}
    </section>
  );
}
