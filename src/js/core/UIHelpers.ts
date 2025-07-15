/**
 * UI Helpers Utilities
 * 
 * This module provides comprehensive UI manipulation and enhancement utilities.
 * It includes functions for DOM manipulation, notifications, animations,
 * and UI state management.
 * 
 * @example
 * ```typescript
 * import { UIHelpers } from '@jagarnath/core';
 * 
 * const ui = new UIHelpers();
 * ui.showNotification('Success!', 'success');
 * ui.scrollToElement('#target');
 * ```
 */

export type NotificationType = 'success' | 'error' | 'warning' | 'info';

export interface NotificationOptions {
  duration?: number;
  position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left' | 'top-center' | 'bottom-center';
  closable?: boolean;
  autoClose?: boolean;
  className?: string;
}

export interface AnimationOptions {
  duration?: number;
  easing?: string;
  delay?: number;
  onComplete?: () => void;
}

export class UIHelpers {
  /**
   * Comprehensive UI manipulation and enhancement utilities.
   * 
   * This class provides extensive UI capabilities including:
   * - DOM manipulation and element management
   * - Notification system with multiple types
   * - Smooth scrolling and animations
   * - Modal and overlay management
   * - Form enhancement and validation display
   * - Responsive design utilities
   * 
   * @example
   * ```typescript
   * const ui = new UIHelpers();
   * 
   * // Show notification
   * ui.showNotification('Operation successful!', 'success');
   * 
   * // Scroll to element
   * ui.scrollToElement('#target', { duration: 1000 });
   * 
   * // Toggle element visibility
   * ui.toggleElement('#sidebar');
   * ```
   */

  private notificationContainer: HTMLElement | null = null;
  private activeModals: Set<HTMLElement> = new Set();

  constructor() {
    this.initializeNotificationContainer();
  }

  /**
   * Show a notification message.
   * 
   * @param message - The message to display
   * @param type - The type of notification
   * @param options - Additional options for the notification
   * @returns The notification element
   * 
   * @example
   * ```typescript
   * const ui = new UIHelpers();
   * 
   * // Basic notification
   * ui.showNotification('Success!', 'success');
   * 
   * // Custom notification
   * ui.showNotification('Error occurred!', 'error', {
   *   duration: 5000,
   *   position: 'top-center',
   *   closable: true
   * });
   * ```
   */
  showNotification(
    message: string, 
    type: NotificationType = 'info', 
    options: NotificationOptions = {}
  ): HTMLElement {
    const {
      duration = 3000,
      position = 'top-right',
      closable = true,
      autoClose = true,
      className = ''
    } = options;

    const notification = document.createElement('div');
    notification.className = `jagarnath-notification jagarnath-notification-${type} ${className}`;
    notification.innerHTML = `
      <div class="jagarnath-notification-content">
        <span class="jagarnath-notification-message">${this.escapeHtml(message)}</span>
        ${closable ? '<button class="jagarnath-notification-close">&times;</button>' : ''}
      </div>
    `;

    // Add styles
    this.addNotificationStyles();
    
    // Position the notification
    notification.style.cssText = `
      position: fixed;
      z-index: 10000;
      padding: 12px 16px;
      border-radius: 4px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      font-size: 14px;
      line-height: 1.4;
      max-width: 350px;
      word-wrap: break-word;
      transition: all 0.3s ease;
      ${this.getPositionStyles(position)}
    `;

    // Add type-specific styles
    this.addNotificationTypeStyles(notification, type);

    // Add to container
    if (this.notificationContainer) {
      this.notificationContainer.appendChild(notification);
    }

    // Add close functionality
    if (closable) {
      const closeBtn = notification.querySelector('.jagarnath-notification-close');
      if (closeBtn) {
        closeBtn.addEventListener('click', () => this.removeNotification(notification));
      }
    }

    // Auto-close after duration
    if (autoClose && duration > 0) {
      setTimeout(() => {
        this.removeNotification(notification);
      }, duration);
    }

    // Animate in
    requestAnimationFrame(() => {
      notification.style.transform = 'translateX(0)';
      notification.style.opacity = '1';
    });

    return notification;
  }

  /**
   * Remove a notification element.
   * 
   * @param notification - The notification element to remove
   * 
   * @example
   * ```typescript
   * const ui = new UIHelpers();
   * const notification = ui.showNotification('Hello!', 'info');
   * 
   * // Remove after 2 seconds
   * setTimeout(() => {
   *   ui.removeNotification(notification);
   * }, 2000);
   * ```
   */
  removeNotification(notification: HTMLElement): void {
    notification.style.transform = 'translateX(100%)';
    notification.style.opacity = '0';
    
    setTimeout(() => {
      if (notification.parentNode) {
        notification.parentNode.removeChild(notification);
      }
    }, 300);
  }

