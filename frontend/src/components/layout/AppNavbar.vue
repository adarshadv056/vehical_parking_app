<script>
export default {
  name: 'AppNavbar',
  props: {
    sidebarOpen: Boolean,
    sidebarCollapsed: Boolean,
    userInfo: Object,
    userRole: String
  },
  emits: ['toggle-sidebar', 'toggle-collapse', 'logout'],
  data() {
    return {
      theme: localStorage.getItem('theme') || 'light'
    }
  },
  mounted() {
    document.documentElement.setAttribute('data-theme', this.theme)
  },
  methods: {
    toggleTheme() {
      this.theme = this.theme === 'light' ? 'dark' : 'light'
      localStorage.setItem('theme', this.theme)
      document.documentElement.setAttribute('data-theme', this.theme)
    }
  },
  computed: {
    brandName() {
      return this.userRole === 'admin' ? 'ParkSync Admin' : 'ParkSync Mobility';
    }
  }
};
</script>

<template>
  <header class="app-navbar" role="banner">
    <div class="app-navbar__container">
      <button
        v-if="!sidebarCollapsed"
        type="button"
        class="app-navbar__menu-toggle"
        @click="$emit('toggle-sidebar')"
        :aria-expanded="sidebarOpen"
        aria-controls="app-sidebar"
        aria-label="Toggle navigation menu"
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="3" y1="6" x2="21" y2="6" />
          <line x1="3" y1="12" x2="21" y2="12" />
          <line x1="3" y1="18" x2="21" y2="18" />
        </svg>
      </button>

      <div class="app-navbar__brand" @click="$emit('navigate-home')">
        <div class="app-navbar__logo">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round">
            <path d="M6 3H13C16.866 3 20 6.13401 20 10C20 13.866 16.866 17 13 17H10V21H6V3Z"/>
            <path d="M10 7H12.5C14.433 7 16 8.567 16 10.5C16 12.433 14.433 14 12.5 10H10V7Z"/>
          </svg>
        </div>
        <span class="app-navbar__brand-text">{{ brandName }}</span>
      </div>

      <div class="app-navbar__spacer" />

      <div class="app-navbar__actions">
        <button
          v-if="sidebarCollapsed"
          type="button"
          class="app-navbar__collapse-toggle"
          @click="$emit('toggle-collapse')"
          :aria-expanded="!sidebarCollapsed"
          aria-label="Expand sidebar"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="15 18 9 12 15 6" />
          </svg>
        </button>

        <div v-if="userInfo" class="app-navbar__user">
          <div class="app-navbar__user-avatar">
            {{ userInfo.name?.charAt(0)?.toUpperCase() || 'U' }}
          </div>
          <div class="app-navbar__user-info">
            <span class="app-navbar__user-name">{{ userInfo.name }}</span>
            <span class="app-navbar__user-role">{{ userRole === 'admin' ? 'Administrator' : 'User' }}</span>
          </div>
          <button
            type="button"
            class="app-navbar__logout"
            @click="toggleTheme"
            aria-label="Toggle theme"
            title="Toggle theme"
          >
            <svg v-if="theme === 'light'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" />
            </svg>
            <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
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
            class="app-navbar__logout"
            @click="$emit('logout')"
            aria-label="Log out"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
              <polyline points="16 17 21 12 16 7"/>
              <line x1="21" y1="12" x2="9" y2="12"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
.app-navbar {
  position: sticky;
  top: 0;
  height: var(--navbar-height, 64px);
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--color-border-default);
  z-index: var(--z-sticky, 200);
}

.app-navbar__container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 var(--space-5, 20px);
  gap: var(--space-4, 16px);
}

.app-navbar__menu-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md, 12px);
  color: var(--color-text-secondary);
  background: transparent;
  transition: color var(--transition-fast), background var(--transition-fast);
  flex-shrink: 0;
}

.app-navbar__menu-toggle:hover {
  color: var(--color-text-primary);
  background: var(--color-bg-muted);
}

@media (min-width: 1025px) {
  .app-navbar__menu-toggle {
    display: none;
  }
}

.app-navbar__brand {
  display: flex;
  align-items: center;
  gap: var(--space-3, 12px);
  text-decoration: none;
  color: inherit;
  flex-shrink: 0;
}

.app-navbar__logo {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: var(--color-navy-deep);
  border-radius: var(--radius-md, 12px);
  color: var(--color-text-inverse);
}

.app-navbar__brand-text {
  font-size: var(--font-size-lg, 18px);
  font-weight: var(--font-weight-bold, 700);
  color: var(--color-text-primary);
  white-space: nowrap;
}

@media (max-width: 640px) {
  .app-navbar__brand-text {
    display: none;
  }
}

.app-navbar__spacer {
  flex: 1;
}

.app-navbar__actions {
  display: flex;
  align-items: center;
  gap: var(--space-3, 12px);
}

.app-navbar__collapse-toggle {
  display: none;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md, 12px);
  color: var(--color-text-secondary);
  transition: color var(--transition-fast), background var(--transition-fast);
}

.app-navbar__collapse-toggle:hover {
  color: var(--color-text-primary);
  background: var(--color-bg-muted);
}

@media (max-width: 1024px) {
  .app-navbar__collapse-toggle {
    display: flex;
  }
}

.app-navbar__user {
  display: flex;
  align-items: center;
  gap: var(--space-3, 12px);
  padding: var(--space-1, 4px) var(--space-3, 12px);
  border-radius: var(--radius-pill, 9999px);
  background: var(--color-bg-muted);
  transition: background var(--transition-fast);
}

.app-navbar__user:hover {
  background: var(--color-border-default);
}

.app-navbar__user-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--color-brand-primary);
  color: var(--color-text-inverse);
  font-size: var(--font-size-sm, 14px);
  font-weight: var(--font-weight-bold, 700);
}

.app-navbar__user-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

@media (max-width: 480px) {
  .app-navbar__user-info {
    display: none;
  }
}

.app-navbar__user-name {
  font-size: var(--font-size-sm, 14px);
  font-weight: var(--font-weight-semibold, 600);
  color: var(--color-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.app-navbar__user-role {
  font-size: var(--font-size-xs, 11px);
  color: var(--color-text-muted);
  text-transform: capitalize;
}

.app-navbar__logout {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md, 12px);
  color: var(--color-text-secondary);
  transition: color var(--transition-fast), background var(--transition-fast);
}

.app-navbar__logout:hover {
  color: var(--color-status-occupied);
  background: var(--color-status-occupied-bg);
}
</style>