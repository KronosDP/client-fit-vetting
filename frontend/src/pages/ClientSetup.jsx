import { useState, useEffect } from 'react'

const ARCHETYPE_DEFAULTS = {
  consulting: { min_communication: 4, min_adaptability: 3, min_collaboration: 4, min_problem_solving: 3, min_leadership: 3 },
  startup: { min_communication: 3, min_adaptability: 4, min_collaboration: 3, min_problem_solving: 3, min_leadership: 4 },
}

export default function ClientSetup() {
  const [clients, setClients] = useState([])
  const [loading, setLoading] = useState(true)
  const [form, setForm] = useState({
    name: '',
    archetype: 'consulting',
    expectations: '',
    ...ARCHETYPE_DEFAULTS.consulting,
  })
  const [submitting, setSubmitting] = useState(false)
  const [success, setSuccess] = useState('')

  useEffect(() => { fetchClients() }, [])

  const fetchClients = async () => {
    try {
      const res = await fetch('/api/clients')
      setClients(await res.json())
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleArchetypeChange = (archetype) => {
    setForm(prev => ({ ...prev, archetype, ...ARCHETYPE_DEFAULTS[archetype] }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSubmitting(true)
    setSuccess('')
    try {
      const res = await fetch('/api/clients', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })
      if (res.ok) {
        setSuccess(`Client "${form.name}" created successfully!`)
        setForm({ name: '', archetype: 'consulting', expectations: '', ...ARCHETYPE_DEFAULTS.consulting })
        fetchClients()
      }
    } catch (err) {
      console.error(err)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <>
      <h1 className="page-title">Client Setup</h1>

      <div className="card">
        <h2>Add New Client</h2>
        {success && <div className="alert-success">{success}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Client Name</label>
            <input type="text" required value={form.name} onChange={e => setForm(f => ({ ...f, name: e.target.value }))} placeholder="e.g. Acme Corp" />
          </div>
          <div className="form-group">
            <label>Archetype</label>
            <select value={form.archetype} onChange={e => handleArchetypeChange(e.target.value)}>
              <option value="consulting">💼 Consulting / Corporate</option>
              <option value="startup">🚀 Startup / Scrappy</option>
            </select>
          </div>
          <div className="form-group">
            <label>Client Expectations</label>
            <textarea value={form.expectations} onChange={e => setForm(f => ({ ...f, expectations: e.target.value }))} placeholder="e.g. Business casual, structured answers, executive presence..." />
          </div>
          <p style={{ fontSize: '0.875rem', fontWeight: 600, marginBottom: 8 }}>Minimum BARS Thresholds</p>
          <div className="form-row">
            {['communication', 'adaptability', 'collaboration', 'problem_solving', 'leadership'].map(field => (
              <div className="form-group" key={field}>
                <label>{field.replace('_', ' ').replace(/\b\w/g, c => c.toUpperCase())}</label>
                <input type="number" min="1" max="5" value={form[`min_${field}`]} onChange={e => setForm(f => ({ ...f, [`min_${field}`]: parseInt(e.target.value) }))} />
              </div>
            ))}
          </div>
          <button type="submit" className="btn btn-primary" disabled={submitting}>
            {submitting ? 'Creating...' : 'Create Client'}
          </button>
        </form>
      </div>

      <div className="card">
        <h2>Existing Clients</h2>
        {loading ? (
          <div className="loading">Loading clients...</div>
        ) : clients.length === 0 ? (
          <p style={{ color: 'var(--text-muted)' }}>No clients yet. Create one above.</p>
        ) : (
          clients.map(c => (
            <div className="client-list-item" key={c.id}>
              <div>
                <strong>{c.name}</strong>{' '}
                <span className={`badge badge-${c.archetype}`}>{c.archetype}</span>
              </div>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                {new Date(c.created_at).toLocaleDateString()}
              </span>
            </div>
          ))
        )}
      </div>
    </>
  )
}
