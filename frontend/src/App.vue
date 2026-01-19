<script>
export default { name: 'App' }
</script>

<template>
  <router-view />
</template>

<style>
body {
  background: linear-gradient(135deg, #f7f3e8 0%, #f3e9d2 100%);
}
#app {
  min-height: 100vh;
  background: #f7f3e8; /* 也可加渐变或纹理 */
}
</style>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
