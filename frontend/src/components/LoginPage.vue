<script>
import { auth } from '@/api/client';
import { AppCard, AppButton, AppInput } from '@/components/ui';

export default {
  name: 'LoginPage',
  components: { AppCard, AppButton, AppInput },
  data() {
    return {
      formData: {
        email: '',
        password: ''
      },
      message: '',
      loading: false
    };
  },
  mounted() {
    document.title = 'Sign In — ParkSync Mobility';
    const regMsg = localStorage.getItem('registered_msg');
    if (regMsg) {
      this.message = regMsg;
      localStorage.removeItem('registered_msg');
    }
  },
  methods: {
    setDemo(role) {
      if (role === 'admin') {
        this.formData.email = 'admin@gmail';
        this.formData.password = 'admin123';
      } else {
        this.formData.email = 'user1@gmail.com';
        this.formData.password = 'user123';
      }
      this.loginUser();
    },
    async loginUser() {
      this.message = '';
      if (!this.formData.email || !this.formData.password) {
        this.message = 'Please enter your email and password';
        return;
      }

      try {
        this.loading = true;
        const { data, error } = await auth.login(this.formData.email, this.formData.password);
        if (error) {
          this.message = error.message || 'Invalid email or password';
          return;
        }

        localStorage.setItem('token', data.access_token);
        const payload = auth.getPayload();
        if (payload?.role === 'admin') {
          this.$router.push('/admin');
        } else if (payload?.role === 'user') {
          this.$router.push('/user');
        } else {
          this.message = 'Invalid user credentials';
        }
      } catch (err) {
        console.error('Login error:', err);
        this.message = 'Network error during sign in';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<template>
  <div class="login-page">
    <div class="login-page__card-wrap">
      <!-- Brand Header -->
      <div class="login-brand">
        <div class="login-brand__logo">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round">
            <path d="M6 3H13C16.866 3 20 6.13401 20 10C20 13.866 16.866 17 13 17H10V21H6V3Z"/>
            <path d="M10 7H12.5C14.433 7 16 8.567 16 10.5C16 12.433 14.433 14 12.5 10H10V7Z"/>
          </svg>
        </div>
        <span class="login-brand__name">ParkSync</span>
      </div>

      <AppCard class="login-page__card">
        <template #header>
          <div class="login-page__header">
            <h2>Welcome Back</h2>
            <p>Access your driver dashboard or operator console</p>
          </div>
        </template>

        <!-- 1-Click Demo Credentials Box -->
        <div class="demo-box">
          <span class="demo-box__title">Portfolio Evaluation Quick-Sign In:</span>
          <div class="demo-box__actions">
            <button type="button" class="demo-btn demo-btn--admin" @click="setDemo('admin')">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="7" height="7"/>
                <rect x="14" y="3" width="7" height="7"/>
                <rect x="14" y="14" width="7" height="7"/>
                <rect x="3" y="14" width="7" height="7"/>
              </svg>
              <span>Demo Admin</span>
            </button>
            <button type="button" class="demo-btn demo-btn--driver" @click="setDemo('driver')">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.4-1.7-1.1-2.2l-2.4-1.8H5.5L3.1 10.8C2.4 11.3 2 12.1 2 13v3c0 .6.4 1 1 1h2" />
                <circle cx="7" cy="17" r="2" />
                <path d="M9 17h6" />
                <circle cx="17" cy="17" r="2" />
              </svg>
              <span>Demo Driver</span>
            </button>
          </div>
        </div>

        <form @submit.prevent="loginUser" class="login-page__form">
          <AppInput
            v-model="formData.email"
            label="Email Address"
            type="email"
            placeholder="driver@gmail.com"
            required
            autocomplete="email"
          />

          <AppInput
            v-model="formData.password"
            label="Password"
            type="password"
            placeholder="Enter your password"
            required
            autocomplete="current-password"
            showPassword
          />

          <div v-if="message" class="login-page__alert" role="alert">
            {{ message }}
          </div>

          <AppButton variant="primary" type="submit" size="lg" fullWidth :loading="loading">
            Sign In to Account
          </AppButton>

          <div class="login-page__footer">
            <span>New to ParkSync?</span>
            <router-link to="/register" class="login-page__link">Create account</router-link>
          </div>
        </form>
      </AppCard>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-6, 24px);
  background: var(--color-bg-page, #F7F9FC);
}

.login-page__card-wrap {
  width: 100%;
  max-width: 440px;
  display: flex;
  flex-direction: column;
  gap: var(--space-4, 16px);
}

.login-brand {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.login-brand__logo {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  background: var(--color-navy-deep, #0B1220);
  border-radius: var(--radius-md, 12px);
  color: #FFFFFF;
}

.login-brand__name {
  font-size: 22px;
  font-weight: 800;
  color: var(--color-text-primary, #111827);
  letter-spacing: -0.02em;
}

.login-page__card {
  width: 100%;
  box-shadow: var(--shadow-lg, 0 12px 24px rgba(15, 23, 42, 0.08));
}

.login-page__header {
  text-align: center;
}

.login-page__header h2 {
  margin: 0;
  font-size: 22px;
  font-weight: 800;
  color: var(--color-text-primary, #111827);
}

.login-page__header p {
  margin: 4px 0 0;
  color: var(--color-text-secondary, #64748B);
  font-size: 13px;
}

/* Demo Box */
.demo-box {
  background: var(--color-bg-muted, #F8FAFC);
  border: 1px solid var(--color-border-default, #E2E8F0);
  border-radius: var(--radius-md, 12px);
  padding: 12px;
  margin-bottom: var(--space-4, 16px);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.demo-box__title {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text-secondary, #64748B);
}

.demo-box__actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.demo-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 10px;
  border-radius: 8px;
  border: 1px solid var(--color-border-strong, #CBD5E1);
  background: #FFFFFF;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.demo-btn--admin {
  color: var(--color-navy-deep, #0B1220);
}

.demo-btn--driver {
  color: var(--color-brand-primary, #2563EB);
  border-color: var(--color-brand-primary, #2563EB);
}

.demo-btn:hover {
  background: var(--color-bg-muted, #F1F5F9);
  transform: translateY(-1px);
}

.login-page__form {
  display: flex;
  flex-direction: column;
  gap: var(--space-4, 16px);
}

.login-page__alert {
  padding: 10px 14px;
  border-radius: var(--radius-md, 10px);
  background: var(--color-status-occupied-bg, #FEE2E2);
  border: 1px solid var(--color-status-occupied, #EF4444);
  color: var(--color-status-occupied, #EF4444);
  font-size: 13px;
  text-align: center;
  font-weight: 600;
}

.login-page__footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: var(--space-2, 8px);
  font-size: 13px;
  color: var(--color-text-secondary, #64748B);
}

.login-page__link {
  color: var(--color-brand-primary, #2563EB);
  font-weight: 700;
  text-decoration: none;
}

.login-page__link:hover {
  text-decoration: underline;
}
</style>