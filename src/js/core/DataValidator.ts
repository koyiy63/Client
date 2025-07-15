/**
 * Data Validation Utilities
 * 
 * This module provides comprehensive data validation utilities for form validation,
 * data type checking, and input sanitization. It includes functions for validating
 * various data types including emails, phone numbers, URLs, and custom patterns.
 * 
 * @example
 * ```typescript
 * import { DataValidator } from '@jagarnath/core';
 * 
 * const validator = new DataValidator();
 * const isValid = validator.validateEmail('user@example.com');
 * const errors = validator.validateForm(formData);
 * ```
 */

export interface ValidationRule {
  required?: boolean;
  minLength?: number;
  maxLength?: number;
  pattern?: RegExp;
  custom?: (value: any) => boolean | string;
  message?: string;
}

export interface ValidationResult {
  isValid: boolean;
  errors: string[];
  value: any;
}

export interface FormValidationResult {
  isValid: boolean;
  errors: Record<string, string[]>;
  validFields: string[];
  invalidFields: string[];
}

export class DataValidator {
  /**
   * Comprehensive data validation utilities.
   * 
   * This class provides extensive validation capabilities including:
   * - Email, phone, and URL validation
   * - Form validation with custom rules
   * - Data type checking and sanitization
   * - Custom validation patterns
   * - Error message customization
   * 
   * @example
   * ```typescript
   * const validator = new DataValidator();
   * 
   * // Validate email
   * const isValid = validator.validateEmail('user@example.com');
   * 
   * // Validate form
   * const formData = { email: 'user@example.com', password: '123456' };
   * const rules = {
   *   email: { required: true, pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/ },
   *   password: { required: true, minLength: 6 }
   * };
   * const result = validator.validateForm(formData, rules);
   * ```
   */
  
  private defaultMessages = {
    required: 'This field is required',
    email: 'Please enter a valid email address',
    phone: 'Please enter a valid phone number',
    url: 'Please enter a valid URL',
    minLength: 'Minimum length is {min} characters',
    maxLength: 'Maximum length is {max} characters',
    pattern: 'Please match the requested format'
  };

  constructor() {}

  /**
   * Validate an email address.
   * 
   * @param email - The email address to validate
   * @returns True if the email is valid, false otherwise
   * 
   * @example
   * ```typescript
   * const validator = new DataValidator();
   * const isValid = validator.validateEmail('user@example.com');
   * console.log(isValid); // true
   * 
   * const isInvalid = validator.validateEmail('invalid-email');
   * console.log(isInvalid); // false
   * ```
   */
  validateEmail(email: string): boolean {
    if (!email || typeof email !== 'string') {
      return false;
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email.trim());
  }

  /**
   * Validate a phone number.
   * 
   * @param phone - The phone number to validate
   * @param country - Country code for validation (default: 'US')
   * @returns True if the phone number is valid, false otherwise
   * 
   * @example
   * ```typescript
   * const validator = new DataValidator();
   * const isValid = validator.validatePhone('+1-555-123-4567');
   * console.log(isValid); // true
   * 
   * const isInvalid = validator.validatePhone('123');
   * console.log(isInvalid); // false
   * ```
   */
  validatePhone(phone: string, country: string = 'US'): boolean {
    if (!phone || typeof phone !== 'string') {
      return false;
    }

    // Remove all non-digit characters
    const digits = phone.replace(/\D/g, '');

    // Basic validation for different countries
    switch (country.toUpperCase()) {
      case 'US':
        return digits.length === 10 || digits.length === 11;
      case 'UK':
        return digits.length >= 10 && digits.length <= 11;
      default:
        return digits.length >= 7 && digits.length <= 15;
    }
  }

  /**
   * Validate a URL.
   * 
   * @param url - The URL to validate
   * @param protocols - Allowed protocols (default: ['http', 'https'])
   * @returns True if the URL is valid, false otherwise
   * 
   * @example
   * ```typescript
   * const validator = new DataValidator();
   * const isValid = validator.validateUrl('https://example.com');
   * console.log(isValid); // true
   * 
   * const isInvalid = validator.validateUrl('not-a-url');
   * console.log(isInvalid); // false
   * ```
   */
  validateUrl(url: string, protocols: string[] = ['http', 'https']): boolean {
    if (!url || typeof url !== 'string') {
      return false;
    }

    try {
      const urlObj = new URL(url);
      return protocols.includes(urlObj.protocol.replace(':', ''));
    } catch {
      return false;
    }
  }

