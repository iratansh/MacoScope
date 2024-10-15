<template>
  <div :class="['reset-password-page', isDarkMode ? 'dark' : 'light']" style="height: 100vh;">
    <header>
      <h1>Password Reset</h1>
    </header>

    <main class="auth-container">
      <section class="auth-box">
        <h2>Enter your new password</h2>
        <form @submit.prevent="resetPassword">
          <div class="input-group">
            <label for="password">New Password</label>
            <input v-model="password" type="password" id="password" required />
          </div>
          <button type="submit" class="auth-button">Reset Password</button>
        </form>

        <ErrorToast
          v-if="errorMessage"
          :title="errorTitle"
          :message="errorMessage"
          @close="errorMessage = ''"
        />
        <UpdateToast
          v-if="updateMessage"
          :title="updateTitle"
          :message="updateMessage"
          @close="updateMessage = ''"
        />
      </section>
    </main>
  </div>
</template>

<script>
import axios from 'axios'
import ErrorToast from './ErrorToast.vue'
import UpdateToast from './UpdateToast.vue'

export default {
  name: 'ResetPassword',
  components: { ErrorToast, UpdateToast },
  data() {
    return {
      password: '',
      errorMessage: '',
      updateMessage: '',
      errorTitle: 'Error',
      updateTitle: 'Success',
      isDarkMode: false,
      uidb64: this.$route.params.uidb64,
      token: this.$route.params.token
    }
  },
  methods: {
    resetPassword() {
      axios
        .post(`http://127.0.0.1:8080/auth/reset-password/${this.uidb64}/${this.token}/`, {
          password: this.password
        })
        .then((response) => {
          this.updateMessage = 'Your password has been reset successfully.'
          this.$router.push('/')
        })
        .catch((error) => {
          console.error('Error during password reset:', error)
          this.errorMessage = 'Failed to reset password. Please try again.'
        })
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
  margin: auto;
  margin-top: 100px
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

.forgot-password {
  text-align: center;
  margin-top: 10px;
}

.forgot-password span {
  color: var(--link-color);
  cursor: pointer;
  font-weight: bold;
}
</style>
