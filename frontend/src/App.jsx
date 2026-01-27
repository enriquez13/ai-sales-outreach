import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [leads, setLeads] = useState([]);
  const [followups, setFollowups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingId, setEditingId] = useState(null);
  const [customMessage, setCustomMessage] = useState("");

  const API_URL = "https://ai-sales-outreach-6umb.onrender.com";

  const loadData = async () => {
    try {
      const [resLeads, resFollows] = await Promise.all([
        fetch(`${API_URL}/leads`),
        fetch(`${API_URL}/followups`)
      ]);
      setLeads(await resLeads.json());
      setFollowups(await resFollows.json());
    } catch (err) {
      console.error("Error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadData(); }, []);

  const handleGenerate = async (id) => {
    setEditingId(id);
    setCustomMessage("🪄 La IA está redactando tu mensaje...");
    try {
      const res = await fetch(`${API_URL}/generate/${id}`, { method: "POST" });
      const data = await res.json();
      setCustomMessage(data.email || "No se pudo generar el texto.");
      loadData(); 
    } catch (err) {
      setCustomMessage("Error al conectar con el servidor.");
    }
  };

  const handleSend = (email) => {
    // Aquí podrías integrar un servicio de email real
    alert(`Mensaje enviado a ${email}`);
    setEditingId(null);
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>🚀 AI Sales Outreach</h1>
        <p>Automatiza tus ventas con inteligencia artificial</p>
      </header>

      {/* SECCIÓN DE ALERTAS */}
      {followups.length > 0 && (
        <section className="section">
          <h2 className="section-title">⚠️ Seguimientos Sugeridos (+5 días)</h2>
          {followups.map(f => (
            <div key={f.id} className="card-followup">
              <div>
                <strong>{f.name}</strong> • {f.company}
              </div>
              <button className="btn-warning" onClick={() => handleGenerate(f.id)}>
                Preparar Seguimiento
              </button>
            </div>
          ))}
        </section>
      )}

      {/* LISTA PRINCIPAL */}
      <section className="section">
        <h2 className="section-title">📋 Dashboard de Leads</h2>
        {loading ? <p>Cargando datos...</p> : (
          <div className="grid">
            {leads.map(l => (
              <div key={l.id} className="card">
                <span className="badge">{l.status}</span>
                <h3>{l.name}</h3>
                <p style={{color: 'var(--text-dim)', marginBottom: '20px'}}>
                  {l.company} • {l.category}
                </p>

                {editingId === l.id ? (
                  <div className="editor-area">
                    <textarea 
                      value={customMessage} 
                      onChange={(e) => setCustomMessage(e.target.value)}
                    />
                    <div style={{display: 'flex', gap: '10px'}}>
                      <button className="btn-cancel" onClick={() => setEditingId(null)}>Descartar</button>
                      <button className="btn-send" onClick={() => handleSend(l.email)}>Enviar Correo</button>
                    </div>
                  </div>
                ) : (
                  <button 
                    className={l.status === 'new' ? 'btn-primary' : 'btn-disabled'}
                    onClick={() => l.status === 'new' && handleGenerate(l.id)}
                  >
                    {l.status === 'new' ? 'Generar Propuesta con IA' : '✓ Contactado'}
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

export default App;