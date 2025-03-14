import React from 'react';
import { useNavigate } from 'react-router-dom';

const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <div className="landing-page">
      <h1>Regulatory Compliance Chatbot</h1>
      <p>Get instant, accurate answers to complex regulatory questions.</p>
      <button onClick={() => navigate('/chat')}>Start Chatting</button>
    </div>
  );
};

export default LandingPage;