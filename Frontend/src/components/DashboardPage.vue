<template>
  <NavBar @themeChanged="updateTheme" />
  <div class="dashboard" :class="theme">
    <header class="dashboard-header">
      <h1>Dashboard</h1>
      <nav class="dashboard-nav">
        <button
          v-for="indicator in indicators"
          :key="indicator"
          :class="{ active: currentIndicator === indicator }"
          @click="setChart(indicator)"
          :disabled="loading"
        >
          {{ indicator }}
        </button>
        <TipStar
          tip="You can switch between GDP, unemployment, and inflation using the buttons."
          :isDarkMode="darkMode"
        />
      </nav>
    </header>

    <section class="chart-container">
      <div class="line-chart-container">
        <canvas ref="lineChartCanvas"></canvas>
      </div>
      <div class="chart-section">
        <div class="text-box">
          <p>Some information about the data</p>
        </div>
        <div class="pie-chart-container">
          <canvas ref="pieChartCanvas"></canvas>
        </div>
      </div>
      <div class="bar-chart-container">
        <canvas ref="barChartCanvas"></canvas>
      </div>

      <div class="text-box-two-radar-chart-container">
        <div class="text-box-two">
          <p>Some information about the data</p>
        </div>
        <div class="radar-chart-container">
          <canvas ref="radarChartCanvas"></canvas>
        </div>

        <div class="text-box-two">
          <p>Some information about the data</p>
        </div>
      </div>
    </section>

    <div v-if="loading" class="loading">Loading chart...</div>
  </div>
</template>

<script>
import NavBar from './NavBar.vue'
import { Chart, registerables } from 'chart.js'
import axios from 'axios'
import TipStar from './TipStar.vue'

Chart.register(...registerables)

