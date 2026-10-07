<script>
import { auth } from '@/api/client';
import { AppCard, AppButton, AppInput } from '@/components/ui';

export default {
  name: 'RegisterPage',
  components: { AppCard, AppButton, AppInput },
  data() {
    return {
      formData: {
        email: '',
        password: '',
        username: '',
        address: '',
        pincode: ''
      },
      message: '',
      isSuccess: false,
      loading: false
    };
  },
  mounted() {
    document.title = 'Create Driver Account — ParkSync';
  },
  methods: {
    async registerUser() {
      try {
        this.loading = true;
        this.message = '';
        const { data, error } = await auth.register(this.formData);
        if (error) {
          this.isSuccess = false;
          this.message = error.message || 'Registration failed';
          return;
        }

        this.isSuccess = true;
        this.message = data?.message || 'Account created successfully! Redirecting to sign in...';
        localStorage.setItem('registered_msg', 'Account registered! Please sign in with your credentials.');
        setTimeout(() => {
          this.$router.push('/login');
        }, 1200);
      } catch (err) {
        console.error('Registration error:', err);
        this.isSuccess = false;
        this.message = 'Network error during registration';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<template>
  <div class="register-page">
    <div class="register-page__card-wrap">
      <!-- Brand Header -->
      <div class="register-brand">
        <div class="register-brand__logo">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round">
            <path d="M6 3H13C16.866 3 20 6.13401 20 10C20 13.866 16.866 17 13 17H10V21H6V3Z"/>
            <path d="M10 7H12.5C14.433 7 16 8.567 16 10.5C16 12.433 14.433 14 12.5 10H10V7Z"/>
          </svg>
        </div>
        <span class="register-brand__name">ParkSync</span>
      </div>

      <AppCard class="register-page__card">
        <template #header>
          <div class="register-page__header">
            <h2>Create Account</h2>
            <p>Join the next-generation smart mobility network</p>
          </div>
        </template>

        <form @submit.prevent="registerUser" class="register-page__form">
          <AppInput
            v-model="formData.username"
            label="Full Name"
            placeholder="Alex Rivera"
            required
            autocomplete="name"
          />

          <AppInput
            v-model="formData.email"
            label="Email Address"
            type="email"
            placeholder="alex.rivera@gmail.com"
            required
            autocomplete="email"
          />

          <AppInput
            v-model="formData.password"
            label="Password"
            type="password"
            placeholder="Create a secure password"
            required
            autocomplete="new-password"
            showPassword
          />

          <AppInput
            v-model="formData.address"
            label="Residential Address"
            type="textarea"
            placeholder="Street address &amp; city"
            required
            :rows="2"
          />

          <AppInput
            v-model="formData.pincode"
            label="Postal Code"
            placeholder="e.g. 10005"
            required
            autocomplete="postal-code"
          />

          <div
            v-if="message"
            class="register-page__alert"
            :class="isSuccess ? 'register-page__alert--success' : 'register-page__alert--error'"
            role="alert"
          >
            {{ message }}
          </div>

          <AppButton variant="primary" type="submit" size="lg" fullWidth :loading="loading">
            Register Driver Profile
          </AppButton>

          <div class="register-page__footer">
            <span>Already have an account?</span>
            <router-link to="/login" class="register-page__link">Sign in</router-link>
          </div>
        </form>
      </AppCard>
    </div>
  </div>
</template>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-6, 24px);
  background: var(--color-bg-page, #F7F9FC);
}

.register-page__card-wrap {
  width: 100%;
  max-width: 480px;
  display: flex;
  flex-direction: column;
  gap: var(--space-4, 16px);
  margin: var(--space-4, 16px) auto;
}

.register-brand {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.register-brand__logo {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  background: var(--color-navy-deep, #0B1220);
  border-radius: var(--radius-md, 12px);
  color: #FFFFFF;
}

.register-brand__name {
  font-size: 22px;
  font-weight: 800;
  color: var(--color-text-primary, #111827);
  letter-spacing: -0.02em;
}

.register-page__card {
  width: 100%;
  box-shadow: var(--shadow-lg, 0 12px 24px rgba(15, 23, 42, 0.08));
}

.register-page__header {
  text-align: center;
}

.register-page__header h2 {
  margin: 0;
  font-size: 22px;
  font-weight: 800;
  color: var(--color-text-primary, #111827);
}

.register-page__header p {
  margin: 4px 0 0;
  color: var(--color-text-secondary, #64748B);
  font-size: 13px;
}

.register-page__form {
  display: flex;
  flex-direction: column;
  gap: var(--space-4, 16px);
}

.register-page__alert {
  padding: 10px 14px;
  border-radius: var(--radius-md, 10px);
  font-size: 13px;
  text-align: center;
  font-weight: 600;
}

.register-page__alert--success {
  background: var(--color-status-available-bg, #DCFCE7);
  border: 1px solid var(--color-status-available, #16A34A);
  color: var(--color-status-available, #16A34A);
}

.register-page__alert--error {
  background: var(--color-status-occupied-bg, #FEE2E2);
  border: 1px solid var(--color-status-occupied, #EF4444);
  color: var(--color-status-occupied, #EF4444);
}

.register-page__footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: var(--space-2, 8px);
  font-size: 13px;
  color: var(--color-text-secondary, #64748B);
}

.register-page__link {
  color: var(--color-brand-primary, #2563EB);
  font-weight: 700;
  text-decoration: none;
}

.register-page__link:hover {
  text-decoration: underline;
}
</style>