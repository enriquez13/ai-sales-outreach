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
    setCustomMessage("🪄 La IA está redactando el correo...");

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
        <h1>🚀 AI Sales Outreach</h1>
        <p style={{ color: "#94a3b8" }}>
          Primer contacto y follow-up automático
        </p>
      </header>

      <div className="grid">
        {leads.map(l => (
          <div key={l.id} className="card">

            <span className="status-badge">
              {l.stage === "followup" ? "Follow-up" : "Nuevo"}
            </span>

            <h2>{l.name}</h2>

            <p style={{ color: "#94a3b8", marginBottom: "20px" }}>
              {l.company}
            </p>

            {editingId === l.id ? (
              <div className="editor">
                <textarea
                  value={customMessage}
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
                    disabled={isGenerating}
                    onClick={() => alert("Correo aprobado")}
                  >
                    Aprobar correo
                  </button>
                </div>
              </div>
            ) : (
              <button
                className="btn-primary"
                onClick={() => handleGenerate(l)}
              >
                {l.stage === "followup"
                  ? "Generar Follow-up"
                  : "Generar Primer Email"}
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
