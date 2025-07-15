/**
 * Button Component
 * 
 * A customizable button component with multiple variants, sizes, and states.
 * Supports loading states, icons, and various styling options.
 * 
 * @example
 * ```tsx
 * import { Button } from '@jagarnath/react';
 * 
 * function App() {
 *   return (
 *     <div>
 *       <Button variant="primary" onClick={() => console.log('clicked')}>
 *         Click Me
 *       </Button>
 *       
 *       <Button variant="secondary" size="large" loading>
 *         Loading...
 *       </Button>
 *     </div>
 *   );
 * }
 * ```
 */

import React, { forwardRef, ButtonHTMLAttributes } from 'react';

export type ButtonVariant = 
  | 'primary' 
  | 'secondary' 
  | 'success' 
  | 'danger' 
  | 'warning' 
  | 'info' 
  | 'light' 
  | 'dark' 
  | 'outline-primary' 
  | 'outline-secondary' 
  | 'outline-success' 
  | 'outline-danger' 
  | 'outline-warning' 
  | 'outline-info' 
  | 'outline-light' 
  | 'outline-dark';

export type ButtonSize = 'small' | 'medium' | 'large';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /**
   * The visual variant of the button
   * @default 'primary'
   */
  variant?: ButtonVariant;
  
  /**
   * The size of the button
   * @default 'medium'
   */
  size?: ButtonSize;
  
  /**
   * Whether the button is in a loading state
   * @default false
   */
  loading?: boolean;
  
  /**
   * Loading text to display when loading is true
   * @default 'Loading...'
   */
  loadingText?: string;
  
  /**
   * Icon to display before the button text
   */
  leftIcon?: React.ReactNode;
  
  /**
   * Icon to display after the button text
   */
  rightIcon?: React.ReactNode;
  
  /**
   * Whether the button should take full width of its container
   * @default false
   */
  fullWidth?: boolean;
  
  /**
   * Whether the button should have rounded corners
   * @default false
   */
  rounded?: boolean;
  
  /**
   * Custom CSS class name
   */
  className?: string;
  
  /**
   * Custom inline styles
   */
  style?: React.CSSProperties;
  
  /**
   * Whether the button should have a disabled appearance
   * @default false
   */
  disabled?: boolean;
  
  /**
   * Whether the button should have a ghost/transparent appearance
   * @default false
   */
  ghost?: boolean;
}

/**
 * Button component with comprehensive styling and functionality options.
 * 
 * This component provides a flexible and accessible button implementation with:
 * - Multiple visual variants (primary, secondary, success, etc.)
 * - Different sizes (small, medium, large)
 * - Loading states with customizable text
 * - Icon support (left and right)
 * - Full width option
 * - Rounded corners option
 * - Ghost/transparent appearance
 * - Comprehensive accessibility features
 * 
 * @example
 * ```tsx
 * // Basic usage
 * <Button onClick={() => console.log('clicked')}>
 *   Click Me
 * </Button>
 * 
 * // With variant and size
 * <Button variant="success" size="large">
 *   Success Button
 * </Button>
 * 
 * // Loading state
 * <Button loading loadingText="Saving...">
 *   Save
 * </Button>
 * 
 * // With icons
 * <Button leftIcon={<Icon name="plus" />} rightIcon={<Icon name="arrow-right" />}>
 *   Add Item
 * </Button>
 * 
 * // Full width and rounded
 * <Button fullWidth rounded variant="primary">
 *   Full Width Button
 * </Button>
 * 
 * // Ghost button
 * <Button ghost variant="outline-primary">
 *   Ghost Button
 * </Button>
 * ```
 */
