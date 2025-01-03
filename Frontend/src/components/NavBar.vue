<!-- Done -->

<template>
  <nav :class="['navbar', theme === 'dark' ? 'navbar-dark bg-dark' : 'navbar-light bg-light']">
    <div class="container-fluid">
      <a class="navbar-brand" href="#" @click="navigateToHome">MacroScope</a>
      <ul class="navbar-nav ms-auto d-flex align-items-center">
        <li class="nav-item" @click="navigateToHome">
          <a :class="['nav-link', theme === 'dark' ? 'text-white' : 'text-dark']" href="#">Home</a>
        </li>
        <li class="nav-item" @click="navigateToAbout">
          <a :class="['nav-link', theme === 'dark' ? 'text-white' : 'text-dark']" href="#">About</a>
        </li>
        <li class="nav-item" @click="navigateToForecast">
          <a :class="['nav-link', theme === 'dark' ? 'text-white' : 'text-dark']" href="#"
            >Forecast</a
          >
        </li>
        <li class="nav-item" @click="navigateToDashboard">
          <a :class="['nav-link', theme === 'dark' ? 'text-white' : 'text-dark']" href="#"
            >Dashboard</a
          >
        </li>
        <li class="nav-item">
          <div class="form-check form-switch ms-3">
            <input
              class="form-check-input"
              type="checkbox"
              id="darkModeSwitch"
              @change="toggleTheme"
              :checked="theme === 'dark'"
            />
            <label
              :class="['form-check-label', theme === 'dark' ? 'text-white' : 'text-dark']"
              for="darkModeSwitch"
            >
              {{ theme === 'dark' ? 'Dark Mode' : 'Light Mode' }}
            </label>
          </div>
        </li>
        <li class="nav-item dropdown" @mouseenter="showDropdown" @mouseleave="hideDropdown">
          <a
            :class="['nav-link dropdown-toggle', theme === 'dark' ? 'text-white' : 'text-dark']"
            href="#"
            id="userDropdown"
            role="button"
          >
            {{ dropdownText }}
          </a>
          <ul
            class="dropdown-menu"
            :class="{
              show: dropdownVisible,
              'bg-dark text-white': theme === 'dark',
              'bg-light text-dark': theme === 'light'
            }"
            aria-labelledby="userDropdown"
          >
            <li @click="navigateToProfile">
              <a
                :class="['dropdown-item', theme === 'dark' ? 'text-white' : 'text-dark']"
                href="#"
                @click="navigateToProfile"
                >Profile</a
              >
            </li>
            <li><hr class="dropdown-divider" /></li>
            <li>
              <a
                :class="['dropdown-item', theme === 'dark' ? 'text-white' : 'text-dark']"
                href="#"
                @click="logout"
                >Logout</a
              >
            </li>
          </ul>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
import axios from 'axios'
import Cookies from 'js-cookie'

axios.defaults.withCredentials = true
export default {
  data() {
    return {
      username: null,
      dropdownVisible: false,
      theme: 'light'
    }
  },
  computed: {
    dropdownText() {
      return this.username ? this.username : 'Error'
    }
  },
  created() {
    this.getUsername()
    this.loadTheme()
  },
  watch: {
    theme(newTheme) {
      document.documentElement.setAttribute('data-theme', newTheme)
      localStorage.setItem('theme', newTheme)
      this.$emit('themeChanged', newTheme)
    }
  },
  methods: {
    getUsername() {
      const storedUsername = localStorage.getItem('username')
      if (storedUsername) {
        this.username = storedUsername
      }
    },
    logout() {
      // Remove user-related data from local storage
      localStorage.removeItem('username')
      localStorage.removeItem('session_id') // Clear session ID if stored

      // Get the CSRF token from cookies
      const csrfToken = Cookies.get('csrftoken')

      // Make a logout request to the backend
      axios
        .post(
          'https://mmacroscope.me/auth/logout/',
          {}, // Empty request body
          {
            withCredentials: true, // Ensure cookies are sent
            headers: {
              'X-CSRFToken': csrfToken,
              'Content-Type': 'application/json'
            }
          }
        )
        .then((response) => {
          console.log('Logout response:', response.data)

          // Check if logout was successful
          if (response.data.success && !response.data.is_active) {
            console.log('Logout successful...')

            // Clear any other relevant data
            localStorage.clear() // Optional: Clear all local storage if needed

            // Redirect to home or login page
            this.$router.push('/')
          } else {
            console.error('Logout failed. No redirect.')
            this.errorMessage = 'Logout failed. Please try again.'
          }
        })
        .catch((error) => {
          console.error('Error during logout:', error)
          this.errorMessage = 'Error during logout. Please try again.'
        })
    },

    showDropdown() {
      this.dropdownVisible = true
    },
    hideDropdown() {
      this.dropdownVisible = false
    },
    toggleTheme(event) {
      this.theme = event.target.checked ? 'dark' : 'light'
    },
    loadTheme() {
      const savedTheme = localStorage.getItem('theme') || 'light'
      this.theme = savedTheme
      document.documentElement.setAttribute('data-theme', this.theme)
    },
    navigateToDashboard() {
      this.$router.push('/dashboard')
    },
    navigateToHome() {
      this.$router.push('/home')
    },
    navigateToAbout() {
      this.$router.push('/about')
    },
    navigateToForecast() {
      this.$router.push('/forecast')
    },
    navigateToProfile() {
      this.$router.push('/profile')
    }
  }
}
</script>

<style scoped>
.navbar-nav {
  flex-direction: row;
}

.nav-item {
  margin-left: 15px;
}

.nav-link {
  padding: 0.5rem 1rem;
}

.dropdown-menu {
  min-width: 150px;
}

.dropdown-menu.show {
  display: block;
}

[data-theme='dark'] {
  background-color: #121212;
  color: white;
}

[data-theme='light'] {
  background-color: white;
  color: black;
}

.dropdown-menu.bg-dark {
  background-color: #343a40;
  color: white;
}

.dropdown-menu.bg-light {
  background-color: #f8f9fa;
  color: black;
}

.dark-label {
  color: white;
}

.light-label {
  color: black;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 1000;
}

.navbar-nav .dropdown:hover .dropdown-menu {
  display: block;
}

.nav-item.dropdown {
  position: relative;
}

.nav-item.dropdown:focus {
  outline: none;
}

.dropdown-item {
  padding: 0.5rem 1rem;
  transition: background-color 0.3s ease;
}

.dropdown-item:hover {
  background-color: #e9ecef;
}

[data-theme='dark'] .dropdown-item:hover {
  background-color: #495057;
}

.form-check-label.text-white {
  color: white;
}

.form-check-label.text-dark {
  color: black;
}
</style>
