import React from 'react';
import { TextField } from '@mui/material';

const SqlQueryInput = ({ value, onChange, placeholder = "Enter your sql query here" }) => {
  return (
    <TextField
      fullWidth
      multiline
      rows={4}
      variant="outlined"
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      sx={{
        mb: 2,
        '& .MuiOutlinedInput-root': {
          '&:hover fieldset': {
            borderColor: '#667eea',
          },
          '&.Mui-focused fieldset': {
            borderColor: '#764ba2',
          },
        },
        '& .MuiInputBase-input': {
          fontSize: '1rem',
        }
      }}
    />
  );
};

export default SqlQueryInput;
