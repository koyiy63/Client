# Jagarnath API Documentation

## Table of Contents

1. [Overview](#overview)
2. [Python APIs](#python-apis)
3. [JavaScript/TypeScript APIs](#javascripttypescript-apis)
4. [REST API](#rest-api)
5. [React Components](#react-components)
6. [Vue Components](#vue-components)
7. [Usage Examples](#usage-examples)
8. [Installation](#installation)

## Overview

Jagarnath is a comprehensive multi-language library providing data processing, machine learning, web scraping, and UI components. This documentation covers all public APIs, functions, and components.

## Python APIs

### DataProcessor

Advanced data processing and transformation utilities.

```python
from jagarnath.data_processor import DataProcessor

# Initialize processor
processor = DataProcessor(encoding="utf-8", max_memory=1024)

# Load data
data = processor.load_csv("data.csv")
data = processor.load_json("data.json")

# Clean data
cleaned_data = processor.clean_data(
    data, 
    remove_duplicates=True,
    handle_missing="fill_mean",
    remove_outliers=True
)

# Transform data
transformed_data = processor.transform_data(
    cleaned_data,
    normalize=True,
    encode_categorical=True,
    create_features=True
)

# Export data
processor.export_to_csv(transformed_data, "output.csv")
processor.export_to_json(transformed_data, "output.json")

# Get statistics
stats = processor.get_statistics(data)
```

### MLUtils

Machine learning utilities for model training and evaluation.

```python
from jagarnath.ml_utils import MLUtils

# Initialize ML utilities
ml_utils = MLUtils(random_state=42, model_storage="models/")

# Train model
model, training_info = ml_utils.train_model(
    data, 
    target_column="target",
    algorithm="random_forest_classifier",
    test_size=0.2
)

# Make predictions
predictions = ml_utils.predict(model, new_data)
predictions, probabilities = ml_utils.predict(model, new_data, return_probabilities=True)

# Evaluate model
metrics = ml_utils.evaluate_model(model, test_data, "target")

# Cross-validation
cv_results = ml_utils.cross_validate(data, "target", "random_forest_classifier", cv_folds=5)

# Hyperparameter tuning
best_model, tuning_results = ml_utils.hyperparameter_tuning(data, "target")

# Save/load models
ml_utils.save_model(model, "my_model.pkl")
loaded_model, metadata = ml_utils.load_model("my_model.pkl")

# Feature importance
importance = ml_utils.get_feature_importance(model, feature_names)
```

### WebScraper

Web scraping utilities with rate limiting and data extraction.

```python
from jagarnath.web_scraper import WebScraper

# Initialize scraper
scraper = WebScraper(delay=1.0, max_retries=3, timeout=30)

# Scrape single website
data = scraper.scrape_website(
    "https://example.com",
    selectors={"title": "h1", "content": ".article-content"},
    extract_text=True,
    extract_links=True
)

# Scrape articles
articles = scraper.scrape_articles(
    "https://news.com",
    article_selector="article",
    title_selector="h1, h2, h3",
    content_selector="p",
    max_pages=5
)

# Scrape table data
df = scraper.scrape_table(
    "https://example.com/data",
    table_selector="table",
    header_row=0,
    extract_links=False
)

# Scrape API
api_data = scraper.scrape_api(
    "https://api.example.com/data",
    params={"page": 1, "limit": 10},
    method="GET"
)

# Export data
scraper.export_data(data, "scraped_data.json", format="json")
scraper.export_data(df, "table_data.csv", format="csv")

# Get statistics
stats = scraper.get_scraping_stats()
```

### FileUtils

File handling and I/O operations utilities.

```python
from jagarnath.file_utils import FileUtils

# Initialize file utilities
file_utils = FileUtils(encoding="utf-8", backup_enabled=True)

# Read files
data = file_utils.read_json("config.json")
df = file_utils.read_csv("data.csv")
yaml_data = file_utils.read_yaml("config.yaml")
pickle_data = file_utils.read_pickle("model.pkl")
xml_root = file_utils.read_xml("config.xml")

# Write files
file_utils.write_json(data, "output.json", indent=2)
file_utils.write_csv(df, "output.csv", index=False)
file_utils.write_yaml(data, "output.yaml")
file_utils.write_pickle(model, "model.pkl")
file_utils.write_xml(element, "output.xml")

# Compression
file_utils.compress_directory("data/", "archive.zip", "zip")
file_utils.extract_archive("archive.zip", "extracted/")

# File operations
file_utils.copy_file("source.txt", "backup.txt")
file_utils.move_file("temp.txt", "final.txt")
file_utils.delete_file("old.log", confirm=True)

# File information
info = file_utils.get_file_info("data.csv")
```

## JavaScript/TypeScript APIs

### DataValidator

Comprehensive data validation utilities.

```typescript
import { DataValidator } from '@jagarnath/core';

const validator = new DataValidator();

// Validate basic types
const isValidEmail = validator.validateEmail('user@example.com');
const isValidPhone = validator.validatePhone('+1-555-123-4567');
const isValidUrl = validator.validateUrl('https://example.com');
const isValidPattern = validator.validatePattern('ABC123', /^[A-Z]{3}\d{3}$/);

// Validate with rules
const rules = {
  required: true,
  minLength: 3,
  maxLength: 10,
  pattern: /^[a-zA-Z]+$/
};

const result = validator.validateValue('ab', rules);
console.log(result.isValid); // false
console.log(result.errors); // ['Minimum length is 3 characters']

// Form validation
const formData = {
  email: 'user@example.com',
  password: '123',
  confirmPassword: '123'
};

const formRules = {
  email: { required: true, pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/ },
  password: { required: true, minLength: 6 },
  confirmPassword: { 
    required: true, 
    custom: (value) => value === formData.password || 'Passwords do not match'
  }
};

const formResult = validator.validateForm(formData, formRules);

// Sanitize input
const sanitized = validator.sanitizeInput('<script>alert("xss")</script>');

// Validate and sanitize
const validationResult = validator.validateAndSanitize(data, rules);
```

### UIHelpers

UI manipulation and enhancement utilities.

```typescript
import { UIHelpers } from '@jagarnath/core';

const ui = new UIHelpers();

// Show notifications
ui.showNotification('Success!', 'success');
ui.showNotification('Error occurred!', 'error', {
  duration: 5000,
  position: 'top-center',
  closable: true
});

// Scroll to element
ui.scrollToElement('#target', { duration: 1000 });

// Toggle element visibility
ui.toggleElement('#sidebar');
ui.toggleElement('#modal', true); // Force show
ui.toggleElement('#tooltip', false); // Force hide

// Modal management
const modal = ui.showModal(`
  <h2>Confirm Action</h2>
  <p>Are you sure you want to proceed?</p>
  <button onclick="confirm()">Yes</button>
  <button onclick="cancel()">No</button>
`, {
  closable: true,
  backdrop: true
});

ui.closeModal(modal, () => console.log('Modal closed'));

// Loading spinners
const spinner = ui.addSpinner('#submit-btn', 'Loading...');
setTimeout(() => ui.removeSpinner(spinner), 2000);

// Animations
ui.animate('#element', { opacity: 1 }, { duration: 500 });
ui.animate('#element', { 
  transform: 'translateX(100px) rotate(45deg)',
  opacity: 0.8
}, {
  duration: 1000,
  easing: 'ease-in-out',
  onComplete: () => console.log('Animation complete')
});

// Debounce and throttle
const debouncedSearch = ui.debounce((query: string) => {
  console.log('Searching for:', query);
}, 300);

const throttledScroll = ui.throttle(() => {
  console.log('Scroll position:', window.scrollY);
}, 100);
```

### StorageUtils

Local storage and session management utilities.

```typescript
import { StorageUtils } from '@jagarnath/core';

const storage = new StorageUtils();

// Basic operations
storage.setItem('user', { id: 1, name: 'John' });
const user = storage.getItem('user');
storage.removeItem('user');
storage.clear();

// Session storage
storage.setSessionItem('token', 'abc123');
const token = storage.getSessionItem('token');

// Complex data
storage.setItem('settings', { theme: 'dark', language: 'en' });
const settings = storage.getItem('settings');

// Check if key exists
if (storage.hasItem('user')) {
  // Key exists
}

// Get all keys
const keys = storage.getAllKeys();

// Subscribe to changes
const unsubscribe = storage.subscribe('user', (newValue, oldValue) => {
  console.log('User data changed:', newValue, oldValue);
});
```

### NetworkUtils

HTTP request utilities and API helpers.

```typescript
import { NetworkUtils } from '@jagarnath/core';

const network = new NetworkUtils({
  baseURL: 'https://api.example.com',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// GET request
const users = await network.get('/users', { page: 1, limit: 10 });

// POST request
const newUser = await network.post('/users', {
  name: 'John Doe',
  email: 'john@example.com'
});

// PUT request
const updatedUser = await network.put('/users/1', {
  name: 'John Smith'
});

// DELETE request
await network.delete('/users/1');

// With authentication
const authNetwork = new NetworkUtils({
  baseURL: 'https://api.example.com',
  headers: {
    'Authorization': 'Bearer token123'
  }
});

// Handle errors
try {
  const data = await network.get('/protected');
} catch (error) {
  console.error('Request failed:', error.message);
}
```

## REST API

### Base URL
```
http://localhost:8000/api/v1
```

### Authentication
All protected endpoints require Bearer token authentication:
```
Authorization: Bearer <your-jwt-token>
```

### Endpoints

#### User Management

```bash
# Create user
POST /api/v1/users
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "password123",
  "full_name": "John Doe",
  "role": "user"
}

# Get users (admin only)
GET /api/v1/users?skip=0&limit=100

# Get user by ID
GET /api/v1/users/{user_id}

# Update user
PUT /api/v1/users/{user_id}
{
  "full_name": "John Smith"
}

# Delete user
DELETE /api/v1/users/{user_id}
```

#### Authentication

```bash
# Login
POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "password123"
}

# Get current user
GET /api/v1/auth/me
```

#### Data Processing

```bash
# Process data
POST /api/v1/data/process
{
  "data": [
    {"id": 1, "name": "John", "age": 30},
    {"id": 2, "name": "Jane", "age": 25}
  ],
  "operation": "filter",
  "parameters": {
    "filters": {"age": 30}
  }
}
```

#### Analytics

```bash
# Get analytics
POST /api/v1/analytics
{
  "metric": "user_count",
  "filters": {"role": "user"},
  "time_range": "last_30_days"
}
```

## React Components

### Button

```tsx
import { Button } from '@jagarnath/react';

function App() {
  return (
    <div>
      {/* Basic usage */}
      <Button onClick={() => console.log('clicked')}>
        Click Me
      </Button>
      
      {/* With variant and size */}
      <Button variant="success" size="large">
        Success Button
      </Button>
      
      {/* Loading state */}
      <Button loading loadingText="Saving...">
        Save
      </Button>
      
      {/* With icons */}
      <Button 
        leftIcon={<Icon name="plus" />} 
        rightIcon={<Icon name="arrow-right" />}
      >
        Add Item
      </Button>
      
      {/* Full width and rounded */}
      <Button fullWidth rounded variant="primary">
        Full Width Button
      </Button>
      
      {/* Ghost button */}
      <Button ghost variant="outline-primary">
        Ghost Button
      </Button>
    </div>
  );
}
```

### Modal

```tsx
import { Modal } from '@jagarnath/react';

function App() {
  const [isOpen, setIsOpen] = useState(false);
  
  return (
    <div>
      <Button onClick={() => setIsOpen(true)}>
        Open Modal
      </Button>
      
      <Modal 
        isOpen={isOpen} 
        onClose={() => setIsOpen(false)}
        title="Confirm Action"
        size="medium"
        closable={true}
        backdrop={true}
      >
        <p>Are you sure you want to proceed?</p>
        <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
          <Button variant="secondary" onClick={() => setIsOpen(false)}>
            Cancel
          </Button>
          <Button variant="primary" onClick={() => {
            // Handle confirmation
            setIsOpen(false);
          }}>
            Confirm
          </Button>
        </div>
      </Modal>
    </div>
  );
}
```

### Form

```tsx
import { Form, FormField } from '@jagarnath/react';

function App() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });
  
  const validationRules = {
    name: { required: true, minLength: 2 },
    email: { required: true, pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/ },
    message: { required: true, minLength: 10 }
  };
  
  return (
    <Form
      data={formData}
      onDataChange={setFormData}
      validationRules={validationRules}
      onSubmit={(data) => console.log('Form submitted:', data)}
    >
      <FormField
        name="name"
        label="Name"
        type="text"
        placeholder="Enter your name"
        required
      />
      
      <FormField
        name="email"
        label="Email"
        type="email"
        placeholder="Enter your email"
        required
      />
      
      <FormField
        name="message"
        label="Message"
        type="textarea"
        placeholder="Enter your message"
        rows={4}
        required
      />
      
      <Button type="submit" variant="primary">
        Submit
      </Button>
    </Form>
  );
}
```

### Table

```tsx
import { Table } from '@jagarnath/react';

function App() {
  const data = [
    { id: 1, name: 'John Doe', email: 'john@example.com', role: 'Admin' },
    { id: 2, name: 'Jane Smith', email: 'jane@example.com', role: 'User' }
  ];
  
  const columns = [
    { key: 'id', label: 'ID', sortable: true },
    { key: 'name', label: 'Name', sortable: true },
    { key: 'email', label: 'Email', sortable: true },
    { key: 'role', label: 'Role', sortable: true },
    {
      key: 'actions',
      label: 'Actions',
      render: (row) => (
        <div>
          <Button size="small" variant="outline-primary">Edit</Button>
          <Button size="small" variant="outline-danger">Delete</Button>
        </div>
      )
    }
  ];
  
  return (
    <Table
      data={data}
      columns={columns}
      sortable={true}
      pagination={true}
      searchable={true}
      selectable={true}
      onRowSelect={(selectedRows) => console.log('Selected:', selectedRows)}
      onSort={(sortConfig) => console.log('Sort:', sortConfig)}
    />
  );
}
```

## Vue Components

### VButton

```vue
<template>
  <div>
    <!-- Basic usage -->
    <VButton @click="handleClick">
      Click Me
    </VButton>
    
    <!-- With variant and size -->
    <VButton variant="success" size="large">
      Success Button
    </VButton>
    
    <!-- Loading state -->
    <VButton :loading="true" loading-text="Saving...">
      Save
    </VButton>
    
    <!-- With slots -->
    <VButton variant="primary">
      <template #left-icon>
        <Icon name="plus" />
      </template>
      Add Item
      <template #right-icon>
        <Icon name="arrow-right" />
      </template>
    </VButton>
  </div>
</template>

<script setup>
import { VButton } from '@jagarnath/vue';

const handleClick = () => {
  console.log('Button clicked');
};
</script>
```

### VModal

```vue
<template>
  <div>
    <VButton @click="showModal = true">
      Open Modal
    </VButton>
    
    <VModal v-model="showModal" title="Confirm Action" size="medium">
      <template #header>
        <h2>Confirm Action</h2>
      </template>
      
      <template #default>
        <p>Are you sure you want to proceed?</p>
      </template>
      
      <template #footer>
        <VButton variant="secondary" @click="showModal = false">
          Cancel
        </VButton>
        <VButton variant="primary" @click="confirm">
          Confirm
        </VButton>
      </template>
    </VModal>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { VButton, VModal } from '@jagarnath/vue';

const showModal = ref(false);

const confirm = () => {
  // Handle confirmation
  showModal.value = false;
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
model = ml_utils.train_model(transformed_data, target_column="target")
predictions = ml_utils.predict(model, new_data)

# Export results
processor.export_to_csv(transformed_data, "processed_data.csv")
ml_utils.save_model(model, "trained_model.pkl")
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

## Installation

### Python

```bash
pip install jagarnath
```

### JavaScript/TypeScript

```bash
npm install @jagarnath/core @jagarnath/react @jagarnath/vue
```

### REST API

```bash
# Install dependencies
pip install fastapi uvicorn

# Run the API
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation at `/docs` when running the REST API
- Join our Discord community

---

**Version**: 1.0.0  
**Last Updated**: July 2024