  /**
   * Scroll to an element smoothly.
   * 
   * @param selector - CSS selector or element to scroll to
   * @param options - Animation options
   * 
   * @example
   * ```typescript
   * const ui = new UIHelpers();
   * 
   * // Scroll to element by selector
   * ui.scrollToElement('#target');
   * 
   * // Scroll with custom options
   * ui.scrollToElement('#section', { duration: 2000, easing: 'ease-in-out' });
   * 
   * // Scroll to element object
   * const element = document.getElementById('target');
   * ui.scrollToElement(element);
   * ```
   */
  scrollToElement(
    selector: string | HTMLElement, 
    options: AnimationOptions = {}
  ): void {
    const element = typeof selector === 'string' 
      ? document.querySelector(selector) as HTMLElement
      : selector;

    if (!element) {
      console.warn(`Element not found: ${selector}`);
      return;
    }

    const { duration = 1000, easing = 'ease-in-out', delay = 0 } = options;

    setTimeout(() => {
      element.scrollIntoView({
        behavior: 'smooth',
        block: 'start',
        inline: 'nearest'
      });
    }, delay);
  }

  /**
   * Toggle element visibility.
   * 
   * @param selector - CSS selector of the element to toggle
   * @param force - Force show/hide (optional)
   * @returns True if element is now visible, false otherwise
   * 
   * @example
   * ```typescript
   * const ui = new UIHelpers();
   * 
   * // Toggle element
   * ui.toggleElement('#sidebar');
   * 
   * // Force show
   * ui.toggleElement('#modal', true);
   * 
   * // Force hide
   * ui.toggleElement('#tooltip', false);
   * ```
   */
  toggleElement(selector: string, force?: boolean): boolean {
    const element = document.querySelector(selector) as HTMLElement;
    
    if (!element) {
      console.warn(`Element not found: ${selector}`);
      return false;
    }

    const isVisible = element.style.display !== 'none' && 
                     element.offsetParent !== null;

    if (force !== undefined) {
      element.style.display = force ? '' : 'none';
      return force;
    } else {
      element.style.display = isVisible ? 'none' : '';
      return !isVisible;
    }
  }

  /**
   * Create and show a modal dialog.
   * 
   * @param content - HTML content for the modal
   * @param options - Modal options
   * @returns The modal element
   * 
   * @example
   * ```typescript
   * const ui = new UIHelpers();
   * 
   * const modal = ui.showModal(`
   *   <h2>Confirm Action</h2>
   *   <p>Are you sure you want to proceed?</p>
   *   <button onclick="confirm()">Yes</button>
   *   <button onclick="cancel()">No</button>
   * `, {
   *   closable: true,
   *   backdrop: true
   * });
   * ```
   */
  showModal(
    content: string, 
    options: {
      closable?: boolean;
      backdrop?: boolean;
      className?: string;
      onClose?: () => void;
    } = {}
  ): HTMLElement {
    const {
      closable = true,
      backdrop = true,
      className = '',
      onClose
    } = options;

    // Create modal container
    const modal = document.createElement('div');
    modal.className = `jagarnath-modal ${className}`;
    modal.innerHTML = `
      ${backdrop ? '<div class="jagarnath-modal-backdrop"></div>' : ''}
      <div class="jagarnath-modal-content">
        ${closable ? '<button class="jagarnath-modal-close">&times;</button>' : ''}
        <div class="jagarnath-modal-body">${content}</div>
      </div>
    `;

    // Add styles
    this.addModalStyles();

    // Add to document
    document.body.appendChild(modal);
    this.activeModals.add(modal);

    // Add event listeners
    if (closable) {
      const closeBtn = modal.querySelector('.jagarnath-modal-close');
      if (closeBtn) {
        closeBtn.addEventListener('click', () => this.closeModal(modal, onClose));
      }
    }

    if (backdrop) {
      const backdropEl = modal.querySelector('.jagarnath-modal-backdrop');
      if (backdropEl) {
        backdropEl.addEventListener('click', () => this.closeModal(modal, onClose));
      }
    }

    // Prevent body scroll
    document.body.style.overflow = 'hidden';

    // Animate in
    requestAnimationFrame(() => {
      modal.style.opacity = '1';
      const contentEl = modal.querySelector('.jagarnath-modal-content');
      if (contentEl) {
        contentEl.style.transform = 'scale(1)';
      }
    });

    return modal;
  }

