<template>
  <div :class="['profile-page', theme]">
    <NavBar @themeChanged="updateTheme" />

    <button v-if="!isSidebarOpen" class="openbtn" @click="openSidebar">☰</button>
    <UpdateToast
      v-if="updateMessage"
      :title="updateTitle"
      :message="updateMessage"
      @close="updateMessage = ''"
      class="update-toast"
    />
    <ErrorToast
      v-if="errorMessage"
      :title="errorTitle"
      :message="errorMessage"
      @close="errorMessage = ''"
      class="error-toast"
    />

    <aside :class="['sidebar', theme]" ref="sidebar">
      <a href="javascript:void(0)" class="closebtn" @click="closeSidebar">&times;</a>
      <ul>
        <li><a href="#" @click="showSection('account')">Account</a></li>
        <li><a href="#preferences" @click="showSection('preferences')">Preferences</a></li>
        <li><a href="#security" @click="showSection('security')">Security</a></li>
        <li><a href="#support" @click="showSection('support')">Support</a></li>
      </ul>
    </aside>

    <section class="profile-content">
      <div v-if="currentSection === 'account'" class="user-info">
        <h2>User Information</h2>
        <p><strong>Full Name:</strong> {{ fullName }}</p>
        <p><strong>Email:</strong> {{ email }}</p>
        <p><strong>Member since:</strong> {{ memberSince }}</p>
      </div>

      <div v-if="currentSection === 'preferences'" class="preferences-section">
        <h2>Preferences</h2>
        <form @submit.prevent="updatePreferences">
          <div class="form-group">
            <label style="margin-top: 50px" for="notifications">Notifications:</label>
            <select style="width: 100px" id="notifications" v-model="preferences.notifications">
              <option value="enabled">Enabled</option>
              <option value="disabled">Disabled</option>
            </select>
          </div>
          <button type="submit" style="margin-top: 250px">Save Preferences</button>
        </form>
      </div>

      <div v-if="currentSection === 'security'" class="security-section">
        <h2>Security</h2>
        <form @submit.prevent="updateSecurity">
          <div class="form-group">
            <label for="email">Email:</label>
            <input
              type="email"
              id="email"
              v-model="security.email"
              placeholder="Enter your new email"
              required
              style="border: 1px solid black; width: 200px"
            />
          </div>

          <div class="form-group">
            <label for="password">New Password:</label>
            <input
              type="password"
              id="password"
              v-model="security.password"
              placeholder="Enter your new password"
              style="border: 1px solid black; width: 200px"
              required
            />
          </div>

          <div class="form-group">
            <label for="confirmPassword">Retype Password:</label>
            <input
              type="password"
              id="confirmPassword"
              v-model="security.confirmPassword"
              placeholder="Retype your new password"
              style="border: 1px solid black; width: 200px"
              required
            />
          </div>

          <button type="submit" :disabled="passwordMismatch" style="margin-top: 50px">
            Update Security Info
          </button>
        </form>
      </div>

      <div v-if="currentSection === 'support'" class="support-section">
        <h2>Support</h2>
        <p>Contact:</p>
        <p><strong>Email:</strong> iratansh@ualberta.ca</p>
      </div>
    </section>
  </div>
</template>

<script>
import NavBar from './NavBar.vue'
import axios from 'axios'
import UpdateToast from './UpdateToast.vue'
import ErrorToast from './ErrorToast.vue'

