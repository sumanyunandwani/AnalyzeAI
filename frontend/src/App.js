import React from 'react';
import GradientBackground from './components/layout/GradientBackground';
import Footer from './components/layout/Footer';
import HomePage from './components/home/HomePage';

function App() {
  return (
    <GradientBackground>
      <HomePage />
      <Footer />
    </GradientBackground>
  );
}

export default App;
