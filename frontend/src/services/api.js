import API_BASE_URL, { API_BASE_URL1 } from '../config/api';

/**
 * Generates AnalyzeAI based on SQL query and business domain
 * @param {Object} params - Request parameters
 * @param {string} params.sqlQuery - SQL query to analyze
 * @param {string} params.businessDomain - Selected business domain
 * @returns {Promise<Object>} - API response
 */
export const generateDocument = async ({ sqlQuery, businessDomain }) => {
  try {
    const response = await fetch(`${API_BASE_URL1}/prompt/sql`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include', // Include cookies for authentication
      body: JSON.stringify({ 
        script: sqlQuery, 
        business: businessDomain 
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(errorData?.message || `Server error: ${response.status}`);
    }

    const data = await response.json();
    
    // Transform the response to match the expected format
    // Adjust this based on your actual API response structure
    return {
      success: true,
      data: {
        documentId: data.documentId || `DOC-${Date.now()}`,
        fileName: data.fileName || `${businessDomain}_analysis_${new Date().toISOString().slice(0, 10)}.pdf`,
        fileSize: data.fileSize,
        generatedAt: data.generatedAt || new Date().toISOString(),
        downloadUrl: data.downloadUrl,
        message: data.message || 'Document generated successfully',
        // Include the raw response in case there are other fields
        ...data
      }
    };
  } catch (error) {
    console.error('Error generating document:', error);
    throw error;
  }
};

/**
 * Downloads a generated document
 * @param {string} documentId - The ID of the document to download
 * @returns {Promise<Blob>} - The document blob
 */
export const downloadDocument = async (documentId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/documents/${documentId}/download`, {
      method: 'GET',
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error(`Failed to download document: ${response.status}`);
    }

    return await response.blob();
  } catch (error) {
    console.error('Error downloading document:', error);
    throw error;
  }
};

/**
 * Gets the status of a document generation request
 * @param {string} requestId - The ID of the generation request
 * @returns {Promise<Object>} - The status response
 */
export const getDocumentStatus = async (requestId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/documents/status/${requestId}`, {
      method: 'GET',
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error(`Failed to get document status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error getting document status:', error);
    throw error;
  }
};
