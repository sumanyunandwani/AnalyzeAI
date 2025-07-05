import React from 'react';
import { FormControl, InputLabel, Select, MenuItem } from '@mui/material';

const businessDomains = [
  { value: 'finance', label: 'Finance' },
  { value: 'healthcare', label: 'Healthcare' },
  { value: 'retail', label: 'Retail' },
  { value: 'technology', label: 'Technology' },
  { value: 'manufacturing', label: 'Manufacturing' },
  { value: 'education', label: 'Education' },
  { value: 'logistics', label: 'Logistics' },
  { value: 'marketing', label: 'Marketing' },
  { value: 'hr', label: 'Human Resources' },
  { value: 'sales', label: 'Sales' },
];

const BusinessDomainSelect = ({ value, onChange, disabled = false }) => {
  return (
    <FormControl fullWidth sx={{ mb: 2 }} disabled={disabled}>
      <InputLabel id="business-domain-label">
        {disabled ? 'Enter SQL query first' : 'Select business domain'}
      </InputLabel>
      <Select
        labelId="business-domain-label"
        id="business-domain-select"
        value={value}
        label={disabled ? 'Enter SQL query first' : 'Select business domain'}
        onChange={onChange}
        sx={{
          '& .MuiOutlinedInput-notchedOutline': {
            borderColor: 'rgba(0, 0, 0, 0.23)',
          },
          '&:hover .MuiOutlinedInput-notchedOutline': {
            borderColor: disabled ? 'rgba(0, 0, 0, 0.23)' : '#667eea',
          },
          '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
            borderColor: '#764ba2',
          },
          '&.Mui-disabled': {
            backgroundColor: 'rgba(0, 0, 0, 0.04)',
          }
        }}
      >
        <MenuItem value="">
          <em>None</em>
        </MenuItem>
        {businessDomains.map((domain) => (
          <MenuItem key={domain.value} value={domain.value}>
            {domain.label}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export default BusinessDomainSelect;
