import React from 'react';
import { Link } from 'react-router-dom';
import logo from '../assets/logo.png';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-logo">
      <img src={logo} alt="REG-Guru Logo" className="logo" />
        <h1>REG-Guru</h1>
      </div>
      <div className="navbar-links">
        <Link to="/">Home</Link>
        <Link to="/features">Features</Link>
        <Link to="/testimonials">Testimonials</Link>
        <Link to="/contact">Contact</Link>
      </div>
    </nav>
  );
};

export default Navbar;