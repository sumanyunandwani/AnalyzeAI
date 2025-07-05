/**
 * Validates SQL query
 * @param {string} query - SQL query to validate
 * @returns {boolean} - true if query is valid
 */
export const isValidSqlQuery = (query) => {
  if (!query || typeof query !== 'string') return false;
  const trimmedQuery = query.trim();
  return trimmedQuery.length > 0;
};

/**
 * Downloads a file with given content
 * @param {string} content - File content
 * @param {string} filename - Name of the file to download
 * @param {string} contentType - MIME type of the file
 */
export const downloadFile = (content, filename, contentType = 'text/plain') => {
  const blob = new Blob([content], { type: contentType });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
};

/**
 * Generates a document filename based on domain and timestamp
 * @param {string} domain - Business domain
 * @returns {string} - Generated filename
 */
export const generateDocumentFilename = (domain) => {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  return `${domain}_analysis_${timestamp}.doc`;
};
