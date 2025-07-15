<template>
  <div class="data-table-container">
    <!-- Search and Filter Controls -->
    <div class="table-controls" v-if="showControls">
      <div class="search-box">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search..."
          class="search-input"
          @input="handleSearch"
        />
        <button @click="clearSearch" class="clear-btn">Clear</button>
      </div>
      
      <div class="filter-controls" v-if="filters.length">
        <select v-model="selectedFilter" class="filter-select">
          <option value="">All Columns</option>
          <option v-for="filter in filters" :key="filter.key" :value="filter.key">
            {{ filter.label }}
          </option>
        </select>
      </div>
    </div>

    <!-- Table -->
    <div class="table-wrapper">
      <table class="data-table" :class="tableClass">
        <thead>
          <tr>
            <th
              v-for="column in visibleColumns"
              :key="column.key"
              @click="handleSort(column.key)"
              :class="{ sortable: column.sortable !== false }"
            >
              <div class="th-content">
                <span>{{ column.label }}</span>
                <span v-if="column.sortable !== false" class="sort-icon">
                  {{ getSortIcon(column.key) }}
                </span>
              </div>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(row, index) in paginatedData"
            :key="getRowKey(row, index)"
            :class="getRowClass(row, index)"
            @click="handleRowClick(row, index)"
          >
            <td
              v-for="column in visibleColumns"
              :key="column.key"
              :class="getCellClass(column, row)"
            >
              <slot
                :name="`cell-${column.key}`"
                :row="row"
                :column="column"
                :value="getCellValue(row, column)"
              >
                {{ formatCellValue(getCellValue(row, column), column) }}
              </slot>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div class="pagination" v-if="showPagination && totalPages > 1">
      <div class="pagination-info">
        Showing {{ startIndex + 1 }} to {{ endIndex }} of {{ filteredData.length }} entries
      </div>
      
      <div class="pagination-controls">
        <button
          @click="goToPage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="pagination-btn"
        >
          Previous
        </button>
        
        <button
          v-for="page in visiblePages"
          :key="page"
          @click="goToPage(page)"
          :class="['pagination-btn', { active: page === currentPage }]"
        >
          {{ page }}
        </button>
        
        <button
          @click="goToPage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="pagination-btn"
        >
          Next
        </button>
      </div>
      
      <div class="page-size-control">
        <label>Show:</label>
        <select v-model="pageSize" @change="handlePageSizeChange">
          <option v-for="size in pageSizeOptions" :key="size" :value="size">
            {{ size }}
          </option>
        </select>
        <span>entries</span>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="filteredData.length === 0" class="empty-state">
      <slot name="empty">
        <div class="empty-content">
          <div class="empty-icon">📊</div>
          <h3>No data available</h3>
          <p>{{ searchQuery ? 'No results match your search criteria.' : 'No data has been loaded yet.' }}</p>
        </div>
      </slot>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, watch, PropType } from 'vue'

export interface DataTableColumn {
  key: string
  label: string
  sortable?: boolean
  filterable?: boolean
  width?: string
  align?: 'left' | 'center' | 'right'
  formatter?: (value: any, row: any) => string
}

export interface DataTableFilter {
  key: string
  label: string
  type: 'text' | 'select' | 'date' | 'number'
  options?: Array<{ value: any; label: string }>
}

