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
@import "assets/styles/dark-style.css";

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  /*color: #2c3e50;*/

  width: 70%;
  margin: 0 auto;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  /*color: #2c3e50;*/
}

#nav a.router-link-exact-active {
  /*color: #42b983;*/
}
</style>
