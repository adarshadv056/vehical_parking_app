<script>
import DashboardIcon from '../icons/DashboardIcon.vue';
import UsersIcon from '../icons/UsersIcon.vue';
import PlusIcon from '../icons/PlusIcon.vue';
import ChartIcon from '../icons/ChartIcon.vue';
import SearchIcon from '../icons/SearchIcon.vue';
import ClockIcon from '../icons/ClockIcon.vue';

const ICON_MAP = { DashboardIcon, UsersIcon, PlusIcon, ChartIcon, SearchIcon, ClockIcon };

export default {
  name: 'AppSidebar',
  props: {
    collapsed: {
      type: Boolean,
      default: false
    },
    items: {
      type: Array,
      default: () => []
    },
    userInfo: {
      type: Object,
      default: null
    },
    userRole: {
      type: String,
      default: 'user'
    },
    theme: {
      type: String,
      default: 'light'
    },
    isMobile: {
      type: Boolean,
      default: false
    }
  },
  emits: ['navigate', 'toggle-collapse', 'close', 'logout', 'toggle-theme'],
  computed: {
    activeRoute() {
      return this.$route?.name || null;
    },
    userInitials() {
      if (!this.userInfo?.name) return 'U';
      return this.userInfo.name
        .split(' ')
        .map(n => n[0])
        .join('')
        .toUpperCase()
        .slice(0, 2);
    },
    brandSubtitle() {
      return this.userRole === 'admin' ? 'ADMIN CONSOLE' : 'MOBILITY PORTAL';
    },
    sectionLabel() {
      return this.userRole === 'admin' ? 'FLEET OPERATIONS' : 'DRIVER MOBILITY';
    }
  },
  methods: {
    iconFor(name) {
      return ICON_MAP[name] || null;
    },
    navigate(item) {
      this.$emit('navigate', item);
    },
    handleHeaderToggle() {
      if (this.isMobile) {
        this.$emit('close');
      } else {
        this.$emit('toggle-collapse');
      }
    }
  }
};
</script>

