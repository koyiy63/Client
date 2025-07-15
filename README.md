# Jagarnath API Documentation

Welcome to the Jagarnath project - a comprehensive multi-language API and component library. This documentation covers all public APIs, functions, and components available in this project.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Getting Started](#getting-started)
3. [API Documentation](#api-documentation)
   - [Python APIs](#python-apis)
   - [JavaScript/TypeScript APIs](#javascripttypescript-apis)
   - [REST API](#rest-api)
4. [Component Documentation](#component-documentation)
   - [React Components](#react-components)
   - [Vue Components](#vue-components)
5. [Usage Examples](#usage-examples)
6. [Contributing](#contributing)

## Project Overview

Jagarnath is a comprehensive library providing:
- **Python APIs**: Data processing, machine learning utilities, and web scraping tools
- **JavaScript/TypeScript APIs**: Frontend utilities, data validation, and UI helpers
- **REST API**: HTTP endpoints for data operations and user management
- **React Components**: Reusable UI components with TypeScript support
- **Vue Components**: Vue 3 composition API components

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd jagarnath

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install

# Start the development server
npm run dev
```

## API Documentation

### Python APIs

The Python APIs are located in the `src/python/` directory and provide various utilities for data processing, machine learning, and web scraping.

#### Core Modules

- **DataProcessor**: Advanced data manipulation and transformation utilities
- **MLUtils**: Machine learning helper functions and model utilities
- **WebScraper**: Web scraping and data extraction tools
- **FileUtils**: File handling and I/O operations

#### Quick Start Example

```python
from jagarnath.data_processor import DataProcessor
from jagarnath.ml_utils import MLUtils

# Initialize data processor
processor = DataProcessor()

# Process data
data = processor.load_csv("data.csv")
processed_data = processor.clean_data(data)

# Use ML utilities
ml_utils = MLUtils()
model = ml_utils.train_model(processed_data)
```

### JavaScript/TypeScript APIs

The JavaScript/TypeScript APIs are located in the `src/js/` directory and provide frontend utilities, data validation, and UI helpers.

#### Core Modules

- **DataValidator**: Comprehensive data validation utilities
- **UIHelpers**: DOM manipulation and UI enhancement functions
- **StorageUtils**: Local storage and session management
- **NetworkUtils**: HTTP request utilities and API helpers

#### Quick Start Example

```typescript
import { DataValidator, UIHelpers, StorageUtils } from '@jagarnath/core';

// Validate data
const validator = new DataValidator();
const isValid = validator.validateEmail('user@example.com');

// UI manipulation
const ui = new UIHelpers();
ui.showNotification('Success!', 'success');

// Storage operations
const storage = new StorageUtils();
storage.setItem('user', { id: 1, name: 'John' });
```

### REST API

The REST API is built with FastAPI and provides HTTP endpoints for various operations.

#### Base URL
```
http://localhost:8000/api/v1
```

#### Authentication
All API endpoints require authentication using Bearer tokens:
```
Authorization: Bearer <your-token>
```

#### Available Endpoints

- **Users**: User management operations
- **Data**: Data processing and retrieval
- **Analytics**: Analytics and reporting endpoints

## Component Documentation

### React Components

React components are located in `src/components/react/` and provide reusable UI elements with TypeScript support.

#### Available Components

- **Button**: Customizable button component with multiple variants
- **Modal**: Modal dialog component with backdrop
- **Form**: Form components with validation
- **Table**: Data table component with sorting and pagination

#### Usage Example

```tsx
import { Button, Modal, Form } from '@jagarnath/react';

function App() {
  return (
    <div>
      <Button variant="primary" onClick={() => console.log('clicked')}>
        Click Me
      </Button>
      
      <Modal isOpen={true} onClose={() => {}}>
        <h2>Modal Content</h2>
      </Modal>
    </div>
  );
}
```

### Vue Components

Vue components are located in `src/components/vue/` and use Vue 3 composition API.

#### Available Components

- **VButton**: Vue button component with slots
- **VModal**: Vue modal component
- **VForm**: Vue form components
- **VTable**: Vue data table component

#### Usage Example

```vue
<template>
  <div>
    <VButton @click="handleClick" variant="primary">
      Click Me
    </VButton>
    
    <VModal v-model="showModal">
      <template #header>
        <h2>Modal Header</h2>
      </template>
      <template #default>
        <p>Modal content</p>
      </template>
    </VModal>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { VButton, VModal } from '@jagarnath/vue';

const showModal = ref(false);

const handleClick = () => {
  showModal.value = true;
};
</script>
```

## Usage Examples

### Complete Python Workflow

```python
from jagarnath.data_processor import DataProcessor
from jagarnath.ml_utils import MLUtils
from jagarnath.web_scraper import WebScraper

# Initialize components
processor = DataProcessor()
ml_utils = MLUtils()
scraper = WebScraper()

# Scrape data
raw_data = scraper.scrape_website("https://example.com")

# Process data
cleaned_data = processor.clean_data(raw_data)
transformed_data = processor.transform_data(cleaned_data)

# Train model
model = ml_utils.train_model(transformed_data)
predictions = ml_utils.predict(model, new_data)
```

### Complete JavaScript Workflow

```typescript
import { DataValidator, UIHelpers, StorageUtils, NetworkUtils } from '@jagarnath/core';

// Initialize utilities
const validator = new DataValidator();
const ui = new UIHelpers();
const storage = new StorageUtils();
const network = new NetworkUtils();

// Validate form data
const formData = {
  email: 'user@example.com',
  password: 'password123'
};

if (validator.validateForm(formData)) {
  // Send data to server
  const response = await network.post('/api/users', formData);
  
  // Store user data
  storage.setItem('user', response.data);
  
  // Show success message
  ui.showNotification('User created successfully!', 'success');
}
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and contribute to the project.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run the test suite: `npm test` and `python -m pytest`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check our [FAQ](FAQ.md)
- Join our Discord community

---

**Last updated**: July 2024
**Version**: 1.0.0