<script setup lang="ts">
import AppShell from './components/AppShell.vue'
import Toast from './components/Toast.vue'
</script>

<template>
  <div class="app-root">
    <AppShell />
    <Toast />
  </div>
</template>

<style>
.app-root {
  min-height: 100vh;
  width: 100%;
  max-width: 100vw;
  overflow-x: hidden;
  position: relative;
}
</style>
