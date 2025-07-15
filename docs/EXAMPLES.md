# Examples and Usage Guide

## Overview

This document provides practical examples and usage patterns for all APIs, components, and functions in the project.

## Quick Start Examples

### Basic API Usage

```javascript
import { apiService } from './services/api';

// Fetch users
const users = await apiService.get('/api/users');

// Create a new user
const newUser = await apiService.post('/api/users', {
  name: 'John Doe',
  email: 'john@example.com'
});

// Update user
const updatedUser = await apiService.put('/api/users/123', {
  name: 'John Updated'
});

// Delete user
await apiService.delete('/api/users/123');
```

### React Component Usage

```jsx
import React, { useState } from 'react';
import { Button, Input, Modal, Card } from './components';

function UserForm() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({ name: '', email: '' });

  const handleSubmit = async () => {
    try {
      await apiService.post('/api/users', formData);
      setIsModalOpen(false);
    } catch (error) {
      console.error('Error creating user:', error);
    }
  };

  return (
    <div>
      <Button onClick={() => setIsModalOpen(true)}>
        Add User
      </Button>

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Add New User"
      >
        <Card>
          <Input
            label="Name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          />
          <Input
            label="Email"
            type="email"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          />
          <Button onClick={handleSubmit}>Save</Button>
        </Card>
      </Modal>
    </div>
  );
}
```

## API Integration Examples

### User Management System

```javascript
// User service with full CRUD operations
class UserService {
  static async getAllUsers(filters = {}) {
    const queryParams = new URLSearchParams(filters);
    return await apiService.get(`/api/users?${queryParams}`);
  }

  static async getUserById(id) {
    return await apiService.get(`/api/users/${id}`);
  }

  static async createUser(userData) {
    return await apiService.post('/api/users', userData);
  }

  static async updateUser(id, updateData) {
    return await apiService.put(`/api/users/${id}`, updateData);
  }

  static async deleteUser(id) {
    return await apiService.delete(`/api/users/${id}`);
  }

  static async searchUsers(query) {
    return await apiService.get('/api/users/search', {
      params: { q: query }
    });
  }
}

// Usage
const userService = new UserService();

// Get all users with pagination
const users = await userService.getAllUsers({
  page: 1,
  limit: 10,
  role: 'admin'
});

// Create a new user
const newUser = await userService.createUser({
  name: 'Jane Smith',
  email: 'jane@example.com',
  role: 'user'
});

// Search users
const searchResults = await userService.searchUsers('john');
```

### Data Table with API Integration

```jsx
import React, { useState, useEffect } from 'react';
import { Table, Button, Input } from './components';
import { debounce } from './utils';

function UserTable() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({ search: '', role: '' });

  const columns = [
    { key: 'name', label: 'Name', sortable: true },
    { key: 'email', label: 'Email', sortable: true },
    { key: 'role', label: 'Role', filterable: true },
    {
      key: 'actions',
      label: 'Actions',
      render: (user) => (
        <div>
          <Button size="sm" variant="outline" onClick={() => editUser(user)}>
            Edit
          </Button>
          <Button size="sm" variant="danger" onClick={() => deleteUser(user.id)}>
            Delete
          </Button>
        </div>
      )
    }
  ];

  const loadUsers = async () => {
    setLoading(true);
    try {
      const response = await apiService.get('/api/users', { params: filters });
      setUsers(response.users);
    } catch (error) {
      console.error('Error loading users:', error);
    } finally {
      setLoading(false);
    }
  };

  const debouncedSearch = debounce((searchTerm) => {
    setFilters(prev => ({ ...prev, search: searchTerm }));
  }, 300);

  useEffect(() => {
    loadUsers();
  }, [filters]);

  const handleSearch = (e) => {
    debouncedSearch(e.target.value);
  };

  const handleRoleFilter = (e) => {
    setFilters(prev => ({ ...prev, role: e.target.value }));
  };

  return (
    <div>
      <div style={{ marginBottom: '20px' }}>
        <Input
          placeholder="Search users..."
          onChange={handleSearch}
          style={{ marginRight: '10px' }}
        />
        <select onChange={handleRoleFilter}>
          <option value="">All Roles</option>
          <option value="admin">Admin</option>
          <option value="user">User</option>
        </select>
      </div>

      <Table
        data={users}
        columns={columns}
        loading={loading}
        sortable={true}
        filterable={true}
        pagination={true}
        pageSize={10}
      />
    </div>
  );
}
```

## Form Handling Examples

### Complex Form with Validation

