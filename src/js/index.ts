/**
 * Jagarnath JavaScript/TypeScript API Package
 * 
 * A comprehensive library providing frontend utilities, data validation,
 * UI helpers, and network utilities.
 * 
 * @version 1.0.0
 * @author Jagarnath Team
 */

// Core utilities
export { DataValidator } from './core/DataValidator';
export { UIHelpers } from './core/UIHelpers';
export { StorageUtils } from './core/StorageUtils';
export { NetworkUtils } from './core/NetworkUtils';

// React components
export { Button } from './components/react/Button';
export { Modal } from './components/react/Modal';
export { Form } from './components/react/Form';
export { Table } from './components/react/Table';

// Vue components
export { default as DataTable } from '../components/vue/DataTable.vue';
export { VButton } from './components/vue/VButton';
export { VModal } from './components/vue/VModal';
export { VForm } from './components/vue/VForm';
export { VTable } from './components/vue/VTable';

// Types
export * from './types';

// Constants
export const VERSION = '1.0.0';
export const AUTHOR = 'Jagarnath Team';