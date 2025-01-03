<template>
  <NavBar @themeChanged="updateTheme" />
  <div class="dashboard" :class="theme">
    <header class="dashboard-header">
      <h1 @click="checkAuthStatus">Dashboard</h1>
      <nav class="dashboard-nav">
        <button
          v-for="indicator in indicators"
          :key="indicator"
          :class="{ active: currentIndicator === indicator }"
          @click="setChart(indicator) && updateInformation(indicator)"
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
          <p>{{ box1Text }}</p>
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
          <p>{{ box2Text }}</p>
        </div>
        <div class="radar-chart-container">
          <canvas ref="radarChartCanvas"></canvas>
        </div>

        <div class="text-box-two">
          <p>{{ box3Text }}</p>
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

axios.defaults.withCredentials = true;
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
      loading: false,

      textBoxContent: {
        GDP: [
          'Gross Domestic Product (GDP) is one of the most vital indicators of economic performance, representing the total monetary value of all finished goods and services produced within a country’s borders over a specific period, usually quarterly or annually. By analyzing GDP growth or contraction, economists and policymakers can gauge the health of an economy, identifying periods of economic expansion or recession. A growing GDP indicates a thriving economy with robust consumer demand and business activity, which can lead to job creation and better living standards.',
          'GDP can be broken down into four main components: consumer spending, business investment, government spending, and net exports. Changes in these areas can highlight shifts in economic activity. For instance, if consumer spending makes up a significant part of GDP, then a decrease in consumer confidence or purchasing power can have a substantial impact on overall economic growth. Similarly, high government spending in a period can artificially boost GDP, though it might not indicate sustainable growth in the private sector.',
          'Tracking GDP over time is essential for making informed decisions on fiscal and monetary policies. Central banks, such as the Federal Reserve, often use GDP growth trends to adjust interest rates or influence inflation, aiming to stabilize the economy. For investors, GDP trends provide insights into potential business cycles, influencing stock prices, investment risks, and financial strategies. Thus, GDP is a foundational metric for understanding economic trajectory and guiding decision-making across sectors.'
        ],
        Unemployment: [
          'Unemployment rates provide a clear picture of the labor market and the percentage of people within the workforce who are actively seeking but unable to find employment. A high unemployment rate often signals economic distress, as it reflects a lack of available jobs and can indicate broader economic challenges, such as low consumer demand or an economic downturn. Conversely, low unemployment suggests that a larger portion of the population is gainfully employed, often coinciding with periods of economic growth and prosperity.',
          'Unemployment is typically classified into various types, including cyclical, structural, and frictional unemployment. Cyclical unemployment rises during economic downturns as companies reduce staff due to decreased demand, while structural unemployment occurs when there is a mismatch between workers’ skills and job requirements. Understanding these distinctions is crucial for policymakers who aim to implement targeted programs to address specific unemployment causes, whether through retraining programs, economic stimulus, or supporting industries facing downturns.',
          'For investors and economists, unemployment trends can provide early indicators of potential shifts in economic health. A rising unemployment rate can signal reduced consumer spending, lower business profits, and a potential downturn in the stock market. Governments also use unemployment rates to shape policies around social welfare and economic support, aiming to create a resilient job market that can better withstand economic shocks.'
        ],
        'Interest Rates': [
          'Interest rates are the cost of borrowing money, typically set by central banks as part of their monetary policy to control inflation, stimulate investment, or curb excessive economic growth. Higher interest rates generally make borrowing more expensive, which can slow down economic activity by discouraging businesses from taking out loans for expansion and consumers from financing big-ticket purchases like homes or cars. On the other hand, lower interest rates make borrowing cheaper, which can stimulate spending and investment, potentially leading to job creation and economic growth.',
          'The impact of interest rates extends across many sectors, from real estate to consumer finance and corporate investments. For instance, a decrease in interest rates often boosts housing markets as mortgages become more affordable, while an increase can dampen market activity as monthly payments rise. In the corporate world, low-interest rates encourage companies to borrow for expansion or research, fostering innovation and potentially boosting stock market performance as profits rise.',
          "For investors, interest rate trends are vital indicators of economic conditions and potential stock market movements. Interest rates directly influence returns on bonds, the risk-free rate of return, and the relative attractiveness of equities. Consequently, changes in interest rates can lead to significant portfolio shifts, as investors weigh risks and returns across asset classes. Interest rate policies are therefore closely watched by markets, influencing both long-term investment strategies and short-term financial decisions."
        ],
        Labour: [
          'Labour statistics encompass a broad range of data, from employment rates to productivity measures, reflecting the supply of workers and their efficiency within an economy. The labor force participation rate, which measures the percentage of working-age individuals who are actively employed or seeking work, is a critical indicator of economic engagement. High labor force participation typically suggests a robust economy with ample job opportunities, whereas a decline could indicate barriers to workforce entry, such as a lack of skills or poor job availability.',
          'Productivity within the labor sector is also a key measure, as it indicates how effectively labor inputs are translated into outputs. High productivity growth means that an economy is able to produce more with the same number of workers, often a result of technological advancements, better management practices, or improved worker skills. Economies with high labor productivity tend to have higher wages and standards of living, as businesses can afford to pay more when their output increases.',
          'Labour statistics influence a range of economic policies, from education and training programs to immigration policies aimed at filling workforce gaps. For businesses, labor market trends can indicate where to find talent and guide decisions on wages and benefits to attract the best employees. For investors, a stable and productive labor market is a positive economic signal, supporting corporate earnings and long-term economic stability.'
        ],
        'Exchange Rates': [
          'Exchange rates represent the value of one currency relative to another, impacting international trade, investment, and travel. A strong domestic currency makes imports cheaper and exports more expensive, while a weak currency has the opposite effect, making exports more competitive on the global market but increasing import costs. This balance is crucial for countries that rely heavily on trade, as fluctuations in exchange rates can significantly impact their trade balance, inflation rates, and overall economic health.',
          'Several factors influence exchange rates, including interest rates, inflation, political stability, and economic performance. For example, countries with higher interest rates tend to attract foreign investors seeking better returns, which can drive up demand for that currency. Conversely, countries with high inflation rates typically see their currencies weaken, as the purchasing power of their currency erodes over time. Exchange rates also respond to geopolitical events, as stability and investor confidence play crucial roles in currency valuation.',
          'For multinational companies, exchange rate trends can impact profitability as revenue and costs fluctuate with currency values. Investors also monitor exchange rates to identify opportunities in foreign markets, manage risks associated with currency volatility, and optimize portfolios with international assets. Consequently, exchange rates are a pivotal factor in global finance, with wide-reaching implications for trade, investment, and economic policy.'
        ]
      },
      box1Text: '',
      box2Text: '',
      box3Text: ''
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
        this.updatePieChart(data)
        this.updateBarChart(data)
        this.updateRadarChart(data)
        // Update text for the selected indicator
        this.updateTextBoxes(indicator)
      } catch (error) {
        console.error('Error fetching chart data:', error)
      } finally {
        setTimeout(() => {
          this.loading = false
        }, 1000)
      }
    },
    updateTextBoxes(indicator) {
      const content = this.textBoxContent[indicator]
      if (content) {
        ;[this.box1Text, this.box2Text, this.box3Text] = content
      }
    },
    async fetchChartData(indicator) {
      const response = await axios.post(`https://mmacroscope.me/forecast/api/${indicator}/`, {
        withCredentials: true
      })

      console.log('Fetched chart data:', response.data)

      if (indicator === 'Exchange Rates') {
        // For multiple datasets
        return {
          labels: response.data.labels,
          datasets: response.data.datasets, // Expecting datasets to be an array of objects for multiple lines
          x_label: response.data.x_label,
          y_label: response.data.y_label
        }
      } else {
        // For a single dataset (non "Exchange Rates" indicators)
        return {
          labels: response.data.labels,
          values: response.data.values,
          label: response.data.label,
          x_label: response.data.x_label,
          y_label: response.data.y_label
        }
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

      const datasets = data.datasets
        ? data.datasets.map((dataset) => ({
            label: dataset.label,
            data: dataset.values,
            borderColor: dataset.borderColor || '#007bff',
            backgroundColor: dataset.backgroundColor || 'rgba(0, 123, 255, 0.5)',
            fill: false,
            tension: 0.4 // Optional: Smoothing of the lines
          }))
        : [
            {
              label: data.label,
              data: data.values,
              borderColor: '#007bff',
              backgroundColor: 'rgba(0, 123, 255, 0.5)',
              fill: false,
              tension: 0.4
            }
          ]

      this.currentLineChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: data.labels,
          datasets: datasets
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              title: {
                display: true,
                text: data.x_label // Set x-axis label from backend
              },
              type: 'category'
            },
            y: {
              title: {
                display: true,
                text: data.y_label // Set y-axis label from backend
              },
              beginAtZero: false
            }
          }
        }
      })
    },

    updatePieChart(data) {
      if (this.currentPieChart) {
        this.currentPieChart.destroy()
      }

      const canvas = this.$refs.pieChartCanvas
      const ctx = canvas.getContext('2d')
      if (!ctx) {
        console.error('Failed to access the canvas context')
        return
      }

      const dataset = data.datasets ? data.datasets[0] : { values: data.values, label: data.label }
      const colors = dataset.values.map(
        (_, index) => `hsl(${(index * 360) / dataset.values.length}, 70%, 60%)`
      )

      this.currentPieChart = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: data.labels,
          datasets: [
            {
              data: dataset.values,
              backgroundColor: colors
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false
        }
      })
    },

    updateBarChart(data) {
      if (this.currentBarChart) {
        this.currentBarChart.destroy()
      }

      const canvas = this.$refs.barChartCanvas
      const ctx = canvas.getContext('2d')
      if (!ctx) {
        console.error('Failed to access the canvas context')
        return
      }

      const datasets = data.datasets
        ? data.datasets.map((dataset, index) => ({
            label: dataset.label,
            data: dataset.values,
            backgroundColor: `hsl(${(index * 360) / data.datasets.length}, 70%, 60%)`, // Different color for each dataset
            borderColor: `hsl(${(index * 360) / data.datasets.length}, 70%, 50%)`,
            borderWidth: 1
          }))
        : [
            {
              label: data.label,
              data: data.values,
              backgroundColor: '#42A5F5',
              borderColor: '#1E88E5',
              borderWidth: 1
            }
          ]

      this.currentBarChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: data.labels,
          datasets: datasets
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              title: {
                display: true,
                text: data.x_label
              },
              stacked: false
            },
            y: {
              title: {
                display: true,
                text: data.y_label
              },
              beginAtZero: true,
              stacked: false
            }
          }
        }
      })
    },

    updateRadarChart(data) {
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
      const datasets = data.datasets
        ? data.datasets.map((dataset, index) => ({
            label: dataset.label,
            data: dataset.values,
            backgroundColor: isDark
              ? `hsla(${(index * 360) / data.datasets.length}, 70%, 50%, 0.2)`
              : `hsla(${(index * 360) / data.datasets.length}, 70%, 60%, 0.2)`,
            borderColor: `hsl(${(index * 360) / data.datasets.length}, 70%, 50%)`,
            borderWidth: 1
          }))
        : [
            {
              label: data.label,
              data: data.values,
              backgroundColor: isDark ? 'rgba(255, 99, 132, 0.2)' : 'rgba(75, 192, 192, 0.2)',
              borderColor: isDark ? '#FF6384' : '#36A2EB',
              borderWidth: 1
            }
          ]

      this.currentRadarChart = new Chart(ctx, {
        type: 'radar',
        data: {
          labels: data.labels,
          datasets: datasets
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
    },
    checkAuthStatus() {
      axios
        .get('https://mmacroscope.me/auth/check-auth/', { withCredentials: true })
        .then((response) => {
          if (response.data.is_authenticated) {
            console.log('User is authenticated:', response.data.user)
          } else {
            console.log('User is not authenticated')
          }
        })
        .catch((error) => {
          console.error('Error checking authentication status:', error)
        })
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
