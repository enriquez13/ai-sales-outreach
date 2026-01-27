import {useEffect,useState} from "react"

function App(){

const [leads,setLeads]=useState([])

useEffect(()=>{
 fetch("http://localhost:8000/leads")
 .then(r=>r.json())
 .then(setLeads)
},[])

return (
<div>
<h2>Leads</h2>

{leads.map(l=>(
<div key={l.id}>
{l.name} - {l.company}
<button onClick={()=>generate(l.id)}>Generate</button>
</div>
))}
</div>
)

function generate(id){
fetch(`http://localhost:8000/generate/${id}`,{method:"POST"})
.then(r=>r.json())
.then(console.log)
}

}

export default App
