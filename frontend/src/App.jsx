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

  const handleGenerate = async (id) => {
    setEditingId(id);
    setIsGenerating(true);
    setCustomMessage("🪄 La IA está redactando una propuesta personalizada...");
    
    try {
      const res = await fetch(`${API_URL}/generate/${id}`, { 
        method: "POST",
        headers: { "Content-Type": "application/json" }
      });
      
      if (!res.ok) throw new Error("Servidor ocupado");
      
      const data = await res.json();
      setCustomMessage(data.email);
    } catch (err) {
      setCustomMessage("❌ Error de conexión. El servidor de Render podría estar 'despertando'. Intenta de nuevo en 10 segundos.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>🚀 AI Sales Outreach</h1>
        <p style={{color: '#94a3b8'}}>Impulsa tus ventas con inteligencia artificial</p>
      </header>

      <div className="grid">
        {leads.map(l => (
          <div key={l.id} className="card">
            <span className="status-badge">{l.status}</span>
            <h2 style={{margin: '0 0 5px 0', fontSize: '1.5rem'}}>{l.name}</h2>
            <p style={{color: '#94a3b8', marginBottom: '20px'}}>{l.company} • {l.category}</p>

            {editingId === l.id ? (
              <div className="editor">
                <textarea 
                  value={customMessage} 
                  onChange={(e) => setCustomMessage(e.target.value)}
                  readOnly={isGenerating}
                />
                <div className="btn-group">
                  <button className="btn-cancel" onClick={() => setEditingId(null)}>Descartar</button>
                  <button className="btn-send" onClick={() => alert("¡Email enviado!")} disabled={isGenerating}>Enviar Correo</button>
                </div>
              </div>
            ) : (
              <button className="btn-primary" onClick={() => handleGenerate(l.id)}>
                Generar Propuesta con IA
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;