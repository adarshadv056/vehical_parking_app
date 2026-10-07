<script>
import AppButton from './Button.vue';
import AppSelect from './Select.vue';
import AppEmptyState from './EmptyState.vue';
import AppLoadingState from './LoadingState.vue';

export default {
  name: 'AppDataTable',
  components: { AppButton, AppSelect, AppEmptyState, AppLoadingState },
  inheritAttrs: false,
  props: {
    columns: {
      type: Array,
      required: true
      // { key, label, sortable, render, width, align }
    },
    items: {
      type: Array,
      default: () => []
    },
    loading: Boolean,
    emptyMessage: { type: String, default: 'No data available' },
    emptyIcon: { type: String, default: 'InboxIcon' },
    selectable: Boolean,
    selectedItems: { type: Array, default: () => [] },
    showPagination: { type: Boolean, default: true },
    pageSize: { type: Number, default: 10 },
    pageSizes: { type: Array, default: () => [10, 25, 50, 100] },
    sortBy: String,
    sortDir: { type: String, default: 'asc', validator: (v) => ['asc', 'desc'].includes(v) }
  },
  emits: ['update:sortBy', 'update:sortDir', 'update:pageSize', 'update:selectedItems', 'row-click'],
  data() {
    return {
      currentPage: 1,
      localSortBy: this.sortBy,
      localSortDir: this.sortDir,
      localPageSize: this.pageSize,
      localSelectedItems: this.selectedItems
    };
  },
  watch: {
    sortBy(val) { this.localSortBy = val; },
    sortDir(val) { this.localSortDir = val; },
    pageSize(val) { this.localPageSize = val; },
    selectedItems(val) { this.localSelectedItems = val; }
  },
  computed: {
    sortedItems() {
      if (!this.localSortBy) return this.items;
      return [...this.items].sort((a, b) => {
        const aVal = a[this.localSortBy];
        const bVal = b[this.localSortBy];
        if (aVal === bVal) return 0;
        const dir = this.localSortDir === 'asc' ? 1 : -1;
        return aVal > bVal ? dir : -dir;
      });
    },
    paginatedItems() {
      if (!this.showPagination) return this.sortedItems;
      const start = (this.currentPage - 1) * this.localPageSize;
      return this.sortedItems.slice(start, start + this.localPageSize);
    },
    totalPages() {
      return Math.ceil(this.sortedItems.length / this.localPageSize) || 1;
    },
    visiblePages() {
      const total = this.totalPages;
      const current = this.currentPage;
      if (total <= 5) {
        return Array.from({ length: total }, (_, i) => i + 1);
      }
      const result = [];
      if (current > 2) result.push(1);
      if (current > 3) result.push('...');
      const start = Math.max(2, current - 1);
      const end = Math.min(total - 1, current + 1);
      for (let i = start; i <= end; i++) result.push(i);
      if (current < total - 2) result.push('...');
      if (current < total - 1) result.push(total);
      return result;
    },
    isAllSelected() {
      return this.selectable && this.paginatedItems.length > 0 &&
        this.paginatedItems.every(item => this.localSelectedItems.includes(this.getRowKey(item)));
    },
    isIndeterminate() {
      return this.selectable && this.paginatedItems.some(item => this.localSelectedItems.includes(this.getRowKey(item))) &&
        !this.isAllSelected;
    }
  },
  methods: {
    getRowKey(item) {
      return item.id ?? JSON.stringify(item);
    },
    isSelected(item) {
      return this.localSelectedItems.includes(this.getRowKey(item));
    },
    onRowClick(item, event) {
      if (this.selectable && event.target.tagName !== 'INPUT') {
        this.toggleRow(item);
      } else {
        this.$emit('row-click', item);
      }
    },
    toggleRow(item) {
      const key = this.getRowKey(item);
      const index = this.localSelectedItems.indexOf(key);
      if (index > -1) {
        this.localSelectedItems.splice(index, 1);
      } else {
        this.localSelectedItems.push(key);
      }
      this.$emit('update:selectedItems', [...this.localSelectedItems]);
    },
    toggleAll() {
      if (this.isAllSelected) {
        this.paginatedItems.forEach(item => {
          const key = this.getRowKey(item);
          const index = this.localSelectedItems.indexOf(key);
          if (index > -1) this.localSelectedItems.splice(index, 1);
        });
      } else {
        this.paginatedItems.forEach(item => {
          const key = this.getRowKey(item);
          if (!this.localSelectedItems.includes(key)) this.localSelectedItems.push(key);
        });
      }
      this.$emit('update:selectedItems', [...this.localSelectedItems]);
    },
    onSort(key) {
      if (this.localSortBy === key) {
        this.localSortDir = this.localSortDir === 'asc' ? 'desc' : 'asc';
      } else {
        this.localSortBy = key;
        this.localSortDir = 'asc';
      }
      this.$emit('update:sortBy', this.localSortBy);
      this.$emit('update:sortDir', this.localSortDir);
    },
    onPageChange(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
    onPageSizeChange(size) {
      this.localPageSize = size;
      this.currentPage = 1;
      this.$emit('update:pageSize', size);
    },
    getCellContent(item, column) {
      if (column.render) {
        return column.render(item, column);
      }
      const value = item[column.key];
      return value ?? '—';
    }
  }
};
</script>

<template>
  <div class="app-data-table" v-bind="$attrs">
    <div class="app-data-table__toolbar" v-if="showPagination || loading">
      <div class="app-data-table__pagination" v-if="showPagination">
        <AppSelect
          v-model="localPageSize"
          :options="pageSizes.map(s => ({ label: `${s} / page`, value: s }))"
          @change="onPageSizeChange"
          size="sm"
          style="width: 140px"
        />
      </div>
    </div>

    <div class="app-data-table__container">
      <table class="app-data-table__table" role="grid">
        <thead>
          <tr>
            <th v-if="selectable" class="app-data-table__th--checkbox" style="width: 48px">
              <input
                type="checkbox"
                class="app-data-table__select-all"
                :checked="isAllSelected"
                :indeterminate="isIndeterminate"
                @change="toggleAll"
                aria-label="Select all rows"
              />
            </th>
            <th
              v-for="column in columns"
              :key="column.key"
              :class="['app-data-table__th', { 'app-data-table__th--sortable': column.sortable, 'app-data-table__th--sorted': localSortBy === column.key }]"
              :style="{ width: column.width }"
              @click="column.sortable ? () => onSort(column.key) : null"
              :aria-sort="localSortBy === column.key ? (localSortDir === 'asc' ? 'ascending' : 'descending') : 'none'"
            >
              <div class="app-data-table__th-content">
                <span>{{ column.label }}</span>
                <svg v-if="column.sortable && localSortBy === column.key" class="app-data-table__sort-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
                  <polyline :points="localSortDir === 'asc' ? '18 15 12 9 6 15' : '6 9 12 15 18 9'" />
                </svg>
              </div>
            </th>
          </tr>
        </thead>
        <tbody v-if="!loading && paginatedItems.length === 0">
          <tr>
            <td :colspan="columns.length + (selectable ? 1 : 0)" class="app-data-table__empty">
              <AppEmptyState :icon="emptyIcon" :title="emptyMessage" size="sm" />
            </td>
          </tr>
        </tbody>
        <tbody v-else>
          <tr v-for="item in paginatedItems" :key="getRowKey(item)" class="app-data-table__row" @click="onRowClick(item, $event)">
            <td v-if="selectable" class="app-data-table__td--checkbox">
              <input
                type="checkbox"
                class="app-data-table__row-checkbox"
                :checked="isSelected(item)"
                @click.stop
                @change="() => toggleRow(item)"
              />
            </td>
            <td v-for="column in columns" :key="column.key" class="app-data-table__td" :style="{ textAlign: column.align || 'left' }">
              <slot :name="column.key" :item="item" :column="column">
                <template v-if="typeof getCellContent(item, column) === 'object' && getCellContent(item, column)">
                  <AppButton
                    v-if="getCellContent(item, column).type === 'button'"
                    v-bind="getCellContent(item, column)"
                    @click.stop="getCellContent(item, column).onClick?.()"
                  >
                    {{ getCellContent(item, column).label }}
                  </AppButton>
                  <span
                    v-else-if="getCellContent(item, column).html"
                    v-html="getCellContent(item, column).html"
                  />
                  <span v-else>{{ getCellContent(item, column).text || getCellContent(item, column) }}</span>
                </template>
                <span v-else>{{ getCellContent(item, column) }}</span>
              </slot>
            </td>
          </tr>
          <tr v-if="loading" class="app-data-table__loading-row">
            <td :colspan="columns.length + (selectable ? 1 : 0)">
              <AppLoadingState type="pulse" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="app-data-table__footer" v-if="showPagination && totalPages > 1">
      <div class="app-data-table__pagination-info">
        Showing {{ (currentPage - 1) * localPageSize + 1 }} to {{ Math.min(currentPage * localPageSize, sortedItems.length) }} of {{ sortedItems.length }}
      </div>
      <div class="app-data-table__pagination-controls">
        <button
          class="app-pagination__btn"
          @click="onPageChange(currentPage - 1)"
          :disabled="currentPage === 1"
          aria-label="Previous page"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="15 18 9 12 15 6" />
          </svg>
        </button>
        <template v-for="page in visiblePages" :key="page">
          <button
            v-if="page !== '...'"
            class="app-pagination__btn"
            :class="{ 'app-pagination__btn--active': currentPage === page }"
            @click="onPageChange(page)"
            :aria-current="currentPage === page ? 'page' : undefined"
          >
            {{ page }}
          </button>
          <span v-else class="app-pagination__ellipsis">…</span>
        </template>
        <button
          class="app-pagination__btn"
          @click="onPageChange(currentPage + 1)"
          :disabled="currentPage === totalPages"
          aria-label="Next page"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 18 15 12 9 6" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.app-data-table {
  background: var(--color-bg-white);
  border-radius: var(--radius-lg, 16px);
  border: 1px solid var(--color-border-default);
  overflow: hidden;
}

