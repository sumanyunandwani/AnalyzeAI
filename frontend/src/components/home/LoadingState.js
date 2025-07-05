import React from 'react';
import { Box, CircularProgress, Typography, Paper } from '@mui/material';

const LoadingState = () => {
  return (
    <Paper
      elevation={6}
      sx={{
        p: 4,
        background: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(10px)',
        borderRadius: 3,
        boxShadow: '0 15px 35px rgba(0, 0, 0, 0.1), 0 5px 15px rgba(0, 0, 0, 0.07)',
        textAlign: 'center'
      }}
    >
      <CircularProgress
        size={60}
        thickness={4}
        sx={{
          color: '#667eea',
          mb: 3
        }}
      />
      
      <Typography
        variant="h6"
        sx={{
          color: '#667eea',
          fontWeight: 600,
          mb: 3
        }}
      >
        Generating your document...
      </Typography>
      
      <Box
        sx={{
          backgroundColor: 'rgba(102, 126, 234, 0.08)',
          borderRadius: 2,
          p: 3,
          border: '1px solid rgba(102, 126, 234, 0.2)'
        }}
      >
        <Typography
          variant="body1"
          sx={{
            color: '#4a5568',
            lineHeight: 1.8,
            fontStyle: 'italic'
          }}
        >
          B-Docs is an intelligent documentation platform that deciphers SQL logic into clear, 
          business-aligned insights, bridging technical depth with executive clarity. 
          It empowers organizations to elevate data transparency, streamline collaboration, 
          and drive strategic decision-making.
        </Typography>
      </Box>
    </Paper>
  );
};

export default LoadingState;
