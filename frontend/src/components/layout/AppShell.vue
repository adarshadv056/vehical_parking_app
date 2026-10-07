<script>
import { computed, ref, onMounted, onBeforeUnmount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import AppSidebar from './AppSidebar.vue';

export default {
  name: 'AppShell',
  components: { AppSidebar },
  props: {
    variant: {
      type: String,
      default: 'app',
      validator: (v) => ['app', 'auth', 'landing'].includes(v)
    }
  },
  setup(props) {
    const route = useRoute();
    const router = useRouter();
    const sidebarOpen = ref(false); // Mobile drawer open/close
    const sidebarCollapsed = ref(false); // Desktop rail collapsed/expanded
    const isDesktop = ref(false);
    const theme = ref(localStorage.getItem('theme') || 'light');
    let mediaQuery = null;
    let onMediaChange = null;

    onMounted(() => {
      mediaQuery = window.matchMedia('(min-width: 1025px)');
      isDesktop.value = mediaQuery.matches;
      onMediaChange = (e) => {
        isDesktop.value = e.matches;
        if (e.matches) {
          sidebarOpen.value = false; // close mobile drawer when switching to desktop
        }
      };
      mediaQuery.addEventListener('change', onMediaChange);
      document.documentElement.setAttribute('data-theme', theme.value);
    });

    onBeforeUnmount(() => {
      if (mediaQuery && onMediaChange) {
        mediaQuery.removeEventListener('change', onMediaChange);
      }
    });

    const toggleTheme = () => {
      theme.value = theme.value === 'light' ? 'dark' : 'light';
      localStorage.setItem('theme', theme.value);
      document.documentElement.setAttribute('data-theme', theme.value);
    };

    const isAuthRoute = computed(() => ['Login', 'Register'].includes(route.name));
    const isAdminRoute = computed(() => route.path.startsWith('/admin'));
    const isUserRoute = computed(() => route.path.startsWith('/user'));

    const showSidebar = computed(() => {
      if (props.variant === 'landing' || props.variant === 'auth') return false;
      return isAdminRoute.value || isUserRoute.value;
    });

    const userRole = computed(() => {
      if (isAdminRoute.value) return 'admin';
      if (isUserRoute.value) return 'user';
      return 'user';
    });

    const toggleSidebar = () => {
      sidebarOpen.value = !sidebarOpen.value;
    };

    const closeSidebar = () => {
      sidebarOpen.value = false;
    };

    const toggleCollapse = () => {
      sidebarCollapsed.value = !sidebarCollapsed.value;
    };

    const navItems = computed(() => {
      if (userRole.value === 'admin') {
        return [
          { name: 'AdminDashboard', label: 'Facility Dashboard', icon: 'DashboardIcon', badge: null },
          { name: 'AllUsers', label: 'Users & Drivers', icon: 'UsersIcon', badge: null },
          { name: 'AddParkingLot', label: 'Create Facility', icon: 'PlusIcon', badge: null },
          { name: 'AdminSummary', label: 'Revenue Analytics', icon: 'ChartIcon', badge: null }
        ];
      }
      if (userRole.value === 'user') {
        return [
          { name: 'UserDashboard', label: 'Find Parking', icon: 'SearchIcon', badge: null },
          { name: 'UserHistory', label: 'Parking History', icon: 'ClockIcon', badge: null },
          { name: 'UserSummary', label: 'My Sessions & Stats', icon: 'ChartIcon', badge: null }
        ];
      }
      return [];
    });

    const userInfo = computed(() => {
      try {
        const token = localStorage.getItem('token');
        if (!token) return null;
        const payloadPart = token.split('.')[1];
        if (!payloadPart) return null;
        const base64 = payloadPart.replace(/-/g, '+').replace(/_/g, '/');
        const padded = base64 + '='.repeat((4 - (base64.length % 4)) % 4);
        const payload = JSON.parse(atob(padded));
        return { name: payload.username || payload.sub, role: payload.role };
      } catch {
        return null;
      }
    });

    const userInitials = computed(() => {
      if (!userInfo.value?.name) return 'U';
      return userInfo.value.name.charAt(0).toUpperCase();
    });

    const logout = () => {
      localStorage.removeItem('token');
      router.push('/login');
    };

    return {
      showSidebar,
      userRole,
      userInfo,
      userInitials,
      navItems,
      logout,
      toggleSidebar,
      closeSidebar,
      toggleCollapse,
      sidebarOpen,
      sidebarCollapsed,
      isDesktop,
      isAuthRoute,
      theme,
      toggleTheme
    };
  }
};
</script>

<template>
  <div
    class="app-shell"
    :class="[
      `app-shell--${variant}`,
      {
        'app-shell--sidebar-open': sidebarOpen,
        'app-shell--sidebar-collapsed': sidebarCollapsed && isDesktop
      }
    ]"
  >
    <!-- Mobile Top Header Bar (Shown only on mobile/tablet screens when authenticated) -->
    <header v-if="showSidebar && !isDesktop" class="app-shell__mobile-bar" role="banner">
      <button
        type="button"
        class="app-shell__mobile-toggle-btn"
        @click="toggleSidebar"
        :aria-expanded="sidebarOpen"
        aria-label="Toggle navigation menu"
      >
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round">
          <line x1="3" y1="6" x2="21" y2="6" />
          <line x1="3" y1="12" x2="21" y2="12" />
          <line x1="3" y1="18" x2="21" y2="18" />
        </svg>
      </button>

      <div class="app-shell__mobile-brand">
        <div class="app-shell__mobile-logo">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round">
            <path d="M6 3H13C16.866 3 20 6.13401 20 10C20 13.866 16.866 17 13 17H10V21H6V3Z"/>
            <path d="M10 7H12.5C14.433 7 16 8.567 16 10.5C16 12.433 14.433 14 12.5 10H10V7Z"/>
          </svg>
        </div>
        <span class="app-shell__mobile-title">ParkSync</span>
      </div>

      <div class="app-shell__mobile-actions">
        <button
          type="button"
          class="app-shell__mobile-icon-btn"
          @click="toggleTheme"
          aria-label="Toggle theme"
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
        <div class="app-shell__mobile-avatar">{{ userInitials }}</div>
      </div>
    </header>

    <div class="app-shell__body">
      <!-- Left Sidebar Container -->
      <aside
        v-if="showSidebar"
        class="app-sidebar"
        :class="{
          'app-sidebar--open': sidebarOpen,
          'app-sidebar--collapsed': sidebarCollapsed && isDesktop
        }"
        :aria-hidden="isDesktop ? 'false' : String(!sidebarOpen)"
      >
        <AppSidebar
          :collapsed="sidebarCollapsed && isDesktop"
          :items="navItems"
          :user-info="userInfo"
          :user-role="userRole"
          :theme="theme"
          :is-mobile="!isDesktop"
          @navigate="closeSidebar"
          @close="closeSidebar"
          @toggle-collapse="toggleCollapse"
          @logout="logout"
          @toggle-theme="toggleTheme"
        />
      </aside>

      <!-- Mobile Backdrop Overlay -->
      <transition name="fade">
        <div
          v-if="showSidebar && sidebarOpen && !isDesktop"
          class="app-sidebar-overlay"
          @click="closeSidebar"
          aria-hidden="true"
        />
      </transition>

      <!-- Main View Content -->
      <main
        class="app-main"
        :class="{
          'app-main--with-sidebar': showSidebar && isDesktop && !sidebarCollapsed,
          'app-main--collapsed': showSidebar && isDesktop && sidebarCollapsed
        }"
      >
        <!-- Desktop Quick Expand Bar when Collapsed -->
        <!-- <div v-if="showSidebar && isDesktop && sidebarCollapsed" class="app-main__expand-strip">
          <button
            type="button"
            class="app-main__expand-btn"
            @click="toggleCollapse"
            title="Expand sidebar navigation"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect width="18" height="18" x="3" y="3" rx="2" />
              <path d="M9 3v18" />
              <path d="m12 9 3 3-3 3" />
            </svg>
            <span>Expand Navigation</span>
          </button>
        </div> -->

        <slot />
      </main>
    </div>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-bg-page);
}