  /**
   * Close a modal dialog.
   * 
   * @param modal - The modal element to close
   * @param onClose - Callback function to execute on close
   * 
   * @example
   * ```typescript
   * const ui = new UIHelpers();
   * const modal = ui.showModal('Content');
   * 
   * // Close with callback
   * ui.closeModal(modal, () => {
   *   console.log('Modal closed');
   * });
   * ```
   */
  closeModal(modal: HTMLElement, onClose?: () => void): void {
    modal.style.opacity = '0';
    const contentEl = modal.querySelector('.jagarnath-modal-content');
    if (contentEl) {
      contentEl.style.transform = 'scale(0.8)';
    }

    setTimeout(() => {
      if (modal.parentNode) {
        modal.parentNode.removeChild(modal);
      }
      this.activeModals.delete(modal);

      // Restore body scroll if no more modals
      if (this.activeModals.size === 0) {
        document.body.style.overflow = '';
      }

      if (onClose) {
        onClose();
      }
    }, 300);
  }

  /**
   * Add loading spinner to an element.
   * 
   * @param selector - CSS selector of the element to add spinner to
   * @param text - Loading text (optional)
   * @returns The spinner element
   * 
   * @example
   * ```typescript
   * const ui = new UIHelpers();
   * 
   * // Add spinner to button
   * const spinner = ui.addSpinner('#submit-btn', 'Loading...');
   * 
   * // Remove spinner after operation
   * setTimeout(() => {
   *   ui.removeSpinner(spinner);
   * }, 2000);
   * ```
   */
  addSpinner(selector: string, text?: string): HTMLElement {
    const element = document.querySelector(selector) as HTMLElement;
    
    if (!element) {
      console.warn(`Element not found: ${selector}`);
      return document.createElement('div');
    }

    const spinner = document.createElement('div');
    spinner.className = 'jagarnath-spinner';
    spinner.innerHTML = `
      <div class="jagarnath-spinner-icon"></div>
      ${text ? `<div class="jagarnath-spinner-text">${text}</div>` : ''}
    `;

    // Store original content
    const originalContent = element.innerHTML;
    element.setAttribute('data-original-content', originalContent);

    // Add spinner
    element.innerHTML = '';
    element.appendChild(spinner);
    element.style.position = 'relative';

    // Add styles
    this.addSpinnerStyles();

    return spinner;
  }

  /**
   * Remove loading spinner from an element.
   * 
   * @param spinner - The spinner element to remove
   * 
   * @example
   * ```typescript
   * const ui = new UIHelpers();
   * const spinner = ui.addSpinner('#button');
   * 
   * // Remove spinner
   * ui.removeSpinner(spinner);
   * ```
   */
  removeSpinner(spinner: HTMLElement): void {
    const parent = spinner.parentElement;
    if (parent) {
      const originalContent = parent.getAttribute('data-original-content');
      if (originalContent) {
        parent.innerHTML = originalContent;
        parent.removeAttribute('data-original-content');
      }
    }
  }

  /**
   * Animate an element with CSS transitions.
   * 
   * @param selector - CSS selector of the element to animate
   * @param properties - CSS properties to animate
   * @param options - Animation options
   * 
   * @example
   * ```typescript
   * const ui = new UIHelpers();
   * 
   * // Fade in
   * ui.animate('#element', { opacity: 1 }, { duration: 500 });
   * 
   * // Slide down
   * ui.animate('#element', { height: '200px' }, { duration: 300 });
   * 
   * // Complex animation
   * ui.animate('#element', {
   *   transform: 'translateX(100px) rotate(45deg)',
   *   opacity: 0.8
   * }, {
   *   duration: 1000,
   *   easing: 'ease-in-out',
   *   onComplete: () => console.log('Animation complete')
   * });
   * ```
   */
  animate(
    selector: string,
    properties: Record<string, string | number>,
    options: AnimationOptions = {}
  ): void {
    const element = document.querySelector(selector) as HTMLElement;
    
    if (!element) {
      console.warn(`Element not found: ${selector}`);
      return;
    }

    const { duration = 300, easing = 'ease', delay = 0, onComplete } = options;

    // Set transition
    element.style.transition = `all ${duration}ms ${easing}`;

    // Apply delay
    if (delay > 0) {
      element.style.transitionDelay = `${delay}ms`;
    }

    // Apply properties
    Object.entries(properties).forEach(([property, value]) => {
      element.style[property as any] = String(value);
    });

    // Handle completion
    if (onComplete) {
      setTimeout(onComplete, duration + delay);
    }
  }

