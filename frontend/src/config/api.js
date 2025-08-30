// API configuration
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';
export const API_BASE_URL1 = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8001';

export const API_ENDPOINTS = {
  // Authentication endpoints
  LOGIN_GOOGLE: `${API_BASE_URL}/login/google`,
  LOGIN_MICROSOFT: `${API_BASE_URL}/login/microsoft`,
  LOGIN_GITHUB: `${API_BASE_URL}/login/github`,
  AUTH_STATUS: `${API_BASE_URL}/status`,
  AUTH_CALLBACK: `${API_BASE_URL}/auth/callback`,
  LOGOUT: `${API_BASE_URL}/auth/logout`,
  
  // Document generation endpoints
  GENERATE_DOCUMENT: `${API_BASE_URL1}/prompt/sql`,
  DOWNLOAD_DOCUMENT: `${API_BASE_URL1}/documents`,
  DOCUMENT_STATUS: `${API_BASE_URL1}/documents/status`,
  
  // Legacy endpoint (kept for reference)
  GENERATE_DOCUMENT_OLD: `${API_BASE_URL}/api/generate-document`
};

export default API_BASE_URL;
