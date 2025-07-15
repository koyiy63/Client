# Component Documentation

## Overview

This document provides comprehensive documentation for all React components in the project.

## Component Categories

- [UI Components](#ui-components)
- [Layout Components](#layout-components)
- [Form Components](#form-components)
- [Data Display Components](#data-display-components)
- [Navigation Components](#navigation-components)

## UI Components

### Button

A versatile button component with multiple variants and states.

**Props:**
- `children` (ReactNode) - Button content
- `variant` (string, optional) - Button style variant ('primary' | 'secondary' | 'outline' | 'ghost' | 'danger')
- `size` (string, optional) - Button size ('sm' | 'md' | 'lg')
- `disabled` (boolean, optional) - Disable the button
- `loading` (boolean, optional) - Show loading state
- `onClick` (function, optional) - Click handler
- `type` (string, optional) - Button type ('button' | 'submit' | 'reset')
- `fullWidth` (boolean, optional) - Make button full width
- `icon` (ReactNode, optional) - Icon to display
- `iconPosition` (string, optional) - Icon position ('left' | 'right')

**Example:**
```jsx
import React from 'react';
import { Button } from './components/Button';

function Example() {
  const handleClick = () => {
    console.log('Button clicked!');
  };

  return (
    <div>
      {/* Primary button */}
      <Button onClick={handleClick}>
        Click me
      </Button>

      {/* Secondary button with icon */}
      <Button 
        variant="secondary" 
        icon={<Icon />} 
        iconPosition="left"
      >
        With Icon
      </Button>

      {/* Loading button */}
      <Button loading={true}>
        Loading...
      </Button>

      {/* Disabled button */}
      <Button disabled={true}>
        Disabled
      </Button>

      {/* Full width button */}
      <Button fullWidth={true}>
        Full Width
      </Button>
    </div>
  );
}
```

### Input

A flexible input component with validation and various types.

**Props:**
- `type` (string, optional) - Input type ('text' | 'email' | 'password' | 'number' | 'tel' | 'url')
- `value` (string, optional) - Input value
- `placeholder` (string, optional) - Placeholder text
- `label` (string, optional) - Input label
- `error` (string, optional) - Error message
- `disabled` (boolean, optional) - Disable the input
- `required` (boolean, optional) - Mark as required
- `onChange` (function, optional) - Change handler
- `onBlur` (function, optional) - Blur handler
- `onFocus` (function, optional) - Focus handler
- `prefix` (ReactNode, optional) - Prefix content
- `suffix` (ReactNode, optional) - Suffix content
- `size` (string, optional) - Input size ('sm' | 'md' | 'lg')

**Example:**
```jsx
import React, { useState } from 'react';
import { Input } from './components/Input';

function Example() {
  const [value, setValue] = useState('');
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setValue(e.target.value);
    if (error) setError('');
  };

  const handleBlur = () => {
    if (!value) {
      setError('This field is required');
    }
  };

  return (
    <div>
      {/* Basic input */}
      <Input
        type="text"
        value={value}
        onChange={handleChange}
        onBlur={handleBlur}
        placeholder="Enter your name"
        label="Name"
        error={error}
      />

      {/* Email input with prefix */}
      <Input
        type="email"
        placeholder="Enter your email"
        label="Email"
        prefix={<EmailIcon />}
        required={true}
      />

      {/* Password input with suffix */}
      <Input
        type="password"
        placeholder="Enter password"
        label="Password"
        suffix={<EyeIcon />}
      />

      {/* Number input */}
      <Input
        type="number"
        placeholder="Enter age"
        label="Age"
        min={0}
        max={120}
      />
    </div>
  );
}
```

### Modal

A modal dialog component for overlays and dialogs.

**Props:**
- `isOpen` (boolean) - Whether modal is open
- `onClose` (function) - Close handler
- `title` (string, optional) - Modal title
- `children` (ReactNode) - Modal content
- `size` (string, optional) - Modal size ('sm' | 'md' | 'lg' | 'xl')
- `closeOnOverlayClick` (boolean, optional) - Close on overlay click (default: true)
- `closeOnEscape` (boolean, optional) - Close on escape key (default: true)
- `showCloseButton` (boolean, optional) - Show close button (default: true)
- `footer` (ReactNode, optional) - Footer content

**Example:**
```jsx
import React, { useState } from 'react';
import { Modal } from './components/Modal';
import { Button } from './components/Button';

function Example() {
  const [isOpen, setIsOpen] = useState(false);

  const handleClose = () => {
    setIsOpen(false);
  };

  return (
    <div>
      <Button onClick={() => setIsOpen(true)}>
        Open Modal
      </Button>

      <Modal
        isOpen={isOpen}
        onClose={handleClose}
        title="Confirmation"
        size="md"
      >
        <p>Are you sure you want to delete this item?</p>
        
        <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
          <Button variant="outline" onClick={handleClose}>
            Cancel
          </Button>
          <Button variant="danger" onClick={handleClose}>
            Delete
          </Button>
        </div>
      </Modal>
    </div>
  );
}
```

## Layout Components

### Container

A responsive container component for layout management.

**Props:**
- `children` (ReactNode) - Container content
- `maxWidth` (string, optional) - Maximum width ('sm' | 'md' | 'lg' | 'xl' | 'full')
- `padding` (string, optional) - Padding size ('none' | 'sm' | 'md' | 'lg')
- `centered` (boolean, optional) - Center the container
- `fluid` (boolean, optional) - Full width container

**Example:**
```jsx
import React from 'react';
import { Container } from './components/Container';

function Example() {
  return (
    <Container maxWidth="lg" padding="md" centered>
      <h1>Welcome to our app</h1>
      <p>This content is contained within a responsive container.</p>
    </Container>
  );
}
```

### Grid

A flexible grid system component.

**Props:**
- `children` (ReactNode) - Grid content
- `columns` (number, optional) - Number of columns (default: 12)
- `gap` (string, optional) - Gap between items ('sm' | 'md' | 'lg')
- `alignItems` (string, optional) - Vertical alignment ('start' | 'center' | 'end' | 'stretch')
- `justifyContent` (string, optional) - Horizontal alignment ('start' | 'center' | 'end' | 'space-between' | 'space-around')

**Example:**
```jsx
import React from 'react';
import { Grid } from './components/Grid';
import { GridItem } from './components/GridItem';

function Example() {
  return (
    <Grid columns={3} gap="md" alignItems="center">
      <GridItem span={1}>
        <div>Item 1</div>
      </GridItem>
      <GridItem span={2}>
        <div>Item 2 (spans 2 columns)</div>
      </GridItem>
      <GridItem span={3}>
        <div>Item 3 (full width)</div>
      </GridItem>
    </Grid>
  );
}
```

### Card

A card component for displaying content in a contained area.

**Props:**
- `children` (ReactNode) - Card content
- `title` (string, optional) - Card title
- `subtitle` (string, optional) - Card subtitle
- `image` (string, optional) - Card image URL
- `actions` (ReactNode, optional) - Action buttons
- `elevation` (number, optional) - Shadow elevation (0-5)
- `padding` (string, optional) - Padding size ('none' | 'sm' | 'md' | 'lg')
- `onClick` (function, optional) - Click handler

**Example:**
```jsx
import React from 'react';
import { Card } from './components/Card';
import { Button } from './components/Button';

function Example() {
  return (
    <Card
      title="Product Card"
      subtitle="High-quality product"
      image="https://example.com/product.jpg"
      elevation={2}
      actions={
        <div style={{ display: 'flex', gap: '10px' }}>
          <Button variant="outline">Details</Button>
          <Button>Add to Cart</Button>
        </div>
      }
    >
      <p>This is a sample product description that goes in the card body.</p>
    </Card>
  );
}
```

## Form Components

### Form

A form component with validation and submission handling.

**Props:**
- `children` (ReactNode) - Form content
- `onSubmit` (function) - Submit handler
- `initialValues` (object, optional) - Initial form values
- `validationSchema` (object, optional) - Validation schema (Yup)
- `loading` (boolean, optional) - Loading state
- `disabled` (boolean, optional) - Disable form

**Example:**
```jsx
import React from 'react';
import { Form } from './components/Form';
import { Input } from './components/Input';
import { Button } from './components/Button';
import * as yup from 'yup';

const validationSchema = yup.object({
  name: yup.string().required('Name is required'),
  email: yup.string().email('Invalid email').required('Email is required'),
  password: yup.string().min(8, 'Password must be at least 8 characters').required('Password is required')
});

function Example() {
  const handleSubmit = (values) => {
    console.log('Form submitted:', values);
  };

  return (
    <Form
      onSubmit={handleSubmit}
      initialValues={{ name: '', email: '', password: '' }}
      validationSchema={validationSchema}
    >
      <Input name="name" label="Name" placeholder="Enter your name" />
      <Input name="email" type="email" label="Email" placeholder="Enter your email" />
      <Input name="password" type="password" label="Password" placeholder="Enter password" />
      
      <Button type="submit" fullWidth>
        Submit
      </Button>
    </Form>
  );
}
```

### Select

A select dropdown component.

**Props:**
- `options` (array) - Array of options
- `value` (any) - Selected value
- `onChange` (function) - Change handler
- `placeholder` (string, optional) - Placeholder text
- `label` (string, optional) - Select label
- `error` (string, optional) - Error message
- `disabled` (boolean, optional) - Disable the select
- `multiple` (boolean, optional) - Allow multiple selection
- `searchable` (boolean, optional) - Enable search functionality

**Example:**
```jsx
import React, { useState } from 'react';
import { Select } from './components/Select';

function Example() {
  const [value, setValue] = useState('');

  const options = [
    { value: 'option1', label: 'Option 1' },
    { value: 'option2', label: 'Option 2' },
    { value: 'option3', label: 'Option 3' }
  ];

  return (
    <Select
      options={options}
      value={value}
      onChange={setValue}
      placeholder="Select an option"
      label="Choose Option"
      searchable={true}
    />
  );
}
```

## Data Display Components

### Table

A data table component with sorting, filtering, and pagination.

**Props:**
- `data` (array) - Table data
- `columns` (array) - Column definitions
- `sortable` (boolean, optional) - Enable sorting
- `filterable` (boolean, optional) - Enable filtering
- `pagination` (boolean, optional) - Enable pagination
- `pageSize` (number, optional) - Items per page
- `onRowClick` (function, optional) - Row click handler
- `loading` (boolean, optional) - Loading state
- `emptyMessage` (string, optional) - Message when no data

**Example:**
```jsx
import React, { useState } from 'react';
import { Table } from './components/Table';

function Example() {
  const [data] = useState([
    { id: 1, name: 'John Doe', email: 'john@example.com', role: 'Admin' },
    { id: 2, name: 'Jane Smith', email: 'jane@example.com', role: 'User' },
    { id: 3, name: 'Bob Johnson', email: 'bob@example.com', role: 'User' }
  ]);

  const columns = [
    { key: 'name', label: 'Name', sortable: true },
    { key: 'email', label: 'Email', sortable: true },
    { key: 'role', label: 'Role', filterable: true },
    {
      key: 'actions',
      label: 'Actions',
      render: (row) => (
        <div>
          <Button size="sm" variant="outline">Edit</Button>
          <Button size="sm" variant="danger">Delete</Button>
        </div>
      )
    }
  ];

  const handleRowClick = (row) => {
    console.log('Clicked row:', row);
  };

  return (
    <Table
      data={data}
      columns={columns}
      sortable={true}
      filterable={true}
      pagination={true}
      pageSize={10}
      onRowClick={handleRowClick}
    />
  );
}
```

### Chart

A chart component for data visualization.

**Props:**
- `type` (string) - Chart type ('line' | 'bar' | 'pie' | 'doughnut' | 'area')
- `data` (object) - Chart data
- `options` (object, optional) - Chart options
- `height` (number, optional) - Chart height
- `width` (number, optional) - Chart width
- `responsive` (boolean, optional) - Make chart responsive

**Example:**
```jsx
import React from 'react';
import { Chart } from './components/Chart';

function Example() {
  const data = {
    labels: ['January', 'February', 'March', 'April', 'May'],
    datasets: [
      {
        label: 'Sales',
        data: [12, 19, 3, 5, 2],
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }
    ]
  };

  const options = {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true
      }
    }
  };

  return (
    <Chart
      type="bar"
      data={data}
      options={options}
      height={400}
    />
  );
}
```

## Navigation Components

### Navigation

A navigation component with menu items and responsive design.

**Props:**
- `items` (array) - Navigation items
- `logo` (ReactNode, optional) - Logo component
- `variant` (string, optional) - Navigation style ('horizontal' | 'vertical')
- `sticky` (boolean, optional) - Make navigation sticky
- `onItemClick` (function, optional) - Item click handler

**Example:**
```jsx
import React from 'react';
import { Navigation } from './components/Navigation';

function Example() {
  const items = [
    { label: 'Home', href: '/', icon: <HomeIcon /> },
    { label: 'Products', href: '/products', icon: <ProductIcon /> },
    { label: 'About', href: '/about', icon: <AboutIcon /> },
    { label: 'Contact', href: '/contact', icon: <ContactIcon /> }
  ];

  const handleItemClick = (item) => {
    console.log('Navigation item clicked:', item);
  };

  return (
    <Navigation
      items={items}
      logo={<Logo />}
      variant="horizontal"
      sticky={true}
      onItemClick={handleItemClick}
    />
  );
}
```

### Breadcrumb

A breadcrumb navigation component.

**Props:**
- `items` (array) - Breadcrumb items
- `separator` (ReactNode, optional) - Separator between items
- `onItemClick` (function, optional) - Item click handler

**Example:**
```jsx
import React from 'react';
import { Breadcrumb } from './components/Breadcrumb';

function Example() {
  const items = [
    { label: 'Home', href: '/' },
    { label: 'Products', href: '/products' },
    { label: 'Electronics', href: '/products/electronics' },
    { label: 'Smartphones' }
  ];

  return (
    <Breadcrumb
      items={items}
      separator={<ChevronRightIcon />}
    />
  );
}
```

## Component Composition

### Higher-Order Components

#### `withLoading`

A HOC that adds loading state to components.

**Example:**
```jsx
import React from 'react';
import { withLoading } from './hocs/withLoading';

function UserList({ users, loading }) {
  if (loading) {
    return <div>Loading users...</div>;
  }

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}

export default withLoading(UserList);
```

#### `withError`

A HOC that adds error handling to components.

**Example:**
```jsx
import React from 'react';
import { withError } from './hocs/withError';

function DataComponent({ data, error }) {
  if (error) {
    return <div>Error: {error.message}</div>;
  }

  return <div>{data}</div>;
}

export default withError(DataComponent);
```

## Styling and Theming

### CSS Variables

Components use CSS variables for consistent theming:

```css
:root {
  /* Colors */
  --primary-color: #007bff;
  --secondary-color: #6c757d;
  --success-color: #28a745;
  --danger-color: #dc3545;
  --warning-color: #ffc107;
  --info-color: #17a2b8;

  /* Typography */
  --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-size-sm: 0.875rem;
  --font-size-md: 1rem;
  --font-size-lg: 1.125rem;

  /* Spacing */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 3rem;

  /* Border radius */
  --border-radius-sm: 0.25rem;
  --border-radius-md: 0.375rem;
  --border-radius-lg: 0.5rem;
}
```

### Custom Themes

Create custom themes by overriding CSS variables:

```css
.theme-dark {
  --primary-color: #4dabf7;
  --background-color: #212529;
  --text-color: #f8f9fa;
  --border-color: #495057;
}
```

## Best Practices

### Component Usage Guidelines

1. **Props Validation**: Always use PropTypes or TypeScript for prop validation
2. **Default Props**: Provide sensible defaults for optional props
3. **Accessibility**: Include proper ARIA labels and keyboard navigation
4. **Performance**: Use React.memo for expensive components
5. **Testing**: Write unit tests for all components

### Example Component Structure

```jsx
import React from 'react';
import PropTypes from 'prop-types';
import './Component.css';

const Component = ({ 
  prop1, 
  prop2 = 'default', 
  children,
  ...otherProps 
}) => {
  return (
    <div className="component" {...otherProps}>
      {children}
    </div>
  );
};

Component.propTypes = {
  prop1: PropTypes.string.isRequired,
  prop2: PropTypes.string,
  children: PropTypes.node
};

Component.defaultProps = {
  prop2: 'default'
};

export default Component;
```

## Testing Components

### Unit Test Example

```jsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Button from './Button';

describe('Button', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByText('Click me')).toBeDisabled();
  });
});
```