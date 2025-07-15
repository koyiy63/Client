# Functions Documentation

## Overview

This document provides comprehensive documentation for all utility functions, service functions, and helper functions in the project.

## Table of Contents

- [Utility Functions](#utility-functions)
- [Service Functions](#service-functions)
- [Helper Functions](#helper-functions)
- [Data Processing Functions](#data-processing-functions)
- [Validation Functions](#validation-functions)
- [Date and Time Functions](#date-and-time-functions)
- [String Manipulation Functions](#string-manipulation-functions)
- [Array and Object Functions](#array-and-object-functions)

## Utility Functions

### `formatCurrency(amount, currency = 'USD', locale = 'en-US')`

**Description:** Formats a number as currency with proper locale formatting.

**Parameters:**
- `amount` (number) - The amount to format
- `currency` (string, optional) - Currency code (default: 'USD')
- `locale` (string, optional) - Locale for formatting (default: 'en-US')

**Returns:**
- `string` - Formatted currency string

**Example:**
```javascript
import { formatCurrency } from './utils/currency';

console.log(formatCurrency(1234.56)); // "$1,234.56"
console.log(formatCurrency(1234.56, 'EUR', 'de-DE')); // "1.234,56 €"
console.log(formatCurrency(1234.56, 'JPY')); // "¥1,235"
```

### `debounce(func, delay)`

**Description:** Creates a debounced function that delays invoking the provided function until after the specified delay has elapsed.

**Parameters:**
- `func` (function) - The function to debounce
- `delay` (number) - The delay in milliseconds

**Returns:**
- `function` - Debounced function

**Example:**
```javascript
import { debounce } from './utils/debounce';

const handleSearch = debounce((searchTerm) => {
  console.log('Searching for:', searchTerm);
  // Perform search API call
}, 300);

// Usage in input change handler
input.addEventListener('input', (e) => {
  handleSearch(e.target.value);
});
```

### `throttle(func, limit)`

**Description:** Creates a throttled function that limits the rate at which the provided function can be called.

**Parameters:**
- `func` (function) - The function to throttle
- `limit` (number) - The time limit in milliseconds

**Returns:**
- `function` - Throttled function

**Example:**
```javascript
import { throttle } from './utils/throttle';

const handleScroll = throttle(() => {
  console.log('Scroll event handled');
  // Handle scroll logic
}, 100);

window.addEventListener('scroll', handleScroll);
```

### `generateId(length = 8)`

**Description:** Generates a random alphanumeric ID of specified length.

**Parameters:**
- `length` (number, optional) - Length of the ID (default: 8)

**Returns:**
- `string` - Random alphanumeric ID

**Example:**
```javascript
import { generateId } from './utils/id';

console.log(generateId()); // "aB3x9K2m"
console.log(generateId(12)); // "x7K9mN2pQ4rT"
```

## Service Functions

### `apiService.get(endpoint, options = {})`

**Description:** Makes a GET request to the specified endpoint.

**Parameters:**
- `endpoint` (string) - API endpoint URL
- `options` (object, optional) - Request options
  - `headers` (object, optional) - Additional headers
  - `params` (object, optional) - Query parameters
  - `timeout` (number, optional) - Request timeout in milliseconds

**Returns:**
- `Promise<Object>` - Response data

**Example:**
```javascript
import { apiService } from './services/api';

// Basic GET request
const users = await apiService.get('/api/users');

// GET request with query parameters
const filteredUsers = await apiService.get('/api/users', {
  params: { role: 'admin', page: 1, limit: 10 }
});

// GET request with custom headers
const userProfile = await apiService.get('/api/users/profile', {
  headers: { 'X-Custom-Header': 'value' }
});
```

### `apiService.post(endpoint, data, options = {})`

**Description:** Makes a POST request to the specified endpoint.

**Parameters:**
- `endpoint` (string) - API endpoint URL
- `data` (object) - Data to send in request body
- `options` (object, optional) - Request options
  - `headers` (object, optional) - Additional headers
  - `timeout` (number, optional) - Request timeout in milliseconds

**Returns:**
- `Promise<Object>` - Response data

**Example:**
```javascript
import { apiService } from './services/api';

// Create a new user
const newUser = await apiService.post('/api/users', {
  name: 'John Doe',
  email: 'john@example.com',
  password: 'securepassword123'
});

// Upload file
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const uploadResult = await apiService.post('/api/upload', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
});
```

### `apiService.put(endpoint, data, options = {})`

**Description:** Makes a PUT request to the specified endpoint.

**Parameters:**
- `endpoint` (string) - API endpoint URL
- `data` (object) - Data to send in request body
- `options` (object, optional) - Request options

**Returns:**
- `Promise<Object>` - Response data

**Example:**
```javascript
import { apiService } from './services/api';

// Update user
const updatedUser = await apiService.put('/api/users/123', {
  name: 'John Doe Updated',
  email: 'john.updated@example.com'
});
```

### `apiService.delete(endpoint, options = {})`

**Description:** Makes a DELETE request to the specified endpoint.

**Parameters:**
- `endpoint` (string) - API endpoint URL
- `options` (object, optional) - Request options

**Returns:**
- `Promise<Object>` - Response data

**Example:**
```javascript
import { apiService } from './services/api';

// Delete user
await apiService.delete('/api/users/123');
```

## Helper Functions

### `isEmpty(value)`

**Description:** Checks if a value is empty (null, undefined, empty string, empty array, or empty object).

**Parameters:**
- `value` (any) - Value to check

**Returns:**
- `boolean` - True if value is empty, false otherwise

**Example:**
```javascript
import { isEmpty } from './utils/helpers';

console.log(isEmpty('')); // true
console.log(isEmpty([])); // true
console.log(isEmpty({})); // true
console.log(isEmpty(null)); // true
console.log(isEmpty(undefined)); // true
console.log(isEmpty('hello')); // false
console.log(isEmpty([1, 2, 3])); // false
console.log(isEmpty({ key: 'value' })); // false
```

### `deepClone(obj)`

**Description:** Creates a deep clone of an object or array.

**Parameters:**
- `obj` (object|array) - Object or array to clone

**Returns:**
- `object|array` - Deep cloned object or array

**Example:**
```javascript
import { deepClone } from './utils/helpers';

const original = {
  name: 'John',
  address: {
    street: '123 Main St',
    city: 'New York'
  },
  hobbies: ['reading', 'gaming']
};

const cloned = deepClone(original);
cloned.address.city = 'Los Angeles';
cloned.hobbies.push('cooking');

console.log(original.address.city); // "New York"
console.log(original.hobbies); // ["reading", "gaming"]
console.log(cloned.address.city); // "Los Angeles"
console.log(cloned.hobbies); // ["reading", "gaming", "cooking"]
```

### `getNestedValue(obj, path, defaultValue = undefined)`

**Description:** Safely retrieves a nested value from an object using a dot-separated path.

**Parameters:**
- `obj` (object) - Object to search in
- `path` (string) - Dot-separated path to the value
- `defaultValue` (any, optional) - Default value if path doesn't exist

**Returns:**
- `any` - Value at the specified path or default value

**Example:**
```javascript
import { getNestedValue } from './utils/helpers';

const user = {
  profile: {
    personal: {
      name: 'John Doe',
      age: 30
    }
  }
};

console.log(getNestedValue(user, 'profile.personal.name')); // "John Doe"
console.log(getNestedValue(user, 'profile.personal.email', 'No email')); // "No email"
console.log(getNestedValue(user, 'nonexistent.path', 'Default')); // "Default"
```

## Data Processing Functions

### `groupBy(array, key)`

**Description:** Groups array elements by a specified key.

**Parameters:**
- `array` (array) - Array to group
- `key` (string|function) - Key to group by or function that returns the key

**Returns:**
- `object` - Object with grouped arrays

**Example:**
```javascript
import { groupBy } from './utils/data';

const users = [
  { id: 1, name: 'John', role: 'admin' },
  { id: 2, name: 'Jane', role: 'user' },
  { id: 3, name: 'Bob', role: 'admin' },
  { id: 4, name: 'Alice', role: 'user' }
];

const groupedByRole = groupBy(users, 'role');
console.log(groupedByRole);
// {
//   admin: [
//     { id: 1, name: 'John', role: 'admin' },
//     { id: 3, name: 'Bob', role: 'admin' }
//   ],
//   user: [
//     { id: 2, name: 'Jane', role: 'user' },
//     { id: 4, name: 'Alice', role: 'user' }
//   ]
// }

// Group by function
const groupedByLength = groupBy(users, user => user.name.length);
console.log(groupedByLength);
// {
//   4: [{ id: 1, name: 'John', role: 'admin' }, { id: 3, name: 'Bob', role: 'admin' }],
//   4: [{ id: 2, name: 'Jane', role: 'user' }],
//   5: [{ id: 4, name: 'Alice', role: 'user' }]
// }
```

### `sortBy(array, key, order = 'asc')`

**Description:** Sorts an array by a specified key.

**Parameters:**
- `array` (array) - Array to sort
- `key` (string|function) - Key to sort by or function that returns the sort value
- `order` (string, optional) - Sort order ('asc' or 'desc', default: 'asc')

**Returns:**
- `array` - Sorted array

**Example:**
```javascript
import { sortBy } from './utils/data';

const products = [
  { id: 1, name: 'Laptop', price: 999 },
  { id: 2, name: 'Mouse', price: 25 },
  { id: 3, name: 'Keyboard', price: 75 }
];

// Sort by price ascending
const sortedByPrice = sortBy(products, 'price');
console.log(sortedByPrice);
// [
//   { id: 2, name: 'Mouse', price: 25 },
//   { id: 3, name: 'Keyboard', price: 75 },
//   { id: 1, name: 'Laptop', price: 999 }
// ]

// Sort by price descending
const sortedByPriceDesc = sortBy(products, 'price', 'desc');
console.log(sortedByPriceDesc);
// [
//   { id: 1, name: 'Laptop', price: 999 },
//   { id: 3, name: 'Keyboard', price: 75 },
//   { id: 2, name: 'Mouse', price: 25 }
// ]

// Sort by function
const sortedByNameLength = sortBy(products, product => product.name.length);
console.log(sortedByNameLength);
// [
//   { id: 2, name: 'Mouse', price: 25 },
//   { id: 1, name: 'Laptop', price: 999 },
//   { id: 3, name: 'Keyboard', price: 75 }
// ]
```

### `filterBy(array, criteria)`

**Description:** Filters an array based on multiple criteria.

**Parameters:**
- `array` (array) - Array to filter
- `criteria` (object) - Filter criteria object

**Returns:**
- `array` - Filtered array

**Example:**
```javascript
import { filterBy } from './utils/data';

const users = [
  { id: 1, name: 'John', age: 25, role: 'admin', active: true },
  { id: 2, name: 'Jane', age: 30, role: 'user', active: true },
  { id: 3, name: 'Bob', age: 35, role: 'admin', active: false },
  { id: 4, name: 'Alice', age: 28, role: 'user', active: true }
];

// Filter by multiple criteria
const filteredUsers = filterBy(users, {
  role: 'admin',
  active: true,
  age: (age) => age > 25
});

console.log(filteredUsers);
// [{ id: 3, name: 'Bob', age: 35, role: 'admin', active: false }]
```

## Validation Functions

### `validateEmail(email)`

**Description:** Validates email format using regex.

**Parameters:**
- `email` (string) - Email address to validate

**Returns:**
- `boolean` - True if email is valid, false otherwise

**Example:**
```javascript
import { validateEmail } from './utils/validation';

console.log(validateEmail('user@example.com')); // true
console.log(validateEmail('invalid-email')); // false
console.log(validateEmail('user@')); // false
console.log(validateEmail('')); // false
```

### `validatePassword(password, options = {})`

**Description:** Validates password strength based on specified criteria.

**Parameters:**
- `password` (string) - Password to validate
- `options` (object, optional) - Validation options
  - `minLength` (number, optional) - Minimum length (default: 8)
  - `requireUppercase` (boolean, optional) - Require uppercase letter (default: true)
  - `requireLowercase` (boolean, optional) - Require lowercase letter (default: true)
  - `requireNumbers` (boolean, optional) - Require numbers (default: true)
  - `requireSpecialChars` (boolean, optional) - Require special characters (default: false)

**Returns:**
- `object` - Validation result with isValid boolean and errors array

**Example:**
```javascript
import { validatePassword } from './utils/validation';

const result1 = validatePassword('weak');
console.log(result1);
// { isValid: false, errors: ['Password must be at least 8 characters long', 'Password must contain at least one uppercase letter', 'Password must contain at least one number'] }

const result2 = validatePassword('StrongPass123');
console.log(result2);
// { isValid: true, errors: [] }

const result3 = validatePassword('password123', { requireSpecialChars: true });
console.log(result3);
// { isValid: false, errors: ['Password must contain at least one special character'] }
```

### `validatePhoneNumber(phone, country = 'US')`

**Description:** Validates phone number format for specified country.

**Parameters:**
- `phone` (string) - Phone number to validate
- `country` (string, optional) - Country code (default: 'US')

**Returns:**
- `boolean` - True if phone number is valid, false otherwise

**Example:**
```javascript
import { validatePhoneNumber } from './utils/validation';

console.log(validatePhoneNumber('(555) 123-4567')); // true
console.log(validatePhoneNumber('555-123-4567')); // true
console.log(validatePhoneNumber('5551234567')); // true
console.log(validatePhoneNumber('invalid')); // false
console.log(validatePhoneNumber('+44 20 7946 0958', 'UK')); // true
```

## Date and Time Functions

### `formatDate(date, format = 'YYYY-MM-DD')`

**Description:** Formats a date according to the specified format.

**Parameters:**
- `date` (Date|string) - Date to format
- `format` (string, optional) - Format string (default: 'YYYY-MM-DD')

**Returns:**
- `string` - Formatted date string

**Example:**
```javascript
import { formatDate } from './utils/date';

const date = new Date('2024-01-15T10:30:00Z');

console.log(formatDate(date)); // "2024-01-15"
console.log(formatDate(date, 'MM/DD/YYYY')); // "01/15/2024"
console.log(formatDate(date, 'MMMM DD, YYYY')); // "January 15, 2024"
console.log(formatDate(date, 'YYYY-MM-DD HH:mm:ss')); // "2024-01-15 10:30:00"
```

### `getRelativeTime(date)`

**Description:** Returns a human-readable relative time string.

**Parameters:**
- `date` (Date|string) - Date to get relative time for

**Returns:**
- `string` - Relative time string

**Example:**
```javascript
import { getRelativeTime } from './utils/date';

const now = new Date();
const oneHourAgo = new Date(now.getTime() - 60 * 60 * 1000);
const oneDayAgo = new Date(now.getTime() - 24 * 60 * 60 * 1000);

console.log(getRelativeTime(oneHourAgo)); // "1 hour ago"
console.log(getRelativeTime(oneDayAgo)); // "1 day ago"
console.log(getRelativeTime(now)); // "just now"
```

### `addDays(date, days)`

**Description:** Adds or subtracts days from a date.

**Parameters:**
- `date` (Date|string) - Base date
- `days` (number) - Number of days to add (negative for subtraction)

**Returns:**
- `Date` - New date object

**Example:**
```javascript
import { addDays } from './utils/date';

const today = new Date();
const tomorrow = addDays(today, 1);
const yesterday = addDays(today, -1);

console.log(formatDate(tomorrow)); // Tomorrow's date
console.log(formatDate(yesterday)); // Yesterday's date
```

## String Manipulation Functions

### `capitalize(str)`

**Description:** Capitalizes the first letter of a string.

**Parameters:**
- `str` (string) - String to capitalize

**Returns:**
- `string` - Capitalized string

**Example:**
```javascript
import { capitalize } from './utils/string';

console.log(capitalize('hello')); // "Hello"
console.log(capitalize('world')); // "World"
console.log(capitalize('')); // ""
```

### `camelCase(str)`

**Description:** Converts a string to camelCase.

**Parameters:**
- `str` (string) - String to convert

**Returns:**
- `string` - camelCase string

**Example:**
```javascript
import { camelCase } from './utils/string';

console.log(camelCase('hello world')); // "helloWorld"
console.log(camelCase('user-name')); // "userName"
console.log(camelCase('first_name')); // "firstName"
```

### `kebabCase(str)`

**Description:** Converts a string to kebab-case.

**Parameters:**
- `str` (string) - String to convert

**Returns:**
- `string` - kebab-case string

**Example:**
```javascript
import { kebabCase } from './utils/string';

console.log(kebabCase('hello world')); // "hello-world"
console.log(kebabCase('userName')); // "user-name"
console.log(kebabCase('first_name')); // "first-name"
```

### `truncate(str, length, suffix = '...')`

**Description:** Truncates a string to the specified length.

**Parameters:**
- `str` (string) - String to truncate
- `length` (number) - Maximum length
- `suffix` (string, optional) - Suffix to add (default: '...')

**Returns:**
- `string` - Truncated string

**Example:**
```javascript
import { truncate } from './utils/string';

console.log(truncate('This is a very long string', 10)); // "This is a..."
console.log(truncate('Short', 10)); // "Short"
console.log(truncate('Long string', 8, '***')); // "Long st***"
```

## Array and Object Functions

### `chunk(array, size)`

**Description:** Splits an array into chunks of specified size.

**Parameters:**
- `array` (array) - Array to chunk
- `size` (number) - Size of each chunk

**Returns:**
- `array` - Array of chunks

**Example:**
```javascript
import { chunk } from './utils/array';

const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

console.log(chunk(numbers, 3));
// [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]

console.log(chunk(numbers, 5));
// [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
```

### `flatten(array, depth = 1)`

**Description:** Flattens a nested array to the specified depth.

**Parameters:**
- `array` (array) - Array to flatten
- `depth` (number, optional) - Flattening depth (default: 1)

**Returns:**
- `array` - Flattened array

**Example:**
```javascript
import { flatten } from './utils/array';

const nested = [1, [2, 3], [4, [5, 6]]];

console.log(flatten(nested)); // [1, 2, 3, 4, [5, 6]]
console.log(flatten(nested, 2)); // [1, 2, 3, 4, 5, 6]
```

### `pick(obj, keys)`

**Description:** Creates an object composed of the picked object properties.

**Parameters:**
- `obj` (object) - Source object
- `keys` (array) - Properties to pick

**Returns:**
- `object` - New object with picked properties

**Example:**
```javascript
import { pick } from './utils/object';

const user = {
  id: 1,
  name: 'John Doe',
  email: 'john@example.com',
  password: 'secret',
  role: 'admin'
};

const publicUser = pick(user, ['id', 'name', 'email']);
console.log(publicUser);
// { id: 1, name: 'John Doe', email: 'john@example.com' }
```

### `omit(obj, keys)`

**Description:** Creates an object composed of properties that are not omitted.

**Parameters:**
- `obj` (object) - Source object
- `keys` (array) - Properties to omit

**Returns:**
- `object` - New object without omitted properties

**Example:**
```javascript
import { omit } from './utils/object';

const user = {
  id: 1,
  name: 'John Doe',
  email: 'john@example.com',
  password: 'secret',
  role: 'admin'
};

const safeUser = omit(user, ['password']);
console.log(safeUser);
// { id: 1, name: 'John Doe', email: 'john@example.com', role: 'admin' }
```

## Error Handling Functions

### `handleAsyncError(asyncFn)`

**Description:** Wraps an async function with error handling.

**Parameters:**
- `asyncFn` (function) - Async function to wrap

**Returns:**
- `function` - Wrapped function with error handling

**Example:**
```javascript
import { handleAsyncError } from './utils/error';

const safeApiCall = handleAsyncError(async (id) => {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) {
    throw new Error('User not found');
  }
  return response.json();
});

// Usage
const result = await safeApiCall(123);
if (result.error) {
  console.error('Error:', result.error);
} else {
  console.log('User:', result.data);
}
```

### `retry(fn, maxAttempts = 3, delay = 1000)`

**Description:** Retries a function with exponential backoff.

**Parameters:**
- `fn` (function) - Function to retry
- `maxAttempts` (number, optional) - Maximum retry attempts (default: 3)
- `delay` (number, optional) - Initial delay in milliseconds (default: 1000)

**Returns:**
- `Promise<any>` - Result of the function

**Example:**
```javascript
import { retry } from './utils/error';

const unreliableApiCall = async () => {
  const response = await fetch('/api/unreliable');
  if (!response.ok) {
    throw new Error('API call failed');
  }
  return response.json();
};

const reliableApiCall = retry(unreliableApiCall, 5, 2000);

// This will retry up to 5 times with exponential backoff
const result = await reliableApiCall();
```

## Performance Functions

### `memoize(fn, resolver)`

**Description:** Creates a memoized function that caches results.

**Parameters:**
- `fn` (function) - Function to memoize
- `resolver` (function, optional) - Function to resolve cache key

**Returns:**
- `function` - Memoized function

**Example:**
```javascript
import { memoize } from './utils/performance';

const expensiveCalculation = memoize((n) => {
  console.log('Calculating...');
  return n * n;
});

console.log(expensiveCalculation(5)); // "Calculating..." then 25
console.log(expensiveCalculation(5)); // 25 (cached)
console.log(expensiveCalculation(6)); // "Calculating..." then 36
```

### `throttle(func, limit)`

**Description:** Creates a throttled function that limits execution rate.

**Parameters:**
- `func` (function) - Function to throttle
- `limit` (number) - Time limit in milliseconds

**Returns:**
- `function` - Throttled function

**Example:**
```javascript
import { throttle } from './utils/performance';

const handleResize = throttle(() => {
  console.log('Window resized');
  // Handle resize logic
}, 100);

window.addEventListener('resize', handleResize);
```

## Testing Functions

### `createMockData(schema, count = 1)`

**Description:** Creates mock data based on a schema.

**Parameters:**
- `schema` (object) - Data schema
- `count` (number, optional) - Number of items to generate (default: 1)

**Returns:**
- `array|object` - Mock data

**Example:**
```javascript
import { createMockData } from './utils/testing';

const userSchema = {
  id: 'number',
  name: 'string',
  email: 'email',
  age: 'number:18-65',
  isActive: 'boolean'
};

const mockUsers = createMockData(userSchema, 5);
console.log(mockUsers);
// [
//   { id: 1, name: 'John Doe', email: 'john@example.com', age: 25, isActive: true },
//   { id: 2, name: 'Jane Smith', email: 'jane@example.com', age: 30, isActive: false },
//   // ... more users
// ]
```

### `wait(ms)`

**Description:** Creates a promise that resolves after specified milliseconds.

**Parameters:**
- `ms` (number) - Milliseconds to wait

**Returns:**
- `Promise<void>` - Promise that resolves after delay

**Example:**
```javascript
import { wait } from './utils/testing';

// In tests
test('async operation', async () => {
  const result = await someAsyncOperation();
  await wait(100); // Wait for 100ms
  expect(result).toBeDefined();
});
```