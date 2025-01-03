<template>
  <Navbar @themeChanged="updateTheme" />
  <div :class="['forecast-page', isDarkMode ? 'dark' : 'light']">
    <main class="forecast-container">
      <h1 :class="{ 'dark-header': isDarkMode }">Forecast</h1>

      <div class="forecast-buttons">
        <TipStar
          tip="Select different economic indicators to view forecasted trends."
          :isDarkMode="isDarkMode"
        />
        <button
          v-for="indicator in indicators"
          :key="indicator"
          :class="{
            'forecast-button': true,
            active: currentIndicator === indicator,
            disabled: loading
          }"
          @click="setChart(indicator)"
          :disabled="loading"
        >
          {{ indicator }}
        </button>
      </div>

      <div class="chart-container">
        <canvas id="forecastChart" ref="lineChartCanvas"></canvas>
      </div>

      <div v-if="loading" :class="{ 'dark-header': isDarkMode }">Loading...</div>
      <div v-if="error" class="error">{{ error }}</div>

      <div class="forecast-info" v-if="currentInterpretation">
        <h2>Interpreting the Data</h2>
        <p>{{ currentInterpretation }}</p>
      </div>
    </main>
  </div>
</template>

<script>
import Navbar from './NavBar.vue'
import { Chart } from 'chart.js/auto'
import TipStar from './TipStar.vue'
import axios from 'axios'

axios.defaults.withCredentials = true;

export default {
  name: 'ForecastPage',
  components: {
    Navbar,
    TipStar
  },
  data() {
    return {
      theme: 'light',
      isDarkMode: false,
      indicators: ['GDP', 'Unemployment', 'Inflation'],
      currentIndicator: 'GDP',
      currentInterpretation: '',
      forecast: [], // Dynamic forecast data
      loading: false,
      chart: null,
      error: null, // To capture any errors
      cache: {}, // Cache to store fetched data
      cooldowns: {} // Track cooldowns for each indicator
    }
  },
  mounted() {
    this.loadTheme()
    this.setChart('GDP')
  },
  methods: {
    async setChart(indicator) {
      if (this.loading) return

      this.loading = true // Start the loading state before any processing
      this.currentIndicator = indicator
      this.error = null

      // Disable all buttons during the cooldown period
      this.disableButtons(true)

      try {
        // If the data is cached, simulate a cooldown effect using a timeout
        if (this.cache[indicator]) {
          setTimeout(() => {
            this.updateChart(indicator, this.cache[indicator])
            this.loading = false // End the loading state after chart update
            // Enable buttons after cooldown
            this.disableButtons(false)
          }, 1000) // Simulate a 1-second cooldown
          return
        }

        // Fetch forecast data from Django API
        const response = await axios.get(
          `https://mmacroscope.me/forecast/api/predict/${indicator.toLowerCase()}`
        )

        if (response.data && response.data.forecast) {
          const forecastData = response.data.forecast
          this.cache[indicator] = forecastData // Cache the data
          this.updateChart(indicator, forecastData)
        } else {
          throw new Error('No forecast data available')
        }
      } catch (error) {
        console.error('Error fetching forecast data:', error)
        this.error = 'Unable to fetch forecast data. Please try again later.'
      } finally {
        this.loading = false // Ensure loading state is reset
        // Enable buttons after processing
        this.disableButtons(false)
      }
    },

    updateChart(indicator, data) {
      this.forecast = data
      this.currentInterpretation = this.getInterpretation(indicator)

      // Destroy previous chart instance if it exists
      if (this.chart) {
        this.chart.destroy()
      }

      const ctx = this.$refs.lineChartCanvas.getContext('2d')

      // Specific x-axis labels for Unemployment
      const labels = [1, 2, 3, 4, 5, 6, 7]
      const x_label = 'Months'
      var y_label

      if (indicator === 'Unemployment' || indicator === 'Inflation') {
        y_label = 'Percentage'
      } else if (indicator === 'GDP') {
        y_label = 'GDP (Millions of Domestic Currency, Seasonally Adjusted)'
      }

      // Create the chart with the fetched data
      this.chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: `${indicator} Forecast`,
              data: this.forecast,
              borderColor: 'blue', // Set line color to blue
              backgroundColor: this.isDarkMode
                ? 'rgba(0, 0, 255, 0.1)' // Blue background for dark mode
                : 'rgba(0, 0, 255, 0.1)', // Blue background for light mode
              borderWidth: 2
            }
          ]
        },
        options: {
          responsive: true,
          scales: {
            x: {
              ticks: {
                color: this.isDarkMode ? '#ffffff' : '#333333'
              },
              title: {
                display: true,
                text: x_label // Set x-axis label from backend
              }
            },
            y: {
              ticks: {
                color: this.isDarkMode ? '#ffffff' : '#333333'
              },
              title: {
                display: true,
                text: y_label // Set x-axis label from backend
              }
            }
          }
        }
      })
    },

    // Helper function to disable or enable buttons
    disableButtons(disable) {
      this.loading = disable // Manage the state directly
    },

    // Function to return interpretations based on the indicator
    getInterpretation(indicator) {
      switch (indicator) {
        case 'GDP':
          return 'GDP represents the total value of all goods and services produced in a country. A rising GDP indicates economic growth.'
        case 'Unemployment':
          return 'The unemployment rate shows the percentage of the labor force that is without work. Lower unemployment rates indicate a healthier job market.'
        case 'Inflation':
          return 'Inflation reflects the rate at which the general price level of goods and services rises. High inflation reduces purchasing power.'
        default:
          return ''
      }
    },

    loadTheme() {
      const savedTheme = localStorage.getItem('theme') || 'light'
      this.theme = savedTheme
      this.isDarkMode = savedTheme === 'dark'
    },

    updateTheme(newTheme) {
      this.theme = newTheme
      this.isDarkMode = newTheme === 'dark'
      localStorage.setItem('theme', newTheme)
    }
  }
}
</script>

<style scoped>
.forecast-page {
  padding: 20px;
  transition:
    background-color 0.3s,
    color 0.3s;
  height: 100vh;
}

.forecast-container {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

.chart-container {
  margin-bottom: 30px;
}

.forecast-buttons {
  margin-bottom: 20px;
  font-size: 16px;
}

.forecast-buttons button {
  padding: 10px 20px;
  margin: 0 10px;
  cursor: pointer;
  border-radius: 0px;
  border: none;
  color: black;
}

.forecast-buttons button.active {
  background-color: #0056b3;
  color: black;
}

.forecast-buttons button.disabled {
  cursor: not-allowed;
  background-color: #d6d6d6;
  opacity: 0.7;
}

.forecast-info {
  background: var(--box-bg);
  color: var(--text-color);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
}

.dark-header {
  color: #ffffff;
}

.light {
  --box-bg: #ffffff;
  --text-color: #333333;
  --button-hover-bg: #e0e0e0;
  background-color: #f0f4f8;
}

.dark {
  --box-bg: #333333;
  --text-color: #ffffff;
  --button-hover-bg: #555555;
  background-color: #1c1c1c;
}
</style>
