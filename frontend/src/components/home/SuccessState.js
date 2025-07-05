import React from 'react';
import { Box, Typography, Paper, Button, Stack } from '@mui/material';
import { Download, Refresh } from '@mui/icons-material';

const SuccessState = ({ onRedownload, onNewQuery }) => {
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
      {/* Success Icon */}
      <Box
        sx={{
          width: 80,
          height: 80,
          borderRadius: '50%',
          background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          mx: 'auto',
          mb: 3,
          boxShadow: '0 4px 20px rgba(16, 185, 129, 0.3)'
        }}
      >
        <Download sx={{ fontSize: 40, color: 'white' }} />
      </Box>

      {/* Success Message */}
      <Typography
        variant="h5"
        sx={{
          color: '#10b981',
          fontWeight: 600,
          mb: 2
        }}
      >
        Document Generated Successfully!
      </Typography>

      <Typography
        variant="body1"
        sx={{
          color: '#4a5568',
          mb: 4
        }}
      >
        Your download should start automatically. If not, please click the button below.
      </Typography>

      {/* Action Buttons */}
      <Stack spacing={2}>
        <Button
          variant="contained"
          size="large"
          fullWidth
          startIcon={<Download />}
          onClick={onRedownload}
          sx={{
            py: 1.5,
            fontSize: '1.1rem',
            textTransform: 'none',
            background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
            boxShadow: '0 4px 15px rgba(16, 185, 129, 0.4)',
            transition: 'all 0.3s ease',
            '&:hover': {
              background: 'linear-gradient(135deg, #059669 0%, #10b981 100%)',
              transform: 'translateY(-2px)',
              boxShadow: '0 6px 20px rgba(16, 185, 129, 0.6)',
            }
          }}
        >
          Re-download Document
        </Button>

        <Button
          variant="outlined"
          size="large"
          fullWidth
          startIcon={<Refresh />}
          onClick={onNewQuery}
          sx={{
            py: 1.5,
            fontSize: '1.1rem',
            textTransform: 'none',
            borderColor: '#667eea',
            color: '#667eea',
            borderWidth: 2,
            transition: 'all 0.3s ease',
            '&:hover': {
              borderColor: '#764ba2',
              borderWidth: 2,
              color: '#764ba2',
              backgroundColor: 'rgba(102, 126, 234, 0.05)',
              transform: 'translateY(-2px)',
            }
          }}
        >
          Analyze Another Script
        </Button>
      </Stack>
    </Paper>
  );
};

export default SuccessState;
