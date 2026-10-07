<script>
import { admin } from '@/api/client';
import { AppPageHeader, AppCard, AppDataTable, AppEmptyState, AppModal, KpiCard } from '@/components/ui';

export default {
  name: 'AllUsers',
  components: {
    AppPageHeader,
    AppCard,
    AppDataTable,
    AppEmptyState,
    AppModal,
    KpiCard
  },
  data() {
    return {
      message: '',
      messageType: 'info',
      users: [],
      searchQuery: '',
      activeFilter: 'all',
      sortBy: 'name_asc', // 'name_asc' | 'id_asc' | 'id_desc'
      viewMode: 'table', // 'table' | 'grid'
      loading: true,
      selectedUser: null,
      showUserModal: false,
      filterPills: [
        { id: 'all', label: 'All Drivers', query: '' },
        { id: 'ny', label: 'New York (10005)', query: '10005' },
        { id: 'la', label: 'Los Angeles (90028)', query: '90028' },
        { id: 'sv', label: 'San Jose (95113)', query: '95113' },
        { id: 'chi', label: 'Chicago (60601)', query: '60601' },
        { id: 'up', label: 'Uttar Pradesh (273306)', query: '273306' }
      ]
    };
  },
  computed: {
    uniquePincodes() {
      const pins = new Set(this.users.map(u => u.pincode).filter(Boolean));
      return pins.size;
    },
    filteredUsers() {
      let result = [...this.users];
      if (this.searchQuery.trim()) {
        const q = this.searchQuery.toLowerCase();
        result = result.filter(u =>
          (u.username && u.username.toLowerCase().includes(q)) ||
          (u.email && u.email.toLowerCase().includes(q)) ||
          (u.address && u.address.toLowerCase().includes(q)) ||
          (u.pincode && String(u.pincode).includes(q))
        );
      }
      if (this.sortBy === 'name_asc') {
        result.sort((a, b) => (a.username || '').localeCompare(b.username || ''));
      } else if (this.sortBy === 'id_asc') {
        result.sort((a, b) => Number(a.id) - Number(b.id));
      } else if (this.sortBy === 'id_desc') {
        result.sort((a, b) => Number(b.id) - Number(a.id));
      }
      return result;
    },
    columns() {
      return [
        {
          key: 'user',
          label: 'Driver Identity',
          render: (u) => ({
            type: 'custom',
            html: `
              <div style="display: flex; align-items: center; gap: 12px; min-width: 220px;">
                <div style="width: 38px; height: 38px; border-radius: 50%; background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); color: #FFFFFF; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 14px; flex-shrink: 0; box-shadow: 0 2px 6px rgba(0,0,0,0.12);">
                  ${(u.username || 'U').charAt(0).toUpperCase()}
                </div>
                <div style="display: flex; flex-direction: column; gap: 2px;">
                  <span style="font-weight: 700; color: var(--color-text-primary, #111827); font-size: 14px; line-height: 1.3;">${u.username}</span>
                  <span style="font-size: 11px; color: var(--color-text-secondary, #64748B); display: inline-flex; align-items: center; gap: 4px;">
                    <span style="padding: 1px 6px; border-radius: 4px; background: #E2E8F0; color: #334155; font-weight: 700;">ID #${u.id}</span>
                    <span>&bull; Verified</span>
                  </span>
                </div>
              </div>
            `
          })
        },
        {
          key: 'email',
          label: 'Email Address',
          render: (u) => ({
            type: 'custom',
            html: `
              <a href="mailto:${u.email}" style="color: var(--color-brand-primary, #2563EB); font-weight: 600; font-size: 13px; text-decoration: none; display: inline-flex; align-items: center; gap: 6px;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
                ${u.email}
              </a>
            `
          })
        },
        {
          key: 'address',
          label: 'Registered Address',
          render: (u) => ({
            type: 'custom',
            html: `
              <div style="display: flex; align-items: center; gap: 6px; color: var(--color-text-primary, #111827); font-size: 13px; min-width: 220px;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color: var(--color-text-muted, #94A3B8); flex-shrink: 0;"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${u.address || 'Address unlisted'}</span>
              </div>
            `
          })
        },
        {
          key: 'pincode',
          label: 'Postal Code',
          width: '130px',
          render: (u) => ({
            type: 'custom',
            html: `
              <span style="font-family: monospace; font-size: 12px; font-weight: 700; padding: 3px 8px; border-radius: 6px; background: var(--color-bg-muted, #F8FAFC); border: 1px solid var(--color-border-default, #E2E8F0); color: var(--color-text-primary, #111827);">
                ${u.pincode || '—'}
              </span>
            `
          })
        },
        {
          key: 'status',
          label: 'Account Status',
          width: '150px',
          render: () => ({
            type: 'custom',
            html: `
              <span style="display: inline-flex; align-items: center; gap: 5px; font-size: 12px; font-weight: 700; color: #16A34A; background: #DCFCE7; padding: 4px 10px; border-radius: 999px;">
                <span style="width: 6px; height: 6px; border-radius: 50%; background: #16A34A;"></span>
                Active Driver
              </span>
            `
          })
        },
        {
          key: 'action',
          label: 'Action',
          width: '130px',
          render: (u) => ({
            type: 'button',
            label: 'Inspect',
            variant: 'secondary',
            size: 'sm',
            onClick: () => this.inspectUser(u)
          })
        }
      ];
    }
  },
  mounted() {
    document.title = 'Driver Directory — ParkSync Admin';
    this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      try {
        this.loading = true;
        const { data, error } = await admin.listUsers();
        if (error) throw new Error(error.message);
        this.users = data.users || [];
      } catch (error) {
        console.error('Error fetching users:', error);
        this.message = 'Failed to load user directory';
        this.messageType = 'error';
      } finally {
        this.loading = false;
      }
    },
    applyFilter(pill) {
      this.activeFilter = pill.id;
      this.searchQuery = pill.query;
    },
    inspectUser(u) {
      this.selectedUser = u;
      this.showUserModal = true;
    },
    getUserInitials(name) {
      if (!name) return 'U';
      return name
        .split(' ')
        .map(n => n[0])
        .join('')
        .toUpperCase()
        .slice(0, 2);
    }
  }
};
</script>

