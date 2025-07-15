# Function Reference

## Overview

This document provides comprehensive documentation for all public functions in the project. Each function includes detailed parameter information, return values, examples, and error handling.

## Table of Contents

1. [Utility Functions](#utility-functions)
2. [Data Processing Functions](#data-processing-functions)
3. [Validation Functions](#validation-functions)
4. [API Helper Functions](#api-helper-functions)
5. [Date/Time Functions](#datetime-functions)
6. [String Manipulation Functions](#string-manipulation-functions)
7. [Array/Object Functions](#arrayobject-functions)
8. [Math Functions](#math-functions)
9. [File System Functions](#file-system-functions)
10. [Testing Utilities](#testing-utilities)

---

## Utility Functions

### `deepClone(obj)`

**Description**: Creates a deep copy of an object or array, handling nested objects and arrays.

**Parameters**:
- `obj` (any): The object or array to clone

**Returns**: `any` - A deep copy of the input object

**Example**:
```javascript
const original = { user: { name: 'John', settings: { theme: 'dark' } } };
const cloned = deepClone(original);
cloned.user.name = 'Jane';
console.log(original.user.name); // 'John' (unchanged)
console.log(cloned.user.name);   // 'Jane'
```

**Throws**:
- `Error`: When object contains circular references

**Since**: v1.0.0

### `debounce(func, delay)`

**Description**: Creates a debounced version of a function that delays execution until after a specified delay.

**Parameters**:
- `func` (Function): The function to debounce
- `delay` (number): The delay in milliseconds

**Returns**: `Function` - The debounced function

**Example**:
```javascript
const debouncedSearch = debounce((query) => {
  console.log('Searching for:', query);
}, 300);

// Will only execute once after 300ms of no calls
debouncedSearch('hello');
debouncedSearch('hello world');
```

**Since**: v1.0.0

### `throttle(func, interval)`

**Description**: Creates a throttled version of a function that executes at most once per interval.

**Parameters**:
- `func` (Function): The function to throttle
- `interval` (number): The interval in milliseconds

**Returns**: `Function` - The throttled function

**Example**:
```javascript
const throttledResize = throttle(() => {
  console.log('Window resized');
}, 100);

window.addEventListener('resize', throttledResize);
```

**Since**: v1.0.0

---

## Data Processing Functions

### `transformData(data, schema)`

**Description**: Transforms data according to a provided schema, mapping fields and applying transformations.

**Parameters**:
- `data` (Object): The data to transform
- `schema` (Object): The transformation schema

**Returns**: `Object` - The transformed data

**Example**:
```javascript
const data = { firstName: 'John', lastName: 'Doe', age: 30 };
const schema = {
  name: (data) => `${data.firstName} ${data.lastName}`,
  age: 'age',
  isAdult: (data) => data.age >= 18
};

const result = transformData(data, schema);
// Result: { name: 'John Doe', age: 30, isAdult: true }
```

**Throws**:
- `TypeError`: When schema is not an object
- `Error`: When required fields are missing

**Since**: v1.0.0

### `filterData(data, filters)`

**Description**: Filters an array of objects based on provided filter criteria.

**Parameters**:
- `data` (Array): Array of objects to filter
- `filters` (Object): Filter criteria

**Returns**: `Array` - Filtered array

**Example**:
```javascript
const users = [
  { name: 'John', age: 25, role: 'admin' },
  { name: 'Jane', age: 30, role: 'user' },
  { name: 'Bob', age: 35, role: 'admin' }
];

const filtered = filterData(users, {
  role: 'admin',
  age: { min: 30 }
});
// Result: [{ name: 'Bob', age: 35, role: 'admin' }]
```

**Since**: v1.0.0

### `sortData(data, sortBy, direction)`

**Description**: Sorts an array of objects by a specified field in ascending or descending order.

**Parameters**:
- `data` (Array): Array of objects to sort
- `sortBy` (string): Field name to sort by
- `direction` (string, optional): Sort direction ('asc' or 'desc'). Default: 'asc'

**Returns**: `Array` - Sorted array

**Example**:
```javascript
const users = [
  { name: 'John', age: 25 },
  { name: 'Jane', age: 30 },
  { name: 'Bob', age: 20 }
];

const sorted = sortData(users, 'age', 'desc');
// Result: [{ name: 'Jane', age: 30 }, { name: 'John', age: 25 }, { name: 'Bob', age: 20 }]
```

**Since**: v1.0.0

---

## Validation Functions

### `validateEmail(email)`

**Description**: Validates if a string is a valid email address.

**Parameters**:
- `email` (string): The email address to validate

**Returns**: `boolean` - True if valid, false otherwise

**Example**:
```javascript
validateEmail('user@example.com');     // true
validateEmail('invalid-email');        // false
validateEmail('user@domain.co.uk');    // true
```

**Since**: v1.0.0

### `validatePassword(password, options)`

**Description**: Validates password strength based on configurable criteria.

**Parameters**:
- `password` (string): The password to validate
- `options` (Object, optional): Validation options

**Options**:
- `minLength` (number): Minimum password length. Default: 8
- `requireUppercase` (boolean): Require uppercase letters. Default: true
- `requireLowercase` (boolean): Require lowercase letters. Default: true
- `requireNumbers` (boolean): Require numbers. Default: true
- `requireSymbols` (boolean): Require symbols. Default: false

**Returns**: `Object` - Validation result with `isValid` boolean and `errors` array

**Example**:
```javascript
const result = validatePassword('MyPass123!', {
  minLength: 10,
  requireSymbols: true
});

// Result: { isValid: true, errors: [] }
```

**Since**: v1.0.0

### `validateRequired(value, fieldName)`

**Description**: Validates that a field has a non-empty value.

**Parameters**:
- `value` (any): The value to validate
- `fieldName` (string): Name of the field for error messages

**Returns**: `Object` - Validation result

**Example**:
```javascript
validateRequired('John', 'name');     // { isValid: true, error: null }
validateRequired('', 'name');         // { isValid: false, error: 'name is required' }
validateRequired(null, 'email');      // { isValid: false, error: 'email is required' }
```

**Since**: v1.0.0

---

## API Helper Functions

### `makeRequest(url, options)`

**Description**: Makes HTTP requests with built-in error handling and retry logic.

**Parameters**:
- `url` (string): The URL to request
- `options` (Object, optional): Request options

**Options**:
- `method` (string): HTTP method. Default: 'GET'
- `body` (any): Request body
- `headers` (Object): Request headers
- `timeout` (number): Request timeout in ms. Default: 5000
- `retries` (number): Number of retry attempts. Default: 3

**Returns**: `Promise<Object>` - Response data

**Example**:
```javascript
// GET request
const users = await makeRequest('/api/users');

// POST request
const newUser = await makeRequest('/api/users', {
  method: 'POST',
  body: { name: 'John', email: 'john@example.com' },
  headers: { 'Content-Type': 'application/json' }
});
```

**Throws**:
- `NetworkError`: When network request fails
- `TimeoutError`: When request times out
- `ValidationError`: When request validation fails

**Since**: v1.0.0

### `buildQuery(params)`

**Description**: Builds a URL query string from an object of parameters.

**Parameters**:
- `params` (Object): Query parameters

**Returns**: `string` - URL query string

**Example**:
```javascript
const query = buildQuery({
  page: 1,
  limit: 10,
  search: 'john doe',
  filters: ['active', 'verified']
});
// Result: '?page=1&limit=10&search=john%20doe&filters=active&filters=verified'
```

**Since**: v1.0.0

### `parseResponse(response)`

**Description**: Parses API response and handles common response formats.

**Parameters**:
- `response` (Object): Raw API response

**Returns**: `Object` - Parsed response data

**Example**:
```javascript
const response = {
  success: true,
  data: { users: [...] },
  pagination: { total: 100, page: 1 }
};

const parsed = parseResponse(response);
// Result: { users: [...], pagination: { total: 100, page: 1 } }
```

**Since**: v1.0.0

---

## Date/Time Functions

### `formatDate(date, format)`

**Description**: Formats a date according to a specified format string.

**Parameters**:
- `date` (Date|string|number): The date to format
- `format` (string): Format string (e.g., 'YYYY-MM-DD', 'DD/MM/YYYY HH:mm')

**Returns**: `string` - Formatted date string

**Example**:
```javascript
const date = new Date('2024-07-15T10:30:00');
formatDate(date, 'YYYY-MM-DD');           // '2024-07-15'
formatDate(date, 'DD/MM/YYYY HH:mm');     // '15/07/2024 10:30'
formatDate(date, 'MMM DD, YYYY');         // 'Jul 15, 2024'
```

**Since**: v1.0.0

### `parseDate(dateString, format)`

**Description**: Parses a date string according to a specified format.

**Parameters**:
- `dateString` (string): The date string to parse
- `format` (string, optional): Expected format. Default: auto-detect

**Returns**: `Date` - Parsed date object

**Example**:
```javascript
parseDate('2024-07-15');                  // Date object
parseDate('15/07/2024', 'DD/MM/YYYY');    // Date object
parseDate('Jul 15, 2024');                // Date object
```

**Throws**:
- `Error`: When date string is invalid

**Since**: v1.0.0

### `getRelativeTime(date)`

**Description**: Gets relative time string (e.g., '2 hours ago', 'in 3 days').

**Parameters**:
- `date` (Date|string|number): The date to compare

**Returns**: `string` - Relative time string

**Example**:
```javascript
const now = new Date();
const past = new Date(now.getTime() - 2 * 60 * 60 * 1000); // 2 hours ago
const future = new Date(now.getTime() + 3 * 24 * 60 * 60 * 1000); // 3 days from now

getRelativeTime(past);     // '2 hours ago'
getRelativeTime(future);   // 'in 3 days'
```

**Since**: v1.0.0

---

## String Manipulation Functions

### `slugify(text)`

**Description**: Converts text to a URL-friendly slug.

**Parameters**:
- `text` (string): The text to slugify

**Returns**: `string` - URL-friendly slug

**Example**:
```javascript
slugify('Hello World! This is a Test');   // 'hello-world-this-is-a-test'
slugify('Special Ch@r@cters & Symbols');  // 'special-chracters-symbols'
```

**Since**: v1.0.0

### `truncate(text, length, suffix)`

**Description**: Truncates text to a specified length with optional suffix.

**Parameters**:
- `text` (string): The text to truncate
- `length` (number): Maximum length
- `suffix` (string, optional): Suffix to add when truncated. Default: '...'

**Returns**: `string` - Truncated text

**Example**:
```javascript
truncate('This is a long text', 10);           // 'This is a...'
truncate('This is a long text', 10, '…');      // 'This is a…'
truncate('Short text', 20);                    // 'Short text'
```

**Since**: v1.0.0

### `capitalize(text)`

**Description**: Capitalizes the first letter of each word in a string.

**Parameters**:
- `text` (string): The text to capitalize

**Returns**: `string` - Capitalized text

**Example**:
```javascript
capitalize('hello world');           // 'Hello World'
capitalize('javaScript is awesome'); // 'JavaScript Is Awesome'
```

**Since**: v1.0.0

---

## Array/Object Functions

### `groupBy(array, key)`

**Description**: Groups array elements by a specified key.

**Parameters**:
- `array` (Array): The array to group
- `key` (string|Function): The key to group by or a function that returns the key

**Returns**: `Object` - Grouped object

**Example**:
```javascript
const users = [
  { name: 'John', role: 'admin' },
  { name: 'Jane', role: 'user' },
  { name: 'Bob', role: 'admin' }
];

const grouped = groupBy(users, 'role');
// Result: { admin: [{ name: 'John', role: 'admin' }, { name: 'Bob', role: 'admin' }], user: [{ name: 'Jane', role: 'user' }] }
```

**Since**: v1.0.0

### `unique(array, key)`

**Description**: Returns unique elements from an array, optionally by a specific key.

**Parameters**:
- `array` (Array): The array to process
- `key` (string, optional): The key to use for uniqueness comparison

**Returns**: `Array` - Array with unique elements

**Example**:
```javascript
unique([1, 2, 2, 3, 3, 4]);              // [1, 2, 3, 4]
unique([{id: 1}, {id: 2}, {id: 1}], 'id'); // [{id: 1}, {id: 2}]
```

**Since**: v1.0.0

### `flatten(array, depth)`

**Description**: Flattens a nested array to a specified depth.

**Parameters**:
- `array` (Array): The array to flatten
- `depth` (number, optional): Depth to flatten. Default: 1

**Returns**: `Array` - Flattened array

**Example**:
```javascript
flatten([1, [2, 3], [4, [5, 6]]]);        // [1, 2, 3, 4, [5, 6]]
flatten([1, [2, 3], [4, [5, 6]]], 2);     // [1, 2, 3, 4, 5, 6]
```

**Since**: v1.0.0

---

## Math Functions

### `randomBetween(min, max)`

**Description**: Generates a random number between min and max (inclusive).

**Parameters**:
- `min` (number): Minimum value
- `max` (number): Maximum value

**Returns**: `number` - Random number between min and max

**Example**:
```javascript
randomBetween(1, 10);    // Random number between 1 and 10
randomBetween(0, 1);     // Random number between 0 and 1
```

**Since**: v1.0.0

### `round(number, decimals)`

**Description**: Rounds a number to a specified number of decimal places.

**Parameters**:
- `number` (number): The number to round
- `decimals` (number): Number of decimal places

**Returns**: `number` - Rounded number

**Example**:
```javascript
round(3.14159, 2);       // 3.14
round(123.456, 0);       // 123
round(1.005, 2);         // 1.01
```

**Since**: v1.0.0

### `clamp(value, min, max)`

**Description**: Clamps a value between a minimum and maximum value.

**Parameters**:
- `value` (number): The value to clamp
- `min` (number): Minimum value
- `max` (number): Maximum value

**Returns**: `number` - Clamped value

**Example**:
```javascript
clamp(5, 0, 10);         // 5
clamp(-5, 0, 10);        // 0
clamp(15, 0, 10);        // 10
```

**Since**: v1.0.0

---

## File System Functions

### `readFile(path, encoding)`

**Description**: Reads a file asynchronously with specified encoding.

**Parameters**:
- `path` (string): Path to the file
- `encoding` (string, optional): File encoding. Default: 'utf8'

**Returns**: `Promise<string>` - File contents

**Example**:
```javascript
const content = await readFile('./config.json');
const binaryData = await readFile('./image.png', 'binary');
```

**Throws**:
- `Error`: When file doesn't exist or can't be read

**Since**: v1.0.0

### `writeFile(path, data, encoding)`

**Description**: Writes data to a file asynchronously.

**Parameters**:
- `path` (string): Path to the file
- `data` (string|Buffer): Data to write
- `encoding` (string, optional): File encoding. Default: 'utf8'

**Returns**: `Promise<void>` - Resolves when file is written

**Example**:
```javascript
await writeFile('./output.txt', 'Hello World');
await writeFile('./data.json', JSON.stringify({key: 'value'}));
```

**Throws**:
- `Error`: When file can't be written

**Since**: v1.0.0

### `pathExists(path)`

**Description**: Checks if a file or directory exists.

**Parameters**:
- `path` (string): Path to check

**Returns**: `Promise<boolean>` - True if path exists

**Example**:
```javascript
const exists = await pathExists('./config.json');
if (exists) {
  console.log('Config file found');
}
```

**Since**: v1.0.0

---

## Testing Utilities

### `createMockFunction(returnValue)`

**Description**: Creates a mock function for testing purposes.

**Parameters**:
- `returnValue` (any, optional): Value to return when called

**Returns**: `Function` - Mock function with call tracking

**Example**:
```javascript
const mockFn = createMockFunction('test result');
mockFn(); // Returns 'test result'
console.log(mockFn.callCount); // 1
console.log(mockFn.calls); // [{ args: [], result: 'test result' }]
```

**Since**: v1.0.0

### `waitFor(condition, timeout)`

**Description**: Waits for a condition to become true within a timeout period.

**Parameters**:
- `condition` (Function): Function that returns a boolean
- `timeout` (number, optional): Timeout in milliseconds. Default: 5000

**Returns**: `Promise<void>` - Resolves when condition is true

**Example**:
```javascript
await waitFor(() => document.getElementById('loading') === null, 3000);
```

**Throws**:
- `TimeoutError`: When condition doesn't become true within timeout

**Since**: v1.0.0

---

## Error Handling

All functions follow consistent error handling patterns:

### Common Error Types

- **`TypeError`**: Invalid parameter types
- **`Error`**: General errors with descriptive messages
- **`ValidationError`**: Input validation failures
- **`NetworkError`**: Network-related errors
- **`TimeoutError`**: Operation timeout errors

### Error Object Structure

```javascript
{
  name: 'ErrorType',
  message: 'Descriptive error message',
  code: 'ERROR_CODE',
  stack: '...', // Stack trace
  // Additional context-specific properties
}
```

---

## Contributing

When adding new functions:

1. Follow the documentation template above
2. Include comprehensive examples
3. Document all parameters and return values
4. Add error handling information
5. Include version information
6. Add unit tests

---

*This function reference is continuously updated. For the latest version, please check the repository.*