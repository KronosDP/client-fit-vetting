import { useState, useEffect } from 'react'

export default function FeedbackForm() {
  const [candidates, setCandidates] = useState([])
  const [clients, setClients] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  // Form states
  const [selectedCandidateId, setSelectedCandidateId] = useState('')
  const [outcome, setOutcome] = useState('accepted')
  const [primaryReason, setPrimaryReason] = useState('communication_soft_skills')
  const [clientNotes, setClientNotes] = useState('')

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [candRes, clientRes, statsRes] = await Promise.all([
        fetch('/api/candidates'),
        fetch('/api/clients'),
        fetch('/api/stats'),
      ])

      const cands = await candRes.json()
      const clis = await clientRes.json()
      const st = await statsRes.json()

      setCandidates(cands)
      setClients(clis)
      setStats(st)

      // Set default selected candidate as the first one that has scores but no feedback
      const pendingFeedback = cands.filter(c => c.score && !c.feedback)
      if (pendingFeedback.length > 0) {
        setSelectedCandidateId(pendingFeedback[0].id)
      } else {
        setSelectedCandidateId('')
      }
    } catch (err) {
      console.error(err)
      setError('Failed to load feedback page data.')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!selectedCandidateId) {
      setError('Please select a candidate.')
      return
    }

    setSubmitting(true)
    setError('')
    setSuccess('')

    try {
      const res = await fetch(`/api/candidates/${selectedCandidateId}/feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          outcome,
          primary_reason: primaryReason,
          client_notes: clientNotes,
        }),
      })

      if (!res.ok) {
        const errData = await res.json()
        throw new Error(errData.detail || 'Failed to submit feedback.')
      }

      setSuccess('Feedback logged successfully!')
      setClientNotes('')
      // Reload stats and candidate list
      await loadData()
    } catch (err) {
      console.error(err)
      setError(err.message || 'Error occurred while logging feedback.')
    } finally {
      setSubmitting(false)
    }
  }

  const getClientName = (clientId) => {
    const client = clients.find(c => c.id === clientId)
    return client ? client.name : 'Unknown Client'
  }

  const getReasonLabel = (reason) => {
    const mapping = {
      communication_soft_skills: '💬 Communication & Soft Skills',
      technical_capability: '💻 Technical Capability',
      alignment_cultural_vibe: '🤝 Alignment / Cultural Vibe',
      candidate_declined: '❌ Candidate Declined',
    }
    return mapping[reason] || reason
  }

  if (loading) {
    return <div className="loading">Loading performance dashboard...</div>
  }

  // Filter candidates who have been scored and need feedback
  const pendingFeedbackCandidates = candidates.filter(c => c.score && !c.feedback)

  return (
    <>
      <h1 className="page-title">Feedback & Performance Dashboard</h1>

      {error && <div className="error">{error}</div>}

      {/* Stats Cards */}
      {stats && (
        <div className="stats-grid" style={{ marginBottom: 24 }}>
          <div className="stat-card">
            <div className="stat-value">{stats.total_candidates}</div>
            <div className="stat-label">Total Vetted</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.acceptance_rate}%</div>
            <div className="stat-label">Client Acceptance</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.feedback_compliance_rate}%</div>
            <div className="stat-label">Feedback Compliance</div>
          </div>
          <div className="stat-card">
            <div className="stat-value" style={{ color: 'var(--success)' }}>{stats.accepted_count}</div>
            <div className="stat-label">Accepted</div>
          </div>
          <div className="stat-card">
            <div className="stat-value" style={{ color: 'var(--danger)' }}>{stats.rejected_count}</div>
            <div className="stat-label">Rejected</div>
          </div>
        </div>
      )}

      {/* Feedback Form */}
      <div className="card">
        <h2>Log Post-Interview Outcome</h2>
        {success && <div className="alert-success">{success}</div>}
        
        {pendingFeedbackCandidates.length === 0 ? (
          <p style={{ color: 'var(--text-muted)' }}>
            All scored candidates have feedback logged. Great job! Go score more candidates to log outcomes.
          </p>
        ) : (
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Select Candidate</label>
              <select value={selectedCandidateId} onChange={e => setSelectedCandidateId(e.target.value)}>
                {pendingFeedbackCandidates.map(c => (
                  <option key={c.id} value={c.id}>
                    {c.name} — {getClientName(c.client_id)} (Match: {Math.round(c.score.overall_match * 100)}%)
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Interview Outcome</label>
              <div className="radio-group">
                <label>
                  <input
                    type="radio"
                    name="outcome"
                    value="accepted"
                    checked={outcome === 'accepted'}
                    onChange={() => setOutcome('accepted')}
                  />
                  🟢 Client Accepted Candidate
                </label>
                <label>
                  <input
                    type="radio"
                    name="outcome"
                    value="rejected"
                    checked={outcome === 'rejected'}
                    onChange={() => setOutcome('rejected')}
                  />
                  🔴 Client Rejected Candidate
                </label>
              </div>
            </div>

            <div className="form-group">
              <label>Primary Factor / Reason</label>
              <div className="radio-group">
                <label>
                  <input
                    type="radio"
                    name="reason"
                    value="communication_soft_skills"
                    checked={primaryReason === 'communication_soft_skills'}
                    onChange={() => setPrimaryReason('communication_soft_skills')}
                  />
                  Communication & Soft Skills (BARS)
                </label>
                <label>
                  <input
                    type="radio"
                    name="reason"
                    value="technical_capability"
                    checked={primaryReason === 'technical_capability'}
                    onChange={() => setPrimaryReason('technical_capability')}
                  />
                  Technical Capability
                </label>
                <label>
                  <input
                    type="radio"
                    name="reason"
                    value="alignment_cultural_vibe"
                    checked={primaryReason === 'alignment_cultural_vibe'}
                    onChange={() => setPrimaryReason('alignment_cultural_vibe')}
                  />
                  Alignment & Cultural Vibe
                </label>
                <label>
                  <input
                    type="radio"
                    name="reason"
                    value="candidate_declined"
                    checked={primaryReason === 'candidate_declined'}
                    onChange={() => setPrimaryReason('candidate_declined')}
                  />
                  Candidate Declined Offer / Process
                </label>
              </div>
            </div>

            <div className="form-group">
              <label>Client Qualitative Feedback Notes</label>
              <textarea
                value={clientNotes}
                onChange={e => setClientNotes(e.target.value)}
                placeholder="Details of client comments, specific strengths/weaknesses mentioned during debrief..."
              />
            </div>

            <button type="submit" className="btn btn-primary" disabled={submitting}>
              {submitting ? 'Submitting...' : 'Log Outcome'}
            </button>
          </form>
        )}
      </div>

      {/* Candidate History Table */}
      <div className="card">
        <h2>Vetting & Interview History</h2>
        {candidates.length === 0 ? (
          <p style={{ color: 'var(--text-muted)' }}>No candidates registered yet.</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Candidate Name</th>
                <th>Client</th>
                <th>Vetting Match</th>
                <th>Status</th>
                <th>Feedback Notes</th>
              </tr>
            </thead>
            <tbody>
              {candidates.map(c => (
                <tr key={c.id}>
                  <td><strong>{c.name}</strong></td>
                  <td>{getClientName(c.client_id)}</td>
                  <td>
                    {c.score ? (
                      <span style={{ fontWeight: 600 }}>
                        {Math.round(c.score.overall_match * 100)}%
                      </span>
                    ) : (
                      <span style={{ color: 'var(--text-muted)' }}>Unscored</span>
                    )}
                  </td>
                  <td>
                    {c.feedback ? (
                      <span className={c.feedback.outcome === 'accepted' ? 'status-pass' : 'status-warning'}>
                        {c.feedback.outcome === 'accepted' ? '🟢 Accepted' : '🔴 Rejected'}
                      </span>
                    ) : c.score ? (
                      <span style={{ color: 'var(--text-muted)' }}>Scored, Pending Feedback</span>
                    ) : (
                      <span style={{ color: 'var(--text-muted)' }}>Pending Evaluation</span>
                    )}
                  </td>
                  <td>
                    {c.feedback ? (
                      <div>
                        <div style={{ fontSize: '0.8rem', fontWeight: 600 }}>
                          {getReasonLabel(c.feedback.primary_reason)}
                        </div>
                        {c.feedback.client_notes && (
                          <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 4 }}>
                            "{c.feedback.client_notes}"
                          </div>
                        )}
                      </div>
                    ) : (
                      <span style={{ color: 'var(--text-muted)' }}>—</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </>
  )
}
