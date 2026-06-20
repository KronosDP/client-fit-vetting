import { NavLink } from 'react-router-dom'

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <span className="navbar-brand">Staffinc Match</span>
        <ul className="navbar-links">
          <li><NavLink to="/" end>Clients</NavLink></li>
          <li><NavLink to="/score">Score Candidate</NavLink></li>
          <li><NavLink to="/feedback">Feedback</NavLink></li>
        </ul>
      </div>
    </nav>
  )
}