export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'medium',
      loading = false,
      loadingText = 'Loading...',
      leftIcon,
      rightIcon,
      fullWidth = false,
      rounded = false,
      className = '',
      style,
      disabled = false,
      ghost = false,
      children,
      onClick,
      ...props
    },
    ref
  ) => {
    // Determine if button should be disabled
    const isDisabled = disabled || loading;
    
    // Handle click event
    const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
      if (isDisabled) {
        event.preventDefault();
        return;
      }
      
      if (onClick) {
        onClick(event);
      }
    };
    
    // Build CSS classes
    const baseClasses = 'jagarnath-button';
    const variantClasses = `jagarnath-button--${variant}`;
    const sizeClasses = `jagarnath-button--${size}`;
    const stateClasses = isDisabled ? 'jagarnath-button--disabled' : '';
    const widthClasses = fullWidth ? 'jagarnath-button--full-width' : '';
    const roundedClasses = rounded ? 'jagarnath-button--rounded' : '';
    const ghostClasses = ghost ? 'jagarnath-button--ghost' : '';
    
    const buttonClasses = [
      baseClasses,
      variantClasses,
      sizeClasses,
      stateClasses,
      widthClasses,
      roundedClasses,
      ghostClasses,
      className
    ].filter(Boolean).join(' ');
    
    // Add styles if not already added
    React.useEffect(() => {
      if (!document.getElementById('jagarnath-button-styles')) {
        const styleElement = document.createElement('style');
        styleElement.id = 'jagarnath-button-styles';
        styleElement.textContent = getButtonStyles();
        document.head.appendChild(styleElement);
      }
    }, []);
    
    return (
      <button
        ref={ref}
        className={buttonClasses}
        style={style}
        disabled={isDisabled}
        onClick={handleClick}
        aria-disabled={isDisabled}
        aria-busy={loading}
        {...props}
      >
        {loading && (
          <span className="jagarnath-button__spinner" aria-hidden="true">
            <svg
              className="jagarnath-button__spinner-icon"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <circle
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeDasharray="31.416"
                strokeDashoffset="31.416"
                className="jagarnath-button__spinner-circle"
              />
            </svg>
          </span>
        )}
        
        {!loading && leftIcon && (
          <span className="jagarnath-button__icon jagarnath-button__icon--left">
            {leftIcon}
          </span>
        )}
        
        <span className="jagarnath-button__content">
          {loading ? loadingText : children}
        </span>
        
        {!loading && rightIcon && (
          <span className="jagarnath-button__icon jagarnath-button__icon--right">
            {rightIcon}
          </span>
        )}
      </button>
    );
  }
);

Button.displayName = 'Button';

/**
 * Get CSS styles for the button component.
 */
