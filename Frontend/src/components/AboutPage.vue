<!-- Done -->

<template>
  <div>
    <Navbar @themeChanged="updateTheme" />
    <div :class="['about-page', isDarkMode ? 'dark' : 'light']">
      <main class="about-container">
        <h1 class="about-header">About MacroScope</h1>
        <section class="about-content">
          <p>
            MacroScope is a dynamic platform designed to provide personalized insights and
            predictions based on key economic indicators. Track metrics like GDP, inflation,
            unemployment rates, and more with ease, offering tailored visualizations and analytics.
          </p>

          <h2>Purpose</h2>
          <p>
            My mission is to empower users to understand relationships between economic indicators,
            using machine learning to forecast trends and enhance decision-making. In addition, the goal of this
            application is to educate the average person about key economic indicators, explain
            their interconnections, and demonstrate how they can impact everyday life.
          </p>

          <h2>Tech Stack</h2>
          <ul>
            <li>Vue.js for frontend development</li>
            <li>Django for backend API and user authentication</li>
            <li>Chart.js for data visualization</li>
            <li>MySQL for data storage (authentication and economic data)</li>
            <li>TensorFlow for machine learning and predictive analytics</li>
            <li>Docker for containerization</li>
            <li>AWS EC2, RDS, S3, Cloudfront for hosting and scaling the application</li>
          </ul>
        </section>
      </main>
    </div>
  </div>
</template>

<script>
import Navbar from './NavBar.vue'

export default {
  name: 'AboutPage',
  components: {
    Navbar
  },
  data() {
    return {
      isDarkMode: false
    }
  },
  created() {
    this.loadTheme()
  },
  methods: {
    loadTheme() {
      const savedTheme = localStorage.getItem('theme') || 'light'
      this.isDarkMode = savedTheme === 'dark'
    },
    updateTheme(newTheme) {
      this.isDarkMode = newTheme === 'dark'
      localStorage.setItem('theme', newTheme)
    }
  }
}
</script>

<style scoped>
.about-page {
  transition:
    background-color 0.3s ease,
    color 0.3s ease;
}

.about-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 30px;
}

.about-header {
  color: var(--text-color);
}

.about-content {
  background: var(--content-bg);
  color: var(--text-color);
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.5s ease;
}

.about-content:hover {
  transform: translateY(-5px);
}

.about-content h1 {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 25px;
}

.about-content h2 {
  font-size: 2rem;
  margin-top: 25px;
  margin-bottom: 15px;
}

.about-content p {
  font-size: 1.1rem;
  margin-bottom: 15px;
  line-height: 1.8;
}

.about-content ul {
  padding-left: 20px;
  list-style-type: disc;
}

.about-content ul li {
  margin-bottom: 10px;
  font-size: 1.1rem;
}

.light {
  --content-bg: #ffffff;
  --text-color: #333333;
  background-color: #f0f4f8;
}

.dark {
  --content-bg: #2b2b2b;
  --text-color: #e0e0e0;
  background-color: #1c1c1c;
}
</style>
