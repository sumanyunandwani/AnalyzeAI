import React from 'react';
import { Box, Typography } from '@mui/material';

const ToolDescription = () => {
  return (
    <Box
      sx={{
        textAlign: 'center',
        mb: 3,
        px: 2
      }}
    >
      <Typography
        variant="h6"
        sx={{
          color: 'rgba(255, 255, 255, 0.95)',
          fontWeight: 400,
          mb: 1,
          fontSize: '1.15rem',
          lineHeight: 1.6,
          textShadow: '1px 1px 2px rgba(0, 0, 0, 0.2)'
        }}
      >
        Transform complex SQL queries into comprehensive business documentation
      </Typography>
      <Typography
        variant="body1"
        sx={{
          color: 'rgba(255, 255, 255, 0.85)',
          fontSize: '1rem',
          lineHeight: 1.5,
          textShadow: '1px 1px 2px rgba(0, 0, 0, 0.2)'
        }}
      >
        Instantly generate executive-ready insights with AI-powered analysis
      </Typography>
    </Box>
  );
};

export default ToolDescription;
