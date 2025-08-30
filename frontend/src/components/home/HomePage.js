import React, { useState } from 'react';
import { Container, Alert, Snackbar } from '@mui/material';
import PageTitle from '../common/PageTitle';
import ToolDescription from '../common/ToolDescription';
import QueryForm from './QueryForm';
import LoadingState from './LoadingState';
import SuccessState from './SuccessState';
import { generateDocument } from '../../services/api';
import { downloadFile, generateDocumentFilename } from '../../utils/helpers';

const HomePage = () => {
  const [sqlQuery, setSqlQuery] = useState('');
  const [businessDomain, setBusinessDomain] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);
  const [error, setError] = useState(null);
  const [lastDocument, setLastDocument] = useState(null);

  const handleDownload = async ({ sqlQuery, businessDomain }) => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Call API to generate document
      const response = await generateDocument({ sqlQuery, businessDomain });
      
      if (response.success) {
        // Store the document info for re-download
        const documentInfo = {
          sqlQuery,
          businessDomain,
          ...response.data
        };
        setLastDocument(documentInfo);
        
        // Success handling
        console.log('Document generated:', response.data);
        
        // Create and download the document
        performDownload(documentInfo);
        
        // Show success state
        setShowSuccess(true);
      }
    } catch (err) {
      setError(err.message || 'An error occurred while generating the document');
    } finally {
      setIsLoading(false);
    }
  };

  const performDownload = (documentInfo) => {
    // TODO: Implement actual file download using documentInfo.downloadUrl
    // For now, we'll create a mock file
    const mockContent = `
AnalyzeAI ANALYSIS REPORT
=====================

Business Domain: ${documentInfo.businessDomain}
Generated: ${new Date().toISOString()}
Document ID: ${documentInfo.documentId}

SQL Query Analysis:
${documentInfo.sqlQuery}

[This is a mock document. In production, this would contain the actual analysis.]
    `;
    
    downloadFile(
      mockContent, 
      documentInfo.fileName || generateDocumentFilename(documentInfo.businessDomain),
      'text/plain'
    );
  };

  const handleRedownload = () => {
    if (lastDocument) {
      performDownload(lastDocument);
    }
  };

  const handleNewQuery = () => {
    // Reset all states to show initial form
    setSqlQuery('');
    setBusinessDomain('');
    setShowSuccess(false);
    setLastDocument(null);
    setError(null);
  };

  const handleCloseError = () => {
    setError(null);
  };

  return (
    <>
      <Container
        component="main"
        maxWidth="md"
        sx={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          py: 2,
          position: 'relative',
          zIndex: 1,
          overflow: 'auto',
          height: '100%'
        }}
      >
        <PageTitle />
        
        {!isLoading && !showSuccess && <ToolDescription />}
        
        {isLoading ? (
          <LoadingState />
        ) : showSuccess ? (
          <SuccessState 
            onRedownload={handleRedownload}
            onNewQuery={handleNewQuery}
          />
        ) : (
          <QueryForm
            sqlQuery={sqlQuery}
            setSqlQuery={setSqlQuery}
            businessDomain={businessDomain}
            setBusinessDomain={setBusinessDomain}
            onDownload={handleDownload}
          />
        )}
      </Container>

      {/* Error Snackbar */}
      <Snackbar
        open={!!error}
        autoHideDuration={6000}
        onClose={handleCloseError}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseError} severity="error" sx={{ width: '100%' }}>
          {error}
        </Alert>
      </Snackbar>
    </>
  );
};

export default HomePage;
