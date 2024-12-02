// main.js
import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { Chart, registerables } from 'chart.js'

import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

import App from './App.vue'
import router from './router'

window.kakao = window.kakao || {}

Chart.register(...registerables)

const app = createApp(App)
const pinia = createPinia()

pinia.use(piniaPluginPersistedstate)

app.use(pinia)  // Pinia 인스턴스를 앱에 추가
app.use(router)

app.mount('#app')