import React, { useState } from 'react'

export default function Filters({ onChange }) {
  const [type, setType] = useState('')
  const [brand, setBrand] = useState('')
  const [decision, setDecision] = useState('')

  const apply = () => {
    const f = {}
    if (type) f.type = type
    if (brand) f.brand = brand
    if (decision) f.decision = decision
    onChange(f)
  }

  return (
    <div className="filters">
      <label>Type: </label>
      <select value={type} onChange={e => setType(e.target.value)}>
        <option value="">All</option>
        <option>Plastic</option>
        <option>Metal</option>
        <option>Paper</option>
      </select>

      <label style={{ marginLeft: 8 }}>Brand: </label>
      <select value={brand} onChange={e => setBrand(e.target.value)}>
        <option value="">All</option>
        <option>Pepsi</option>
        <option>Dasani</option>
        <option>Other</option>
      </select>

      <label style={{ marginLeft: 8 }}>Decision: </label>
      <select value={decision} onChange={e => setDecision(e.target.value)}>
        <option value="">All</option>
        <option>Accept</option>
        <option>Reject</option>
      </select>

      <button style={{ marginLeft: 8 }} onClick={apply}>Apply</button>
    </div>
  )
}
