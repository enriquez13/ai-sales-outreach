import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [leads, setLeads] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [customMessage, setCustomMessage] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);

  const API_URL = "https://ai-sales-outreach-6umb.onrender.com";

  useEffect(() => {
    fetch(`${API_URL}/leads`)
      .then(res => res.json())
      .then(setLeads)
      .catch(err => console.error("Error inicial:", err));
  }, []);

  const handleGenerate = async (lead) => {
    setEditingId(lead.id);
    setIsGenerating(true);
    setCustomMessage(""); // Limpiamos para mostrar el esqueleto

    const endpoint =
      lead.stage === "followup"
        ? `/generate/followup/${lead.id}`
        : `/generate/first/${lead.id}`;

    try {
      const res = await fetch(`${API_URL}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" }
      });
      if (!res.ok) throw new Error("Servidor ocupado");
      const data = await res.json();
      setCustomMessage(data.email);
    } catch (err) {
      setCustomMessage("❌ Error de conexión. Intenta nuevamente.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <div className="header-top">
          <div className="logo">
             <span className="logo-icon">🧠</span>
             <span>AI Sales Connect</span>
          </div>
          <div className="user-avatar">AE</div>
        </div>
        <div className="status-bar">
           <span>All Leads</span>
           <div className="toggle-mock"></div>
        </div>
      </header>

      <main className="grid">
        {leads.map(l => (
          <div key={l.id} className={`card ${editingId === l.id ? 'active' : ''}`}>
            <div className="card-content">
              <div className="card-info">
                <div className="name-row">
                  <h2>{l.name}</h2>
                  <span className={`status-badge ${l.stage}`}>
                    {l.stage === "followup" ? "Follow-up" : "New"}
                  </span>
                </div>
                <p className="company-name">{l.company}</p>
                {l.stage === "followup" && <p className="timer">🕒 5 days</p>}
              </div>
              
              <button 
                className="action-button" 
                onClick={() => handleGenerate(l)}
                disabled={isGenerating && editingId === l.id}
              >
                {isGenerating && editingId === l.id ? (
                  <div className="spinner"></div>
                ) : (
                  <span className="bolt-icon">⚡</span>
                )}
              </button>
            </div>

            {editingId === l.id && (
              <div className="editor-overlay">
                {isGenerating ? (
                  <div className="skeleton-container">
                    <div className="skeleton-line"></div>
                    <div className="skeleton-line"></div>
                    <div className="skeleton-line short"></div>
                  </div>
                ) : (
                  <div className="email-result">
                    <h3>AI-Crafted Email</h3>
                    <textarea
                      value={customMessage}
                      onChange={(e) => setCustomMessage(e.target.value)}
                    />
                    <div className="btn-group">
                      <button className="btn-cancel" onClick={() => setEditingId(null)}>Descartar</button>
                      <button className="btn-send" onClick={() => {alert("Copiado!"); setEditingId(null)}}>Copiar Email</button>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </main>
    </div>
  );
}

export default App;