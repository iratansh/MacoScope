<template>
  <div :class="['start-page', isDarkMode ? 'dark' : 'light']">
    <header class="start-page-header">
      <h1>MacroScope</h1>
      <p>Get personalized insights and predictions based on key economic indicators.</p>
      <button @click="toggleDarkMode" class="mode-toggle" style="margin: auto;">
        {{ isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode' }}
      </button>
    </header>

    <main class="auth-container">
      <section class="auth-box">
        <h2>{{ isRegistering ? 'Register' : 'Login' }}</h2>
        <form @submit.prevent="isRegistering ? handleRegister : handleLogin">
          <div class="input-group">
            <label for="email">{{ isRegistering ? 'Email' : 'Email' }}</label>
            <input v-model="email" type="email" id="email" required />
          </div>
          <div class="input-group">
            <label for="password">{{ isRegistering ? 'Password' : 'Password' }}</label>
            <input v-model="password" type="password" id="password" required />
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
export default {
  name: 'StartPage',
  data() {
    return {
      isDarkMode: false,
      isRegistering: false,
      email: '',
      password: ''
    }
  },
  methods: {
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode
    },
    toggleAuthMode() {
      this.isRegistering = !this.isRegistering
    },
    handleLogin() {
      console.log('Login, ', this.email, this.password)
      this.$router.push('/dashboard')
    },
    handleRegister() {
      console.log('Register ', this.email, this.password)
      this.$router.push('/dashboard')
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
  background-color: transparent;
  border: 2px solid currentColor;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9rem;
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