axios.defaults.withCredentials = true
export default {
  name: 'ProfilePage',
  components: {
    NavBar,
    UpdateToast,
    ErrorToast
  },
  data() {
    return {
      theme: 'light',
      isSidebarOpen: false,
      currentSection: 'account',
      preferences: {
        notifications: 'enabled'
      },
      security: {
        email: '',
        password: '',
        confirmPassword: ''
      },
      passwordMismatch: false,
      errorMessage: '',
      updateMessage: '',
      errorTitle: 'Error',
      updateTitle: 'Success',
      fullName: '',
      email: '',
      memberSince: ''
    }
  },
  created() {
    this.loadTheme()
  },
  methods: {
    loadTheme() {
      const savedTheme = localStorage.getItem('theme') || 'light'
      this.theme = savedTheme
    },
    openSidebar() {
      this.isSidebarOpen = true
      this.$refs.sidebar.style.width = '250px'
    },
    closeSidebar() {
      this.isSidebarOpen = false
      this.$refs.sidebar.style.width = '0'
    },
    showSection(section) {
      this.currentSection = section
      this.closeSidebar()
    },
    updatePreferences() {
      alert('Preferences saved!')
    },
    getAccountInfo() {
      const sessionId = localStorage.getItem('session_id') // Retrieve session ID from local storage

      if (!sessionId) {
        this.errorMessage = 'No session ID found. Please log in again.'
        return
      }

      axios
        .post(
          'https://mmacroscope.me/auth/account-info/',
          {},
          {
            withCredentials: true,
            headers: {
              'X-Session-ID': sessionId, // Pass the session ID as a custom header
              'X-CSRFToken': this.getCsrfToken()
            }
          }
        )
        .then((response) => {
          if (response.status === 200) {
            this.fullName = response.data.full_name
            this.email = response.data.email
            this.memberSince = response.data.member_since
            this.errorMessage = ''
          } else {
            this.errorMessage = response.data.message || 'Unable to retrieve user information.'
          }
        })
        .catch((error) => {
          this.errorMessage =
            error.response?.data?.message || 'An error occurred while retrieving user information.'
        })
    },

    getCsrfToken() {
      const cookieValue = document.cookie
        .split('; ')
        .find((row) => row.startsWith('csrftoken='))
        ?.split('=')[1]
      return cookieValue
    },

    updateSecurity() {
      // Validate password and confirmPassword match before submission
      if (this.security.password !== this.security.confirmPassword) {
        this.errorMessage = 'Passwords do not match.'
        this.passwordMismatch = true
        return
      }
      this.passwordMismatch = false
      this.errorMessage = ''

      const payload = {
        email: this.security.email,
        password: this.security.password
      }

      axios
        .post('https://mmacroscope.me/auth/update-security/', payload)
        .then((response) => {
          if (response.data.success) {
            this.updateMessage =
              'Account details have been updated. Please check your new email for verification.'
            this.errorMessage = ''
          } else if (response.data.error === 'email_in_use') {
            this.errorMessage = 'This email is already associated with an account.'
          } else if (response.data.error === 'email_verification_required') {
            this.updateMessage =
              'Please verify your new email address. A verification link has been sent.'
          } else {
            this.errorMessage = response.data.message
          }
        })
        .catch((error) => {
          this.errorMessage = 'An error occurred while updating security information.'
        })
    },

    updateTheme(newTheme) {
      this.theme = newTheme
      localStorage.setItem('theme', newTheme)
    }
  },
  mounted() {
    this.getAccountInfo()
  }
}
</script>

<style scoped>
.profile-page.light {
  background-color: #f0f2f5;
  color: #333;
}

.profile-page.dark {
  background-color: #1c1c1c;
  color: #f8f8f8;
}

.profile-container {
  display: flex;
  height: 100vh;
  padding: 20px;
}

.sidebar {
  height: calc(100vh - 60px);
  width: 0;
  position: fixed;
  z-index: 1;
  top: 55px;
  left: 0;
  background-color: var(--sidebar-bg, #333);
  overflow-x: hidden;
  padding-top: 20px;
  transition: 0.5s;
}

.sidebar.light {
  background-color: #e9ecef;
}

.sidebar.dark {
  background-color: #2b2b2b;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar ul li {
  margin: 80px 0px;
}

.sidebar ul li a {
  text-decoration: none;
  font-size: 18px;
  padding: 10px 20px;
  color: var(--link-color);
  display: block;
}

.sidebar ul li a:hover {
  background-color: #444;
  border-radius: 8px;
  color: #f1f1f1;
}

.closebtn {
  position: absolute;
  top: 5px;
  right: 30px;
  font-size: 24px;
  color: var(--btn-color);
  cursor: pointer;
}

.openbtn {
  font-size: 24px;
  cursor: pointer;
  background: none;
  color: var(--btn-color);
  padding: 10px;
  border: none;
  position: fixed;
  top: 70px;
  left: 20px;
  z-index: 2;
  transition: 0.3s;
}

.openbtn:hover {
  opacity: 0.7;
}

.openbtn.light {
  color: #333;
}

.openbtn.dark {
  color: #f8f8f8;
}

.profile-content {
  flex: 1;
  padding: 30px;
  margin-left: 0;
  transition: margin-left 0.5s;
  overflow-y: auto;
  height: calc(100vh - 60px);
}

.member-info {
  margin-bottom: 30px;
}

.preferences-section h2 {
  margin-top: 20px;
}

.profile-page.dark .sidebar ul li a {
  color: #ddd;
}

.profile-page.dark .sidebar ul li a:hover {
  background-color: #444;
}

.member-info,
.user-info,
.preferences-section {
  margin-bottom: 30px;
}

.recent-activity {
  margin-top: 250px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

select {
  padding: 8px;
  width: 100%;
  border-radius: 4px;
  border: 1px solid #ccc;
}

button[type='submit'] {
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button[type='submit']:hover {
  background-color: #0056b3;
}
</style>
