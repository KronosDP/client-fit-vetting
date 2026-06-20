import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'

export default function BriefPreview() {
  const { candidateId } = useParams()
  const navigate = useNavigate()
  const [brief, setBrief] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function fetchBrief() {
      try {
        const res = await fetch(`/api/candidates/${candidateId}/brief`)
        if (!res.ok) {
          const errData = await res.json()
          throw new Error(errData.detail || 'Failed to fetch brief.')
        }
        const data = await res.json()
        setBrief(data)
      } catch (err) {
        console.error(err)
        setError(err.message || 'Could not load prep brief.')
      } finally {
        setLoading(false)
      }
    }
    fetchBrief()
  }, [candidateId])

  const handlePrint = () => {
    window.print()
  }

  if (loading) {
    return <div className="loading">Generating prep brief...</div>
  }

  if (error) {
    return (
      <div className="card">
        <h2 className="status-warning">⚠️ Error</h2>
        <p>{error}</p>
        <button className="btn btn-secondary" style={{ marginTop: 12 }} onClick={() => navigate('/score')}>
          Back to Scoring
        </button>
      </div>
    )
  }

  if (!brief) return null

  return (
    <>
      <div className="no-print" style={{ marginBottom: 16, display: 'flex', gap: 12 }}>
        <button className="btn btn-secondary" onClick={() => navigate('/score')}>
          ← Back to Scoring
        </button>
        <button className="btn btn-success" onClick={handlePrint}>
          🖨️ Print Prep Brief
        </button>
      </div>

      <div className="card brief-card" style={{ borderTop: '6px solid var(--accent)' }}>
        <div className="brief-header">
          <span className="badge badge-consulting" style={{ marginBottom: 8 }}>
            {brief.client_archetype === 'consulting' ? '💼 Corporate Vetting Profile' : '🚀 Startup Vetting Profile'}
          </span>
          <h1>Candidate Interview Preparation Brief</h1>
          <p style={{ color: 'var(--text-muted)' }}>
            Prepared for <strong>{brief.candidate_name}</strong> for their interview with <strong>{brief.client_name}</strong>
          </p>
        </div>

        <hr style={{ border: '0', borderTop: '1px solid var(--border)', margin: '20px 0' }} />

        <div className="form-group">
          <strong>Client Expectations:</strong>
          <p style={{ background: '#f8f9fa', padding: 12, borderRadius: 'var(--radius)', border: '1px solid var(--border)', marginTop: 8 }}>
            {brief.client_expectations || 'No specific custom expectations logged.'}
          </p>
        </div>

        <div style={{ marginTop: 24 }}>
          <h3>Competency Alignment Check</h3>
          <table className="table" style={{ marginTop: 8 }}>
            <thead>
              <tr>
                <th>Competency</th>
                <th>Candidate Score</th>
                <th>Min. Required</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {brief.competency_scores.map((comp) => (
                <tr key={comp.name}>
                  <td><strong>{comp.name}</strong></td>
                  <td>{comp.score} / 5</td>
                  <td>{comp.min_required} / 5</td>
                  <td className={comp.status === 'pass' ? 'status-pass' : 'status-warning'}>
                    {comp.status === 'pass' ? '✓ Meets Expectations' : '⚠️ Gap Identified'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div style={{ marginTop: 28 }}>
          <h3 style={{ color: 'var(--accent)' }}>💡 Tailored Vetting Coaching & Strategy</h3>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: 12 }}>
            Prioritized tips targeting areas of potential client mismatch:
          </p>
          <ul style={{ paddingLeft: 20, lineHeight: 1.7 }}>
            {brief.coaching_tips.map((tip, idx) => (
              <li key={idx} style={{ marginBottom: 10 }}>
                {tip}
              </li>
            ))}
          </ul>
        </div>

        <div style={{ marginTop: 28 }}>
          <h3>🎯 High-Probability Practice Questions</h3>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: 12 }}>
            Have the candidate practice the STAR method with these archetype-relevant questions:
          </p>
          <ul style={{ paddingLeft: 20, lineHeight: 1.7 }}>
            {brief.practice_questions.map((q, idx) => (
              <li key={idx} style={{ marginBottom: 10, fontStyle: 'italic' }}>
                "{q}"
              </li>
            ))}
          </ul>
        </div>

        <div className="no-print" style={{ marginTop: 32, fontSize: '0.8rem', color: 'var(--text-muted)', textAlign: 'center' }}>
          Generated via Staffinc Match on {new Date(brief.generated_at).toLocaleString()}
        </div>
      </div>
    </>
  )
}
