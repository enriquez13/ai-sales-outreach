import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [leads, setLeads] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [customMessage, setCustomMessage] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);

  const API_URL = "https://ai-sales-outreach-production.up.railway.app";

// CORRECCIÓN DE SEGURIDAD PARA .FILTER
useEffect(() => {
  fetch(`${API_URL}/leads`)
    .then(res => {
      if (!res.ok) throw new Error("Backend no responde");
      return res.json();
    })
    .then(data => {
      // Forzamos que sea un array para que .filter no rompa la app
      setLeads(Array.isArray(data) ? data : []);
    })
    .catch(err => {
      console.error("Error:", err);
      setLeads([]); // Si hay error, lista vacía
    });
}, []);

  // --- FUNCIÓN 1: ENVIAR EMAIL (Mailto) ---
const handleSendEmail = async (lead, message) => {
  if (!lead) return;
  
  const subject = `${lead.company} & Delfia (Observabilidade)`;
  const mailtoLink = `mailto:${lead.email || ''}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(message)}`;
  
  // Abrimos el correo
  window.location.href = mailtoLink;

  try {
    // Llamamos al backend para completar la etapa
    const res = await fetch(`${API_URL}/leads/${lead.id}/complete`, { method: "PATCH" });
    const data = await res.json();

    if (res.ok) {
      // ACTUALIZACIÓN MAESTRA:
      // Usamos 'data.lead' que viene del servidor (ya trae el nuevo stage: negotiation)
      setLeads(prev => prev.map(l => l.id === lead.id ? { ...l, ...data.lead } : l));
    }
  } catch (err) {
    console.error("Error al actualizar estado:", err);
  }
  
  setEditingId(null);
};

const formatLastSent = (dateStr) => {
  if (!dateStr) return "";
  const date = new Date(dateStr);
  const now = new Date();
  
  const isToday = date.toDateString() === now.toDateString();
  const options = { hour: '2-digit', minute: '2-digit' };
  const time = date.toLocaleTimeString([], options);

  if (isToday) return `Enviado hoje às ${time}`;
  
  const dayOptions = { day: 'numeric', month: 'short' };
  return `Enviado em ${date.toLocaleDateString([], dayOptions)} às ${time}`;
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
        ? `{API_URL}/generate/followup/${lead.id}`
        : `{API_URL}/generate/first/${lead.id}`;

    try {
      const res = await fetch(endpoint, {
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

  useEffect(() => {
  const loadLeads = () => {
    fetch(`${API_URL}/leads`)
      .then(res => res.json())
      .then(setLeads)
      .catch(err => console.error("Error:", err));
  };

  loadLeads(); // Carga inicial

  // REFRESCO INTELIGENTE: Se activa al volver a la pestaña o cambiar de app
  window.addEventListener("focus", loadLeads);
  
  return () => window.removeEventListener("focus", loadLeads);
}, []);

  const renderCard = (l) => (
    <div key={l.id} className={`card ${editingId === l.id ? 'active' : ''}`}>
      <div className="card-content">
        <div className="card-info">
          <div className="name-row">
            <h2>{l.name}</h2>
            {/* Actualizamos los colores de las etiquetas aquí */}
            <span className={`status-badge ${l.stage}`}>
              {l.stage === "followup" ? "Follow-up" : l.stage === "negotiation" ? "Negociação" : "New"}
            </span>
          </div>
          <p className="company-name">{l.company}</p>
          
          <div className="status-row">
            {/* EL TIMER: Solo se ve en Follow-up */}
            {l.stage === "followup" && (
              <p className="timer">
                🕒 {l.days_left !== undefined ? `Prossiga em ${l.days_left} dias` : "Calculando..."}
              </p>
            )}

            {/* EL BADGE DE ENVÍO: Se ve en Follow-up Y en Negociación */}
            {l.sent_at && (
              <span className="sent-badge">
                ✓ {formatLastSent(l.sent_at)}
              </span>
            )}
          </div>
        </div>
        
        {/* BOTÓN DE ACCIÓN: Solo lo mostramos si NO está en negociación (opcional) */}
        {l.stage !== "negotiation" && (
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
        )}
      </div>
    </div>
  );

  return (
    <div className="app-container">
      <header className="header">
        <div className="header-top">
          <div className="logo">
             <span className="logo-icon">🚀</span>
             <span>Conexão de Vendas com IA</span>
          </div>
          <div className="user-avatar">AE</div>
        </div>
        <div className="status-bar">
           <span>Gestão de Leads</span>
           <div className="toggle-mock"></div>
        </div>
      </header>

      <main className="main-content">
        {/* CONTENEDOR 1: NEW LEADS */}
        <section className="category-section">
  <h3 className="section-title">
    Nuevos Prospectos 
    <span className="count-pill">
      {leads.filter(l => l.stage === 'new').length}
    </span>
  </h3>
  <div className="grid-inner">
    {leads.filter(l => l.stage === 'new').map(l => renderCard(l))}
  </div>
</section>

        {/* CONTENEDOR 2: FOLLOW-UP */}
<section className="category-section">
  <h3 className="section-title">
    Seguimientos Pendientes
    <span className="count-pill">
      {leads.filter(l => l.stage === 'followup').length}
    </span>
  </h3>
  <div className="grid-inner">
    {leads.filter(l => l.stage === 'followup').map(l => renderCard(l))}
  </div>
</section>

{/* CONTENEDOR 3: EN NEGOCIACIÓN */}
<section className="category-section">
  <h3 className="section-title">
    Em Negociação 🤝
    <span className="count-pill">
      {leads.filter(l => l.stage === 'negotiation').length}
    </span>
  </h3>
  <div className="grid-inner">
    {leads.filter(l => l.stage === 'negotiation').map(l => renderCard(l))}
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
                <p className="loading-text">🪄 IA redactando...</p>
                <div className="skeleton-line"></div>
                <div className="skeleton-line"></div>
                <div className="skeleton-line short"></div>
              </div>
            ) : (
              <div className="email-result">
                <h3>Email Criado por IA</h3>
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
                    📧 Enviar por Email
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

