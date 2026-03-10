import React, { useState, useEffect } from 'react';
import './App.css';
import HomePage from './components/HomePage';
import AuthPage from './components/AuthPage/AuthPage';
import Dashboard from './components/Dashboard/Dashboard';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// Root App Component
function App() {
    const [user, setUser] = useState(null);
    const [loadingInitial, setLoadingInitial] = useState(true);
    const [showLanding, setShowLanding] = useState(true);
    const [isDarkMode, setIsDarkMode] = useState(true);

    useEffect(() => {
        const token = localStorage.getItem('token');
        const userName = localStorage.getItem('userName');
        if (token && userName) {
            setUser({ name: userName, token: token });
        }

        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            setIsDarkMode(savedTheme === 'dark');
        }

        setLoadingInitial(false);
    }, []);

    const toggleTheme = () => {
        setIsDarkMode(prev => {
            const next = !prev;
            localStorage.setItem('theme', next ? 'dark' : 'light');
            return next;
        });
    };

    const handleLogin = (userData) => {
        localStorage.setItem('token', userData.token);
        localStorage.setItem('userName', userData.name);
        setUser(userData);
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('userName');
        setUser(null);
        setShowLanding(true);
    };

    if (loadingInitial) {
        return (
            <div className="loading-splash">
                <div className="modern-loader"></div>
            </div>
        );
    }

    if (!user && showLanding) {
        return (
            <div data-theme={isDarkMode ? 'dark' : 'light'}>
                <HomePage onGetStarted={() => setShowLanding(false)} />
            </div>
        );
    }

    return (
        <div className="app-root" data-theme={isDarkMode ? 'dark' : 'light'}>
            <ToastContainer theme={isDarkMode ? 'dark' : 'light'} />

            {user ? (
                <Dashboard
                    user={user}
                    onLogout={handleLogout}
                    toggleTheme={toggleTheme}
                    isDarkMode={isDarkMode}
                />
            ) : (
                <AuthPage onLogin={handleLogin} />
            )}
        </div>
    );
}

export default App;