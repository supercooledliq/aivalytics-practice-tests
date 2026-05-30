import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './user/components/ui/Layout';
import Dashboard from './user/pages/Dashboard';
import PracticeTests from './user/pages/PracticeTests';
import TestSelection from './user/pages/TestSelection';
import TestInstructions from './user/pages/TestInstructions';
import ActiveTest from './user/pages/ActiveTest';
import TestResults from './user/pages/TestResults';

function App() {
  return (
    <Router>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/practice-tests" element={<PracticeTests />} />
          <Route path="/test-selection" element={<TestSelection />} />
          <Route path="/test-instructions" element={<TestInstructions />} />
          <Route path="/test-results" element={<TestResults />} />
        </Route>
        <Route path="/active-test" element={<ActiveTest />} />
      </Routes>
    </Router>
  )
}

export default App
