<template>
  <div class="login-container">
    <div class="login-card">
      <div class="card-body">
        <h4 class="card-title mb-4">회원 탈퇴</h4>
        <p>회원 탈퇴를 진행하시려면 비밀번호를 입력해 주세요.</p>
        <form @submit.prevent="signout">
          <div class="mb-3">
            <input type="password" class="form-control custom-input" placeholder="비밀번호를 입력하세요" aria-label="Password" v-model="inputPw">
          </div>
          <p class="error-message" v-show="isInvalid">비밀번호는 최소 8자 이상이어야 합니다.</p>
          <button type="submit" class="btn btn-danger btn-block">회원 탈퇴</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore()

const inputPw = ref('')

const isInvalid = computed(() => {
  if (inputPw.value.length < 8) {
    return true
  }
})

const signout = function () {
  if (confirm('회원 탈퇴를 진행하시겠습니까?')) {
    store.signout(inputPw.value)
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