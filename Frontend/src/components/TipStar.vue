<template>
    <div class="tip-star-container" @mouseover="showTip = true" @mouseleave="showTip = false">
      <div :class="['tip-star', isDarkMode ? 'dark' : 'light']">
        ⭐
      </div>
      <div v-if="showTip" 
           :class="['tip-popup', isDarkMode ? 'dark' : 'light']"
           :style="{ marginLeft: marginLeft + 'px' }">
        {{ tip }}
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'TipStar',
    props: {
      tip: {
        type: String,
        required: true
      },
      isDarkMode: {
        type: Boolean,
        required: true
      },
      marginLeft: {
        type: Number,
        default: 50 
      }
    },
    data() {
      return {
        showTip: false
      }
    }
  }
  </script>
  
  <style scoped>
  .tip-star-container {
    display: inline-block;
    position: relative;
  }
  
  .tip-star {
    display: inline-block;
    cursor: pointer;
    font-size: 1.5rem;
    transition: color 0.3s;
  }
  
  .tip-star.light {
    color: #333333;
  }
  
  .tip-star.dark {
    color: #ffffff;
  }
  
  .tip-popup {
    position: absolute;
    top: 30px;
    padding: 10px;
    border-radius: 5px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    width: 200px;
    font-size: 0.9rem;
    text-align: left;
    z-index: 10;
    transition:
      background-color 0.3s,
      color 0.3s;
  }
  
  .tip-popup.light {
    background-color: #ffffff;
    color: #333333;
  }
  
  .tip-popup.dark {
    background-color: #333333;
    color: #ffffff;
  }
  </style>
  