export default {
  components: {
    NavBar,
    TipStar
  },
  data() {
    return {
      theme: 'light',
      currentLineChart: null,
      currentPieChart: null,
      currentBarChart: null,
      currentRadarChart: null,
      currentIndicator: 'GDP',
      indicators: ['GDP', 'Unemployment', 'Interest Rates', 'Labour', 'Exchange Rates'],
      loading: false
    }
  },
  created() {
    this.setChart('GDP')
    this.loadTheme()
  },
  mounted() {
    this.setChart('GDP')
    this.loadTheme()
    window.addEventListener('resize', this.handleResize)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize)
  },
  methods: {
    async setChart(indicator) {
      if (this.loading) return
      this.loading = true
      this.currentIndicator = indicator

      try {
        const data = await this.fetchChartData(indicator)
        this.updateLineChart(data)
        this.updatePieChart()
        this.updateBarChart()
        this.updateRadarChart()
      } catch (error) {
        console.error('Error fetching chart data:', error)
      } finally {
        setTimeout(() => {
          this.loading = false
        }, 1000)
      }
    },
    async fetchChartData(indicator) {
      const response = await axios.post(`http://127.0.0.1:8080/forecast/api/${indicator}/`)
      return {
        labels: response.data.labels,
        values: response.data.values,
        label: response.data.label
      }
    },
    updateLineChart(data) {
      if (this.currentLineChart) {
        this.currentLineChart.destroy()
      }

      const canvas = this.$refs.lineChartCanvas
      const ctx = canvas.getContext('2d')
      if (!ctx) {
        console.error('Failed to access the canvas context')
        return
      }

      this.currentLineChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: data.labels,
          datasets: [
            {
              label: data.label,
              data: data.values,
              borderColor: '#007bff',
              backgroundColor: 'rgba(0, 123, 255, 0.5)'
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              title: {
                display: true,
                text: 'Year'
              },
              type: 'category'
            },
            y: {
              title: {
                display: true,
                text: 'Value'
              },
              beginAtZero: true
            }
          }
        }
      })
    },
    updatePieChart() {
      if (this.currentPieChart) {
        this.currentPieChart.destroy()
      }

      const canvas = this.$refs.pieChartCanvas
      canvas.width = canvas.width

      const ctx = canvas.getContext('2d')
      if (!ctx) {
        console.error('Failed to access the canvas context')
        return
      }

      this.currentPieChart = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: ['Label 1', 'Label 2', 'Label 3'],
          datasets: [
            {
              data: [10, 20, 30],
              backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false
        }
      })
    },
    updateBarChart() {
      if (this.currentBarChart) {
        this.currentBarChart.destroy()
      }

      const canvas = this.$refs.barChartCanvas

      const ctx = canvas.getContext('2d')
      if (!ctx) {
        console.error('Failed to access the canvas context')
        return
      }

      this.currentBarChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['January', 'February', 'March', 'April', 'May', 'June'],
          datasets: [
            {
              label: 'Sales',
              data: [12, 19, 3, 5, 2, 3],
              backgroundColor: '#42A5F5',
              borderColor: '#1E88E5',
              borderWidth: 1
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              title: {
                display: true,
                text: 'Month'
              },
              grid: {
                display: false
              }
            },
            y: {
              title: {
                display: true,
                text: 'Sales'
              },
              beginAtZero: true,
              grid: {
                display: false
              }
            }
          }
        }
      })
    },
    updateRadarChart() {
      if (this.currentRadarChart) {
        this.currentRadarChart.destroy()
      }

      const canvas = this.$refs.radarChartCanvas
      const ctx = canvas.getContext('2d')
      if (!ctx) {
        console.error('Failed to access the canvas context')
        return
      }

      const isDark = this.theme === 'dark'

      this.currentRadarChart = new Chart(ctx, {
        type: 'radar',
        data: {
          labels: ['January', 'February', 'March', 'April', 'May', 'June'],
          datasets: [
            {
              label: 'Sales',
              data: [65, 59, 90, 81, 56, 55, 40],
              backgroundColor: isDark ? 'rgba(255, 99, 132, 0.2)' : 'rgba(75, 192, 192, 0.2)',
              borderColor: isDark ? '#FF6384' : '#36A2EB',
              borderWidth: 1
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            r: {
              grid: {
                color: isDark ? '#444' : '#ddd'
              },
              angleLines: {
                color: isDark ? '#444' : '#ddd'
              }
            }
          }
        }
      })
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
    },
    handleResize() {
      this.updateRadarChart()
    }
  }
}
</script>

<style scoped>
.dashboard.light {
  background-color: #f0f4f8;
  color: black;
}

.dashboard.dark {
  background-color: #1c1c1c;
  color: white;
}

.dashboard-nav button {
  margin-right: 10px;
  padding: 10px 15px;
  font-size: 16px;
  cursor: pointer;
  border: none;
}

.dashboard-nav button.active {
  background-color: #0056b3;
}

.dashboard-nav button:disabled {
  background-color: #d6d6d6;
}

.loading {
  text-align: center;
  font-size: 18px;
  margin-top: 20px;
}

.chart-container {
  padding: 20px;
}

.line-chart-container,
.pie-chart-container,
.bar-chart-container,
.radar-chart-container {
  position: relative;
  height: 400px;
  width: 100%;
  margin-bottom: 20px;
}

.chart-section {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 20px;
}

.pie-chart-container,
.bar-chart-container,
.radar-chart-container {
  flex: 1;
}

.text-box,
.text-box-two {
  flex: 0 80 600px;
  height: 400px;
  background-color: #f8f9fa;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  margin-left: auto;
  position: relative;
  transition: all 0.5s ease;
}

.text-box-two {
  width: 600px;
  margin: auto;
}

.text-box-two-radar-chart-container {
  display: inline-flex;
}

.dark .text-box,
.dark .text-box-two {
  background-color: #333;
  color: white;
  border-color: #444;
}

canvas {
  width: 100% !important;
  height: 100% !important;
}

.radar-chart-container {
  position: relative;
  height: 400px;
  width: 100%;
  margin-bottom: 20px;
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