  /**
   * Debounce a function call.
   * 
   * @param func - Function to debounce
   * @param delay - Delay in milliseconds
   * @returns Debounced function
   * 
   * @example
   * ```typescript
   * const ui = new UIHelpers();
   * 
   * const debouncedSearch = ui.debounce((query: string) => {
   *   // Perform search
   *   console.log('Searching for:', query);
   * }, 300);
   * 
   * // Use in input event
   * input.addEventListener('input', (e) => {
   *   debouncedSearch(e.target.value);
   * });
   * ```
   */
  debounce<T extends (...args: any[]) => any>(
    func: T, 
    delay: number
  ): (...args: Parameters<T>) => void {
    let timeoutId: NodeJS.Timeout;
    
    return (...args: Parameters<T>) => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => func(...args), delay);
    };
  }

  /**
   * Throttle a function call.
   * 
   * @param func - Function to throttle
   * @param delay - Delay in milliseconds
   * @returns Throttled function
   * 
   * @example
   * ```typescript
   * const ui = new UIHelpers();
   * 
   * const throttledScroll = ui.throttle(() => {
   *   // Handle scroll event
   *   console.log('Scroll position:', window.scrollY);
   * }, 100);
   * 
   * window.addEventListener('scroll', throttledScroll);
   * ```
   */
  throttle<T extends (...args: any[]) => any>(
    func: T, 
    delay: number
  ): (...args: Parameters<T>) => void {
    let lastCall = 0;
    
    return (...args: Parameters<T>) => {
      const now = Date.now();
      if (now - lastCall >= delay) {
        lastCall = now;
        func(...args);
      }
    };
  }

  // Private helper methods

  private initializeNotificationContainer(): void {
    this.notificationContainer = document.createElement('div');
    this.notificationContainer.className = 'jagarnath-notification-container';
    this.notificationContainer.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 10000;
      pointer-events: none;
    `;
    document.body.appendChild(this.notificationContainer);
  }

  private addNotificationStyles(): void {
    if (document.getElementById('jagarnath-notification-styles')) {
      return;
    }

    const style = document.createElement('style');
    style.id = 'jagarnath-notification-styles';
    style.textContent = `
      .jagarnath-notification {
        transform: translateX(100%);
        opacity: 0;
        margin-bottom: 10px;
        pointer-events: auto;
      }
      
      .jagarnath-notification-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
      }
      
      .jagarnath-notification-close {
        background: none;
        border: none;
        font-size: 18px;
        cursor: pointer;
        margin-left: 10px;
        opacity: 0.7;
      }
      
      .jagarnath-notification-close:hover {
        opacity: 1;
      }
    `;
    document.head.appendChild(style);
  }

  private addNotificationTypeStyles(notification: HTMLElement, type: NotificationType): void {
    const colors = {
      success: '#52c41a',
      error: '#ff4d4f',
      warning: '#faad14',
      info: '#1890ff'
    };

    notification.style.backgroundColor = colors[type];
    notification.style.color = 'white';
  }

  private addModalStyles(): void {
    if (document.getElementById('jagarnath-modal-styles')) {
      return;
    }

    const style = document.createElement('style');
    style.id = 'jagarnath-modal-styles';
    style.textContent = `
      .jagarnath-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 10000;
        opacity: 0;
        transition: opacity 0.3s ease;
      }
      
      .jagarnath-modal-backdrop {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
      }
      
      .jagarnath-modal-content {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) scale(0.8);
        background: white;
        border-radius: 8px;
        padding: 20px;
        max-width: 90%;
        max-height: 90%;
        overflow: auto;
        transition: transform 0.3s ease;
      }
      
      .jagarnath-modal-close {
        position: absolute;
        top: 10px;
        right: 10px;
        background: none;
        border: none;
        font-size: 24px;
        cursor: pointer;
        opacity: 0.7;
      }
      
      .jagarnath-modal-close:hover {
        opacity: 1;
      }
    `;
    document.head.appendChild(style);
  }

  private addSpinnerStyles(): void {
    if (document.getElementById('jagarnath-spinner-styles')) {
      return;
    }

    const style = document.createElement('style');
    style.id = 'jagarnath-spinner-styles';
    style.textContent = `
      .jagarnath-spinner {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px;
      }
      
      .jagarnath-spinner-icon {
        width: 20px;
        height: 20px;
        border: 2px solid #f3f3f3;
        border-top: 2px solid #3498db;
        border-radius: 50%;
        animation: spin 1s linear infinite;
      }
      
      .jagarnath-spinner-text {
        margin-top: 10px;
        font-size: 14px;
        color: #666;
      }
      
      @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
    `;
    document.head.appendChild(style);
  }

  private getPositionStyles(position: string): string {
    const positions = {
      'top-right': 'top: 20px; right: 20px;',
      'top-left': 'top: 20px; left: 20px;',
      'bottom-right': 'bottom: 20px; right: 20px;',
      'bottom-left': 'bottom: 20px; left: 20px;',
      'top-center': 'top: 20px; left: 50%; transform: translateX(-50%);',
      'bottom-center': 'bottom: 20px; left: 50%; transform: translateX(-50%);'
    };

    return positions[position as keyof typeof positions] || positions['top-right'];
  }

  private escapeHtml(text: string): string {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}