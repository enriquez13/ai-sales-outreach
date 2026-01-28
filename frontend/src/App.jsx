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

  // --- FUNCIÓN 1: ENVIAR EMAIL (Mailto) ---
const handleSendEmail = (lead, message) => {
  if (!lead) return;
  
  // Fijamos el asunto exactamente como lo pides
  // Usamos el nombre de la empresa que viene del lead + el texto fijo
  const subject = `${lead.company} & Delfia (Observabilidade)`;
    
  // Construimos el link mailto con el nuevo asunto fijo
  const mailtoLink = `mailto:${lead.email || ''}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(message)}`;
  
  // Abrimos Outlook automáticamente
  window.location.href = mailtoLink;
  
  setEditingId(null);
};

  // --- FUNCIÓN 2: GENERAR CON IA ---
  const handleGenerate = async (lead) => {
    if (editingId === lead.id) {
      setEditingId(null);
      return;
    }

    setEditingId(lead.id);
    setIsGenerating(true);
    setCustomMessage(""); 

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

  const renderCard = (l) => (
    <div key={l.id} className={`card ${editingId === l.id ? 'active' : ''}`}>
      <div className="card-content">
        <div className="card-info">
          <div className="name-row">
            <h2>{l.name}</h2>
            <span className={`status-badge ${l.stage === 'followup' ? 'followup' : 'new'}`}>
              {l.stage === "followup" ? "Follow-up" : "New"}
            </span>
          </div>
          <p className="company-name">{l.company}</p>
          {l.stage === "followup" && <p className="timer">🕒 5 days</p>}
        </div>
        
        <button 
          className={`action-button ${editingId === l.id ? 'open' : ''}`} 
          onClick={() => handleGenerate(l)}
          disabled={isGenerating && editingId === l.id}
        >
          {isGenerating && editingId === l.id ? (
            <div className="spinner"></div>
          ) : (
            <span className="bolt-icon">{editingId === l.id ? '✕' : '⚡'}</span>
          )}
        </button>
      </div>
    </div>
  );

  return (
    <div className="app-container">
      <header className="header">
        <div className="header-top">
          <div className="logo">
             <span className="logo-icon">🚀</span>
             <span>AI Sales Connect</span>
          </div>
          <div className="user-avatar">AE</div>
        </div>
        <div className="status-bar">
           <span>Gestión de Leads</span>
           <div className="toggle-mock"></div>
        </div>
      </header>

      <main className="main-content">
        <section className="category-section">
          <h3 className="section-title">
            Nuevos Prospectos 
            <span className="count-pill">{leads.filter(l => l.stage !== 'followup').length}</span>
          </h3>
          <div className="grid-inner">
            {leads.filter(l => l.stage !== 'followup').map(l => renderCard(l))}
          </div>
        </section>

        <section className="category-section">
          <h3 className="section-title">
            Seguimientos Pendientes
            <span className="count-pill">{leads.filter(l => l.stage === 'followup').length}</span>
          </h3>
          <div className="grid-inner">
            {leads.filter(l => l.stage === 'followup').map(l => renderCard(l))}
          </div>
        </section>
      </main>

      {/* MODAL CORREGIDO */}
      {editingId && (
        <div className="modal-overlay" onClick={() => setEditingId(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setEditingId(null)}>✕</button>
            
            {isGenerating ? (
              <div className="skeleton-container">
                <p className="loading-text">🪄 Llama 3 redactando...</p>
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
                  spellCheck="false"
                />
                <div className="btn-group-modal">
                  <button 
                    className="btn-send-modal" 
                    onClick={() => handleSendEmail(leads.find(l => l.id === editingId), customMessage)}
                  >
                    📧 Enviar vía Outlook
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;