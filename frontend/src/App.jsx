import { useEffect, useState } from "react"

function App() {
  const [leads, setLeads] = useState([])

  // 1. Definimos la URL base. 
  // Vercel usará la variable que pusimos en su panel, 
  // y tu PC usará localhost por defecto.
  const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

  useEffect(() => {
    // 2. Usamos ${API_URL} en lugar de escribir la dirección completa
    fetch(`${API_URL}/leads`)
      .then(r => r.json())
      .then(setLeads)
      .catch(err => console.error("Error cargando leads:", err))
  }, [API_URL])

  function generate(id) {
    // 3. Aplicamos lo mismo para la función de generar
    fetch(`${API_URL}/generate/${id}`, { method: "POST" })
      .then(r => r.json())
      .then(console.log)
      .catch(err => console.error("Error generando:", err))
  }

  return (
    <div style={{ padding: "20px" }}>
      <h2>Leads</h2>
      {leads.length === 0 && <p>Cargando leads o no hay conexión con el backend...</p>}
      {leads.map(l => (
        <div key={l.id} style={{ marginBottom: "10px", borderBottom: "1px solid #ccc" }}>
          <strong>{l.name}</strong> - {l.company} 
          <button onClick={() => generate(l.id)} style={{ marginLeft: "10px" }}>
            Generate Email
          </button>
        </div>
      ))}
    </div>
  )
}

export default App