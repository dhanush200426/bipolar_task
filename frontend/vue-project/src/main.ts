import './styles/base.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import Toast from './components/Toast.vue'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.component('Toast', Toast)

// Global error handler
app.config.errorHandler = (err, instance, info) => {
  console.error('Global error:', err, info)
  // In production, you might want to show a global error state
}

// Window error handlers
if (typeof window !== 'undefined') {
  window.addEventListener('error', (event) => {
    console.error('Window error:', event.error)
  })

  window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled rejection:', event.reason)
  })
}

app.mount('#app')
