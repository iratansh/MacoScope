<template>
    <b-navbar toggleable="lg" variant="light" type="light">
      <b-navbar-brand href="#" class="brand-logo">MacroScope</b-navbar-brand>
  
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
  
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav class="ml-auto nav-links">
          <b-nav-item href="#" class="nav-link">Dashboard</b-nav-item>
          <b-nav-item href="#" class="nav-link">Forecasts</b-nav-item>
          <b-nav-item href="#" class="nav-link">About</b-nav-item>
          <b-nav-item href="#" class="nav-link">Contact</b-nav-item>
  
          <b-nav-item class="nav-link">
            <b-dropdown right>
              <template #button-content>
                {{ username }}
              </template>
              <b-dropdown-item href="#">Profile</b-dropdown-item>
              <b-dropdown-item href="#">Logout</b-dropdown-item>
            </b-dropdown>
          </b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: 'Testing'
      };
    }
  };
  </script>
  
  <style scoped>
  .brand-logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: #000000;
    margin-right: auto;
  }
  
  .nav-links {
    display: flex;
    justify-content: flex-end;
    align-items: center;
  }
  
  .nav-link {
    color: #000000 !important;
    margin-left: 1rem;
    font-size: 1rem;
    padding: 0.5rem 1rem;
    transition: color 0.3s ease, background-color 0.3s ease;
  }
  
  .nav-link:hover {
    color: #007bff !important; 
    background-color: rgba(0, 123, 255, 0.1); 
    border-radius: 0.25rem;
  }
  
  .dropdown-toggle {
    font-weight: bold;
    color: #000000 !important;
    margin-left: 1rem;
  }
  
  .dropdown-menu {
    min-width: auto;
  }
  
  .dropdown-item:hover {
    background-color: #007bff;
    color: #ffffff !important;
  }
  </style>
  
  