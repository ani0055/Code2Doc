import React, { useState } from 'react';
import { login, register } from '../../services/api';
import './AuthPage.css';

const AuthPage = ({ onLogin }) => {
    const [isLogin, setIsLogin] = useState(true);
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: ''
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
        setError('');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            if (isLogin) {
                const response = await login(formData.email, formData.password);
                onLogin({
                    name: formData.email.split('@')[0],
                    token: response.access_token
                });
            } else {
                await register(formData.email, formData.name, formData.password);
                const loginResponse = await login(formData.email, formData.password);
                onLogin({
                    name: formData.name,
                    token: loginResponse.access_token
                });
            }
        } catch (err) {
            setError(err.message || 'An error occurred');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-container modern-auth-bg">
            <div className="auth-card glass-panel">
                <div className="auth-header">
                    <h2>{isLogin ? 'Welcome Back' : 'Create Account'}</h2>
                    <p>{isLogin ? 'Log in to continue your journey.' : 'Sign up to modernize your docs.'}</p>
                </div>

                {error && <div className="error-message">{error}</div>}

                <form onSubmit={handleSubmit} className="modern-form">
                    {!isLogin && (
                        <div className="floating-input-group">
                            <input
                                type="text"
                                name="name"
                                id="name"
                                placeholder=" "
                                value={formData.name}
                                onChange={handleChange}
                                required
                                className="floating-input"
                            />
                            <label htmlFor="name" className="floating-label">Your Name</label>
                        </div>
                    )}

                    <div className="floating-input-group">
                        <input
                            type="email"
                            name="email"
                            id="email"
                            placeholder=" "
                            value={formData.email}
                            onChange={handleChange}
                            required
                            className="floating-input"
                        />
                        <label htmlFor="email" className="floating-label">Email Address</label>
                    </div>

                    <div className="floating-input-group">
                        <input
                            type="password"
                            name="password"
                            id="password"
                            placeholder=" "
                            value={formData.password}
                            onChange={handleChange}
                            required
                            minLength="6"
                            className="floating-input"
                        />
                        <label htmlFor="password" className="floating-label">Password</label>
                    </div>

                    {isLogin && <div className="forgot-password">Forgot Password?</div>}

                    <button type="submit" className="btn-modern-primary" disabled={loading}>
                        {loading ? <span className="loader-small"></span> : (isLogin ? 'Login' : 'Sign Up')}
                    </button>
                </form>

                <div className="auth-toggle-modern">
                    <p>
                        {isLogin ? "Don't have an account? " : "Already have an account? "}
                        <button
                            type="button"
                            className="toggle-btn"
                            onClick={() => { setIsLogin(!isLogin); setError(''); }}
                        >
                            {isLogin ? 'Sign Up' : 'Login'}
                        </button>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default AuthPage;
