import React from 'react';
import { Paper } from '@mui/material';
import SqlQueryInput from './SqlQueryInput';
import BusinessDomainSelect from './BusinessDomainSelect';
import DownloadButton from './DownloadButton';

const QueryForm = ({ 
  sqlQuery, 
  setSqlQuery, 
  businessDomain, 
  setBusinessDomain, 
  onDownload 
}) => {
  const isQueryEmpty = !sqlQuery || sqlQuery.trim() === '';
  const isFormValid = !isQueryEmpty && businessDomain;

  const handleDownload = () => {
    if (isFormValid) {
      onDownload({ sqlQuery, businessDomain });
    }
  };

  return (
    <Paper
      elevation={6}
      sx={{
        p: 3,
        background: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(10px)',
        borderRadius: 3,
        boxShadow: '0 15px 35px rgba(0, 0, 0, 0.1), 0 5px 15px rgba(0, 0, 0, 0.07)'
      }}
    >
      <SqlQueryInput 
        value={sqlQuery}
        onChange={(e) => setSqlQuery(e.target.value)}
      />
      
      <BusinessDomainSelect
        value={businessDomain}
        onChange={(e) => setBusinessDomain(e.target.value)}
        disabled={isQueryEmpty}
      />
      
      <DownloadButton 
        onClick={handleDownload}
        disabled={!isFormValid}
      />
    </Paper>
  );
};

export default QueryForm;
