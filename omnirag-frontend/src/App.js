import { useState, useEffect } from 'react';
import Login from './Login';
import Documents from './Documents';
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // On page load, check if a token already exists (so refreshing doesn't log you out)
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      setIsLoggedIn(true);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setIsLoggedIn(false);
  };

  if (!isLoggedIn) {
    return <Login onLoginSuccess={() => setIsLoggedIn(true)} />;
  }

  return (
    <div className="App">
      <div style={{ textAlign: 'center', paddingTop: '30px' }}>
        <h2>Welcome to the OmniRAG Dashboard</h2>
        <p>You are logged in.</p>
        <button onClick={handleLogout} style={{ padding: '8px 16px', cursor: 'pointer' }}>
          Logout
        </button>
      </div>
      <Documents />
    </div>
  );
}

export default App;