.app-data-table__toolbar {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: var(--space-4, 16px) var(--space-5, 20px);
  border-bottom: 1px solid var(--color-border-default);
  flex-wrap: wrap;
  gap: var(--space-3, 12px);
}

.app-data-table__container {
  overflow-x: auto;
}

.app-data-table__table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--font-size-sm, 14px);
}

.app-data-table__th {
  padding: var(--space-3, 12px) var(--space-4, 16px);
  text-align: left;
  font-weight: var(--font-weight-semibold, 600);
  font-size: var(--font-size-xs, 12px);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--color-text-muted);
  background: var(--color-bg-muted);
  border-bottom: 1px solid var(--color-border-default);
  white-space: nowrap;
  user-select: none;
}

.app-data-table__th-content {
  display: flex;
  align-items: center;
  gap: var(--space-1, 4px);
}

.app-data-table__th--sortable {
  cursor: pointer;
}

.app-data-table__th--sortable:hover {
  background: var(--color-border-default);
}

.app-data-table__sort-icon {
  flex-shrink: 0;
  color: var(--color-text-muted);
}

.app-data-table__th--checkbox {
  width: 48px;
  text-align: center;
}

.app-data-table__select-all {
  width: 16px;
  height: 16px;
  accent-color: var(--color-brand-primary);
}

