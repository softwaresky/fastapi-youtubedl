<template>
  <div id="app">
    <div id="nav">
      <router-link to="/ydl/list">List</router-link>
    </div>
    <div>
      <router-view />
    </div>

  </div>
</template>

<style>

body {
  color: #f8f8f2 !important;
  background: #282a36 !important;
}

label {
  color: #f8f8f2 !important;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;


  width: 70%;
  margin: 0 auto;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #50fa7b !important;
}

#nav a.router-link-exact-active {
  color: #50fa7b !important;
}
</style>
