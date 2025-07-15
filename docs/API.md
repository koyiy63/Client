# API Documentation

## Overview

This document provides detailed documentation for all public APIs in the project.

## Authentication

### API Keys

Most endpoints require authentication via API key. Include your API key in the request headers:

```javascript
const headers = {
  'Authorization': 'Bearer YOUR_API_KEY',
  'Content-Type': 'application/json'
};
```

### Rate Limiting

- **Rate Limit:** 1000 requests per hour per API key
- **Rate Limit Header:** `X-RateLimit-Remaining`
- **Reset Time:** `X-RateLimit-Reset`

## Endpoints

### Users API

#### `GET /api/users`

**Description:** Retrieve a list of users.

**Query Parameters:**
- `page` (number, optional) - Page number (default: 1)
- `limit` (number, optional) - Items per page (default: 10, max: 100)
- `search` (string, optional) - Search term for user names or emails
- `role` (string, optional) - Filter by user role

**Response:**
```json
{
  "users": [
    {
      "id": "123",
      "name": "John Doe",
      "email": "john@example.com",
      "role": "admin",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100,
    "pages": 10
  }
}
```

**Example:**
```javascript
import { apiService } from './src/services/api';

async function getUsers() {
  try {
    const response = await apiService.get('/api/users?page=1&limit=20&role=admin');
    console.log('Users:', response.users);
    console.log('Total pages:', response.pagination.pages);
  } catch (error) {
    console.error('Error fetching users:', error);
  }
}
```

#### `GET /api/users/:id`

**Description:** Retrieve a specific user by ID.

**Path Parameters:**
- `id` (string) - User ID

**Response:**
```json
{
  "id": "123",
  "name": "John Doe",
  "email": "john@example.com",
  "role": "admin",
  "profile": {
    "avatar": "https://example.com/avatar.jpg",
    "bio": "Software developer"
  },
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-20T15:45:00Z"
}
```

**Example:**
```javascript
async function getUserById(userId) {
  try {
    const user = await apiService.get(`/api/users/${userId}`);
    console.log('User details:', user);
  } catch (error) {
    if (error.status === 404) {
      console.log('User not found');
    } else {
      console.error('Error fetching user:', error);
    }
  }
}
```

#### `POST /api/users`

**Description:** Create a new user.

**Request Body:**
```json
{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "password": "securepassword123",
  "role": "user"
}
```

**Response:**
```json
{
  "id": "124",
  "name": "Jane Smith",
  "email": "jane@example.com",
  "role": "user",
  "created_at": "2024-01-21T09:15:00Z"
}
```

**Example:**
```javascript
async function createUser(userData) {
  try {
    const newUser = await apiService.post('/api/users', userData);
    console.log('Created user:', newUser);
    return newUser;
  } catch (error) {
    if (error.status === 400) {
      console.log('Validation error:', error.message);
    } else {
      console.error('Error creating user:', error);
    }
    throw error;
  }
}
```

#### `PUT /api/users/:id`

**Description:** Update an existing user.

**Path Parameters:**
- `id` (string) - User ID

**Request Body:**
```json
{
  "name": "Jane Smith Updated",
  "email": "jane.updated@example.com"
}
```

**Response:**
```json
{
  "id": "124",
  "name": "Jane Smith Updated",
  "email": "jane.updated@example.com",
  "role": "user",
  "updated_at": "2024-01-21T10:30:00Z"
}
```

**Example:**
```javascript
async function updateUser(userId, updateData) {
  try {
    const updatedUser = await apiService.put(`/api/users/${userId}`, updateData);
    console.log('Updated user:', updatedUser);
    return updatedUser;
  } catch (error) {
    console.error('Error updating user:', error);
    throw error;
  }
}
```

#### `DELETE /api/users/:id`

**Description:** Delete a user.

**Path Parameters:**
- `id` (string) - User ID

**Response:**
```json
{
  "message": "User deleted successfully"
}
```

**Example:**
```javascript
async function deleteUser(userId) {
  try {
    await apiService.delete(`/api/users/${userId}`);
    console.log('User deleted successfully');
  } catch (error) {
    console.error('Error deleting user:', error);
    throw error;
  }
}
```

### Products API

#### `GET /api/products`

**Description:** Retrieve a list of products.

**Query Parameters:**
- `category` (string, optional) - Filter by category
- `price_min` (number, optional) - Minimum price filter
- `price_max` (number, optional) - Maximum price filter
- `sort` (string, optional) - Sort field (name, price, created_at)
- `order` (string, optional) - Sort order (asc, desc)

**Response:**
```json
{
  "products": [
    {
      "id": "prod_123",
      "name": "Sample Product",
      "description": "A sample product description",
      "price": 29.99,
      "category": "electronics",
      "in_stock": true,
      "images": ["https://example.com/image1.jpg"],
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 50,
    "pages": 5
  }
}
```

