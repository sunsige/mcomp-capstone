import React from 'react';
import { Link } from 'react-router-dom';
import logo from '../assets/logo.png';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-logo">
      <img src={logo} alt="REG-Guru Logo" className="logo" />
        <h0>REG-GURU</h0>
      </div>
      <div className="navbar-links">
        <Link to="/">Home</Link>
        <Link to="/chat">Chat</Link>
        <Link to="/features">Features</Link>
        {/* <Link to="/testimonials">Testimonials</Link> */}
        <Link to="/contact">Contact</Link>
      </div>
    </nav>
  );
};

export default Navbar;