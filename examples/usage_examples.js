/**
 * Comprehensive Usage Examples for Jagarnath JavaScript/TypeScript APIs
 * 
 * This file demonstrates how to use all the JavaScript/TypeScript APIs including:
 * - DataValidator: Data validation, sanitization, and form validation
 * - UIHelpers: UI manipulation, notifications, modals, and animations
 * - React Components: Button, Modal, Form, Table components
 * - Vue Components: DataTable and other Vue components
 * 
 * @author: Jagarnath Team
 * @version: 1.0.0
 */

// Import our custom modules
import { DataValidator } from '../src/js/core/DataValidator.js';
import { UIHelpers } from '../src/js/core/UIHelpers.js';
import { Button } from '../src/js/components/react/Button.js';
import DataTable from '../src/components/vue/DataTable.vue';

// Initialize utilities
const validator = new DataValidator();
const uiHelpers = new UIHelpers();

/**
 * Data Validation Examples
 */
function dataValidationExamples() {
    console.log('=== Data Validation Examples ===\n');
    
    // Example 1: Email validation
    console.log('1. Email validation:');
    const emails = [
        'user@example.com',
        'invalid-email',
        'test.email@domain.co.uk',
        'user@.com'
    ];
    
    emails.forEach(email => {
        const isValid = validator.validateEmail(email);
        console.log(`  ${email}: ${isValid ? 'Valid' : 'Invalid'}`);
    });
    
    // Example 2: Phone number validation
    console.log('\n2. Phone number validation:');
    const phones = [
        '+1-555-123-4567',
        '555-123-4567',
        '1234567890',
        'invalid-phone'
    ];
    
    phones.forEach(phone => {
        const isValid = validator.validatePhone(phone);
        console.log(`  ${phone}: ${isValid ? 'Valid' : 'Invalid'}`);
    });
    
    // Example 3: URL validation
    console.log('\n3. URL validation:');
    const urls = [
        'https://example.com',
        'http://subdomain.example.co.uk/path?param=value',
        'ftp://invalid-url',
        'not-a-url'
    ];
    
    urls.forEach(url => {
        const isValid = validator.validateURL(url);
        console.log(`  ${url}: ${isValid ? 'Valid' : 'Invalid'}`);
    });
    
    // Example 4: Form validation
    console.log('\n4. Form validation:');
    const formData = {
        username: 'john_doe',
        email: 'john@example.com',
        password: 'password123',
        confirmPassword: 'password123',
        age: '25',
        website: 'https://example.com'
    };
    
    const validationRules = {
        username: {
            required: true,
            minLength: 3,
            maxLength: 20,
            pattern: /^[a-zA-Z0-9_]+$/
        },
        email: {
            required: true,
            type: 'email'
        },
        password: {
            required: true,
            minLength: 8,
            pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/
        },
        confirmPassword: {
            required: true,
            match: 'password'
        },
        age: {
            required: true,
            type: 'number',
            min: 18,
            max: 100
        },
        website: {
            required: false,
            type: 'url'
        }
    };
    
    const formValidation = validator.validateForm(formData, validationRules);
    console.log('Form validation results:');
    console.log(JSON.stringify(formValidation, null, 2));
    
    // Example 5: Data sanitization
    console.log('\n5. Data sanitization:');
    const dirtyData = {
        name: '<script>alert("xss")</script>John Doe',
        email: '  JOHN@EXAMPLE.COM  ',
        phone: '+1 (555) 123-4567',
        text: '   Multiple    spaces   and\ttabs\there   '
    };
    
    const sanitizedData = validator.sanitizeData(dirtyData);
    console.log('Sanitized data:');
    console.log(JSON.stringify(sanitizedData, null, 2));
}

/**
 * UI Helpers Examples
 */
