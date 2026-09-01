import { useState, useEffect } from 'react';
import Login from './Login';
import Documents from './Documents';
import Analytics from './Analytics';
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
    <div className="min-h-screen bg-gray-100">
      <div className="bg-white shadow-sm py-6 px-4 text-center">
        <h2 className="text-2xl font-bold text-gray-800">Welcome to the OmniRAG Dashboard</h2>
        <p className="text-gray-500 mt-1">You are logged in.</p>
        <button
          onClick={handleLogout}
          className="mt-4 px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition-colors"
        >
          Logout
        </button>
      </div>

      <div className="max-w-3xl mx-auto py-8 px-4 space-y-8">
        <Analytics />
        <Documents />
      </div>
    </div>
  );
}

export default App;