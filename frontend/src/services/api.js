/**
 * Mock API service for B-Docs
 * Replace the mockGenerateDocument function with actual API call
 */

// Mock API delay (simulates network latency)
const API_MOCK_DELAY = 3000; // 3 seconds

/**
 * Generates B-Doc based on SQL query and business domain
 * @param {Object} params - Request parameters
 * @param {string} params.sqlQuery - SQL query to analyze
 * @param {string} params.businessDomain - Selected business domain
 * @returns {Promise<Object>} - API response
 */
export const generateDocument = async ({ sqlQuery, businessDomain }) => {
  try {
    // TODO: Replace this mock with actual API call
    // Example:
    // const response = await fetch('/api/generate-document', {
    //   method: 'POST',
    //   headers: {
    //     'Content-Type': 'application/json',
    //   },
    //   body: JSON.stringify({ sqlQuery, businessDomain }),
    // });
    // const data = await response.json();
    // return data;

    // Mock implementation
    return await mockGenerateDocument({ sqlQuery, businessDomain });
  } catch (error) {
    console.error('Error generating document:', error);
    throw error;
  }
};

/**
 * Mock function to simulate API response
 * Remove this when implementing actual API
 */
const mockGenerateDocument = ({ sqlQuery, businessDomain }) => {
  return new Promise((resolve, reject) => {
    // Simulate API processing time
    setTimeout(() => {
      // Simulate random success/failure (90% success rate)
      if (Math.random() > 0.9) {
        reject(new Error('Failed to generate document. Please try again.'));
      } else {
        resolve({
          success: true,
          data: {
            documentId: `DOC-${Date.now()}`,
            fileName: `${businessDomain}_analysis_${new Date().toISOString().slice(0, 10)}.pdf`,
            fileSize: Math.floor(Math.random() * 1000) + 500, // Random size between 500-1500 KB
            generatedAt: new Date().toISOString(),
            downloadUrl: `https://api.example.com/documents/download/${Date.now()}`,
            message: 'Document generated successfully'
          }
        });
      }
    }, API_MOCK_DELAY);
  });
};
