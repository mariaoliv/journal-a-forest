import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Landing from './pages/Landing'
import Onboarding from './pages/Onboarding'
import Main from './pages/Main'
import Journaling from './pages/Journaling'
import Forest from './pages/Forest'
import Settings from './pages/Settings'
import Insights from './pages/Insights'
import { SessionProvider } from './contexts/SessionContext'

function App() {
  return (
    <SessionProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/onboarding" element={<Onboarding />} />
          <Route path="/main" element={<Main />} />
          <Route path="/journaling/:promptId?" element={<Journaling />} />
          <Route path="/forest" element={<Forest />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/insights" element={<Insights />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </SessionProvider>
  )
}

export default App

