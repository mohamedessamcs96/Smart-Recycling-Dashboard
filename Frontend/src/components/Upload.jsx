import React, { useState } from "react";
import axios from "axios";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function Upload({ onDone }) {
  const [file, setFile] = useState(null);
  const [uploaded, setUploaded] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      const res = await axios.post(`${API}/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setUploaded(res.data);
      onDone?.(res.data);
    } catch (err) {
      console.error(err);
      setUploaded({ type: "Error", brand: "", decision: "Upload failed" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="upload-form" onSubmit={handleUpload}>
      {/* Custom file input */}
      <label className="file-label">
        {file ? file.name : "Choose File"}
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setFile(e.target.files[0])}
        />
      </label>

      <button
        type="submit"
        className="upload-btn"
        disabled={loading || !file}
      >
        {loading ? "Uploading..." : "Upload"}
      </button>

      {uploaded && (
        <div className="upload-result">
          Uploaded: <strong>{uploaded.type}</strong> /{" "}
          <strong>{uploaded.brand}</strong> — {uploaded.decision}
        </div>
      )}
    </form>
  );
}