.app-shell__body {
  flex: 1;
  display: flex;
  min-width: 0;
  min-height: 0;
  position: relative;
}

/* Mobile Top Header Bar */
.app-shell__mobile-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
  padding: 0 16px;
  background: var(--color-bg-white);
  border-bottom: 1px solid var(--color-border-default);
  position: sticky;
  top: 0;
  z-index: 100;
  flex-shrink: 0;
}

.app-shell__mobile-toggle-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border-radius: 8px;
  background: transparent;
  border: 1px solid var(--color-border-default);
  color: var(--color-text-primary);
  cursor: pointer;
}

.app-shell__mobile-brand {
  display: flex;
  align-items: center;
  gap: 8px;
}

.app-shell__mobile-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
  border-radius: 7px;
  color: #FFFFFF;
}

.app-shell__mobile-title {
  font-size: 16px;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--color-text-primary);
}

.app-shell__mobile-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.app-shell__mobile-icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: transparent;
  border: 1px solid var(--color-border-default);
  color: var(--color-text-secondary);
  cursor: pointer;
}

.app-shell__mobile-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: #1E293B;
  color: #FFFFFF;
  font-size: 13px;
  font-weight: 700;
}

/* Sidebar Container */
.app-sidebar {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: 260px;
  height: 100vh;
  background: var(--color-bg-white);
  border-right: 1px solid var(--color-border-default);
  z-index: 200;
  transition: width 0.25s cubic-bezier(0.16, 1, 0.3, 1), transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Desktop Collapsed */
.app-sidebar--collapsed {
  width: 68px;
}

/* Mobile Screen Behavior */
@media (max-width: 1024px) {
  .app-sidebar {
    width: 280px;
    z-index: 500;
    transform: translateX(-100%);
    box-shadow: none;
  }

  .app-sidebar--open {
    transform: translateX(0);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  }
}

/* Mobile Backdrop Overlay */
.app-sidebar-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  backdrop-filter: blur(4px);
  z-index: 499;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Main Content Area */
.app-main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  transition: margin-left 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.app-main--with-sidebar {
  margin-left: 260px;
}

.app-main--collapsed {
  margin-left: 68px;
}

/* Desktop Quick Expand Strip when Collapsed */
.app-main__expand-strip {
  padding: 12px 24px 0 24px;
}

.app-main__expand-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  font-size: 12px;
  font-weight: 700;
  color: var(--color-brand-primary);
  background: var(--color-brand-primary-light, rgba(37, 99, 235, 0.08));
  border: 1px solid rgba(37, 99, 235, 0.2);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.app-main__expand-btn:hover {
  background: var(--color-brand-primary);
  color: #FFFFFF;
}

/* Responsive adjustment for Mobile */
@media (max-width: 1024px) {
  .app-main--with-sidebar,
  .app-main--collapsed {
    margin-left: 0;
  }
}

/* Landing & Auth Variants */
.app-shell--landing .app-main,
.app-shell--auth .app-main {
  margin-left: 0;
}

.app-shell--auth .app-main {
  align-items: center;
  justify-content: center;
  padding: 32px 16px;
}
</style>