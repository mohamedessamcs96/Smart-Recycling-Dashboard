import React, { useEffect, useState } from 'react'
import axios from 'axios'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function ItemModal({ id, onClose }) {
  const [item, setItem] = useState(null)

  useEffect(() => {
    const load = async () => {
      try {
        const r = await axios.get(`${API}/items/${id}`)
        setItem(r.data)
      } catch (e) {
        console.error(e)
      }
    }
    load()
  }, [id])

  if (!item) return <div className="modal">Loading...</div>

  return (
    <div className="modal">
      <button onClick={onClose} style={{ float: 'right' }}>Close</button>
      <h3>Item #{item.id}</h3>
      <img src={`${API}${item.image_path}`} alt="" style={{ width: 300 }} />
      <p><strong>Type:</strong> {item.type} ({(item.confidence*100).toFixed(0)}%)</p>
      <p><strong>Brand:</strong> {item.brand}</p>
      <p><strong>Decision:</strong> {item.decision}</p>
      <p><strong>Reasoning:</strong> {item.reasoning}</p>
      <p><strong>Model Meta:</strong> <code>{JSON.stringify(item.model_meta)}</code></p>
    </div>
  )
}
