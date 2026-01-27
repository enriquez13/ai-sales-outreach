import { useEffect, useState } from "react"

function App() {
  const [leads, setLeads] = useState([])

  // Detecta automáticamente si debe usar Render o Localhost
  const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

  useEffect(() => {
    fetch(`${API_URL}/leads`)
      .then(r => {
        if (!r.ok) throw new Error("Error en la respuesta del servidor");
        return r.json();
      })
      .then(setLeads)
      .catch(err => console.error("Error cargando leads:", err))
  }, [API_URL])

  function generate(id) {
    fetch(`${API_URL}/generate/${id}`, { method: "POST" })
      .then(r => r.json())
      .then(data => {
        alert("Email Generado: " + data.email);
        console.log(data);
      })
      .catch(err => console.error("Error al generar email:", err))
  }

  return (
    <div style={{ padding: "20px", fontFamily: "sans-serif" }}>
      <h1>AI Sales Outreach</h1>
      <h2>Leads Disponibles</h2>
      
      {leads.length === 0 ? (
        <p>Cargando datos desde Render... (esto puede tardar si el backend estaba dormido)</p>
      ) : (
        leads.map(l => (
          <div key={l.id} style={{ 
            border: "1px solid #ddd", 
            padding: "10px", 
            marginBottom: "10px",
            borderRadius: "8px" 
          }}>
            <strong>{l.name}</strong> - {l.company}
            <br />
            <button 
              onClick={() => generate(l.id)}
              style={{ marginTop: "10px", cursor: "pointer" }}
            >
              Generar Email con IA
            </button>
          </div>
        ))
      )}
    </div>
  )
}

export default App