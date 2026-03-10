import React from 'react';

const Sidebar = ({ currentView, onViewChange }) => {
    return (
        <aside className="dashboard-sidebar glass-panel">
            <div className="sidebar-brand">
                <h2>Code<span>2</span>Doc</h2>
            </div>

            <nav className="sidebar-nav">
                <button
                    className={`nav-item ${currentView === 'main' ? 'active' : ''}`}
                    onClick={() => onViewChange('main')}
                >
                    <span className="nav-icon">✨</span>
                    <span className="nav-label">Analyze Code</span>
                </button>
                <button
                    className={`nav-item ${currentView === 'history' ? 'active' : ''}`}
                    onClick={() => onViewChange('history')}
                >
                    <span className="nav-icon">🕒</span>
                    <span className="nav-label">History</span>
                </button>
            </nav>
        </aside>
    );
};

export default Sidebar;
