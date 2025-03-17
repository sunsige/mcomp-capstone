import React from 'react';

const FeaturesSection = () => {
  const features = [
    {
      icon: '🌍',
      title: 'Multi-Jurisdictional Support',
      description: 'Navigate regulations across multiple regions with ease.',
    },
    {
      icon: '⏰',
      title: 'Real-Time Updates',
      description: 'Stay up-to-date with the latest regulatory changes.',
    },
    {
      icon: '🖥️',
      title: 'User-Friendly Interface',
      description: 'Interact with the chatbot using simple, intuitive chat-based queries.',
    },
  ];

  return (
    <div className="features-section">
      <h2>Key Features</h2>
      <div className="features-grid">
        {features.map((feature, index) => (
          <div key={index} className="feature-card">
            <span className="feature-icon">{feature.icon}</span>
            <h3>{feature.title}</h3>
            <p>{feature.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default FeaturesSection;