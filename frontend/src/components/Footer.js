import React from 'react';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-contact">
          <h3>Contact Us</h3>
          <p>Email: support@reg-guru.com</p>
          <p>Phone: +65 8888-8888</p>
        </div>
        <div className="footer-social">
          <h3>Follow Us</h3>
          <p><a href="https://linkedin.com">LinkedIn</a></p>
          <p><a href="https://twitter.com">Twitter</a></p>
        </div>
        <div className="footer-legal">
          <h3>Legal</h3>
          <p><a href="/privacy-policy">Privacy Policy</a></p>
          <p><a href="/terms-of-service">Terms of Service</a></p>
        </div>
      </div>
      <div className="footer-copyright">
        <p>© 2023 Regulatory Compliance Chatbot. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;