<template>
  <div class="all-users-page">
    <AppPageHeader
      title="Driver &amp; User Directory"
      subtitle="Comprehensive registry of verified drivers and mobility accounts across metropolitan garages"
      :backRoute="{ name: 'AdminDashboard' }"
      :actions="[
        { label: 'Facility Dashboard', variant: 'secondary', icon: 'DashboardIcon', onClick: () => $router.push('/admin') },
        { label: 'Create Facility', variant: 'primary', icon: 'PlusIcon', onClick: () => $router.push('/admin/add_lot') }
      ]"
    />

    <!-- Toast Notification Banner -->
    <transition name="fade">
      <div v-if="message" class="all-users__alert" :class="`all-users__alert--${messageType}`">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="8" x2="12" y2="12" />
          <line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
        <span>{{ message }}</span>
      </div>
    </transition>

    <div class="all-users__content">
      <!-- KPI Metric Row (4 Aligned Columns on Desktop) -->
      <section class="all-users__kpi-grid">
        <KpiCard
          label="Registered Drivers"
          :value="users.length"
          suffix="accounts"
          subtext="Active in mobility network"
          icon="UsersIcon"
        />
        <KpiCard
          label="Active Driver Status"
          :value="users.length"
          suffix="verified"
          subtext="100% KYC &amp; plate compliant"
          variant="success"
          icon="CheckCircleIcon"
        />
        <KpiCard
          label="Coverage Zones"
          :value="uniquePincodes"
          suffix="pincodes"
          subtext="Distinct metropolitan hubs"
          icon="MapPinIcon"
        />
        <KpiCard
          label="Access Compliance"
          value="100%"
          subtext="Automated gate clearance"
          variant="primary"
          icon="ShieldIcon"
        />
      </section>

      <!-- Search, Filters & View Toggle Bar -->
      <section class="all-users__toolbar">
        <div class="all-users__search-wrap">
          <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            class="all-users__search-input"
            placeholder="Search drivers by name, email, street address, or pincode..."
          />
          <button
            v-if="searchQuery"
            type="button"
            class="all-users__clear-btn"
            @click="searchQuery = ''; activeFilter = 'all'"
            title="Clear search"
          >
            &times;
          </button>
        </div>

        <div class="all-users__controls-group">
          <!-- Sort Dropdown -->
          <div class="all-users__sort-wrap">
            <select v-model="sortBy" class="sort-select" aria-label="Sort users">
              <option value="name_asc">Name: A to Z</option>
              <option value="id_asc">ID: Low to High</option>
              <option value="id_desc">ID: High to Low</option>
            </select>
          </div>

          <!-- View Toggle Buttons -->
          <div class="all-users__view-toggles">
            <button
              type="button"
              class="view-toggle-btn"
              :class="{ 'view-toggle-btn--active': viewMode === 'table' }"
              @click="viewMode = 'table'"
              title="Table View"
            >
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="8" y1="6" x2="21" y2="6" stroke-linecap="round"/>
                <line x1="8" y1="12" x2="21" y2="12" stroke-linecap="round"/>
                <line x1="8" y1="18" x2="21" y2="18" stroke-linecap="round"/>
                <line x1="3" y1="6" x2="3.01" y2="6" stroke-width="3" stroke-linecap="round"/>
                <line x1="3" y1="12" x2="3.01" y2="12" stroke-width="3" stroke-linecap="round"/>
                <line x1="3" y1="18" x2="3.01" y2="18" stroke-width="3" stroke-linecap="round"/>
              </svg>
              <span>Table</span>
            </button>
            <button
              type="button"
              class="view-toggle-btn"
              :class="{ 'view-toggle-btn--active': viewMode === 'grid' }"
              @click="viewMode = 'grid'"
              title="Cards Grid View"
            >
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="7" height="7" rx="1.5"/>
                <rect x="14" y="3" width="7" height="7" rx="1.5"/>
                <rect x="14" y="14" width="7" height="7" rx="1.5"/>
                <rect x="3" y="14" width="7" height="7" rx="1.5"/>
              </svg>
              <span>Cards</span>
            </button>
          </div>
        </div>
      </section>

      <!-- Filter Pills Row -->
      <div class="all-users__pills">
        <button
          v-for="pill in filterPills"
          :key="pill.id"
          type="button"
          class="filter-pill"
          :class="{ 'filter-pill--active': activeFilter === pill.id }"
          @click="applyFilter(pill)"
        >
          {{ pill.label }}
        </button>
        <span class="all-users__count-badge">{{ filteredUsers.length }} drivers found</span>
      </div>

      <!-- Main Directory Content -->
      <section v-if="viewMode === 'table'" class="all-users__table-wrap">
        <AppCard>
          <AppDataTable
            :columns="columns"
            :items="filteredUsers"
            :loading="loading"
            emptyMessage="No drivers found matching your search criteria"
            emptyIcon="UsersIcon"
            :showPagination="filteredUsers.length > 10"
            :pageSize="10"
          />
        </AppCard>
      </section>

      <!-- Grid Cards View -->
      <section v-else class="all-users__grid">
        <div
          v-for="u in filteredUsers"
          :key="u.id"
          class="driver-card"
          @click="inspectUser(u)"
        >
          <div class="driver-card__head">
            <div class="driver-card__avatar">
              {{ getUserInitials(u.username) }}
            </div>
            <div class="driver-card__meta">
              <span class="driver-card__name">{{ u.username }}</span>
              <span class="driver-card__id">Driver ID #{{ u.id }}</span>
            </div>
            <span class="driver-card__status">
              <span class="status-dot"></span>
              Active
            </span>
          </div>

          <div class="driver-card__body">
            <div class="driver-card__item">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                <polyline points="22,6 12,13 2,6"/>
              </svg>
              <a :href="`mailto:${u.email}`" class="driver-card__link" @click.stop>{{ u.email }}</a>
            </div>

            <div class="driver-card__item">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                <circle cx="12" cy="10" r="3"/>
              </svg>
              <span class="driver-card__address">{{ u.address || 'Address unlisted' }}</span>
            </div>

            <div class="driver-card__item">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="2" y="7" width="20" height="14" rx="2" ry="2"/>
                <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
              </svg>
              <span class="driver-card__pin">Postal Pin: {{ u.pincode || '—' }}</span>
            </div>
          </div>

          <div class="driver-card__footer">
            <button type="button" class="inspect-btn" @click.stop="inspectUser(u)">
              Inspect Account
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="5" y1="12" x2="19" y2="12"/>
                <polyline points="12 5 19 12 12 19"/>
              </svg>
            </button>
          </div>
        </div>

        <div v-if="!loading && filteredUsers.length === 0" class="all-users__empty-wrap">
          <AppEmptyState
            icon="UsersIcon"
            title="No matching drivers"
            description="Try clearing your search query or selecting 'All Drivers'"
            :action="{ label: 'Show All Drivers', onClick: () => applyFilter(filterPills[0]), variant: 'primary' }"
          />
        </div>
      </section>
    </div>

    <!-- User Inspection Modal -->
    <AppModal
      v-if="selectedUser"
      v-model="showUserModal"
      title="Driver Profile &amp; Account Clearance"
      size="md"
      @close="showUserModal = false"
    >
      <div class="modal-driver">
        <div class="modal-driver__head">
          <div class="modal-driver__avatar">
            {{ getUserInitials(selectedUser.username) }}
          </div>
          <div>
            <h3 class="modal-driver__name">{{ selectedUser.username }}</h3>
            <span class="modal-driver__sub">Verified Driver &bull; System ID #{{ selectedUser.id }}</span>
          </div>
        </div>

        <div class="modal-driver__details">
          <div class="detail-row">
            <span class="detail-label">Email Address</span>
            <span class="detail-val">
              <a :href="`mailto:${selectedUser.email}`" class="detail-link">{{ selectedUser.email }}</a>
            </span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Account Role</span>
            <span class="detail-val">Verified Mobility Driver</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Registered Address</span>
            <span class="detail-val">{{ selectedUser.address || 'Not specified' }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Postal Pincode</span>
            <span class="detail-val font-mono">{{ selectedUser.pincode || '—' }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Gate Access Status</span>
            <span class="detail-val status-green">Authorized (100% Clearance)</span>
          </div>
        </div>

        <!-- <div class="modal-driver__actions">
          <a :href="`mailto:${selectedUser.email}`" class="contact-email-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
              <polyline points="22,6 12,13 2,6"/>
            </svg>
            Send Direct Email
          </a>
        </div> -->
      </div>
    </AppModal>
  </div>
</template>

<style scoped>
.all-users-page {
  width: 100%;
  max-width: 100%;
  padding: 24px 32px 48px 32px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.all-users__content {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Alert Notification */
.all-users__alert {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 18px;
  border-radius: var(--radius-md, 12px);
  font-size: 14px;
  font-weight: 600;
}

.all-users__alert--error {
  background: var(--color-status-occupied-bg, #FEE2E2);
  color: var(--color-status-occupied, #EF4444);
  border: 1px solid var(--color-status-occupied, #EF4444);
}

.all-users__alert--info {
  background: var(--color-status-info-bg, #EAF2FF);
  color: var(--color-brand-primary, #2563EB);
  border: 1px solid var(--color-brand-primary, #2563EB);
}

/* KPI Grid - Full Width 4 Columns */
.all-users__kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  width: 100%;
}

@media (max-width: 1200px) {
  .all-users__kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .all-users__kpi-grid {
    grid-template-columns: 1fr;
  }
}

/* Toolbar */
.all-users__toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  width: 100%;
}

.all-users__search-wrap {
  position: relative;
  display: flex;
  align-items: center;
  flex: 1;
  min-width: min(320px, 100%);
}

.all-users__search-wrap .search-icon {
  position: absolute;
  left: 14px;
  color: var(--color-text-muted, #94A3B8);
  pointer-events: none;
}

.all-users__search-input {
  width: 100%;
  height: 44px;
  padding: 0 40px 0 42px;
  font-size: 14px;
  font-family: inherit;
  border: 1px solid var(--color-border-default, #E2E8F0);
  border-radius: 10px;
  background: var(--color-bg-white, #FFFFFF);
  color: var(--color-text-primary, #111827);
  outline: none;
  box-sizing: border-box;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.all-users__search-input:focus {
  border-color: var(--color-brand-primary, #2563EB);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.all-users__clear-btn {
  position: absolute;
  right: 12px;
  background: transparent;
  border: none;
  font-size: 18px;
  color: var(--color-text-muted, #94A3B8);
  cursor: pointer;
  padding: 4px;
  line-height: 1;
}

.all-users__controls-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.sort-select {
  padding: 0 12px;
  height: 44px;
  border-radius: 10px;
  border: 1px solid var(--color-border-default, #E2E8F0);
  background: var(--color-bg-white, #FFFFFF);
  color: var(--color-text-primary, #111827);
  font-size: 13px;
  font-weight: 600;
  outline: none;
  cursor: pointer;
  transition: border-color 0.15s ease;
}

.sort-select:focus {
  border-color: var(--color-brand-primary, #2563EB);
}

/* View Toggles */
.all-users__view-toggles {
  display: flex;
  align-items: center;
  background: var(--color-bg-white, #FFFFFF);
  border: 1px solid var(--color-border-default, #E2E8F0);
  border-radius: 10px;
  padding: 3px;
  gap: 3px;
  height: 44px;
  box-sizing: border-box;
}

.view-toggle-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0 12px;
  height: 36px;
  border: none;
  background: transparent;
  color: var(--color-text-secondary, #64748B);
  font-size: 13px;
  font-weight: 700;
  border-radius: 7px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.view-toggle-btn:hover {
  color: var(--color-text-primary, #111827);
}

.view-toggle-btn--active {
  background: var(--color-brand-primary, #2563EB);
  color: #FFFFFF !important;
}

/* Filter Pills */
.all-users__pills {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.filter-pill {
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  border: 1px solid var(--color-border-default, #E2E8F0);
  background: var(--color-bg-white, #FFFFFF);
  color: var(--color-text-secondary, #64748B);
  cursor: pointer;
  transition: all 0.15s ease;
}

.filter-pill:hover {
  background: var(--color-bg-muted, #F8FAFC);
  color: var(--color-text-primary, #111827);
}

.filter-pill--active {
  background: var(--color-navy-deep, #0B1220) !important;
  color: #FFFFFF !important;
  border-color: var(--color-navy-deep, #0B1220) !important;
}

.all-users__count-badge {
  margin-left: auto;
  font-size: 12px;
  font-weight: 700;
  color: var(--color-text-secondary, #64748B);
}

/* Table Wrap */
.all-users__table-wrap {
  width: 100%;
  background: var(--color-bg-white, #FFFFFF);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
}

/* Grid Cards */
.all-users__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
  width: 100%;
}

.driver-card {
  background: var(--color-bg-white, #FFFFFF);
  border: 1px solid var(--color-border-default, #E2E8F0);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
  cursor: pointer;
}

.driver-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.06);
  border-color: var(--color-brand-primary, #2563EB);
}

.driver-card__head {
  display: flex;
  align-items: center;
  gap: 12px;
}

.driver-card__avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 15px;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.15);
}

.driver-card__meta {
  display: flex;
  flex-direction: column;
  min-width: 0;
  flex: 1;
}

.driver-card__name {
  font-size: 15px;
  font-weight: 700;
  color: var(--color-text-primary, #111827);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.driver-card__id {
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text-secondary, #64748B);
}

.driver-card__status {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  font-weight: 700;
  color: #16A34A;
  background: #DCFCE7;
  padding: 3px 8px;
  border-radius: 999px;
  flex-shrink: 0;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #16A34A;
}

.driver-card__body {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding-top: 10px;
  border-top: 1px solid var(--color-border-default, #E2E8F0);
}

.driver-card__item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--color-text-secondary, #64748B);
}

.driver-card__item svg {
  color: var(--color-text-muted, #94A3B8);
  flex-shrink: 0;
}

.driver-card__link {
  color: var(--color-brand-primary, #2563EB);
  font-weight: 600;
  text-decoration: none;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.driver-card__link:hover {
  text-decoration: underline;
}

.driver-card__address {
  color: var(--color-text-primary, #111827);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.driver-card__pin {
  font-family: monospace;
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-primary, #111827);
}

.driver-card__footer {
  margin-top: auto;
  padding-top: 8px;
}

.inspect-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid var(--color-border-default, #E2E8F0);
  background: var(--color-bg-muted, #F8FAFC);
  color: var(--color-text-primary, #111827);
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
}

.inspect-btn:hover {
  background: var(--color-brand-primary, #2563EB);
  color: #FFFFFF;
  border-color: var(--color-brand-primary, #2563EB);
}

.all-users__empty-wrap {
  grid-column: 1 / -1;
  padding: 48px 0;
}

/* Modal Styling */
.modal-driver {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.modal-driver__head {
  display: flex;
  align-items: center;
  gap: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--color-border-default, #E2E8F0);
}

.modal-driver__avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 20px;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
}

.modal-driver__name {
  margin: 0;
  font-size: 18px;
  font-weight: 800;
  color: var(--color-text-primary, #111827);
}

.modal-driver__sub {
  font-size: 12px;
  color: var(--color-text-secondary, #64748B);
  font-weight: 600;
}

.modal-driver__details {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  background: var(--color-bg-muted, #F8FAFC);
  border-radius: 8px;
  gap: 16px;
}

.detail-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-secondary, #64748B);
}

.detail-val {
  font-size: 13px;
  font-weight: 700;
  color: var(--color-text-primary, #111827);
  text-align: right;
}

.detail-link {
  color: var(--color-brand-primary, #2563EB);
  text-decoration: none;
}

.detail-link:hover {
  text-decoration: underline;
}

.status-green {
  color: #16A34A;
}

.font-mono {
  font-family: monospace;
}

.modal-driver__actions {
  display: flex;
  gap: 10px;
  margin-top: 8px;
}

.contact-email-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 18px;
  border-radius: 8px;
  background: var(--color-brand-primary, #2563EB);
  color: #FFFFFF;
  font-size: 13px;
  font-weight: 700;
  text-decoration: none;
  transition: background 0.15s ease;
}

.contact-email-btn:hover {
  background: var(--color-brand-primary-hover, #1D4ED8);
  color: #FFFFFF;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .all-users-page {
    padding: 16px 16px 36px 16px;
    gap: 16px;
  }
}

@media (max-width: 640px) {
  .all-users__grid {
    grid-template-columns: 1fr;
  }
  .all-users__search-wrap {
    min-width: 100%;
    width: 100%;
  }
  .all-users__controls-group {
    width: 100%;
    justify-content: space-between;
  }
}
</style>