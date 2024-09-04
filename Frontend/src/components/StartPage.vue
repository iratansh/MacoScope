<template>
  <div :class="['start-page', isDarkMode ? 'dark' : 'light']">
    <ErrorToast
      v-if="errorMessage"
      :title="errorTitle"
      :message="errorMessage"
      @close="errorMessage = ''"
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
              <button type="button" class="toggle-password" @click="togglePasswordVisibility">
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
      </section>
    </main>
  </div>
</template>

<script>
import axios from 'axios'
import ErrorToast from './ErrorToast.vue'

export default {
  name: 'StartPage',
  components: {
    ErrorToast
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
  methods: {
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode
      const modeButton = document.querySelector('.mode-toggle')
      if (this.isDarkMode) {
        modeButton.style.backgroundColor = '#121212'
        modeButton.style.color = '#ffffff'
      } else {
        modeButton.style.backgroundColor = '#f0f4f8'
        modeButton.style.color = '#333333'
      }
    },
    toggleAuthMode() {
      this.isRegistering = !this.isRegistering
    },
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword
    },
    handleLogin() {
      console.log('Login:', this.email, this.password)

      const payload = {
        email: this.email,
        password: this.password
      }

      axios
        .post('http://127.0.0.1:8080/auth/login/', payload)
        .then((response) => {
          console.log('Login response:', response.data)
          if (response.data.success && response.data.is_active) {
            this.$router.push('/dashboard')
          } else if (!response.data.is_active) {
            this.errorMessage =
              'Your account is not activated. Please check your email to activate your account.'
          } else {
            this.errorMessage = response.data.message
          }
        })
        .catch((error) => {
          console.error('Error during login:', error)
          if (error.response && error.response.status === 404) {
            this.errorMessage = 'Account does not exist. Please register first.'
          } else if (error.response && error.response.status === 401) {
            this.errorMessage = 'Invalid email or password.'
          } else if (error.response && error.response.status === 403) {
            this.errorMessage = 'Your account is not activated. Please check your email.'
          } else {
            this.errorMessage = 'An error occurred while trying to log in. Please try again later.'
          }
        })
    },

    handleRegister() {
      console.log('Registering with:', this.email, this.password)
      const payload = {
        email: this.email,
        password: this.password
      }
      console.log(payload)

      fetch('http://127.0.0.1:8080/auth/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            this.errorTitle = 'Success'
            this.errorMessage = 'Please check your email to verify your account.'
          } else {
            this.errorMessage = 'Error: ' + data.message
          }
        })
        .catch((error) => {
          console.error('Error during registration:', error)
          this.errorMessage = 'An error occurred while trying to register. Please try again later.'
        })
    },

    validateEmail() {
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailPattern.test(this.email)) {
        this.errorMessage = 'Please enter a valid email address'
      }
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
  background-color: #121212;
  color: #ffffff;
}
</style>
