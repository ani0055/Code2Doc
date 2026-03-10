import React from 'react';

const Header = ({ user, onLogout, toggleTheme, isDarkMode }) => {
    return (
        <header className="dashboard-header glass-panel">
            <div className="header-greeting">
                <h1>Welcome back, <span className="highlight">{user.name}</span>!</h1>
            </div>

            <div className="header-actions">
                <button className="theme-toggle-btn" onClick={toggleTheme} aria-label="Toggle Theme">
                    <span className="theme-icon">{isDarkMode ? '☀️ Light' : '🌙 Dark'}</span>
                </button>

                <div className="user-profile">
                    <div className="avatar">{user.name.charAt(0).toUpperCase()}</div>
                    <button onClick={onLogout} className="btn-logout-modern">Logout</button>
                </div>
            </div>
        </header>
    );
};

export default Header;