  /**
   * Validate a value against a custom pattern.
   * 
   * @param value - The value to validate
   * @param pattern - Regular expression pattern
   * @returns True if the value matches the pattern, false otherwise
   * 
   * @example
   * ```typescript
   * const validator = new DataValidator();
   * const isValid = validator.validatePattern('ABC123', /^[A-Z]{3}\d{3}$/);
   * console.log(isValid); // true
   * 
   * const isInvalid = validator.validatePattern('123ABC', /^[A-Z]{3}\d{3}$/);
   * console.log(isInvalid); // false
   * ```
   */
  validatePattern(value: any, pattern: RegExp): boolean {
    if (value === null || value === undefined) {
      return false;
    }

    return pattern.test(String(value));
  }

  /**
   * Validate a value against multiple rules.
   * 
   * @param value - The value to validate
   * @param rules - Validation rules to apply
   * @returns Validation result with errors
   * 
   * @example
   * ```typescript
   * const validator = new DataValidator();
   * const rules = {
   *   required: true,
   *   minLength: 3,
   *   maxLength: 10,
   *   pattern: /^[a-zA-Z]+$/
   * };
   * 
   * const result = validator.validateValue('ab', rules);
   * console.log(result.isValid); // false
   * console.log(result.errors); // ['Minimum length is 3 characters']
   * ```
   */
  validateValue(value: any, rules: ValidationRule): ValidationResult {
    const errors: string[] = [];

    // Check if required
    if (rules.required && (value === null || value === undefined || value === '')) {
      errors.push(rules.message || this.defaultMessages.required);
      return { isValid: false, errors, value };
    }

    // Skip other validations if value is empty and not required
    if (value === null || value === undefined || value === '') {
      return { isValid: true, errors: [], value };
    }

    const stringValue = String(value);

    // Check minimum length
    if (rules.minLength && stringValue.length < rules.minLength) {
      const message = (rules.message || this.defaultMessages.minLength)
        .replace('{min}', rules.minLength.toString());
      errors.push(message);
    }

    // Check maximum length
    if (rules.maxLength && stringValue.length > rules.maxLength) {
      const message = (rules.message || this.defaultMessages.maxLength)
        .replace('{max}', rules.maxLength.toString());
      errors.push(message);
    }

    // Check pattern
    if (rules.pattern && !rules.pattern.test(stringValue)) {
      errors.push(rules.message || this.defaultMessages.pattern);
    }

    // Check custom validation
    if (rules.custom) {
      const customResult = rules.custom(value);
      if (customResult !== true) {
        errors.push(typeof customResult === 'string' ? customResult : 'Invalid value');
      }
    }

    return {
      isValid: errors.length === 0,
      errors,
      value
    };
  }

  /**
   * Validate a form object against validation rules.
   * 
   * @param formData - Object containing form data
   * @param rules - Object containing validation rules for each field
   * @returns Form validation result with field-specific errors
   * 
   * @example
   * ```typescript
   * const validator = new DataValidator();
   * 
   * const formData = {
   *   email: 'user@example.com',
   *   password: '123',
   *   confirmPassword: '123'
   * };
   * 
   * const rules = {
   *   email: { required: true, pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/ },
   *   password: { required: true, minLength: 6 },
   *   confirmPassword: { 
   *     required: true, 
   *     custom: (value) => value === formData.password || 'Passwords do not match'
   *   }
   * };
   * 
   * const result = validator.validateForm(formData, rules);
   * console.log(result.isValid); // false
   * console.log(result.errors); // { password: ['Minimum length is 6 characters'] }
   * ```
   */
  validateForm(
    formData: Record<string, any>, 
    rules: Record<string, ValidationRule>
  ): FormValidationResult {
    const errors: Record<string, string[]> = {};
    const validFields: string[] = [];
    const invalidFields: string[] = [];

    for (const [fieldName, fieldRules] of Object.entries(rules)) {
      const fieldValue = formData[fieldName];
      const validation = this.validateValue(fieldValue, fieldRules);

      if (validation.isValid) {
        validFields.push(fieldName);
      } else {
        invalidFields.push(fieldName);
        errors[fieldName] = validation.errors;
      }
    }

    return {
      isValid: invalidFields.length === 0,
      errors,
      validFields,
      invalidFields
    };
  }

