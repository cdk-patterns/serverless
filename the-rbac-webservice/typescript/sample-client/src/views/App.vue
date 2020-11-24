<template>
    <div id="app">
      <img alt="Vue logo" src="../assets/logo.png">
      <Home msg="Welcome there traveller..."/>
    </div>

</template>

<script>
import Home from '../components/Home.vue'

export default {
  name: 'App',
  components: {
    'Home': Home
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
