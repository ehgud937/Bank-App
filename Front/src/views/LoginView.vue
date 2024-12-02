<template>
  <div class="login-container">
    <div class="login-card">
      <div class="card-body">
        <h4 class="card-title mb-4">로그인</h4>
        <form @submit.prevent="login">
          <div class="mb-3">
            <input type="text" class="form-control custom-input" placeholder="아이디를 입력하세요" aria-label="Username" v-model="inputId">
          </div>
          <div class="mb-3">
            <input type="password" class="form-control custom-input" placeholder="비밀번호를 입력하세요" aria-label="Password" v-model="inputPw">
          </div>
          <p class="error-message" v-show="isInvalid">비밀번호는 최소 8자 이상이어야 합니다.</p>
          <button type="submit" class="btn btn-primary btn-block">로그인</button>
        </form>
        <div class="divider">또는</div>
        <button class="btn btn-kakao btn-block" @click="kakaoLogin">카카오로 로그인</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore()

const inputId = ref('')
const inputPw = ref('')

const isInvalid = computed(() => {
  if (inputPw.value.length < 8) {
    return true
  }
})

const login = function () {
  const payload = {
    email: inputId.value,
    password: inputPw.value
  }
  store.login(payload)
}

const kakaoLogin = async () => {
  try {
    const result = await store.kakaoLogin()
    if (result.needsAdditionalInfo) {
      router.push('/additional-info')
    } else {
      // 로그인 성공 처리 (예: 홈페이지로 리다이렉트)
      router.push('/')
    }
  } catch (error) {
    console.error('카카오 로그인 에러:', error)
    // 에러 처리 (예: 에러 메시지 표시)
  }
}

</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.login-card {
  width: 400px;
  border: none;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1), 0 8px 16px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
  padding: 20px;
}

.card-title {
  color: #1c1e21;
  font-weight: bold;
  text-align: center;
}

.custom-input {
  border-radius: 6px;
  border: 1px solid #dddfe2;
  font-size: 17px;
  padding: 10px 10px;
  transition: border .3s ease;
  width: 100%;
}

.custom-input:focus {
  border-color: #1877f2;
  box-shadow: 0 0 0 2px rgba(24, 119, 242, 0.2);
}

.error-message {
  color: #ff4d4f;
  font-size: 14px;
  margin-top: -10px;
  margin-bottom: 10px;
}

.btn-primary {
  background-color: #1877f2;
  border: none;
  padding: 10px 0px;
  transition: background-color .3s ease;
}

.btn-primary:hover {
  background-color: #166fe5;
}

.btn-block {
  display: block;
  width: 100%;
}

.divider {
  text-align: center;
  margin: 20px 0;
  color: #96999e;
}

.divider::before,
.divider::after {
  content: "";
  display: inline-block;
  width: 40%;
  border-top: 1px solid #ccd0d5;
  margin: 0 10px;
  vertical-align: middle;
}

.btn-kakao {
  background-color: #FEE500;
  color: #000000;
  padding: 8px 10px;
}

.btn-kakao:hover {
  background-color: #FDD835;
}
</style>