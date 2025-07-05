import React from 'react';
import { Button } from '@mui/material';

const DownloadButton = ({ onClick, disabled = false, label = "Download B-Doc" }) => {
  return (
    <Button
      variant="contained"
      size="large"
      fullWidth
      onClick={onClick}
      disabled={disabled}
      sx={{
        py: 1.5,
        fontSize: '1.1rem',
        textTransform: 'none',
        background: disabled 
          ? 'linear-gradient(135deg, #9ca3af 0%, #6b7280 100%)'
          : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        boxShadow: disabled 
          ? 'none'
          : '0 4px 15px rgba(102, 126, 234, 0.4)',
        transition: 'all 0.3s ease',
        '&:hover': {
          background: disabled
            ? 'linear-gradient(135deg, #9ca3af 0%, #6b7280 100%)'
            : 'linear-gradient(135deg, #764ba2 0%, #667eea 100%)',
          transform: disabled ? 'none' : 'translateY(-2px)',
          boxShadow: disabled 
            ? 'none'
            : '0 6px 20px rgba(102, 126, 234, 0.6)',
        },
        '&.Mui-disabled': {
          color: 'rgba(255, 255, 255, 0.7)',
        }
      }}
    >
      {label}
    </Button>
  );
};

export default DownloadButton;
