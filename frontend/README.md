# AnalyzeAI Frontend

This is a minimal React application with Material-UI (MUI) system design.

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install --legacy-peer-deps
```

### Running the Application

Start the development server:
```bash
npm start
```

The application will open in your browser at [http://localhost:3000](http://localhost:3000).

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm build` - Builds the app for production
- `npm test` - Runs the test suite

## API Integration

The application includes a placeholder for API integration in `src/services/api.js`. 

### Current Implementation (Mock)
- Simulates a 3-second API response time
- 90% success rate simulation
- Generates mock document metadata

### To Integrate Real API
1. Navigate to `src/services/api.js`
2. Replace the `generateDocument` function with your actual API call
3. Update the endpoint URL and request format as needed

Example:
```javascript
export const generateDocument = async ({ sqlQuery, businessDomain }) => {
  const response = await fetch('YOUR_API_ENDPOINT/generate-document', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      // Add authentication headers if needed
    },
    body: JSON.stringify({ sqlQuery, businessDomain }),
  });
  
  if (!response.ok) {
    throw new Error('Failed to generate document');
  }
  
  return await response.json();
};
```

## Features

- SQL Query input with validation
- Business domain selection (disabled until query is entered)
- Loading state with informative message about AnalyzeAI
- Success/Error notifications
- Automatic form reset after successful download
- Mock file download functionality

## Tech Stack

- React 18
- Material-UI v5
- Emotion (for styling)
- MUI Lab (for additional components)

## Project Structure

```
src/
├── components/
│   ├── common/         # Reusable components
│   ├── home/          # Home page specific components
│   └── layout/        # Layout components
├── services/          # API services
├── utils/             # Helper functions
└── constants/         # Application constants
```
