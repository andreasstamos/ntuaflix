import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Admin from './pages/admin/Admin';
import './App.css';

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path='/admin/' exact element={<Admin />} />
        </Routes>
    </Router>
  </div>

  );
}

export default App;
