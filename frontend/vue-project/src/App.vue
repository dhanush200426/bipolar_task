<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router'
import { computed } from 'vue'
import AppShell from './components/AppShell.vue'
import Toast from './components/Toast.vue'

const route = useRoute()
const isLoginPage = computed(() => route.name === 'login')
</script>

<template>
  <div id="app">
    <AppShell v-if="!isLoginPage">
      <RouterView />
    </AppShell>
    <RouterView v-else />
    <Toast />
  </div>
</template>

<style>
#app {
  min-height: 100vh;
}
</style>
