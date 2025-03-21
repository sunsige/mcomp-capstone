import React from 'react';

const TestimonialsSection = () => {
  const testimonials = [
    {
      name: 'John Doe',
      role: 'Compliance Officer',
      feedback: 'This chatbot has revolutionised our compliance process. Highly recommended!',
    },
    {
      name: 'Jane Smith',
      role: 'Risk Manager',
      feedback: 'This is a game-changer for our team.',
    },
  ];

  return (
    <div className="testimonials-section">
      <h2>What Our Users Say</h2>
      <div className="testimonials-grid">
        {testimonials.map((testimonial, index) => (
          <div key={index} className="testimonial-card">
            <p>"{testimonial.feedback}"</p>
            <h3>{testimonial.name}</h3>
            <p>{testimonial.role}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TestimonialsSection;