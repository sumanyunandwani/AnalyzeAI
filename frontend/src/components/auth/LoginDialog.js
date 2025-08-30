import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  Box,
  Button,
  Typography,
  IconButton,
  Divider,
  CircularProgress,
  Alert
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import GoogleIcon from '@mui/icons-material/Google';
import GitHubIcon from '@mui/icons-material/GitHub';
import EmailIcon from '@mui/icons-material/Email';
import { useAuth } from './AuthContext';
import { API_ENDPOINTS } from '../../config/api';

const LoginDialog = ({ open, onClose }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { login } = useAuth();

  const handleSSOLogin = async (provider) => {
    setLoading(true);
    setError(null);
    
    try {
      // Map provider names to endpoint tags
      const endpointMap = {
        'Google': API_ENDPOINTS.LOGIN_GOOGLE,
        'Outlook': API_ENDPOINTS.LOGIN_MICROSOFT,
        'GitHub': API_ENDPOINTS.LOGIN_GITHUB
      };
      
      const loginUrl = endpointMap[provider];
      
      // For OAuth flows, we typically redirect to the login endpoint
      // The backend will handle the OAuth flow and redirect back
      window.location.href = loginUrl;
      
    } catch (error) {
      console.error('Login failed:', error);
      setError(error.message || 'Failed to login. Please try again.');
      setLoading(false);
    }
  };

  const ssoProviders = [
    {
      name: 'Google',
      icon: <GoogleIcon />,
      color: '#4285f4',
      textColor: '#fff'
    },
    {
      name: 'Outlook',
      icon: <EmailIcon />,
      color: '#0078d4',
      textColor: '#fff'
    },
    {
      name: 'GitHub',
      icon: <GitHubIcon />,
      color: '#24292e',
      textColor: '#fff'
    }
  ];

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="xs"
      fullWidth
      PaperProps={{
        sx: {
          borderRadius: 2,
          position: 'relative'
        }
      }}
    >
      <IconButton
        onClick={onClose}
        sx={{
          position: 'absolute',
          right: 8,
          top: 8,
          color: 'grey.500'
        }}
        disabled={loading}
      >
        <CloseIcon />
      </IconButton>

      <DialogTitle sx={{ textAlign: 'center', pt: 3 }}>
        <Typography variant="h5" component="div" fontWeight="600">
          Welcome to B-Docs
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          Sign in to continue
        </Typography>
      </DialogTitle>

      <DialogContent sx={{ pb: 4 }}>
        <Box sx={{ mt: 2 }}>
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{ mb: 3, textAlign: 'center' }}
          >
            Choose your preferred sign-in method
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
              {error}
            </Alert>
          )}

          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            {ssoProviders.map((provider) => (
              <Button
                key={provider.name}
                fullWidth
                variant="contained"
                size="large"
                startIcon={loading ? null : provider.icon}
                onClick={() => handleSSOLogin(provider.name)}
                disabled={loading}
                sx={{
                  backgroundColor: provider.color,
                  color: provider.textColor,
                  textTransform: 'none',
                  py: 1.5,
                  fontSize: '1rem',
                  fontWeight: 500,
                  '&:hover': {
                    backgroundColor: provider.color,
                    filter: 'brightness(0.9)'
                  }
                }}
              >
                {loading ? (
                  <CircularProgress size={24} sx={{ color: provider.textColor }} />
                ) : (
                  `Continue with ${provider.name}`
                )}
              </Button>
            ))}
          </Box>

          <Divider sx={{ my: 3 }}>
            <Typography variant="caption" color="text.secondary">
              OR
            </Typography>
          </Divider>

          <Typography
            variant="body2"
            color="text.secondary"
            sx={{ textAlign: 'center' }}
          >
            By signing in, you agree to our Terms of Service and Privacy Policy
          </Typography>
        </Box>
      </DialogContent>
    </Dialog>
  );
};

export default LoginDialog;