<template>
  <div class="app-sidebar__inner" :class="{ 'app-sidebar__inner--collapsed': collapsed && !isMobile }">
    <!-- Header: Logo, Brand & Toggle Button -->
    <div class="app-sidebar__header">
      <div v-if="!collapsed || isMobile" class="app-sidebar__brand">
        <div class="app-sidebar__logo">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round">
            <path d="M6 3H13C16.866 3 20 6.13401 20 10C20 13.866 16.866 17 13 17H10V21H6V3Z"/>
            <path d="M10 7H12.5C14.433 7 16 8.567 16 10.5C16 12.433 14.433 14 12.5 10H10V7Z"/>
          </svg>
        </div>
        <div class="app-sidebar__brand-meta">
          <span class="app-sidebar__brand-name">ParkSync</span>
          <span class="app-sidebar__brand-badge">{{ brandSubtitle }}</span>
        </div>
      </div>

      <!-- Collapsed Logo Icon (Clickable to Expand) -->
      <button
        v-else
        type="button"
        class="app-sidebar__collapsed-logo-btn"
        @click="$emit('toggle-collapse')"
        title="Expand sidebar"
        aria-label="Expand sidebar"
      >
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round">
          <path d="M6 3H13C16.866 3 20 6.13401 20 10C20 13.866 16.866 17 13 17H10V21H6V3Z"/>
          <path d="M10 7H12.5C14.433 7 16 8.567 16 10.5C16 12.433 14.433 14 12.5 10H10V7Z"/>
        </svg>
      </button>

      <!-- Toggle / Close Button -->
      <button
        type="button"
        class="app-sidebar__toggle-btn"
        :class="{ 'app-sidebar__toggle-btn--collapsed': collapsed && !isMobile }"
        @click="handleHeaderToggle"
        :aria-label="isMobile ? 'Close sidebar' : (collapsed ? 'Expand sidebar' : 'Collapse sidebar')"
        :title="isMobile ? 'Close sidebar' : (collapsed ? 'Expand sidebar' : 'Collapse sidebar')"
      >
        <!-- Mobile close X icon -->
        <svg v-if="isMobile" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round">
          <line x1="18" y1="6" x2="6" y2="18" />
          <line x1="6" y1="6" x2="18" y2="18" />
        </svg>
        <!-- Desktop Collapse Icon (PanelLeftClose) -->
        <svg v-else-if="!collapsed" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect width="18" height="18" x="3" y="3" rx="2" />
          <path d="M9 3v18" />
          <path d="m14 9-3 3 3 3" />
        </svg>
        <!-- Desktop Expand Icon (PanelLeftOpen) -->
        <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect width="18" height="18" x="3" y="3" rx="2" />
          <path d="M9 3v18" />
          <path d="m12 9 3 3-3 3" />
        </svg>
      </button>
    </div>

    <!-- Section Label -->
    <div v-if="!collapsed || isMobile" class="app-sidebar__section-tag">
      {{ sectionLabel }}
    </div>

    <!-- Main Navigation Items -->
    <nav class="app-sidebar__nav" role="navigation" aria-label="Main navigation">
      <ul class="app-sidebar__list" role="list">
        <li v-for="item in items" :key="item.name" class="app-sidebar__item">
          <router-link
            :to="{ name: item.name }"
            class="app-sidebar__link"
            :class="{ 'app-sidebar__link--active': activeRoute === item.name }"
            :aria-current="activeRoute === item.name ? 'page' : undefined"
            :aria-label="item.label"
            :title="collapsed && !isMobile ? item.label : undefined"
            @click="navigate(item)"
          >
            <span class="app-sidebar__icon">
              <component :is="iconFor(item.icon)" class="app-sidebar__icon-svg" />
            </span>
            <span v-if="!collapsed || isMobile" class="app-sidebar__label">{{ item.label }}</span>
            <span v-if="item.badge && (!collapsed || isMobile)" class="app-sidebar__badge">{{ item.badge }}</span>
          </router-link>
        </li>
      </ul>
    </nav>

    <!-- Bottom User Profile Card & Utilities -->
    <div class="app-sidebar__footer-wrapper">
      <!-- Expanded State Footer -->
      <div v-if="!collapsed || isMobile" class="app-sidebar__footer">
        <div class="app-sidebar__user-card">
          <div class="app-sidebar__avatar-wrap">
            <div class="app-sidebar__user-avatar">{{ userInitials }}</div>
            <span class="app-sidebar__status-dot" title="Active"></span>
          </div>
          <div class="app-sidebar__user-info">
            <span class="app-sidebar__user-name" :title="userInfo?.name">{{ userInfo?.name || 'Authorized User' }}</span>
            <span class="app-sidebar__user-role">{{ userRole === 'admin' ? 'Administrator' : 'Verified Driver' }}</span>
          </div>
        </div>

        <div class="app-sidebar__footer-actions">
          <button
            type="button"
            class="app-sidebar__action-btn"
            @click="$emit('toggle-theme')"
            :title="theme === 'light' ? 'Switch to Dark Mode' : 'Switch to Light Mode'"
            aria-label="Toggle theme"
          >
            <svg v-if="theme === 'light'" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" />
            </svg>
            <svg v-else width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="5" />
              <line x1="12" y1="1" x2="12" y2="3" />
              <line x1="12" y1="21" x2="12" y2="23" />
              <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
              <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
              <line x1="1" y1="12" x2="3" y2="12" />
              <line x1="21" y1="12" x2="23" y2="12" />
              <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
              <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
            </svg>
          </button>
          <button
            type="button"
            class="app-sidebar__action-btn app-sidebar__action-btn--logout"
            @click="$emit('logout')"
            title="Sign Out"
            aria-label="Sign out"
          >
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
              <polyline points="16 17 21 12 16 7"/>
              <line x1="21" y1="12" x2="9" y2="12"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- Collapsed State Footer -->
      <div v-else class="app-sidebar__footer-collapsed">
        <div class="app-sidebar__avatar-wrap" :title="`${userInfo?.name || 'User'} (${userRole})`">
          <div class="app-sidebar__user-avatar">{{ userInitials }}</div>
          <span class="app-sidebar__status-dot"></span>
        </div>
        <button
          type="button"
          class="app-sidebar__action-btn"
          @click="$emit('toggle-theme')"
          :title="theme === 'light' ? 'Switch to Dark Mode' : 'Switch to Light Mode'"
          aria-label="Toggle theme"
        >
          <svg v-if="theme === 'light'" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" />
          </svg>
          <svg v-else width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="5" />
            <line x1="12" y1="1" x2="12" y2="3" />
            <line x1="12" y1="21" x2="12" y2="23" />
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
            <line x1="1" y1="12" x2="3" y2="12" />
            <line x1="21" y1="12" x2="23" y2="12" />
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
          </svg>
        </button>
        <button
          type="button"
          class="app-sidebar__action-btn app-sidebar__action-btn--logout"
          @click="$emit('logout')"
          title="Sign Out"
          aria-label="Sign out"
        >
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
            <polyline points="16 17 21 12 16 7"/>
            <line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.app-sidebar__inner {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: var(--space-4, 16px);
  gap: var(--space-3, 12px);
  background: var(--color-bg-white);
  box-sizing: border-box;
}

.app-sidebar__inner--collapsed {
  padding: var(--space-4, 16px) var(--space-2, 8px);
  align-items: center;
}

