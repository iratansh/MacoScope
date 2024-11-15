<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

body[data-theme='light'] {
  background-color: #f8f9fa;
  color: #212529;
}

body[data-theme='dark'] {
  background-color: #212529;
  color: #f8f9fa;
}

.navbar-dark .navbar-brand, .navbar-dark .nav-link {
  color: #f8f9fa;
}

body.dark-mode {
  background-color: #222;
  color: #eee;
}

body.light-mode {
  background-color: #fff;
  color: #333;
}

</style>

