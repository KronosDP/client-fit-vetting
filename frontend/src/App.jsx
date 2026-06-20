import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar.jsx'
import ClientSetup from './pages/ClientSetup.jsx'
import CandidateScoring from './pages/CandidateScoring.jsx'
import BriefPreview from './pages/BriefPreview.jsx'
import FeedbackForm from './pages/FeedbackForm.jsx'

function App() {
  return (
    <>
      <Navbar />
      <div className="container">
        <Routes>
          <Route path="/" element={<ClientSetup />} />
          <Route path="/score" element={<CandidateScoring />} />
          <Route path="/brief/:candidateId" element={<BriefPreview />} />
          <Route path="/feedback" element={<FeedbackForm />} />
        </Routes>
      </div>
    </>
  )
}

export default App
