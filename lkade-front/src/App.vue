<template>
  <div id="app">
    <!--<img src="./assets/logo.png">-->
    <router-view />
    <Triples></Triples>


  </div>
</template>

<script>
import Triples from './components/Triples.vue'

// import

export default {
  name: 'App',
  components: {
    Triples,
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
