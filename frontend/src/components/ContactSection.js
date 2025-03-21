import React from 'react';

const ContactSection = () => {
  const features = [
    {
      title: 'Email',
      description: 'support@reg-guru.com',
    },
    {
      title: 'Phone',
      description: '+65 8888-8888',
    },
  ];

  return (
    <div className="features-section">
      <h2>Contact Us at</h2>
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

export default ContactSection;