import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Admin from './pages/admin/Admin';
import './App.css';
import Index from './pages/Index';
import Auth from './pages/auth/Auth';
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import Navbar from './components/Navbar';
import Movie from './pages/Movie';
import NotRegistered from './pages/NotRegistered';
import Preloader from './components/Preloader';
import Movies from './pages/Movies';


function App() {
  
  return (
    <div className="App">
      <Router>

      <Navbar/>

        <Routes>
          <Route path='/' exact element={<Index />} />
          <Route path='/movie/' exact element={<Movie />} />
          <Route path='/movies/' exact element={<Movies />} />

          <Route path='/preloader/' exact element={<Preloader />} />
          <Route path='/admin/' exact element={<Admin />} />
          <Route path='/watchlist/' exact element={<NotRegistered />} />
          
          
          <Route path='/auth' exact element={<Auth/>}>
            <Route path='login/' element={<Login/>} />
            <Route path='register/' element={<Register/>} />
          </Route>


        </Routes>
    </Router>
  </div>

  );
}

export default App;
