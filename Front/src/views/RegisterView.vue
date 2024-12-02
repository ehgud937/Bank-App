<template>
  <div class="signup-container">
    <div class="signup-card">
      <div class="card-body">
        <h4 class="card-title mb-4">회원가입</h4>
        <form @submit.prevent="signup">
          <div class="mb-3">
            <input type="email" class="form-control custom-input" placeholder="이메일을 입력하세요" v-model="email">
          </div>
          <div class="mb-3">
            <input type="password" class="form-control custom-input" placeholder="비밀번호를 입력하세요" v-model="password1">
          </div>
          <div class="mb-3">
            <input type="password" class="form-control custom-input" placeholder="비밀번호를 다시 입력하세요" v-model="password2">
          </div>
          <div class="mb-3">
            <input type="text" class="form-control custom-input" placeholder="닉네임을 입력하세요" v-model="username">
          </div>
          <div class="mb-3">
            <input type="date" class="form-control custom-input" v-model="birthdate">
          </div>
          <div class="mb-3">
            <input type="text" class="form-control custom-input" placeholder="보유한 자산을 입력하세요" v-model="assets">
          </div>
          <div class="mb-3">
            <input type="text" class="form-control custom-input" placeholder="연 소득을 입력하세요" v-model="annual_income">
          </div>
          <div class="mb-3">
            <select class="form-select custom-select" v-model="investment_type">
              <option value="" disabled selected>투자 유형을 선택하세요</option>
              <option value="CONSERVATIVE">안정형</option>
              <option value="MODERATE">중립형</option>
              <option value="AGGRESSIVE">공격형</option>
              <option value="SPECULATIVE">위험추구형</option>
            </select>
          </div>
          <div class="mb-3">
            <select class="form-select custom-select" v-model="primary_bank">
              <option value="" disabled selected>주거래 은행을 선택하세요</option>
              <option value="KB">KB국민은행</option>
              <option value="SH">신한은행</option>
              <option value="WR">우리은행</option>
              <option value="NH">농협은행</option>
              <option value="IBK">기업은행</option>
              <option value="KEB">하나은행</option>
              <option value="ETC">기타</option>
            </select>
          </div>
          <button type="submit" class="btn btn-primary btn-block">회원가입</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore()

const email = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const birthdate = ref(null)
const assets = ref(null)
const annual_income = ref(null)
const investment_type = ref(null)
const primary_bank = ref(null)
const username = ref(null)

const signup = function () {
  const payload = {
    email: email.value,
    username: username.value,
    password1: password1.value, 
    password2: password2.value,  
    birthdate: birthdate.value,
    assets: assets.value,
    annual_income: annual_income.value,
    investment_type: investment_type.value,
    primary_bank: primary_bank.value
  }
  store.signup(payload)
}

</script>

<style scoped>
.signup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}

.signup-card {
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

.custom-input,
.custom-select {
  border-radius: 6px;
  border: 1px solid #dddfe2;
  font-size: 17px;
  padding: 10px 10px;
  transition: border .3s ease;
  width: 100%;
}

.custom-input:focus,
.custom-select:focus {
  border-color: #1877f2;
  box-shadow: 0 0 0 2px rgba(24, 119, 242, 0.2);
}

.btn-primary {
  background-color: #1877f2;
  border: none;
  padding: 10px 20px;
  transition: background-color .3s ease;
}

.btn-primary:hover {
  background-color: #166fe5;
}

.btn-block {
  display: block;
  width: 100%;
}
</style>