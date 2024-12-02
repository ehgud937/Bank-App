<template>
  <div class="chat-container">
    <div class="messages-container">
      <div v-for="(message, index) in store.messages" :key="index" 
           :class="['message', message.role]" 
           :style="{ animationDelay: `${index * 0.1}s` }">
        {{ message.content }}
      </div>
    </div>
    <hr>
    <div class="input-container">
      <input class="message-input" v-model="inputMessage" @keyup.enter="sendMessage" placeholder="메시지를 입력하세요...">
      <button class="send-button" @click="sendMessage">
        <span class="send-icon">▶</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore()

const inputMessage = ref('')

const sendMessage = () => {
  if (inputMessage.value.trim()) {
    sendMessageToAi(inputMessage.value)
    inputMessage.value = ''
  }
}

const sendMessageToAi = function (inputMessage) {
  store.messages.push({ role: 'user', content: inputMessage })

  axios({
    method: 'post',
    url: `${store.API_URL}/chat/message/`,
    headers: {
      Authorization: `Token ${store.token}`
    },
    data: {
      message: inputMessage,
      conversation_id: store.conversation_id
    }
  })
    .then((response) => {
      console.log(response)
      store.conversation_id = response.data.conversation_id
      store.messages.push({ role: 'ai', content: response.data.message })
    })
    .catch((error) => {
      console.log(error)
      store.messages.push({ role: 'system', content: '메시지 전송 중 오류가 발생했습니다.' })
    })
}
</script>

<style scoped>
.chat-container {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  background-color: #f9f9f9;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
}

.messages-container {
  max-height: 400px;
  overflow-y: auto;
  padding: 10px;
}

.message {
  padding: 12px 18px;
  margin: 8px 0;
  border-radius: 20px;
  max-width: 80%;
  word-wrap: break-word;
  animation: fadeIn 0.5s ease-out forwards;
  opacity: 0;
  transform: translateY(20px);
}

@keyframes fadeIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.user {
  background-color: #007bff;
  color: white;
  margin-left: auto;
  border-bottom-right-radius: 5px;
}

.ai {
  background-color: #e9ecef;
  color: #343a40;
  margin-right: auto;
  border-bottom-left-radius: 5px;
}

.system {
  background-color: #ffc107;
  color: #343a40;
  text-align: center;
  margin: 10px auto;
}

.input-container {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  width: 100%;
}

.message-input {
  flex-grow: 1;
  padding: 12px 20px;
  border: none;
  border-radius: 25px;
  font-size: 16px;
  background-color: #e9ecef;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.message-input:focus {
  outline: none;
  box-shadow: 0 0 0 2px #007bff;
}

.send-button {
  width: 50px;
  height: 50px;
  min-width: 50px;  /* 버튼의 최소 너비 설정 */
  border-radius: 50%;
  background-color: #007bff;
  color: white;
  border: none;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.send-button:hover {
  background-color: #0056b3;
  transform: scale(1.05);
}

.send-icon {
  transform: translateX(1px);
}

/* 반응형 디자인 */
@media screen and (max-width: 480px) {
  .chat-container {
    padding: 10px;
  }

  .message {
    max-width: 90%;
  }

  .input-container {
    flex-direction: column;
    gap: 5px;
  }

  .message-input {
    width: 100%;
  }

  .send-button {
    width: 100%;
    height: 40px;
    border-radius: 20px;
  }
}
</style>