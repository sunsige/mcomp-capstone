import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import LandingPage from './components/LandingPage';
import FeaturesSection from './components/FeaturesSection';
import TestimonialsSection from './components/TestimonialsSection';
import Footer from './components/Footer';
import ChatWindow from './components/ChatWindow';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <main>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/features" element={<FeaturesSection />} />
            <Route path="/testimonials" element={<TestimonialsSection />} />
            <Route path="/chat" element={<ChatWindow />} />
          </Routes>
          </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;