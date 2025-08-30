import React from 'react';
import { AuthProvider } from './components/auth/AuthContext';
import GradientBackground from './components/layout/GradientBackground';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import HomePage from './components/home/HomePage';

function App() {
  return (
    <AuthProvider>
      <GradientBackground>
        <Header />
        <HomePage />
        <Footer />
      </GradientBackground>
    </AuthProvider>
  );
}

export default App;
