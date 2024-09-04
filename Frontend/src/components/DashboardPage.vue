<template>
  <NavBar />
  <div class="dashboard">
    <header class="dashboard-header">
      <h1>Dashboard</h1>
      <nav class="dashboard-nav">
        <button @click="setChart('GDP')">GDP</button>
        <button @click="setChart('Unemployment')">Unemployment</button>
        <button @click="setChart('Interest Rates')">Interest Rates</button>
        <button @click="setChart('Labour')">Labour</button>
        <button @click="setChart('Exchange Rates')">Exchange Rates</button>
      </nav>
    </header>

    <section class="chart-container">
      <canvas id="economic-chart"></canvas>
    </section>
  </div>
</template>

<script>
import { Chart } from 'chart.js';
import axios from 'axios';
import ErrorToast from './ErrorToast.vue'
import NavBar from './NavBar.vue';

export default {
  components: {
    NavBar,
  },
  data() {
    return {
      currentChart: null,
    };
  },
  methods: {
    setChart(indicator) {
      // Need to fetch bullshit data based on the selected indicator
      this.fetchChartData(indicator).then(data => {
        this.updateChart(data);
      });
    },
    async fetchChartData(indicator) {
      // Fetch the bullshit data from API Django 
      const response = await axios.get(`http://127.0.0.1:8080/forecast/api/${indicator}`);
      console.log(response.data);
      return {
        labels: response.data.labels,
        values: response.data.values,
        label: response.data.label,
      };
    },
    updateChart(data) {
      if (this.currentChart) {
        this.currentChart.destroy();
      }
      const ctx = document.getElementById('economic-chart').getContext('2d');
      // Need to make it so that the user can change the type of chart
      this.currentChart = new Chart(ctx, {
        type: 'line', 
        data: {
          labels: data.labels,
          datasets: [{
            label: data.label,
            data: data.values,
            borderColor: '#007bff',
            backgroundColor: 'rgba(0, 123, 255, 0.5)',
          }],
        },
      });
    },
  },
  mounted() {
    // Default chart on page load
    this.setChart('GDP'); 
  },
};
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.dashboard-nav button {
  margin-right: 10px;
  padding: 10px 15px;
  font-size: 16px;
  cursor: pointer;
  border: none;
  background-color: #007bff;
  color: white;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.dashboard-nav button:hover {
  background-color: #0056b3;
}

.chart-container {
  position: relative;
  height: 400px;
  width: 100%;
}
</style>

