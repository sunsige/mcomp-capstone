import React from 'react';
import { useNavigate } from 'react-router-dom';

const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <div className="landing-page">
      <div className="hero-section">
        <h1>Simplify Regulatory Compliance with AI</h1>
        <p>Get instant, accurate answers to complex regulatory questions.</p>
        <button onClick={() => navigate('/chat')}>Get Started</button>
      </div>
    </div>
  );
};

export default LandingPage;