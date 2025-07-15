# Component Guide

## Overview

This guide provides comprehensive documentation for all UI components in the project. Each component includes detailed prop information, styling options, usage examples, and accessibility guidelines.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Layout Components](#layout-components)
3. [Form Components](#form-components)
4. [Data Display Components](#data-display-components)
5. [Navigation Components](#navigation-components)
6. [Feedback Components](#feedback-components)
7. [Overlay Components](#overlay-components)
8. [Utility Components](#utility-components)
9. [Theming and Customization](#theming-and-customization)
10. [Accessibility Guidelines](#accessibility-guidelines)

---

## Getting Started

### Installation

```bash
npm install @project/components
```

### Basic Usage

```jsx
import { Button, Card, Form } from '@project/components';

function App() {
  return (
    <Card>
      <Form>
        <Button>Click me</Button>
      </Form>
    </Card>
  );
}
```

### Theming

```jsx
import { ThemeProvider } from '@project/components';
import { darkTheme } from '@project/components/themes';

function App() {
  return (
    <ThemeProvider theme={darkTheme}>
      <YourApp />
    </ThemeProvider>
  );
}
```

---

## Layout Components

### Container

**Description**: A flexible container component that provides consistent spacing and max-width across different screen sizes.

**Props**:
- `maxWidth` (string, optional): Maximum width ('sm', 'md', 'lg', 'xl', 'full'). Default: 'lg'
- `padding` (string, optional): Padding size ('none', 'sm', 'md', 'lg'). Default: 'md'
- `fluid` (boolean, optional): Whether to use full width. Default: false
- `children` (React.ReactNode): Content to display inside the container

**Example**:
```jsx
<Container maxWidth="md" padding="lg">
  <h1>Welcome to our app</h1>
  <p>This content is centered and has consistent padding.</p>
</Container>
```

**CSS Classes**:
- `.container` - Base container class
- `.container-sm` - Small max-width
- `.container-md` - Medium max-width
- `.container-lg` - Large max-width
- `.container-xl` - Extra large max-width
- `.container-fluid` - Full width container

**Since**: v1.0.0

### Grid

**Description**: A responsive grid system for creating layouts with rows and columns.

**Props**:
- `columns` (number, optional): Number of columns (1-12). Default: 12
- `gap` (string, optional): Gap size ('none', 'sm', 'md', 'lg'). Default: 'md'
- `children` (React.ReactNode): Grid items

**Example**:
```jsx
<Grid columns={12} gap="lg">
  <Grid.Item span={6}>
    <Card>Left column</Card>
  </Grid.Item>
  <Grid.Item span={6}>
    <Card>Right column</Card>
  </Grid.Item>
</Grid>
```

**Grid.Item Props**:
- `span` (number): Number of columns to span (1-12)
- `offset` (number, optional): Number of columns to offset
- `xs`, `sm`, `md`, `lg`, `xl` (number, optional): Responsive column spans

**Since**: v1.0.0

### Flex

**Description**: A flexible box layout component with common flex properties.

**Props**:
- `direction` (string, optional): Flex direction ('row', 'column', 'row-reverse', 'column-reverse'). Default: 'row'
- `justify` (string, optional): Justify content ('start', 'center', 'end', 'between', 'around', 'evenly'). Default: 'start'
- `align` (string, optional): Align items ('start', 'center', 'end', 'stretch', 'baseline'). Default: 'stretch'
- `wrap` (string, optional): Flex wrap ('nowrap', 'wrap', 'wrap-reverse'). Default: 'nowrap'
- `gap` (string, optional): Gap size ('none', 'sm', 'md', 'lg'). Default: 'none'

**Example**:
```jsx
<Flex direction="column" justify="center" align="center" gap="md">
  <Button>Button 1</Button>
  <Button>Button 2</Button>
  <Button>Button 3</Button>
</Flex>
```

**Since**: v1.0.0

---

## Form Components

### Button

**Description**: A versatile button component with multiple variants and states.

**Props**:
- `variant` (string, optional): Button variant ('primary', 'secondary', 'success', 'warning', 'danger', 'ghost'). Default: 'primary'
- `size` (string, optional): Button size ('sm', 'md', 'lg'). Default: 'md'
- `disabled` (boolean, optional): Whether the button is disabled. Default: false
- `loading` (boolean, optional): Whether to show loading state. Default: false
- `type` (string, optional): Button type ('button', 'submit', 'reset'). Default: 'button'
- `onClick` (Function, optional): Click event handler
- `children` (React.ReactNode): Button content

**Example**:
```jsx
<Button variant="primary" size="lg" onClick={handleSubmit}>
  Submit Form
</Button>

<Button variant="secondary" disabled>
  Disabled Button
</Button>

<Button variant="danger" loading>
  Loading...
</Button>
```

**CSS Classes**:
- `.btn` - Base button class
- `.btn-primary`, `.btn-secondary`, etc. - Variant classes
- `.btn-sm`, `.btn-md`, `.btn-lg` - Size classes
- `.btn-disabled` - Disabled state
- `.btn-loading` - Loading state

**Since**: v1.0.0

### Input

**Description**: A flexible input component with validation and various types.

**Props**:
- `type` (string, optional): Input type ('text', 'email', 'password', 'number', 'search', 'tel', 'url'). Default: 'text'
- `placeholder` (string, optional): Placeholder text
- `value` (string, optional): Input value (controlled)
- `defaultValue` (string, optional): Default value (uncontrolled)
- `disabled` (boolean, optional): Whether the input is disabled
- `required` (boolean, optional): Whether the input is required
- `error` (string, optional): Error message to display
- `label` (string, optional): Label text
- `helperText` (string, optional): Helper text
- `onChange` (Function, optional): Change event handler
- `onBlur` (Function, optional): Blur event handler
- `onFocus` (Function, optional): Focus event handler

**Example**:
```jsx
<Input
  type="email"
  label="Email Address"
  placeholder="Enter your email"
  helperText="We'll never share your email"
  error={emailError}
  onChange={handleEmailChange}
  required
/>
```

**Since**: v1.0.0

### Select

**Description**: A dropdown select component with search and multi-select capabilities.

**Props**:
- `options` (Array): Array of option objects with `value` and `label` properties
- `value` (string|Array, optional): Selected value(s)
- `defaultValue` (string|Array, optional): Default selected value(s)
- `multiple` (boolean, optional): Whether to allow multiple selections
- `searchable` (boolean, optional): Whether to enable search functionality
- `placeholder` (string, optional): Placeholder text
- `disabled` (boolean, optional): Whether the select is disabled
- `error` (string, optional): Error message to display
- `label` (string, optional): Label text
- `onChange` (Function, optional): Change event handler

**Example**:
```jsx
const options = [
  { value: 'us', label: 'United States' },
  { value: 'ca', label: 'Canada' },
  { value: 'uk', label: 'United Kingdom' }
];

<Select
  label="Country"
  options={options}
  searchable
  placeholder="Select a country"
  onChange={handleCountryChange}
/>
```

**Since**: v1.0.0

### Textarea

**Description**: A multi-line text input component with auto-resize functionality.

**Props**:
- `placeholder` (string, optional): Placeholder text
- `value` (string, optional): Textarea value (controlled)
- `defaultValue` (string, optional): Default value (uncontrolled)
- `disabled` (boolean, optional): Whether the textarea is disabled
- `required` (boolean, optional): Whether the textarea is required
- `error` (string, optional): Error message to display
- `label` (string, optional): Label text
- `rows` (number, optional): Number of visible rows. Default: 3
- `autoResize` (boolean, optional): Whether to auto-resize based on content
- `maxLength` (number, optional): Maximum character length
- `onChange` (Function, optional): Change event handler

**Example**:
```jsx
<Textarea
  label="Message"
  placeholder="Enter your message"
  rows={5}
  autoResize
  maxLength={500}
  onChange={handleMessageChange}
/>
```

**Since**: v1.0.0

### Checkbox

**Description**: A checkbox input component with custom styling and indeterminate state.

**Props**:
- `checked` (boolean, optional): Whether the checkbox is checked
- `defaultChecked` (boolean, optional): Default checked state
- `indeterminate` (boolean, optional): Whether to show indeterminate state
- `disabled` (boolean, optional): Whether the checkbox is disabled
- `label` (string, optional): Label text
- `error` (string, optional): Error message to display
- `onChange` (Function, optional): Change event handler

**Example**:
```jsx
<Checkbox
  label="I agree to the terms and conditions"
  checked={agreed}
  onChange={handleAgreementChange}
/>

<Checkbox
  label="Select all"
  indeterminate={someSelected}
  onChange={handleSelectAll}
/>
```

**Since**: v1.0.0

### RadioGroup

**Description**: A group of radio button options with consistent styling.

**Props**:
- `options` (Array): Array of option objects with `value` and `label` properties
- `value` (string, optional): Selected value
- `defaultValue` (string, optional): Default selected value
- `disabled` (boolean, optional): Whether the radio group is disabled
- `error` (string, optional): Error message to display
- `label` (string, optional): Label text
- `direction` (string, optional): Layout direction ('horizontal', 'vertical'). Default: 'vertical'
- `onChange` (Function, optional): Change event handler

**Example**:
```jsx
const options = [
  { value: 'small', label: 'Small' },
  { value: 'medium', label: 'Medium' },
  { value: 'large', label: 'Large' }
];

<RadioGroup
  label="Size"
  options={options}
  value={selectedSize}
  direction="horizontal"
  onChange={handleSizeChange}
/>
```

**Since**: v1.0.0

---

## Data Display Components

### Table

**Description**: A feature-rich table component with sorting, pagination, and selection.

**Props**:
- `data` (Array): Array of data objects
- `columns` (Array): Array of column definitions
- `sortable` (boolean, optional): Whether to enable sorting. Default: true
- `selectable` (boolean, optional): Whether to enable row selection. Default: false
- `pagination` (Object|boolean, optional): Pagination configuration or false to disable
- `loading` (boolean, optional): Whether to show loading state
- `emptyMessage` (string, optional): Message to show when no data
- `onSort` (Function, optional): Sort event handler
- `onSelect` (Function, optional): Selection event handler
- `onRowClick` (Function, optional): Row click event handler

**Column Definition**:
- `key` (string): Data key
- `label` (string): Column header
- `sortable` (boolean, optional): Whether column is sortable
- `width` (string, optional): Column width
- `render` (Function, optional): Custom render function

**Example**:
```jsx
const columns = [
  { key: 'name', label: 'Name', sortable: true },
  { key: 'email', label: 'Email', sortable: true },
  { key: 'role', label: 'Role', width: '120px' },
  {
    key: 'actions',
    label: 'Actions',
    render: (user) => (
      <Button size="sm" onClick={() => editUser(user)}>
        Edit
      </Button>
    )
  }
];

<Table
  data={users}
  columns={columns}
  sortable
  selectable
  pagination={{ pageSize: 10 }}
  onSort={handleSort}
  onSelect={handleSelect}
/>
```

**Since**: v1.0.0

### Card

**Description**: A container component for grouping related content with optional header and footer.

**Props**:
- `title` (string, optional): Card title
- `subtitle` (string, optional): Card subtitle
- `header` (React.ReactNode, optional): Custom header content
- `footer` (React.ReactNode, optional): Custom footer content
- `padding` (string, optional): Padding size ('none', 'sm', 'md', 'lg'). Default: 'md'
- `shadow` (string, optional): Shadow size ('none', 'sm', 'md', 'lg'). Default: 'sm'
- `border` (boolean, optional): Whether to show border. Default: true
- `hoverable` (boolean, optional): Whether to show hover effect. Default: false
- `onClick` (Function, optional): Click event handler

**Example**:
```jsx
<Card
  title="User Profile"
  subtitle="Manage your account settings"
  hoverable
  onClick={handleCardClick}
>
  <p>Card content goes here...</p>
</Card>

<Card
  header={<CustomHeader />}
  footer={
    <Button variant="primary">Save Changes</Button>
  }
>
  <Form>
    {/* Form content */}
  </Form>
</Card>
```

**Since**: v1.0.0

### Badge

**Description**: A small status indicator component for showing labels, counts, or status.

**Props**:
- `variant` (string, optional): Badge variant ('primary', 'secondary', 'success', 'warning', 'danger', 'info'). Default: 'primary'
- `size` (string, optional): Badge size ('sm', 'md', 'lg'). Default: 'md'
- `pill` (boolean, optional): Whether to use pill-shaped badge. Default: false
- `outline` (boolean, optional): Whether to use outline style. Default: false
- `children` (React.ReactNode): Badge content

**Example**:
```jsx
<Badge variant="success">Active</Badge>
<Badge variant="warning" pill>5</Badge>
<Badge variant="danger" outline>Error</Badge>
```

**Since**: v1.0.0

### Avatar

**Description**: A user avatar component with support for images, initials, and icons.

**Props**:
- `src` (string, optional): Image source URL
- `alt` (string, optional): Alt text for the image
- `size` (string, optional): Avatar size ('sm', 'md', 'lg', 'xl'). Default: 'md'
- `shape` (string, optional): Avatar shape ('circle', 'square'). Default: 'circle'
- `name` (string, optional): Name for generating initials
- `icon` (React.ReactNode, optional): Icon to display
- `backgroundColor` (string, optional): Background color
- `textColor` (string, optional): Text color

**Example**:
```jsx
<Avatar src="/user.jpg" alt="John Doe" size="lg" />
<Avatar name="Jane Smith" size="md" />
<Avatar icon={<UserIcon />} shape="square" />
```

**Since**: v1.0.0

---

## Navigation Components

### Navbar

**Description**: A navigation bar component with branding, navigation links, and actions.

**Props**:
- `brand` (React.ReactNode, optional): Brand content (logo, text)
- `fixed` (boolean, optional): Whether to fix the navbar to the top. Default: false
- `transparent` (boolean, optional): Whether to use transparent background. Default: false
- `children` (React.ReactNode): Navigation content

**Example**:
```jsx
<Navbar brand={<Logo />} fixed>
  <Navbar.Nav>
    <Navbar.Link href="/home">Home</Navbar.Link>
    <Navbar.Link href="/about">About</Navbar.Link>
    <Navbar.Link href="/contact">Contact</Navbar.Link>
  </Navbar.Nav>
  <Navbar.Actions>
    <Button variant="primary">Sign In</Button>
  </Navbar.Actions>
</Navbar>
```

**Since**: v1.0.0

### Breadcrumb

**Description**: A navigation aid that shows the current page's location within a hierarchy.

**Props**:
- `items` (Array): Array of breadcrumb items with `label` and `href` properties
- `separator` (string, optional): Separator character. Default: '/'
- `maxItems` (number, optional): Maximum number of items to show before collapsing

**Example**:
```jsx
const items = [
  { label: 'Home', href: '/' },
  { label: 'Category', href: '/category' },
  { label: 'Product', href: '/category/product' },
  { label: 'Details' } // Current page (no href)
];

<Breadcrumb items={items} separator=">" maxItems={3} />
```

**Since**: v1.0.0

### Tabs

**Description**: A tab navigation component for switching between different content panels.

**Props**:
- `activeTab` (string): Currently active tab key
- `onTabChange` (Function): Tab change event handler
- `variant` (string, optional): Tab variant ('line', 'card', 'pill'). Default: 'line'
- `size` (string, optional): Tab size ('sm', 'md', 'lg'). Default: 'md'
- `children` (React.ReactNode): Tab content

**Example**:
```jsx
<Tabs activeTab={activeTab} onTabChange={setActiveTab}>
  <Tabs.Tab key="profile" label="Profile">
    <ProfileContent />
  </Tabs.Tab>
  <Tabs.Tab key="settings" label="Settings">
    <SettingsContent />
  </Tabs.Tab>
  <Tabs.Tab key="billing" label="Billing">
    <BillingContent />
  </Tabs.Tab>
</Tabs>
```

**Since**: v1.0.0

### Sidebar

**Description**: A collapsible sidebar navigation component.

**Props**:
- `collapsed` (boolean, optional): Whether the sidebar is collapsed. Default: false
- `width` (string, optional): Sidebar width when expanded. Default: '280px'
- `collapsedWidth` (string, optional): Sidebar width when collapsed. Default: '60px'
- `position` (string, optional): Sidebar position ('left', 'right'). Default: 'left'
- `overlay` (boolean, optional): Whether to show overlay on mobile. Default: true
- `onToggle` (Function, optional): Toggle event handler

**Example**:
```jsx
<Sidebar collapsed={sidebarCollapsed} onToggle={setSidebarCollapsed}>
  <Sidebar.Header>
    <Logo />
  </Sidebar.Header>
  <Sidebar.Nav>
    <Sidebar.Item icon={<HomeIcon />} label="Dashboard" href="/dashboard" />
    <Sidebar.Item icon={<UsersIcon />} label="Users" href="/users" />
    <Sidebar.Item icon={<SettingsIcon />} label="Settings" href="/settings" />
  </Sidebar.Nav>
</Sidebar>
```

**Since**: v1.0.0

---

## Feedback Components

### Alert

**Description**: A feedback component for displaying important messages to users.

**Props**:
- `variant` (string, optional): Alert variant ('info', 'success', 'warning', 'error'). Default: 'info'
- `title` (string, optional): Alert title
- `dismissible` (boolean, optional): Whether the alert can be dismissed. Default: false
- `icon` (React.ReactNode, optional): Custom icon
- `onDismiss` (Function, optional): Dismiss event handler
- `children` (React.ReactNode): Alert content

**Example**:
```jsx
<Alert variant="success" title="Success!" dismissible onDismiss={handleDismiss}>
  Your changes have been saved successfully.
</Alert>

<Alert variant="error" icon={<ErrorIcon />}>
  There was an error processing your request.
</Alert>
```

**Since**: v1.0.0

### Toast

**Description**: A temporary notification component that appears and disappears automatically.

**Props**:
- `variant` (string, optional): Toast variant ('info', 'success', 'warning', 'error'). Default: 'info'
- `title` (string, optional): Toast title
- `duration` (number, optional): Auto-dismiss duration in ms. Default: 5000
- `position` (string, optional): Toast position ('top-right', 'top-left', 'bottom-right', 'bottom-left'). Default: 'top-right'
- `onDismiss` (Function, optional): Dismiss event handler

**Example**:
```jsx
// Using the toast system
import { toast } from '@project/components';

// Show different types of toasts
toast.success('Profile updated successfully!');
toast.error('Failed to save changes');
toast.info('New feature available', { duration: 3000 });
```

**Since**: v1.0.0

### Progress

**Description**: A progress indicator component for showing task completion status.

**Props**:
- `value` (number): Current progress value (0-100)
- `max` (number, optional): Maximum value. Default: 100
- `variant` (string, optional): Progress variant ('primary', 'success', 'warning', 'error'). Default: 'primary'
- `size` (string, optional): Progress size ('sm', 'md', 'lg'). Default: 'md'
- `label` (string, optional): Progress label
- `showValue` (boolean, optional): Whether to show percentage value. Default: true
- `animated` (boolean, optional): Whether to animate the progress bar. Default: false

**Example**:
```jsx
<Progress value={75} label="Upload Progress" animated />
<Progress value={50} variant="success" size="lg" />
<Progress value={30} variant="warning" showValue={false} />
```

**Since**: v1.0.0

### Spinner

**Description**: A loading spinner component for indicating ongoing processes.

**Props**:
- `size` (string, optional): Spinner size ('sm', 'md', 'lg'). Default: 'md'
- `variant` (string, optional): Spinner variant ('primary', 'secondary', 'light', 'dark'). Default: 'primary'
- `label` (string, optional): Accessibility label
- `overlay` (boolean, optional): Whether to show as overlay. Default: false

**Example**:
```jsx
<Spinner size="lg" label="Loading..." />
<Spinner variant="light" overlay />
```

**Since**: v1.0.0

---

## Overlay Components

### Modal

**Description**: A modal dialog component for displaying content in an overlay.

**Props**:
- `isOpen` (boolean): Whether the modal is open
- `onClose` (Function): Close event handler
- `title` (string, optional): Modal title
- `size` (string, optional): Modal size ('sm', 'md', 'lg', 'xl'). Default: 'md'
- `closeOnOverlayClick` (boolean, optional): Whether to close when overlay is clicked. Default: true
- `closeOnEsc` (boolean, optional): Whether to close when Escape is pressed. Default: true
- `children` (React.ReactNode): Modal content

**Example**:
```jsx
<Modal
  isOpen={isModalOpen}
  onClose={closeModal}
  title="Edit Profile"
  size="lg"
>
  <Modal.Body>
    <Form>
      {/* Form content */}
    </Form>
  </Modal.Body>
  <Modal.Footer>
    <Button variant="secondary" onClick={closeModal}>
      Cancel
    </Button>
    <Button variant="primary" onClick={handleSave}>
      Save Changes
    </Button>
  </Modal.Footer>
</Modal>
```

**Since**: v1.0.0

### Popover

**Description**: A floating content container that appears relative to a trigger element.

**Props**:
- `trigger` (React.ReactNode): Element that triggers the popover
- `content` (React.ReactNode): Popover content
- `placement` (string, optional): Popover placement ('top', 'bottom', 'left', 'right'). Default: 'bottom'
- `interactive` (boolean, optional): Whether the popover content is interactive. Default: true
- `arrow` (boolean, optional): Whether to show arrow. Default: true
- `delay` (number, optional): Show/hide delay in ms. Default: 0

**Example**:
```jsx
<Popover
  trigger={<Button>Show Info</Button>}
  content={
    <div>
      <h3>Additional Information</h3>
      <p>This is some helpful information.</p>
    </div>
  }
  placement="top"
  arrow
/>
```

**Since**: v1.0.0

### Tooltip

**Description**: A simple tooltip component for providing additional context on hover.

**Props**:
- `content` (string): Tooltip content
- `placement` (string, optional): Tooltip placement ('top', 'bottom', 'left', 'right'). Default: 'top'
- `delay` (number, optional): Show delay in ms. Default: 500
- `children` (React.ReactNode): Element that triggers the tooltip

**Example**:
```jsx
<Tooltip content="This button saves your changes" placement="bottom">
  <Button variant="primary">Save</Button>
</Tooltip>
```

**Since**: v1.0.0

### Dropdown

**Description**: A dropdown menu component for displaying a list of actions or options.

**Props**:
- `trigger` (React.ReactNode): Element that triggers the dropdown
- `items` (Array): Array of dropdown items
- `placement` (string, optional): Dropdown placement ('bottom-start', 'bottom-end', 'top-start', 'top-end'). Default: 'bottom-start'
- `onSelect` (Function, optional): Item selection handler

**Item Structure**:
- `key` (string): Unique item key
- `label` (string): Item label
- `icon` (React.ReactNode, optional): Item icon
- `disabled` (boolean, optional): Whether item is disabled
- `divider` (boolean, optional): Whether to show divider after item

**Example**:
```jsx
const items = [
  { key: 'edit', label: 'Edit', icon: <EditIcon /> },
  { key: 'copy', label: 'Copy', icon: <CopyIcon /> },
  { key: 'divider', divider: true },
  { key: 'delete', label: 'Delete', icon: <DeleteIcon />, disabled: true }
];

<Dropdown
  trigger={<Button>Actions</Button>}
  items={items}
  onSelect={handleItemSelect}
/>
```

**Since**: v1.0.0

---

## Utility Components

### Portal

**Description**: A component that renders its children in a different DOM node.

**Props**:
- `container` (Element, optional): Container element to render into. Default: document.body
- `children` (React.ReactNode): Content to render

**Example**:
```jsx
<Portal container={document.getElementById('modal-root')}>
  <div>This content is rendered in a different DOM node</div>
</Portal>
```

**Since**: v1.0.0

### ErrorBoundary

**Description**: A component that catches JavaScript errors in its child components.

**Props**:
- `fallback` (React.ReactNode|Function, optional): Fallback UI to render when error occurs
- `onError` (Function, optional): Error event handler
- `children` (React.ReactNode): Components to wrap

**Example**:
```jsx
<ErrorBoundary
  fallback={<div>Something went wrong. Please try again.</div>}
  onError={handleError}
>
  <App />
</ErrorBoundary>
```

**Since**: v1.0.0

### Conditional

**Description**: A utility component for conditional rendering.

**Props**:
- `condition` (boolean): Whether to render children
- `fallback` (React.ReactNode, optional): Fallback content when condition is false
- `children` (React.ReactNode): Content to render when condition is true

**Example**:
```jsx
<Conditional condition={isLoggedIn} fallback={<LoginForm />}>
  <Dashboard />
</Conditional>
```

**Since**: v1.0.0

---

## Theming and Customization

### Theme Provider

**Description**: Provides theme context to all child components.

**Props**:
- `theme` (Object): Theme configuration object
- `children` (React.ReactNode): Components to provide theme to

**Example**:
```jsx
import { ThemeProvider, createTheme } from '@project/components';

const customTheme = createTheme({
  colors: {
    primary: '#007bff',
    secondary: '#6c757d',
    success: '#28a745',
    warning: '#ffc107',
    error: '#dc3545'
  },
  spacing: {
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px'
  },
  breakpoints: {
    sm: '576px',
    md: '768px',
    lg: '992px',
    xl: '1200px'
  }
});

<ThemeProvider theme={customTheme}>
  <App />
</ThemeProvider>
```

### CSS Variables

The component library uses CSS variables for easy customization:

```css
:root {
  --primary-color: #007bff;
  --secondary-color: #6c757d;
  --success-color: #28a745;
  --warning-color: #ffc107;
  --error-color: #dc3545;
  
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  
  --border-radius: 4px;
  --border-color: #dee2e6;
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
}
```

---

## Accessibility Guidelines

### ARIA Support

All components include proper ARIA attributes:

- **Buttons**: `aria-label`, `aria-pressed`, `aria-expanded`
- **Forms**: `aria-describedby`, `aria-invalid`, `aria-required`
- **Modals**: `aria-modal`, `aria-labelledby`, `aria-describedby`
- **Tables**: `aria-sort`, `aria-selected`, `aria-rowcount`

### Keyboard Navigation

Components support keyboard navigation:

- **Tab**: Navigate between focusable elements
- **Enter/Space**: Activate buttons and links
- **Arrow keys**: Navigate within components (tabs, dropdowns)
- **Escape**: Close modals and dropdowns

### Screen Reader Support

- Semantic HTML elements are used where appropriate
- Proper heading hierarchy is maintained
- Form labels are associated with inputs
- Status messages are announced appropriately

### Color Contrast

All components meet WCAG 2.1 AA color contrast requirements:

- Normal text: 4.5:1 contrast ratio
- Large text: 3:1 contrast ratio
- UI components: 3:1 contrast ratio

### Focus Management

- Visible focus indicators on all interactive elements
- Logical focus order throughout the interface
- Focus is trapped within modals and dropdowns
- Focus is restored when overlays are closed

---

## Browser Support

The component library supports:

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Performance Considerations

- Components are tree-shakeable for smaller bundle sizes
- Lazy loading is supported for large components
- Virtual scrolling is available for large lists
- Memoization is used to prevent unnecessary re-renders

---

## Contributing

When adding new components:

1. Follow the component template structure
2. Include comprehensive prop documentation
3. Add accessibility features
4. Include unit and integration tests
5. Update the style guide
6. Add Storybook stories

---

*This component guide is continuously updated. For the latest version, please check the repository.*