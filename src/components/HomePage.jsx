import React from 'react';
import '../HomePage.css';

const HomePage = ({ onGetStarted }) => {
    return (
        <div className="homepage-container">
            {/* Hero Section */}
            <section className="hero-section">
                <div className="hero-content glass-card">
                    <h1 className="hero-title">Welcome to Code2Doc</h1>
                    <p className="hero-subtitle">Generate comprehensive markdown documentation and flow diagrams instantly from your codebase.</p>
                    <button onClick={onGetStarted} className="btn-primary btn-large cta-button">
                        Get Started
                    </button>
                </div>
            </section>

            {/* Bento Grid Features */}
            <section className="features-section">
                <div className="bento-grid">
                    <div className="bento-item glass-card feature-code">
                        <h3>AI Code Analysis</h3>
                        <p>Automatically detect your language, functions, and classes to build a structured understanding of your project.</p>
                    </div>
                    <div className="bento-item glass-card feature-diagram">
                        <h3>Flow Diagrams</h3>
                        <p>Visualize the logic flow with beautiful, auto-generated diagrams tailored to your specific code structure.</p>
                    </div>
                    <div className="bento-item glass-card feature-export">
                        <h3>Multiple Formats</h3>
                        <p>Export your comprehensive documentation to PDF, DOCX, or pure Markdown with a single click.</p>
                    </div>
                    <div className="bento-item glass-card feature-metrics">
                        <h3>Code Quality</h3>
                        <p>Get instant feedback on code complexity and maintainability to ensure your architecture stays pristine.</p>
                    </div>
                </div>
            </section>
        </div>
    );
};

export default HomePage;
