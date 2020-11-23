<template>
  <div id="app">
    <img alt="Vue logo" src="../assets/logo.png">
    <HitCounter/>
    <button onclick="alert('yay');">Increment the Count</button>
  </div>
</template>

<script>
import HitCounter from '../components/HitCounter.vue'

export default {
  name: 'App',
  components: {
    'HitCounter': HitCounter
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
