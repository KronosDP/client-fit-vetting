export default function MismatchAlert({ mismatches }) {
  if (!mismatches || mismatches.length === 0) return null

  return (
    <div className="alert-warning">
      <strong>⚠️ Mismatch Warnings</strong>
      <ul>
        {mismatches.map((m, i) => (
          <li key={i}>{m}</li>
        ))}
      </ul>
    </div>
  )
}