function getButtonStyles(): string {
  return `
    .jagarnath-button {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      border: 1px solid transparent;
      border-radius: 6px;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      font-weight: 500;
      text-decoration: none;
      cursor: pointer;
      transition: all 0.2s ease-in-out;
      user-select: none;
      position: relative;
      overflow: hidden;
      white-space: nowrap;
      vertical-align: middle;
      line-height: 1;
      outline: none;
    }
    
    .jagarnath-button:focus {
      outline: 2px solid #3b82f6;
      outline-offset: 2px;
    }
    
    .jagarnath-button:focus:not(:focus-visible) {
      outline: none;
    }
    
    .jagarnath-button:hover:not(:disabled) {
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .jagarnath-button:active:not(:disabled) {
      transform: translateY(0);
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Sizes */
    .jagarnath-button--small {
      padding: 6px 12px;
      font-size: 12px;
      min-height: 32px;
    }
    
    .jagarnath-button--medium {
      padding: 8px 16px;
      font-size: 14px;
      min-height: 40px;
    }
    
    .jagarnath-button--large {
      padding: 12px 24px;
      font-size: 16px;
      min-height: 48px;
    }
    
    /* Variants */
    .jagarnath-button--primary {
      background-color: #3b82f6;
      border-color: #3b82f6;
      color: white;
    }
    
    .jagarnath-button--primary:hover:not(:disabled) {
      background-color: #2563eb;
      border-color: #2563eb;
    }
    
    .jagarnath-button--secondary {
      background-color: #6b7280;
      border-color: #6b7280;
      color: white;
    }
    
    .jagarnath-button--secondary:hover:not(:disabled) {
      background-color: #4b5563;
      border-color: #4b5563;
    }
    
    .jagarnath-button--success {
      background-color: #10b981;
      border-color: #10b981;
      color: white;
    }
    
    .jagarnath-button--success:hover:not(:disabled) {
      background-color: #059669;
      border-color: #059669;
    }
    
    .jagarnath-button--danger {
      background-color: #ef4444;
      border-color: #ef4444;
      color: white;
    }
    
    .jagarnath-button--danger:hover:not(:disabled) {
      background-color: #dc2626;
      border-color: #dc2626;
    }
    
    .jagarnath-button--warning {
      background-color: #f59e0b;
      border-color: #f59e0b;
      color: white;
    }
    
    .jagarnath-button--warning:hover:not(:disabled) {
      background-color: #d97706;
      border-color: #d97706;
    }
    
    .jagarnath-button--info {
      background-color: #06b6d4;
      border-color: #06b6d4;
      color: white;
    }
    
    .jagarnath-button--info:hover:not(:disabled) {
      background-color: #0891b2;
      border-color: #0891b2;
    }
    
    .jagarnath-button--light {
      background-color: #f3f4f6;
      border-color: #f3f4f6;
      color: #374151;
    }
    
    .jagarnath-button--light:hover:not(:disabled) {
      background-color: #e5e7eb;
      border-color: #e5e7eb;
    }
    
    .jagarnath-button--dark {
      background-color: #374151;
      border-color: #374151;
      color: white;
    }
    
    .jagarnath-button--dark:hover:not(:disabled) {
      background-color: #1f2937;
      border-color: #1f2937;
    }
    
    /* Outline variants */
    .jagarnath-button--outline-primary {
      background-color: transparent;
      border-color: #3b82f6;
      color: #3b82f6;
    }
    
    .jagarnath-button--outline-primary:hover:not(:disabled) {
      background-color: #3b82f6;
      color: white;
    }
    
    .jagarnath-button--outline-secondary {
      background-color: transparent;
      border-color: #6b7280;
      color: #6b7280;
    }
    
    .jagarnath-button--outline-secondary:hover:not(:disabled) {
      background-color: #6b7280;
      color: white;
    }
    
    .jagarnath-button--outline-success {
      background-color: transparent;
      border-color: #10b981;
      color: #10b981;
    }
    
    .jagarnath-button--outline-success:hover:not(:disabled) {
      background-color: #10b981;
      color: white;
    }
    
    .jagarnath-button--outline-danger {
      background-color: transparent;
      border-color: #ef4444;
      color: #ef4444;
    }
    
    .jagarnath-button--outline-danger:hover:not(:disabled) {
      background-color: #ef4444;
      color: white;
    }
    
    .jagarnath-button--outline-warning {
      background-color: transparent;
      border-color: #f59e0b;
      color: #f59e0b;
    }
    
    .jagarnath-button--outline-warning:hover:not(:disabled) {
      background-color: #f59e0b;
      color: white;
    }
    
    .jagarnath-button--outline-info {
      background-color: transparent;
      border-color: #06b6d4;
      color: #06b6d4;
    }
    
    .jagarnath-button--outline-info:hover:not(:disabled) {
      background-color: #06b6d4;
      color: white;
    }
    
    .jagarnath-button--outline-light {
      background-color: transparent;
      border-color: #f3f4f6;
      color: #6b7280;
    }
    
    .jagarnath-button--outline-light:hover:not(:disabled) {
      background-color: #f3f4f6;
      color: #374151;
    }
    
    .jagarnath-button--outline-dark {
      background-color: transparent;
      border-color: #374151;
      color: #374151;
    }
    
    .jagarnath-button--outline-dark:hover:not(:disabled) {
      background-color: #374151;
      color: white;
    }
    
    /* States */
    .jagarnath-button--disabled,
    .jagarnath-button:disabled {
      opacity: 0.6;
      cursor: not-allowed;
      transform: none !important;
      box-shadow: none !important;
    }
    
    .jagarnath-button--disabled:hover,
    .jagarnath-button:disabled:hover {
      transform: none;
      box-shadow: none;
    }
    
    /* Modifiers */
    .jagarnath-button--full-width {
      width: 100%;
    }
    
    .jagarnath-button--rounded {
      border-radius: 9999px;
    }
    
    .jagarnath-button--ghost {
      background-color: transparent;
      border-color: transparent;
    }
    
    .jagarnath-button--ghost:hover:not(:disabled) {
      background-color: rgba(0, 0, 0, 0.05);
    }
    
    /* Icons */
    .jagarnath-button__icon {
      display: inline-flex;
      align-items: center;
      justify-content: center;
    }
    
    .jagarnath-button__icon--left {
      margin-right: 4px;
    }
    
    .jagarnath-button__icon--right {
      margin-left: 4px;
    }
    
    /* Spinner */
    .jagarnath-button__spinner {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      margin-right: 8px;
    }
    
    .jagarnath-button__spinner-icon {
      width: 16px;
      height: 16px;
      animation: spin 1s linear infinite;
    }
    
    .jagarnath-button__spinner-circle {
      animation: dash 1.5s ease-in-out infinite;
    }
    
    @keyframes spin {
      100% {
        transform: rotate(360deg);
      }
    }
    
    @keyframes dash {
      0% {
        stroke-dasharray: 1, 150;
        stroke-dashoffset: 0;
      }
      50% {
        stroke-dasharray: 90, 150;
        stroke-dashoffset: -35;
      }
      100% {
        stroke-dasharray: 90, 150;
        stroke-dashoffset: -124;
      }
    }
    
    /* Content */
    .jagarnath-button__content {
      display: inline-flex;
      align-items: center;
      justify-content: center;
    }
  `;
}

export default Button;