function uiHelpersExamples() {
    console.log('\n=== UI Helpers Examples ===\n');
    
    // Example 1: Notifications
    console.log('1. Notifications:');
    
    // Show different types of notifications
    uiHelpers.showNotification('Success message', 'success');
    uiHelpers.showNotification('Error message', 'error');
    uiHelpers.showNotification('Warning message', 'warning');
    uiHelpers.showNotification('Info message', 'info');
    
    // Example 2: Modal operations
    console.log('\n2. Modal operations:');
    
    // Create and show a modal
    const modalId = 'example-modal';
    const modalContent = `
        <div class="modal-content">
            <h2>Example Modal</h2>
            <p>This is an example modal created with UIHelpers.</p>
            <button onclick="closeModal()">Close</button>
        </div>
    `;
    
    uiHelpers.showModal(modalId, modalContent);
    
    // Close modal after 3 seconds
    setTimeout(() => {
        uiHelpers.closeModal(modalId);
    }, 3000);
    
    // Example 3: Loading spinners
    console.log('\n3. Loading spinners:');
    
    // Show loading spinner
    uiHelpers.showSpinner('Loading data...');
    
    // Hide spinner after 2 seconds
    setTimeout(() => {
        uiHelpers.hideSpinner();
    }, 2000);
    
    // Example 4: Animations
    console.log('\n4. Animations:');
    
    // Fade in element
    const element = document.createElement('div');
    element.textContent = 'Animated element';
    element.style.padding = '10px';
    element.style.background = '#f0f0f0';
    document.body.appendChild(element);
    
    uiHelpers.fadeIn(element, 1000);
    
    // Fade out after 3 seconds
    setTimeout(() => {
        uiHelpers.fadeOut(element, 1000, () => {
            document.body.removeChild(element);
        });
    }, 3000);
    
    // Example 5: Debounce and throttle
    console.log('\n5. Debounce and throttle:');
    
    // Debounced function
    const debouncedSearch = uiHelpers.debounce((query) => {
        console.log(`Searching for: ${query}`);
    }, 300);
    
    // Throttled function
    const throttledScroll = uiHelpers.throttle(() => {
        console.log('Scroll event throttled');
    }, 100);
    
    // Simulate rapid calls
    for (let i = 0; i < 5; i++) {
        debouncedSearch(`query-${i}`);
        throttledScroll();
    }
}

/**
 * React Components Examples
 */
function reactComponentsExamples() {
    console.log('\n=== React Components Examples ===\n');
    
    // Example 1: Button component
    console.log('1. Button component:');
    
    // Create different button variants
    const buttonExamples = [
        { variant: 'primary', text: 'Primary Button' },
        { variant: 'secondary', text: 'Secondary Button' },
        { variant: 'success', text: 'Success Button' },
        { variant: 'danger', text: 'Danger Button' },
        { variant: 'warning', text: 'Warning Button' },
        { variant: 'info', text: 'Info Button' }
    ];
    
    buttonExamples.forEach(example => {
        console.log(`  ${example.variant}: ${example.text}`);
    });
    
    // Example 2: Button sizes
    console.log('\n2. Button sizes:');
    const sizes = ['small', 'medium', 'large'];
    sizes.forEach(size => {
        console.log(`  ${size} size button`);
    });
    
    // Example 3: Button states
    console.log('\n3. Button states:');
    const states = ['default', 'loading', 'disabled'];
    states.forEach(state => {
        console.log(`  ${state} state button`);
    });
}

/**
 * Vue Components Examples
 */
function vueComponentsExamples() {
    console.log('\n=== Vue Components Examples ===\n');
    
    // Example 1: DataTable component
    console.log('1. DataTable component:');
    
    // Sample data for the table
    const tableData = [
        { id: 1, name: 'John Doe', email: 'john@example.com', age: 30, department: 'IT' },
        { id: 2, name: 'Jane Smith', email: 'jane@example.com', age: 25, department: 'HR' },
        { id: 3, name: 'Bob Johnson', email: 'bob@example.com', age: 35, department: 'Finance' },
        { id: 4, name: 'Alice Brown', email: 'alice@example.com', age: 28, department: 'Marketing' },
        { id: 5, name: 'Charlie Wilson', email: 'charlie@example.com', age: 32, department: 'IT' }
    ];
    
    // Table columns configuration
    const columns = [
        { key: 'id', label: 'ID', sortable: true, width: '80px' },
        { key: 'name', label: 'Name', sortable: true },
        { key: 'email', label: 'Email', sortable: true },
        { key: 'age', label: 'Age', sortable: true, align: 'center' },
        { key: 'department', label: 'Department', sortable: true }
    ];
    
    // Table filters
    const filters = [
        { key: 'department', label: 'Department', type: 'select' },
        { key: 'age', label: 'Age Range', type: 'number' }
    ];
    
    console.log('  DataTable configured with:');
    console.log(`    - ${tableData.length} rows of data`);
    console.log(`    - ${columns.length} columns`);
    console.log(`    - ${filters.length} filters`);
    console.log('    - Sorting enabled');
    console.log('    - Pagination enabled');
    console.log('    - Search functionality');
}

/**
 * Network and API Examples
 */
