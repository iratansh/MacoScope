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
          :class="[
            'forecast-button',
            currentIndicator === indicator ? 'active' : '',
            loading ? 'disabled' : ''
          ]"
          @click="setChart(indicator)"
          :disabled="loading"
        >
          {{ indicator }}
        </button>
      </div>

      <div class="chart-container">
        <canvas id="forecastChart" ref="lineChartCanvas"></canvas>
      </div>

      <div class="forecast-info">
        <h2>Interpreting the Data</h2>
        <p>
          {{ currentInterpretation }}
        </p>
      </div>
    </main>
  </div>
</template>

<script>
import Navbar from './NavBar.vue'
import { Chart } from 'chart.js/auto'
import TipStar from './TipStar.vue'

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
      forecastData: {
        GDP: {
          data: [100, 120, 150, 170, 200],
          interpretation:
            'GDP represents the total value of all goods and services produced in a country. A rising GDP indicates economic growth.'
        },
        Unemployment: {
          data: [7.1, 6.9, 6.8, 7.0, 6.7],
          interpretation:
            'The unemployment rate shows the percentage of the labor force that is without work. Lower unemployment rates indicate a healthier job market.'
        },
        Inflation: {
          data: [1.5, 1.8, 2.0, 2.2, 2.5],
          interpretation:
            'Inflation reflects the rate at which the general price level of goods and services rises. High inflation reduces purchasing power.'
        }
      },
      currentIndicator: 'GDP',
      currentInterpretation: '',
      loading: false,
      chart: null
    }
  },
  mounted() {
    this.loadTheme()
    this.setChart('GDP')
  },
  methods: {
    async setChart(indicator) {
      if (this.loading) return
      this.loading = true
      this.currentIndicator = indicator

      try {
        const chartData = this.forecastData[indicator].data
        this.currentInterpretation = this.forecastData[indicator].interpretation

        if (this.chart) {
          this.chart.destroy()
        }

        const ctx = this.$refs.lineChartCanvas.getContext('2d')
        this.chart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: ['2020', '2021', '2022', '2023', '2024'],
            datasets: [
              {
                label: `${indicator} Forecast`,
                data: chartData,
                borderColor: this.isDarkMode ? '#ffffff' : '#333333',
                backgroundColor: this.isDarkMode
                  ? 'rgba(255, 255, 255, 0.1)'
                  : 'rgba(0, 0, 0, 0.1)',
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
                }
              },
              y: {
                ticks: {
                  color: this.isDarkMode ? '#ffffff' : '#333333'
                }
              }
            }
          }
        })
      } catch (error) {
        console.error('Error loading chart data:', error)
      } finally {
        setTimeout(() => {
          this.loading = false
        }, 1000)
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
}

.forecast-container {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

.chart-container {
  margin-bottom: 30px;
}

.forecast-page {
  padding: 20px;
  transition:
    background-color 0.3s,
    color 0.3s;
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