export default defineComponent({
  name: 'DataTable',
  props: {
    data: {
      type: Array as PropType<any[]>,
      required: true,
      default: () => []
    },
    columns: {
      type: Array as PropType<DataTableColumn[]>,
      required: true
    },
    filters: {
      type: Array as PropType<DataTableFilter[]>,
      default: () => []
    },
    pageSize: {
      type: Number,
      default: 10
    },
    pageSizeOptions: {
      type: Array as PropType<number[]>,
      default: () => [10, 25, 50, 100]
    },
    showPagination: {
      type: Boolean,
      default: true
    },
    showControls: {
      type: Boolean,
      default: true
    },
    sortable: {
      type: Boolean,
      default: true
    },
    searchable: {
      type: Boolean,
      default: true
    },
    rowKey: {
      type: String,
      default: 'id'
    },
    tableClass: {
      type: String,
      default: ''
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  emits: ['row-click', 'sort-change', 'page-change', 'search-change'],
  setup(props, { emit }) {
    // Reactive state
    const currentPage = ref(1)
    const searchQuery = ref('')
    const selectedFilter = ref('')
    const sortColumn = ref('')
    const sortDirection = ref<'asc' | 'desc'>('asc')
    const pageSize = ref(props.pageSize)

    // Computed properties
    const filteredData = computed(() => {
      let filtered = [...props.data]

      // Apply search filter
      if (searchQuery.value && props.searchable) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(row => {
          return Object.values(row).some(value =>
            String(value).toLowerCase().includes(query)
          )
        })
      }

      // Apply column filter
      if (selectedFilter.value) {
        filtered = filtered.filter(row => {
          const value = row[selectedFilter.value]
          return value !== null && value !== undefined && value !== ''
        })
      }

      return filtered
    })

    const sortedData = computed(() => {
      if (!sortColumn.value || !props.sortable) {
        return filteredData.value
      }

      return [...filteredData.value].sort((a, b) => {
        const aVal = a[sortColumn.value]
        const bVal = b[sortColumn.value]

        if (aVal === bVal) return 0
        if (aVal === null || aVal === undefined) return 1
        if (bVal === null || bVal === undefined) return -1

        const comparison = aVal < bVal ? -1 : 1
        return sortDirection.value === 'asc' ? comparison : -comparison
      })
    })

    const totalPages = computed(() => {
      return Math.ceil(sortedData.value.length / pageSize.value)
    })

    const startIndex = computed(() => {
      return (currentPage.value - 1) * pageSize.value
    })

    const endIndex = computed(() => {
      return Math.min(startIndex.value + pageSize.value, sortedData.value.length)
    })

    const paginatedData = computed(() => {
      return sortedData.value.slice(startIndex.value, endIndex.value)
    })

    const visibleColumns = computed(() => {
      return props.columns.filter(col => col.key !== 'actions' || props.showActions)
    })

    const visiblePages = computed(() => {
      const pages = []
      const maxVisible = 5
      let start = Math.max(1, currentPage.value - Math.floor(maxVisible / 2))
      let end = Math.min(totalPages.value, start + maxVisible - 1)

      if (end - start + 1 < maxVisible) {
        start = Math.max(1, end - maxVisible + 1)
      }

      for (let i = start; i <= end; i++) {
        pages.push(i)
      }

      return pages
    })

    // Methods
    const handleSort = (columnKey: string) => {
      if (!props.sortable) return

      if (sortColumn.value === columnKey) {
        sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
      } else {
        sortColumn.value = columnKey
        sortDirection.value = 'asc'
      }

      emit('sort-change', { column: columnKey, direction: sortDirection.value })
    }

    const handleSearch = () => {
      currentPage.value = 1
      emit('search-change', searchQuery.value)
    }

    const clearSearch = () => {
      searchQuery.value = ''
      selectedFilter.value = ''
      currentPage.value = 1
      emit('search-change', '')
    }

    const goToPage = (page: number) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
        emit('page-change', page)
      }
    }

    const handlePageSizeChange = () => {
      currentPage.value = 1
    }

    const handleRowClick = (row: any, index: number) => {
      emit('row-click', { row, index, originalIndex: startIndex.value + index })
    }

    const getRowKey = (row: any, index: number) => {
      return row[props.rowKey] || index
    }

    const getRowClass = (row: any, index: number) => {
      return {
        'table-row': true,
        'clickable': true,
        'even': (startIndex.value + index) % 2 === 0
      }
    }

    const getCellClass = (column: DataTableColumn, row: any) => {
      return {
        [`align-${column.align || 'left'}`]: true,
        [`column-${column.key}`]: true
      }
    }

    const getCellValue = (row: any, column: DataTableColumn) => {
      return row[column.key]
    }

    const formatCellValue = (value: any, column: DataTableColumn) => {
      if (column.formatter) {
        return column.formatter(value, row)
      }
      return value
    }

    const getSortIcon = (columnKey: string) => {
      if (sortColumn.value !== columnKey) {
        return '↕️'
      }
      return sortDirection.value === 'asc' ? '↑' : '↓'
    }

    // Watchers
    watch(() => props.data, () => {
      currentPage.value = 1
    })

    return {
      currentPage,
      searchQuery,
      selectedFilter,
      sortColumn,
      sortDirection,
      pageSize,
      filteredData,
      sortedData,
      totalPages,
      startIndex,
      endIndex,
      paginatedData,
      visibleColumns,
      visiblePages,
      handleSort,
      handleSearch,
      clearSearch,
      goToPage,
      handlePageSizeChange,
      handleRowClick,
      getRowKey,
      getRowClass,
      getCellClass,
      getCellValue,
      formatCellValue,
      getSortIcon
    }
  }
})
</script>

<style scoped>
.data-table-container {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.table-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  gap: 1rem;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.search-input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 200px;
}

.clear-btn {
  padding: 0.5rem 1rem;
  background: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}

.filter-select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.table-wrapper {
  overflow-x: auto;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

.data-table th {
  background: #f8f9fa;
  padding: 0.75rem;
  text-align: left;
  font-weight: 600;
  border-bottom: 2px solid #dee2e6;
}

.data-table th.sortable {
  cursor: pointer;
  user-select: none;
}

.data-table th.sortable:hover {
  background: #e9ecef;
}

.th-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sort-icon {
  font-size: 0.8rem;
  opacity: 0.7;
}

.data-table td {
  padding: 0.75rem;
  border-bottom: 1px solid #dee2e6;
}

.data-table tr:hover {
  background: #f8f9fa;
}

.data-table tr.clickable {
  cursor: pointer;
}

.data-table tr.even {
  background: #fafafa;
}

.align-left { text-align: left; }
.align-center { text-align: center; }
.align-right { text-align: right; }

.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  padding: 1rem 0;
}

.pagination-info {
  color: #6c757d;
  font-size: 0.9rem;
}

.pagination-controls {
  display: flex;
  gap: 0.25rem;
}

.pagination-btn {
  padding: 0.5rem 0.75rem;
  border: 1px solid #ddd;
  background: white;
  cursor: pointer;
  border-radius: 4px;
}

.pagination-btn:hover:not(:disabled) {
  background: #f8f9fa;
}

.pagination-btn.active {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-size-control {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.page-size-control select {
  padding: 0.25rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #6c757d;
}

.empty-content {
  max-width: 300px;
  margin: 0 auto;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.empty-content h3 {
  margin: 0 0 0.5rem 0;
  color: #495057;
}

.empty-content p {
  margin: 0;
  font-size: 0.9rem;
}
</style>