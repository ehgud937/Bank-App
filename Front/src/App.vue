<template>
  <TheNavigation class="sticky-top" />

  <div class="viewer">
    <RouterView />
  </div>
  
  <button v-if="store.isLogin" @click="togglePopup" class="ai-chat-button">
    <span class="button-text">AI 채팅</span>
  </button>

  <TheFooter class="bottom-0"/>

  <!-- Custom Popup -->
  <transition name="fade">
    <div v-if="isPopupVisible" class="custom-popup">
      <div class="popup-content">
        <div class="popup-header">
          <h5 class="popup-title">AI 상담</h5>
          <div class="d-flex align-items-center gap-3">
            <button @click="clearMessage" class="btn btn-primary">새 대화 시작하기</button>
            <button @click="togglePopup" class="btn-close" aria-label="Close"></button>
          </div>
        </div>
        <div class="popup-body">
          <AiChat />
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import TheNavigation from '@/components/layout/TheNavigation.vue';
import TheFooter from '@/components/layout/TheFooter.vue';
import AiChat from './components/home/AiChat.vue';

import { ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { useCounterStore } from './stores/counter';

const store = useCounterStore()

const isPopupVisible = ref(false)

const togglePopup = () => {
  isPopupVisible.value = !isPopupVisible.value
}

const clearMessage = function () {
  store.clearMessage()
}
</script>

<style scoped>
.custom-popup {
  position: fixed;
  bottom: 80px;
  right: 20px;
  width: 400px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  z-index: 1001;
}

.popup-content {
  display: flex;
  flex-direction: column;
  max-height: 80vh;
}

.popup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e9ecef;
}

.popup-title {
  margin: 0;
}

.popup-body {
  padding: 1rem;
  overflow-y: auto;
}

.popup-footer {
  display: flex;
  justify-content: flex-end;
  padding: 1rem;
  border-top: 1px solid #e9ecef;
  gap: 0.5rem;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.ai-chat-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: #007bff;
  color: white;
  border: none;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.ai-chat-button::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: rgba(255, 255, 255, 0.1);
  transform: rotate(45deg);
  transition: all 0.3s ease;
}

.ai-chat-button:hover {
  background-color: #0056b3;
  transform: scale(1.05);
}

.ai-chat-button:hover::before {
  top: -75%;
  left: -75%;
}

.button-text {
  position: relative;
  z-index: 1;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(0, 123, 255, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(0, 123, 255, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(0, 123, 255, 0);
  }
}

.ai-chat-button:focus {
  outline: none;
  animation: pulse 1.5s infinite;
}

.viewer {
  min-height: 70vh;
}

</style>