  /**
   * Sanitize input data to prevent XSS attacks.
   * 
   * @param input - The input string to sanitize
   * @returns Sanitized string
   * 
   * @example
   * ```typescript
   * const validator = new DataValidator();
   * const sanitized = validator.sanitizeInput('<script>alert("xss")</script>');
   * console.log(sanitized); // '&lt;script&gt;alert("xss")&lt;/script&gt;'
   * ```
   */
  sanitizeInput(input: string): string {
    if (typeof input !== 'string') {
      return String(input);
    }

    return input
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#x27;')
      .replace(/\//g, '&#x2F;');
  }

  /**
   * Validate and sanitize an object recursively.
   * 
   * @param obj - The object to validate and sanitize
   * @param rules - Validation rules for object properties
   * @returns Object with validation results and sanitized values
   * 
   * @example
   * ```typescript
   * const validator = new DataValidator();
   * 
   * const data = {
   *   name: '<script>alert("xss")</script>',
   *   email: 'user@example.com'
   * };
   * 
   * const rules = {
   *   name: { required: true, maxLength: 50 },
   *   email: { required: true, pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/ }
   * };
   * 
   * const result = validator.validateAndSanitize(data, rules);
   * console.log(result.sanitized.name); // '&lt;script&gt;alert("xss")&lt;/script&gt;'
   * ```
   */
  validateAndSanitize(
    obj: Record<string, any>,
    rules: Record<string, ValidationRule>
  ): {
    isValid: boolean;
    errors: Record<string, string[]>;
    sanitized: Record<string, any>;
  } {
    const validation = this.validateForm(obj, rules);
    const sanitized: Record<string, any> = {};

    for (const [key, value] of Object.entries(obj)) {
      if (typeof value === 'string') {
        sanitized[key] = this.sanitizeInput(value);
      } else {
        sanitized[key] = value;
      }
    }

    return {
      isValid: validation.isValid,
      errors: validation.errors,
      sanitized
    };
  }

  /**
   * Check if a value is a valid number.
   * 
   * @param value - The value to check
   * @param options - Validation options
   * @returns True if the value is a valid number, false otherwise
   * 
   * @example
   * ```typescript
   * const validator = new DataValidator();
   * const isValid = validator.isNumber('123.45');
   * console.log(isValid); // true
   * 
   * const isInvalid = validator.isNumber('not-a-number');
   * console.log(isInvalid); // false
   * ```
   */
  isNumber(
    value: any, 
    options: { min?: number; max?: number; integer?: boolean } = {}
  ): boolean {
    const num = Number(value);
    
    if (isNaN(num)) {
      return false;
    }

    if (options.integer && !Number.isInteger(num)) {
      return false;
    }

    if (options.min !== undefined && num < options.min) {
      return false;
    }

    if (options.max !== undefined && num > options.max) {
      return false;
    }

    return true;
  }

  /**
   * Check if a value is a valid date.
   * 
   * @param value - The value to check
   * @param options - Validation options
   * @returns True if the value is a valid date, false otherwise
   * 
   * @example
   * ```typescript
   * const validator = new DataValidator();
   * const isValid = validator.isDate('2023-12-25');
   * console.log(isValid); // true
   * 
   * const isInvalid = validator.isDate('invalid-date');
   * console.log(isInvalid); // false
   * ```
   */
  isDate(
    value: any,
    options: { min?: Date; max?: Date; future?: boolean; past?: boolean } = {}
  ): boolean {
    const date = new Date(value);
    
    if (isNaN(date.getTime())) {
      return false;
    }

    const now = new Date();

    if (options.future && date <= now) {
      return false;
    }

    if (options.past && date >= now) {
      return false;
    }

    if (options.min && date < options.min) {
      return false;
    }

    if (options.max && date > options.max) {
      return false;
    }

    return true;
  }

  /**
   * Check if a value is empty (null, undefined, empty string, or empty array).
   * 
   * @param value - The value to check
   * @returns True if the value is empty, false otherwise
   * 
   * @example
   * ```typescript
   * const validator = new DataValidator();
   * console.log(validator.isEmpty('')); // true
   * console.log(validator.isEmpty(null)); // true
   * console.log(validator.isEmpty([])); // true
   * console.log(validator.isEmpty('hello')); // false
   * ```
   */
  isEmpty(value: any): boolean {
    if (value === null || value === undefined) {
      return true;
    }

    if (typeof value === 'string') {
      return value.trim() === '';
    }

    if (Array.isArray(value)) {
      return value.length === 0;
    }

    if (typeof value === 'object') {
      return Object.keys(value).length === 0;
    }

    return false;
  }
}