/* Header */
.app-sidebar__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 0 12px 0;
  border-bottom: 1px solid var(--color-border-default);
  min-height: 48px;
}

.app-sidebar__inner--collapsed .app-sidebar__header {
  flex-direction: column;
  gap: 12px;
  justify-content: center;
  width: 100%;
  border-bottom: 1px solid var(--color-border-default);
  padding-bottom: 12px;
}

.app-sidebar__brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  min-width: 0;
}

.app-sidebar__logo {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
  border-radius: 10px;
  color: #FFFFFF;
  box-shadow: 0 4px 10px rgba(37, 99, 235, 0.25);
  flex-shrink: 0;
}

.app-sidebar__collapsed-logo-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
  border-radius: 10px;
  color: #FFFFFF;
  border: none;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(37, 99, 235, 0.25);
  transition: transform 0.15s ease;
}

.app-sidebar__collapsed-logo-btn:hover {
  transform: scale(1.05);
}

.app-sidebar__brand-meta {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.app-sidebar__brand-name {
  font-size: 16px;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--color-text-primary);
  line-height: 1.2;
}

.app-sidebar__brand-badge {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--color-brand-primary);
  line-height: 1.2;
}

/* Header Toggle Button */
.app-sidebar__toggle-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: transparent;
  border: 1px solid var(--color-border-default);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all 0.15s ease;
  flex-shrink: 0;
}

.app-sidebar__toggle-btn:hover {
  background: var(--color-bg-muted);
  color: var(--color-text-primary);
  border-color: var(--color-border-strong);
}

.app-sidebar__toggle-btn--collapsed {
  margin-top: 4px;
}

/* Section Tag */
.app-sidebar__section-tag {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--color-text-muted);
  padding: 6px 8px 2px 8px;
  text-transform: uppercase;
}

/* Nav list */
.app-sidebar__nav {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  margin: 0 -4px;
  padding: 0 4px;
}

.app-sidebar__list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.app-sidebar__item {
  width: 100%;
}

.app-sidebar__link {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: 10px;
  color: var(--color-text-secondary);
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.18s ease;
  box-sizing: border-box;
}

.app-sidebar__inner--collapsed .app-sidebar__link {
  justify-content: center;
  padding: 10px;
}

.app-sidebar__link:hover {
  color: var(--color-text-primary);
  background: var(--color-bg-muted);
}

.app-sidebar__link--active {
  color: var(--color-brand-primary) !important;
  background: var(--color-brand-primary-light, rgba(37, 99, 235, 0.08)) !important;
  font-weight: 700;
}

/* Active indicator accent bar */
.app-sidebar__link--active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 6px;
  bottom: 6px;
  width: 3.5px;
  border-radius: 0 4px 4px 0;
  background: var(--color-brand-primary);
}

.app-sidebar__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  flex-shrink: 0;
}

.app-sidebar__icon-svg {
  width: 20px;
  height: 20px;
}

.app-sidebar__label {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.app-sidebar__badge {
  font-size: 11px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 999px;
  background: var(--color-brand-primary-light);
  color: var(--color-brand-primary);
}

/* Footer Wrapper */
.app-sidebar__footer-wrapper {
  margin-top: auto;
  border-top: 1px solid var(--color-border-default);
  padding-top: 12px;
  width: 100%;
}

.app-sidebar__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.app-sidebar__user-card {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
  flex: 1;
}

.app-sidebar__avatar-wrap {
  position: relative;
  flex-shrink: 0;
}

.app-sidebar__user-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
  color: #FFFFFF;
  font-size: 13px;
  font-weight: 700;
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.15);
}

.app-sidebar__status-dot {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #16A34A;
  border: 2px solid var(--color-bg-white);
}

.app-sidebar__user-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.app-sidebar__user-name {
  font-size: 13px;
  font-weight: 700;
  color: var(--color-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.3;
}

.app-sidebar__user-role {
  font-size: 11px;
  font-weight: 500;
  color: var(--color-text-secondary);
  line-height: 1.2;
}

.app-sidebar__footer-actions {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-shrink: 0;
}

.app-sidebar__action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: transparent;
  border: 1px solid var(--color-border-default);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all 0.15s ease;
}

.app-sidebar__action-btn:hover {
  background: var(--color-bg-muted);
  color: var(--color-text-primary);
  border-color: var(--color-border-strong);
}

.app-sidebar__action-btn--logout:hover {
  background: var(--color-status-occupied-bg, #FEE2E2);
  color: var(--color-status-occupied, #EF4444);
  border-color: #FECACA;
}

/* Collapsed footer */
.app-sidebar__footer-collapsed {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  width: 100%;
}
</style>