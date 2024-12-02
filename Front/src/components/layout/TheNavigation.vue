<template>
  <div>
    <nav class="navbar navbar-expand-lg" style="background-color: #e3f2fd;">
      <div class="container-fluid ms-2">
        <a class="navbar-brand" href="#"><RouterLink class="nav-link" :to="{ name: 'home' }"><img :src="notextLogo" alt="MAIN" style="height: 45px;"></RouterLink></a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item" v-if="store.isLogin">
              <RouterLink class="nav-link" :to="{ name: 'product' }">PRODUCTS</RouterLink>
            </li>
            <li class="nav-item" v-if="store.isLogin">
              <RouterLink class="nav-link" :to="{ name: 'recommend' }">RECOMMENDATION</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'exchange' }">EXCHANGE</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'bankmap' }">BANK MAP</RouterLink>
            </li>
            <li class="nav-item" v-if="store.isLogin">
              <RouterLink class="nav-link" :to="{ name: 'community_all' }">COMMUNITY</RouterLink>
            </li>
          </ul>
          <!-- 로그인 관련 -->
          <div v-if="!store.isLogin">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item" v-show="!store.isLogin">
                <RouterLink class="nav-link" :to="{ name: 'login' }">LOGIN</RouterLink>
              </li>
              <li class="nav-item" v-show="!store.isLogin">
                <RouterLink class="nav-link" :to="{ name: 'register' }">SIGNUP</RouterLink>
              </li>
            </ul>
          </div>
          <div v-else class="nav-item dropdown">
            <a class="d-flex justify-content-center align-items-center nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              <img src="@/assets/common/blank-profile.png" alt="Avatar" class="m-2" width="32" height="32">
              <strong>{{ store.loginusername }}</strong>
            </a>
            <ul class="dropdown-menu dropdown-menu-end">
              <li class="dropdown-item">
                <RouterLink class="nav-link" :to="{ name: 'profile' }">회원 정보</RouterLink>
              </li>
              <li class="dropdown-item">
                <RouterLink class="nav-link" :to="{ name: 'modify-profile' }">회원 정보 수정</RouterLink>
              </li>
              <li><hr class="dropdown-divider"></li>
              <li class="dropdown-item">
                <div class="d-flex justify-content-start align-items-center">
                  <img src="@/assets/common/logout.png" width="24" alt="logout">
                  <button class="btn btn-link text-decoration-none" style="vertical-align: middle; color: red" @click.prevent="logout"><strong>Logout</strong></button>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';
import { useCounterStore } from '@/stores/counter';

import notextLogo from '@/assets/common/Main_logo_2.png'

const store = useCounterStore()

const logout = function () {
  store.logout()
}

</script>

<style scoped>
.navbar {
  background: linear-gradient(to right, #e3f2fd, #a1c6ea);
}

.nav-link {
  transition: all 0.3s ease, color 0.3s ease;
  margin-bottom: 2px;
}

.nav-link:hover {
  background-color: rgba(0, 123, 255, 0.1);
  color: black; 
  border-radius: 8px;
  font-weight: bold;
}

.router-link-active {
  font-weight: bold;
}

.router-link-exact-active {
  color: black; 
}
</style>