.app-data-table__td {
  padding: var(--space-3, 12px) var(--space-4, 16px);
  border-bottom: 1px solid var(--color-border-default);
  color: var(--color-text-primary);
}

.app-data-table__td--checkbox {
  text-align: center;
}

.app-data-table__row {
  transition: background var(--transition-fast);
}

.app-data-table__row:hover {
  background: var(--color-bg-muted);
}

.app-data-table__row-checkbox {
  width: 16px;
  height: 16px;
  accent-color: var(--color-brand-primary);
}

.app-data-table__empty {
  padding: var(--space-8, 32px) !important;
}

.app-data-table__loading-row td {
  padding: var(--space-8, 32px) !important;
}

.app-data-table__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: var(--space-4, 16px);
  padding: var(--space-4, 16px) var(--space-5, 20px);
  border-top: 1px solid var(--color-border-default);
}

.app-data-table__pagination-info {
  font-size: var(--font-size-sm, 14px);
  color: var(--color-text-secondary);
}

.app-data-table__pagination-controls {
  display: flex;
  align-items: center;
  gap: var(--space-2, 8px);
}

.app-pagination__btn {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 36px;
  height: 36px;
  padding: 0 var(--space-3, 12px);
  border-radius: var(--radius-md, 12px);
  border: 1px solid var(--color-border-default);
  background: var(--color-bg-white);
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm, 14px);
  font-weight: var(--font-weight-medium, 500);
  transition: all var(--transition-fast);
}

.app-pagination__btn:hover:not(:disabled) {
  background: var(--color-bg-muted);
  border-color: var(--color-border-strong);
  color: var(--color-text-primary);
}

.app-pagination__btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.app-pagination__btn--active {
  background: var(--color-brand-primary);
  border-color: var(--color-brand-primary);
  color: var(--color-text-inverse);
}

.app-pagination__ellipsis {
  padding: 0 var(--space-2, 8px);
  color: var(--color-text-muted);
}

/* Responsive */
@media (max-width: 768px) {
  .app-data-table__container {
    margin: 0 calc(var(--space-4, 16px) * -1);
    width: calc(100% + var(--space-8, 32px));
  }

  .app-data-table__table {
    min-width: 600px;
  }
}
</style>