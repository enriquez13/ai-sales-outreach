import { useEffect, useState } from "react";

function App() {
  const [leads, setLeads] = useState([]);
  const [followups, setFollowups] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [customMessage, setCustomMessage] = useState("");
  
  const API_URL = "https://ai-sales-outreach-6umb.onrender.com";

  const loadData = () => {
    fetch(`${API_URL}/leads`).then(res => res.json()).then(setLeads);
    fetch(`${API_URL}/followups`).then(res => res.json()).then(setFollowups);
  };

  useEffect(() => { loadData(); }, []);

  const startFollowup = (lead) => {
    setEditingId(lead.id);
    setCustomMessage(`Hola ${lead.name}, hace unos días te contacté sobre ${lead.company}. ¿Pudiste revisar mi propuesta?`);
  };

  const finalizeSend = (id) => {
    alert(`Enviando a lead #${id}: ${customMessage}`);
    // Aquí podrías hacer un fetch a un endpoint de envío real
    setEditingId(null);
  };

  return (
    <div style={{ padding: '20px', backgroundColor: '#121212', color: 'white', minHeight: '100vh' }}>
      <h1>Ventas con IA</h1>

      <section style={{ border: '2px solid #f1c40f', padding: '15px', borderRadius: '8px' }}>
        <h2>🔔 Notificaciones de Seguimiento (+5 días)</h2>
        {followups.length === 0 ? <p>Todo al día. No hay seguimientos pendientes.</p> : 
          followups.map(f => (
            <div key={f.id} style={{ marginBottom: '10px', background: '#333', padding: '10px' }}>
              <strong>{f.name}</strong> - {f.company} 
              <button onClick={() => startFollowup(f)} style={{ marginLeft: '10px' }}>Preparar Mensaje</button>
              
              {editingId === f.id && (
                <div style={{ marginTop: '10px' }}>
                  <textarea 
                    value={customMessage} 
                    onChange={(e) => setCustomMessage(e.target.value)}
                    style={{ width: '100%', height: '80px', borderRadius: '5px' }}
                  />
                  <button onClick={() => finalizeSend(f.id)} style={{ backgroundColor: '#2ecc71', color: 'white', marginTop: '5px' }}>
                    Enviar Sugerencia Editada
                  </button>
                </div>
              )}
            </div>
          ))
        }
      </section>

      <hr style={{ margin: '30px 0' }} />

      <section>
        <h2>Lista General de Leads</h2>
        {leads.map(l => (
          <div key={l.id} style={{ padding: '5px', borderBottom: '1px solid #444' }}>
            {l.name} - <span style={{ color: '#3498db' }}>{l.status}</span>
          </div>
        ))}
      </section>
    </div>
  );
}

export default App;