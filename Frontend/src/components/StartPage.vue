<template>
  <div :class="['start-page', isDarkMode ? 'dark' : 'light']">
    <ErrorToast
      v-if="errorMessage"
      :title="errorTitle"
      :message="errorMessage"
      @close="errorMessage = ''"
      class="error-toast"
    />
    <UpdateToast
      v-if="updateMessage"
      :title="updateTitle"
      :message="updateMessage"
      @close="updateMessage = ''"
      class="update-toast"
    />
    <header class="start-page-header">
      <h1>MacroScope</h1>
      <p>Get personalized insights and predictions based on key economic indicators.</p>
      <button @click="toggleDarkMode" class="mode-toggle" style="margin: auto">
        {{ isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode' }}
      </button>
    </header>

    <main class="auth-container">
      <section class="auth-box">
        <h2>{{ isRegistering ? 'Register' : 'Login' }}</h2>
        <form @submit.prevent="isRegistering ? handleRegister() : handleLogin()">
          <div class="input-group">
            <label for="email">{{ isRegistering ? 'Email' : 'Email' }}</label>
            <input v-model="email" type="email" id="email" required @blur="validateEmail" />
          </div>

          <div class="input-group">
            <label for="password">{{ isRegistering ? 'Password' : 'Password' }}</label>
            <div class="password-wrapper">
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                id="password"
                required
              />
              <button
                type="button"
                class="toggle-password"
                @click="togglePasswordVisibility"
                aria-label="Toggle password visibility"
              >
                {{ showPassword ? 'Hide' : 'Show' }}
              </button>
            </div>
          </div>
          <button type="submit" class="auth-button">
            {{ isRegistering ? 'Register' : 'Login' }}
          </button>
        </form>
        <p class="switch-auth-mode">
          {{ isRegistering ? 'Already have an account?' : 'New User?' }}
          <span @click="toggleAuthMode">
            {{ isRegistering ? 'Login' : 'Register' }}
          </span>
        </p>
        <p v-if="!isRegistering" class="forgot-password">
          <span @click="navigateToForgotPassword">Forgot Password?</span>
        </p>
      </section>
    </main>
  </div>
</template>

<script>
import axios from 'axios'
import ErrorToast from './ErrorToast.vue'
import UpdateToast from './UpdateToast.vue'

axios.defaults.withCredentials = true
export default {
  name: 'StartPage',
  components: {
    ErrorToast,
    UpdateToast
  },
  data() {
    return {
      isDarkMode: false,
      isRegistering: false,
      email: '',
      password: '',
      showPassword: false,
      errorMessage: '',
      errorTitle: 'Error'
    }
  },
  created() {
    const savedMode = localStorage.getItem('isDarkMode')
    this.isDarkMode = savedMode === 'true'
  },
  methods: {
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode
      localStorage.setItem('isDarkMode', this.isDarkMode)
    },
    toggleAuthMode() {
      this.isRegistering = !this.isRegistering
      this.email = ''
      this.password = ''
    },
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword
    },
    handleLogin() {
      const payload = { email: this.email, password: this.password }

      axios
        .post('https://mmacroscope.me/auth/login/', payload, { withCredentials: true })
        .then((response) => {
          const { success, is_active, username, message } = response.data

          if (success && is_active) {
            // Save username and session data in localStorage
            localStorage.setItem('username', username)

            // Optionally store the session ID if needed for other requests
            const sessionId = response.headers['set-cookie']
            if (sessionId) {
              localStorage.setItem('sessionid', sessionId)
            }

            // Delay to ensure session cookie is set before navigating
            setTimeout(() => {
              this.$router.push('/dashboard')
            }, 100) // Adjust the delay if necessary
          } else if (!is_active) {
            // If the account is not activated
            this.errorMessage =
              'Your account is not activated. Please check your email to activate your account.'
          } else {
            // General failure message from the backend
            this.errorMessage = message || 'Login failed. Please try again.'
          }
        })
        .catch((error) => {
          // Handle different error scenarios with more detailed messages
          if (error.response) {
            const status = error.response.status

            if (status === 404) {
              this.errorMessage = 'Account does not exist. Please register first.'
            } else if (status === 401) {
              this.errorMessage = 'Invalid email or password.'
            } else if (status === 403) {
              this.errorMessage = 'Your account is not activated.'
            } else {
              this.errorMessage = 'An error occurred during login. Please try again later.'
            }
          } else {
            this.errorMessage = 'Network error. Please check your connection and try again.'
          }
        })
    },

    handleRegister() {
      const payload = { email: this.email, password: this.password }
      fetch('https://mmacroscope.me/auth/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            this.updateTitle = 'Success'
            this.updateMessage = 'Please check your email to verify your account.'
          } else {
            this.errorMessage = 'Error: ' + data.message
          }
        })
        .catch((error) => {
          this.errorMessage = 'An error occurred during registration. Please try again later.'
        })
    },
    validateEmail() {
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailPattern.test(this.email)) {
        this.errorMessage = 'Please enter a valid email address'
      }
    },
    navigateToForgotPassword() {
      this.$router.push('/forgot-password')
    }
  }
}
</script>

<style scoped>
.start-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  padding: 20px;
  transition:
    background-color 0.3s,
    color 0.3s;
}

.start-page-header {
  text-align: center;
  margin-bottom: 40px;
  position: relative;
}

.start-page-header h1 {
  font-size: 2.5rem;
}

.start-page-header p {
  font-size: 1.2rem;
  margin-bottom: 20px;
}

.mode-toggle {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 8px 12px;
  border: 2px solid currentColor;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9rem;
  transition:
    background-color 0.3s,
    color 0.3s;
}

.auth-container {
  display: flex;
  justify-content: center;
  width: 100%;
  max-width: 400px;
}

.auth-box {
  background: var(--box-bg);
  color: var(--text-color);
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
  width: 100%;
}

.auth-box h2 {
  text-align: center;
  margin-bottom: 20px;
}

.input-group {
  margin-bottom: 15px;
}

.input-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.input-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.password-wrapper {
  position: relative;
  width: 100%;
}

@media (max-width: 768px) {
  .auth-box {
    width: 90%;
  }
}

.toggle-password {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--link-color);
  cursor: pointer;
  font-size: 0.9rem;
  outline: none;
}

.auth-button {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  background-color: var(--button-bg);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.auth-button:hover {
  background-color: var(--button-hover-bg);
}

.switch-auth-mode {
  text-align: center;
  margin-top: 15px;
}

.switch-auth-mode span {
  color: var(--link-color);
  cursor: pointer;
  font-weight: bold;
}

.light {
  --box-bg: #ffffff;
  --text-color: #333333;
  --button-bg: #007bff;
  --button-hover-bg: #0056b3;
  --link-color: #007bff;
  background-color: #f0f4f8;
  color: #333333;
}
.dark {
  --box-bg: #333333;
  --text-color: #ffffff;
  --button-bg: #007bff;
  --button-hover-bg: #0056b3;
  --link-color: #80c0ff;
  background-color: #1c1c1c;
  color: #ffffff;
}

.forgot-password {
  text-align: center;
  margin-top: 10px;
}

.forgot-password span {
  color: var(--link-color);
  cursor: pointer;
  font-weight: bold;
}

.auth-button {
  transition: transform 0.2s ease;
}
.auth-button:hover {
  transform: translateY(-2px);
}
</style>
