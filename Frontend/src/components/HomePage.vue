<!-- Done -->

<template>
  <NavBar @themeChanged="updateTheme" />
  <div :class="darkMode ? 'dark' : 'light'">
    <div class="container home-container">
      <h1 class="text-center mb-4">Welcome to MacroScope</h1>
      <div class="row">
        <div class="col-md-6">
          <div :class="['card', darkMode ? 'dark-card' : 'light-card']">
            <div class="card-body">
              <h5 class="card-title">Economic Indicators</h5>
              <p class="card-text">
                Economic indicators are crucial for understanding the state of an economy. Here are
                some key indicators:
              </p>
              <ul class="list">
                <li>
                  <strong>Gross Domestic Product (GDP):</strong> Measures the total value of goods
                  and services produced in a country.
                </li>
                <li>
                  <strong>Inflation Rate:</strong> Shows the rate at which prices for goods and
                  services are rising.
                </li>
                <li>
                  <strong>Unemployment Rate:</strong> Represents the percentage of the workforce
                  that is jobless and actively seeking employment.
                </li>
                <li>
                  <strong>Consumer Confidence Index (CCI):</strong> Reflects consumer optimism
                  regarding the economic outlook.
                </li>
              </ul>
              <p class="card-text">
                These indicators help gauge economic stability and predict future growth trends.
                They are also interconnected:
              </p>
              <ul class="list">
                <li>
                  <strong>GDP and Unemployment Rate:</strong> A growing GDP often leads to lower
                  unemployment, as businesses expand and hire more workers.
                </li>
                <li>
                  <strong>Inflation and Consumer Confidence:</strong> High inflation can erode
                  purchasing power, reducing consumer confidence and spending.
                </li>
              </ul>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div :class="['card', darkMode ? 'dark-card' : 'light-card']">
            <div class="card-body">
              <h5 class="card-title">Forecasting Trends</h5>
              <p class="card-text">
                Forecasting economic trends using machine learning models like Long Short-Term
                Memory (LSTM) networks offers significant advantages:
              </p>
              <ul class="list">
                <li>
                  <strong>Predictive Analytics:</strong> Anticipates future economic conditions
                  based on historical data.
                </li>
                <li>
                  <strong>Risk Management:</strong> Helps identify and manage potential economic
                  risks.
                </li>
                <li>
                  <strong>Strategic Planning:</strong> Provides insights for long-term economic and
                  investment strategies.
                </li>
              </ul>
              <p class="card-text">
                Leveraging these models can enhance decision-making processes for both policymakers
                and investors by providing a deeper understanding of economic trends and their
                interconnections.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from './NavBar.vue'

export default {
  name: 'HomePage',
  components: {
    NavBar
  },
  data() {
    return {
      theme: 'light',
      darkMode: false
    }
  },
  created() {
    this.loadTheme() 
  },
  methods: {
    loadTheme() {
      const savedTheme = localStorage.getItem('theme') || 'light'
      this.theme = savedTheme
      this.darkMode = this.theme === 'dark'
    },
    updateTheme(newTheme) {
      this.theme = newTheme
      this.darkMode = newTheme === 'dark'
      localStorage.setItem('theme', newTheme)
    }
  }
}
</script>

<style scoped>
html,
body,
#app {
  height: 100%;
  margin: 0;
  padding: 0;
}

.home-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.card {
  margin-bottom: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.5s ease;
}
.card:hover {
  transform: translateY(-5px);
}
.card-body {
  padding: 20px;
}

.light {
  background-color: #f0f4f8;
  color: #333;
}
.light-card {
  background-color: white;
  color: #333;
}

.dark {
  background-color: #1c1c1c;
  color: #f9f9f9;
}
.dark-card {
  background-color: #444;
  color: #f9f9f9;
}

.card-title {
  font-size: 1.5rem;
  margin-bottom: 15px;
}

.card-text {
  color: inherit;
}

.list {
  padding-left: 1.5rem;
  list-style-type: disc;
}
.list li {
  margin-bottom: 10px;
  color: inherit;
}

html,
body,
#app,
.light,
.dark {
  min-height: 100vh;
  margin: 0;
  padding: 0;
}
</style>