```jsx
import React, { useState } from 'react';
import { Form, Input, Select, Button } from './components';
import { validateEmail, validatePassword } from './utils/validation';

function RegistrationForm() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: '',
    role: '',
    agreeToTerms: false
  });

  const [errors, setErrors] = useState({});

  const validateForm = () => {
    const newErrors = {};

    // Required fields
    if (!formData.firstName) newErrors.firstName = 'First name is required';
    if (!formData.lastName) newErrors.lastName = 'Last name is required';
    if (!formData.email) newErrors.email = 'Email is required';
    if (!formData.password) newErrors.password = 'Password is required';
    if (!formData.role) newErrors.role = 'Role is required';

    // Email validation
    if (formData.email && !validateEmail(formData.email)) {
      newErrors.email = 'Invalid email format';
    }

    // Password validation
    if (formData.password) {
      const passwordValidation = validatePassword(formData.password);
      if (!passwordValidation.isValid) {
        newErrors.password = passwordValidation.errors[0];
      }
    }

    // Password confirmation
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    // Terms agreement
    if (!formData.agreeToTerms) {
      newErrors.agreeToTerms = 'You must agree to the terms';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      try {
        const response = await apiService.post('/api/users', formData);
        console.log('User created:', response);
        // Handle success (redirect, show message, etc.)
      } catch (error) {
        console.error('Error creating user:', error);
        // Handle error
      }
    }
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  return (
    <Form onSubmit={handleSubmit}>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        <Input
          label="First Name"
          value={formData.firstName}
          onChange={(e) => handleChange('firstName', e.target.value)}
          error={errors.firstName}
          required
        />
        
        <Input
          label="Last Name"
          value={formData.lastName}
          onChange={(e) => handleChange('lastName', e.target.value)}
          error={errors.lastName}
          required
        />
      </div>

      <Input
        label="Email"
        type="email"
        value={formData.email}
        onChange={(e) => handleChange('email', e.target.value)}
        error={errors.email}
        required
      />

      <Input
        label="Password"
        type="password"
        value={formData.password}
        onChange={(e) => handleChange('password', e.target.value)}
        error={errors.password}
        required
      />

      <Input
        label="Confirm Password"
        type="password"
        value={formData.confirmPassword}
        onChange={(e) => handleChange('confirmPassword', e.target.value)}
        error={errors.confirmPassword}
        required
      />

      <Select
        label="Role"
        value={formData.role}
        onChange={(e) => handleChange('role', e.target.value)}
        options={[
          { value: 'user', label: 'User' },
          { value: 'admin', label: 'Administrator' },
          { value: 'moderator', label: 'Moderator' }
        ]}
        error={errors.role}
        required
      />

      <div>
        <label>
          <input
            type="checkbox"
            checked={formData.agreeToTerms}
            onChange={(e) => handleChange('agreeToTerms', e.target.checked)}
          />
          I agree to the terms and conditions
        </label>
        {errors.agreeToTerms && <div style={{ color: 'red' }}>{errors.agreeToTerms}</div>}
      </div>

      <Button type="submit" fullWidth>
        Register
      </Button>
    </Form>
  );
}
```

## Data Visualization Examples

### Chart Integration

```jsx
import React, { useState, useEffect } from 'react';
import { Chart, Card } from './components';
import { formatCurrency } from './utils/currency';

function Dashboard() {
  const [salesData, setSalesData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSalesData();
  }, []);

  const loadSalesData = async () => {
    try {
      const response = await apiService.get('/api/sales/analytics');
      setSalesData(response);
    } catch (error) {
      console.error('Error loading sales data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;

  const chartData = {
    labels: salesData.months,
    datasets: [
      {
        label: 'Sales',
        data: salesData.sales,
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 2
      },
      {
        label: 'Revenue',
        data: salesData.revenue,
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 2
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: (value) => formatCurrency(value)
        }
      }
    },
    plugins: {
      tooltip: {
        callbacks: {
          label: (context) => {
            const label = context.dataset.label || '';
            const value = context.parsed.y;
            return `${label}: ${formatCurrency(value)}`;
          }
        }
      }
    }
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
      <Card title="Sales Overview">
        <Chart
          type="line"
          data={chartData}
          options={chartOptions}
          height={300}
        />
      </Card>

      <Card title="Revenue Distribution">
        <Chart
          type="doughnut"
          data={{
            labels: ['Online', 'In-Store', 'Mobile'],
            datasets: [{
              data: [60, 25, 15],
              backgroundColor: [
                'rgba(75, 192, 192, 0.8)',
                'rgba(255, 99, 132, 0.8)',
                'rgba(255, 205, 86, 0.8)'
              ]
            }]
          }}
          height={300}
        />
      </Card>
    </div>
  );
}
```

## Error Handling Examples

### Comprehensive Error Handling

