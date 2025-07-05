import React from 'react';
import { Typography, Box } from '@mui/material';
import { Description } from '@mui/icons-material';

const PageTitle = () => {
  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        mb: 1,
        gap: 2
      }}
    >
      <Description 
        sx={{ 
          fontSize: { xs: '2.5rem', sm: '3rem', md: '3.5rem' },
          color: 'white',
          filter: 'drop-shadow(2px 2px 4px rgba(0, 0, 0, 0.3))'
        }} 
      />
      <Typography
        variant="h3"
        component="h1"
        sx={{
          textAlign: 'center',
          color: 'white',
          fontWeight: 'bold',
          fontSize: { xs: '2rem', sm: '2.5rem', md: '3rem' },
          textShadow: '2px 2px 4px rgba(0, 0, 0, 0.3)'
        }}
      >
        B-Docs
      </Typography>
    </Box>
  );
};

export default PageTitle;
