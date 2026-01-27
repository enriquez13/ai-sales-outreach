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
      .then(data => {
        console.log("Leads recibidos:", data);
        setLeads(data);
      })
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
      setCustomMessage("❌ Error de conexión. El servidor puede estar despertando. Intenta de nuevo.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>🚀 AI Sales Outreach</h1>
        <p style={{ color: "#94a3b8" }}>
          Impulsa tus ventas con inteligencia artificial
        </p>
      </header>

      <div className="grid">
        {leads.map(l => (
          <div key={l.id} className="card">
            <span className="status-badge">Nuevo</span>

            <h2 style={{ margin: "10px 0" }}>{l.name}</h2>

            <p style={{ color: "#94a3b8", marginBottom: "20px" }}>
              {l.company}
            </p>

            {editingId === l.id ? (
              <div className="editor">
                <textarea
                  value={customMessage}
                  onChange={(e) => setCustomMessage(e.target.value)}
                  readOnly={isGenerating}
                />

                <div className="btn-group">
                  <button
                    className="btn-cancel"
                    onClick={() => setEditingId(null)}
                  >
                    Descartar
                  </button>

                  <button
                    className="btn-send"
                    onClick={() => alert("Correo aprobado")}
                    disabled={isGenerating}
                  >
                    Aprobar correo
                  </button>
                </div>
              </div>
            ) : (
              <button
                className="btn-primary"
                onClick={() => handleGenerate(l.id)}
              >
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