```javascript
// Error handling utility
class ErrorHandler {
  static handle(error, context = '') {
    console.error(`Error in ${context}:`, error);

    if (error.response) {
      // API error response
      const { status, data } = error.response;
      
      switch (status) {
        case 400:
          return { type: 'validation', message: data.message || 'Invalid request' };
        case 401:
          return { type: 'auth', message: 'Please log in to continue' };
        case 403:
          return { type: 'permission', message: 'You do not have permission to perform this action' };
        case 404:
          return { type: 'notFound', message: 'Resource not found' };
        case 429:
          return { type: 'rateLimit', message: 'Too many requests. Please try again later.' };
        case 500:
          return { type: 'server', message: 'Server error. Please try again later.' };
        default:
          return { type: 'unknown', message: 'An unexpected error occurred' };
      }
    } else if (error.request) {
      // Network error
      return { type: 'network', message: 'Network error. Please check your connection.' };
    } else {
      // Other error
      return { type: 'unknown', message: error.message || 'An unexpected error occurred' };
    }
  }

  static async withRetry(fn, maxAttempts = 3) {
    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      try {
        return await fn();
      } catch (error) {
        if (attempt === maxAttempts) {
          throw error;
        }
        
        // Wait before retrying (exponential backoff)
        await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
      }
    }
  }
}

// Usage in components
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadUser();
  }, [userId]);

  const loadUser = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const userData = await ErrorHandler.withRetry(() => 
        apiService.get(`/api/users/${userId}`)
      );
      
      setUser(userData);
    } catch (error) {
      const errorInfo = ErrorHandler.handle(error, 'UserProfile.loadUser');
      setError(errorInfo);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!user) return <div>User not found</div>;

  return (
    <Card>
      <h2>{user.name}</h2>
      <p>Email: {user.email}</p>
      <p>Role: {user.role}</p>
    </Card>
  );
}
```

## Performance Optimization Examples

### Memoization and Caching

```javascript
import { memoize, debounce } from './utils/performance';

// Memoized expensive calculation
const calculateUserStats = memoize(async (userId) => {
  const user = await apiService.get(`/api/users/${userId}`);
  const orders = await apiService.get(`/api/users/${userId}/orders`);
  const reviews = await apiService.get(`/api/users/${userId}/reviews`);
  
  return {
    totalOrders: orders.length,
    totalSpent: orders.reduce((sum, order) => sum + order.total, 0),
    averageRating: reviews.reduce((sum, review) => sum + review.rating, 0) / reviews.length
  };
});

// Debounced search
const debouncedSearch = debounce(async (searchTerm) => {
  if (searchTerm.length < 2) return [];
  
  const results = await apiService.get('/api/search', {
    params: { q: searchTerm }
  });
  
  return results;
}, 300);

// Usage in component
function SearchComponent() {
  const [searchTerm, setSearchTerm] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (term) => {
    setLoading(true);
    try {
      const searchResults = await debouncedSearch(term);
      setResults(searchResults);
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Input
        placeholder="Search..."
        value={searchTerm}
        onChange={(e) => {
          setSearchTerm(e.target.value);
          handleSearch(e.target.value);
        }}
      />
      
      {loading && <div>Searching...</div>}
      
      <div>
        {results.map(result => (
          <div key={result.id}>{result.name}</div>
        ))}
      </div>
    </div>
  );
}
```

## Testing Examples

### Component Testing

```javascript
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { UserForm } from './UserForm';
import { apiService } from './services/api';

// Mock the API service
jest.mock('./services/api');

describe('UserForm', () => {
  beforeEach(() => {
    apiService.post.mockClear();
  });

  it('renders form fields', () => {
    render(<UserForm />);
    
    expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /submit/i })).toBeInTheDocument();
  });

  it('submits form with valid data', async () => {
    apiService.post.mockResolvedValue({ id: 1, name: 'John Doe' });
    
    render(<UserForm />);
    
    fireEvent.change(screen.getByLabelText(/name/i), {
      target: { value: 'John Doe' }
    });
    
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'john@example.com' }
    });
    
    fireEvent.click(screen.getByRole('button', { name: /submit/i }));
    
    await waitFor(() => {
      expect(apiService.post).toHaveBeenCalledWith('/api/users', {
        name: 'John Doe',
        email: 'john@example.com'
      });
    });
  });

  it('shows validation errors for invalid data', async () => {
    render(<UserForm />);
    
    fireEvent.click(screen.getByRole('button', { name: /submit/i }));
    
    await waitFor(() => {
      expect(screen.getByText(/name is required/i)).toBeInTheDocument();
      expect(screen.getByText(/email is required/i)).toBeInTheDocument();
    });
  });
});
```

### API Testing

```javascript
import { apiService } from './services/api';

describe('API Service', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  it('makes GET request successfully', async () => {
    const mockResponse = { users: [{ id: 1, name: 'John' }] };
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse
    });

    const result = await apiService.get('/api/users');
    
    expect(fetch).toHaveBeenCalledWith('/api/users', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-token'
      }
    });
    expect(result).toEqual(mockResponse);
  });

  it('handles API errors correctly', async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      status: 404,
      json: async () => ({ message: 'Not found' })
    });

    await expect(apiService.get('/api/users/999')).rejects.toThrow('Not found');
  });
});
```

## Best Practices Summary

1. **Error Handling**: Always wrap API calls in try-catch blocks
2. **Loading States**: Show loading indicators for async operations
3. **Validation**: Validate data on both client and server side
4. **Performance**: Use memoization and debouncing for expensive operations
5. **Testing**: Write comprehensive tests for components and functions
6. **Accessibility**: Include proper ARIA labels and keyboard navigation
7. **Responsive Design**: Ensure components work on all screen sizes
8. **Security**: Never expose sensitive data in client-side code
9. **Documentation**: Keep documentation up to date with code changes
10. **Code Organization**: Use consistent patterns and folder structure