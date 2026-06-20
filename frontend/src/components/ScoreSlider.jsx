export default function ScoreSlider({ label, value, onChange, anchors }) {
  const getAnchorText = () => {
    if (!anchors) return ''
    if (value >= 4) return anchors[5] || ''
    if (value >= 2) return anchors[3] || ''
    return anchors[1] || ''
  }

  return (
    <div className="score-slider">
      <div className="score-slider-header">
        <span className="score-slider-label">{label}</span>
        <span className="score-slider-value">{value}</span>
      </div>
      <input
        type="range"
        min="1"
        max="5"
        step="1"
        value={value}
        onChange={(e) => onChange(parseInt(e.target.value))}
      />
      <div className="score-slider-anchor">{getAnchorText()}</div>
    </div>
  )
}
