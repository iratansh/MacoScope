<template>
    <div
      v-if="visible"
      class="toast show position-fixed top-0 end-0 m-3 bg-success text-white"
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
    >
      <div class="d-flex">
        <div class="toast-body">
          <strong>{{ title }}</strong>
          <p>{{ message }}</p>
        </div>
        <button
          type="button"
          class="btn-close btn-close-white me-2 m-auto"
          aria-label="Close"
          @click="hide"
        ></button>
      </div>
    </div>
  </template>
  
  <script>
  import 'bootstrap/dist/css/bootstrap.min.css'
  import 'bootstrap'
  export default {
    props: {
      title: {
        type: String,
        default: 'Update'
      },
      message: {
        type: String,
        required: true
      }
    },
    data() {
      return {
        visible: true
      }
    },
    methods: {
      hide() {
        this.visible = false
      }
    }
  }
  </script>
  
  <style scoped>
  .toast {
    z-index: 1055;
  }
  </style>
  