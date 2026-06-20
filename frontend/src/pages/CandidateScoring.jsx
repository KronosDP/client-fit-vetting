import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import ScoreSlider from '../components/ScoreSlider.jsx'
import MismatchAlert from '../components/MismatchAlert.jsx'

export default function CandidateScoring() {
  const navigate = useNavigate()
  const [clients, setClients] = useState([])
  const [barsData, setBarsData] = useState(null)
  const [loading, setLoading] = useState(true)

  // Form states
  const [selectedClientId, setSelectedClientId] = useState('')
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [recruiterNotes, setRecruiterNotes] = useState('')

  // Competency scores (default to 3)
  const [scores, setScores] = useState({
    communication: 3,
    adaptability: 3,
    collaboration: 3,
    problem_solving: 3,
    leadership: 3,
  })

  // Results after submission
  const [submittedCandidate, setSubmittedCandidate] = useState(null)
  const [mismatches, setMismatches] = useState([])
  const [overallMatch, setOverallMatch] = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadData() {
      try {
        const [clientsRes, barsRes] = await Promise.all([
          fetch('/api/clients'),
          fetch('/api/bars'),
        ])
        const clientsJson = await clientsRes.json()
        const barsJson = await barsRes.json()

        setClients(clientsJson)
        setBarsData(barsJson)

        if (clientsJson.length > 0) {
          setSelectedClientId(clientsJson[0].id)
        }
      } catch (err) {
        console.error(err)
        setError('Failed to load initial data. Make sure the backend is running.')
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [])

  const handleScoreChange = (competency, val) => {
    setScores(prev => ({
      ...prev,
      [competency]: val,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!selectedClientId) {
      setError('Please select a client first.')
      return
    }

    setSubmitting(true)
    setError('')
    setSubmittedCandidate(null)
    setMismatches([])
    setOverallMatch(null)

    try {
      // 1. Create candidate
      const candidateRes = await fetch('/api/candidates', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name,
          email,
          recruiter_notes: recruiterNotes,
          client_id: parseInt(selectedClientId),
        }),
      })

      if (!candidateRes.ok) {
        const errJson = await candidateRes.json()
        throw new Error(errJson.detail || 'Failed to create candidate.')
      }

      const candidate = await candidateRes.json()

      // 2. Submit scores for the candidate
      const scoreRes = await fetch(`/api/candidates/${candidate.id}/scores`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(scores),
      })

      if (!scoreRes.ok) {
        const errJson = await scoreRes.json()
        throw new Error(errJson.detail || 'Failed to submit scores.')
      }

      const scoreData = await scoreRes.json()

      setSubmittedCandidate(candidate)
      setMismatches(scoreData.mismatches || [])
      setOverallMatch(scoreData.overall_match)
    } catch (err) {
      console.error(err)
      setError(err.message || 'An error occurred during submission.')
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) {
    return <div className="loading">Loading candidates and BARS setup...</div>
  }

  if (clients.length === 0) {
    return (
      <div className="card">
        <h2>No Clients Found</h2>
        <p>You must set up at least one client before scoring candidates.</p>
        <button className="btn btn-primary" style={{ marginTop: 12 }} onClick={() => navigate('/')}>
          Go to Client Setup
        </button>
      </div>
    )
  }

  return (
    <>
      <h1 className="page-title">Candidate Scoring</h1>

      {error && <div className="error">{error}</div>}

      <div className="card">
        <h2>Candidate & Scoring Form</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Target Client</label>
            <select value={selectedClientId} onChange={e => setSelectedClientId(e.target.value)}>
              {clients.map(c => (
                <option key={c.id} value={c.id}>
                  {c.name} ({c.archetype === 'consulting' ? '💼 Consulting' : '🚀 Startup'})
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Candidate Name</label>
            <input
              type="text"
              required
              value={name}
              onChange={e => setName(e.target.value)}
              placeholder="e.g. John Doe"
            />
          </div>

          <div className="form-group">
            <label>Candidate Email (Optional)</label>
            <input
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              placeholder="e.g. john.doe@example.com"
            />
          </div>

          <div className="form-group">
            <label>Recruiter Notes (Optional)</label>
            <textarea
              value={recruiterNotes}
              onChange={e => setRecruiterNotes(e.target.value)}
              placeholder="Context about the candidate, past roles, resume highlights..."
            />
          </div>

          <h3 style={{ marginTop: 24, marginBottom: 16 }}>Vetting Competencies (BARS 1-5)</h3>
          
          {barsData && Object.keys(barsData.questions).map(comp => (
            <div key={comp} className="card" style={{ padding: 16, border: '1px solid var(--border)', background: '#fafafa' }}>
              <p style={{ fontSize: '0.875rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: 8 }}>
                VETTING QUESTION:
              </p>
              <blockquote style={{ fontStyle: 'italic', borderLeft: '3px solid var(--accent)', paddingLeft: 12, marginBottom: 16, fontSize: '0.9rem' }}>
                "{barsData.questions[comp]}"
              </blockquote>
              <ScoreSlider
                label={comp.replace('_', ' ').replace(/\b\w/g, c => c.toUpperCase())}
                value={scores[comp]}
                onChange={(val) => handleScoreChange(comp, val)}
                anchors={barsData.anchors[comp]}
              />
            </div>
          ))}

          <button type="submit" className="btn btn-primary" disabled={submitting}>
            {submitting ? 'Submitting...' : 'Save & Score Candidate'}
          </button>
        </form>
      </div>

      {submittedCandidate && (
        <div className="card" style={{ border: '2px solid var(--accent)' }}>
          <h2 style={{ color: 'var(--accent)' }}>Scoring Results for {submittedCandidate.name}</h2>
          
          <div className="match-percentage">
            <div className="value">{Math.round(overallMatch * 100)}%</div>
            <div className="label">Competency Match Score</div>
          </div>

          <MismatchAlert mismatches={mismatches} />

          <div style={{ marginTop: 24, display: 'flex', gap: 12 }}>
            <button
              className="btn btn-success"
              onClick={() => navigate(`/brief/${submittedCandidate.id}`)}
            >
              📄 Generate Prep Brief
            </button>
            <button
              className="btn btn-secondary"
              onClick={() => {
                // reset form
                setName('')
                setEmail('')
                setRecruiterNotes('')
                setScores({
                  communication: 3,
                  adaptability: 3,
                  collaboration: 3,
                  problem_solving: 3,
                  leadership: 3,
                })
                setSubmittedCandidate(null)
                setMismatches([])
                setOverallMatch(null)
              }}
            >
              Score Another Candidate
            </button>
          </div>
        </div>
      )}
    </>
  )
}