function networkExamples() {
    console.log('\n=== Network and API Examples ===\n');
    
    // Example 1: API calls
    console.log('1. API calls:');
    
    // GET request
    fetch('https://jsonplaceholder.typicode.com/posts/1')
        .then(response => response.json())
        .then(data => {
            console.log('  GET request result:', data.title);
        })
        .catch(error => {
            console.log('  GET request error:', error.message);
        });
    
    // POST request
    const postData = {
        title: 'Test Post',
        body: 'This is a test post',
        userId: 1
    };
    
    fetch('https://jsonplaceholder.typicode.com/posts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(postData)
    })
        .then(response => response.json())
        .then(data => {
            console.log('  POST request result:', data.id);
        })
        .catch(error => {
            console.log('  POST request error:', error.message);
        });
    
    // Example 2: Error handling
    console.log('\n2. Error handling:');
    
    // Simulate network error
    fetch('https://invalid-url-that-does-not-exist.com')
        .then(response => response.json())
        .catch(error => {
            console.log('  Network error handled:', error.message);
        });
}

/**
 * Storage Examples
 */
function storageExamples() {
    console.log('\n=== Storage Examples ===\n');
    
    // Example 1: Local storage
    console.log('1. Local storage:');
    
    // Store data
    const userData = {
        id: 1,
        name: 'John Doe',
        email: 'john@example.com',
        preferences: {
            theme: 'dark',
            language: 'en'
        }
    };
    
    localStorage.setItem('user', JSON.stringify(userData));
    console.log('  Data stored in localStorage');
    
    // Retrieve data
    const storedUser = JSON.parse(localStorage.getItem('user'));
    console.log('  Retrieved user:', storedUser.name);
    
    // Example 2: Session storage
    console.log('\n2. Session storage:');
    
    sessionStorage.setItem('sessionId', 'abc123');
    sessionStorage.setItem('lastActivity', new Date().toISOString());
    
    console.log('  Session ID:', sessionStorage.getItem('sessionId'));
    console.log('  Last activity:', sessionStorage.getItem('lastActivity'));
    
    // Example 3: Cookies
    console.log('\n3. Cookies:');
    
    // Set cookie
    document.cookie = 'user_preference=dark_theme; expires=Fri, 31 Dec 2024 23:59:59 GMT; path=/';
    console.log('  Cookie set: user_preference');
    
    // Read cookies
    const cookies = document.cookie.split(';').reduce((acc, cookie) => {
        const [key, value] = cookie.trim().split('=');
        acc[key] = value;
        return acc;
    }, {});
    
    console.log('  All cookies:', cookies);
}

/**
 * Utility Functions Examples
 */
function utilityExamples() {
    console.log('\n=== Utility Functions Examples ===\n');
    
    // Example 1: Array utilities
    console.log('1. Array utilities:');
    
    const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    
    // Chunk array
    const chunks = numbers.reduce((acc, item, index) => {
        const chunkIndex = Math.floor(index / 3);
        if (!acc[chunkIndex]) acc[chunkIndex] = [];
        acc[chunkIndex].push(item);
        return acc;
    }, []);
    
    console.log('  Chunked array:', chunks);
    
    // Example 2: Object utilities
    console.log('\n2. Object utilities:');
    
    const deepObject = {
        user: {
            profile: {
                name: 'John',
                settings: {
                    theme: 'dark',
                    notifications: true
                }
            }
        }
    };
    
    // Deep get
    const theme = deepObject?.user?.profile?.settings?.theme;
    console.log('  Deep get theme:', theme);
    
    // Example 3: String utilities
    console.log('\n3. String utilities:');
    
    const text = 'hello world example';
    
    // Capitalize
    const capitalized = text.replace(/\b\w/g, l => l.toUpperCase());
    console.log('  Capitalized:', capitalized);
    
    // Slugify
    const slug = text.toLowerCase().replace(/\s+/g, '-').replace(/[^\w\-]+/g, '');
    console.log('  Slugified:', slug);
}

/**
 * Main function to run all examples
 */
function runAllExamples() {
    console.log('Jagarnath JavaScript/TypeScript API Examples');
    console.log('='.repeat(50));
    
    try {
        // Run all examples
        dataValidationExamples();
        uiHelpersExamples();
        reactComponentsExamples();
        vueComponentsExamples();
        networkExamples();
        storageExamples();
        utilityExamples();
        
        console.log('\n' + '='.repeat(50));
        console.log('All examples completed successfully!');
        
    } catch (error) {
        console.error('\nError running examples:', error);
    }
}

// Export functions for use in other modules
export {
    dataValidationExamples,
    uiHelpersExamples,
    reactComponentsExamples,
    vueComponentsExamples,
    networkExamples,
    storageExamples,
    utilityExamples,
    runAllExamples
};

// Run examples if this file is executed directly
if (typeof window !== 'undefined') {
    // Browser environment
    window.runAllExamples = runAllExamples;
} else {
    // Node.js environment
    runAllExamples();
}