**Example:**
```javascript
async function getProducts(filters = {}) {
  try {
    const queryParams = new URLSearchParams(filters);
    const response = await apiService.get(`/api/products?${queryParams}`);
    return response.products;
  } catch (error) {
    console.error('Error fetching products:', error);
    throw error;
  }
}

// Usage
const electronics = await getProducts({
  category: 'electronics',
  price_min: 10,
  price_max: 100,
  sort: 'price',
  order: 'asc'
});
```

### Orders API

#### `POST /api/orders`

**Description:** Create a new order.

**Request Body:**
```json
{
  "user_id": "123",
  "items": [
    {
      "product_id": "prod_123",
      "quantity": 2
    }
  ],
  "shipping_address": {
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip": "10001",
    "country": "USA"
  }
}
```

**Response:**
```json
{
  "id": "order_456",
  "user_id": "123",
  "items": [
    {
      "product_id": "prod_123",
      "quantity": 2,
      "price": 29.99,
      "total": 59.98
    }
  ],
  "total": 59.98,
  "status": "pending",
  "created_at": "2024-01-21T11:00:00Z"
}
```

## Error Handling

### Error Response Format

All API errors follow this format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": {
      "field": "email",
      "value": "invalid-email"
    }
  }
}
```

### Common Error Codes

- `400` - Bad Request (validation errors)
- `401` - Unauthorized (invalid API key)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found (resource doesn't exist)
- `429` - Too Many Requests (rate limit exceeded)
- `500` - Internal Server Error

### Error Handling Example

```javascript
class APIError extends Error {
  constructor(message, status, code, details) {
    super(message);
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

async function handleAPIError(response) {
  if (!response.ok) {
    const errorData = await response.json();
    throw new APIError(
      errorData.error.message,
      response.status,
      errorData.error.code,
      errorData.error.details
    );
  }
  return response.json();
}

// Usage in API service
async function apiCall(endpoint, options = {}) {
  try {
    const response = await fetch(endpoint, {
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    });
    
    return await handleAPIError(response);
  } catch (error) {
    if (error instanceof APIError) {
      // Handle specific API errors
      switch (error.code) {
        case 'VALIDATION_ERROR':
          console.log('Validation error:', error.details);
          break;
        case 'RATE_LIMIT_EXCEEDED':
          console.log('Rate limit exceeded, retry later');
          break;
        default:
          console.error('API error:', error.message);
      }
    } else {
      // Handle network or other errors
      console.error('Network error:', error);
    }
    throw error;
  }
}
```

## Webhooks

### Webhook Events

The API supports webhooks for real-time notifications:

- `user.created` - When a new user is created
- `user.updated` - When a user is updated
- `order.created` - When a new order is created
- `order.status_changed` - When order status changes

### Webhook Payload Format

```json
{
  "event": "user.created",
  "timestamp": "2024-01-21T12:00:00Z",
  "data": {
    "id": "123",
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

### Webhook Setup

```javascript
// Register webhook endpoint
async function registerWebhook(url, events) {
  const webhookData = {
    url: url,
    events: events
  };
  
  const webhook = await apiService.post('/api/webhooks', webhookData);
  console.log('Webhook registered:', webhook);
  return webhook;
}

// Example usage
registerWebhook('https://your-app.com/webhooks', ['user.created', 'order.created']);
```

## SDK Examples

### JavaScript/TypeScript SDK

```javascript
import { APIClient } from './sdk';

const client = new APIClient({
  apiKey: 'your-api-key',
  baseURL: 'https://api.example.com'
});

// Users
const users = await client.users.list({ page: 1, limit: 10 });
const user = await client.users.get('123');
const newUser = await client.users.create({ name: 'John', email: 'john@example.com' });

// Products
const products = await client.products.list({ category: 'electronics' });
const product = await client.products.get('prod_123');

// Orders
const order = await client.orders.create({
  user_id: '123',
  items: [{ product_id: 'prod_123', quantity: 2 }]
});
```

### Python SDK

```python
from api_client import APIClient

client = APIClient(api_key='your-api-key')

# Users
users = client.users.list(page=1, limit=10)
user = client.users.get('123')
new_user = client.users.create(name='John', email='john@example.com')

# Products
products = client.products.list(category='electronics')
product = client.products.get('prod_123')
```

## Testing

### Test API Endpoints

```bash
# Test authentication
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.example.com/api/users

# Test user creation
curl -X POST \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"name":"Test User","email":"test@example.com"}' \
     https://api.example.com/api/users
```

### Postman Collection

Import the provided Postman collection for testing all endpoints:

```json
{
  "info": {
    "name": "API Documentation",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Users",
      "item": [
        {
          "name": "Get Users",
          "request": {
            "method": "GET",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{api_key}}"
              }
            ],
            "url": {
              "raw": "{{base_url}}/api/users?page=1&limit=10",
              "host": ["{{base_url}}"],
              "path": ["api", "users"],
              "query": [
                {
                  "key": "page",
                  "value": "1"
                },
                {
                  "key": "limit",
                  "value": "10"
                }
              ]
            }
          }
        }
      ]
    }
  ]
}
```