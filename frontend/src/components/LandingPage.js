import React from 'react';
import { useNavigate } from 'react-router-dom';

const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <div className="landing-page">
      <div className="hero-section">
        <h1>Hi, I'm Reg-Guru</h1>
        <p>Your Compliance Assistant.</p> 
        <p>Get instant, accurate answers to complex regulatory questions.</p>
        <button onClick={() => navigate('/chat')}>Ask Me Anything</button>
      </div>
    </div>
  );
};

export default LandingPage;