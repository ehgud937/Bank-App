<template>
  <div class="product-container">
    <h3 v-show="store.isLogin" class="product-title">전체 상품 목록</h3>
    
    <div class="product-card">
      <div class="product-nav">
        <ul class="nav-list">
          <li class="nav-item">
            <RouterLink class="nav-link" :to="{ name: 'deposit-product'}">예금</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" :to="{ name: 'saving-product'}">적금</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" :to="{ name: 'mortgage-product'}">주택 담보 대출</RouterLink>
          </li>
        </ul>
      </div>
      <div class="product-content">
        <RouterView />
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter';
import { RouterLink, RouterView } from 'vue-router'

const store = useCounterStore()
</script>

<style scoped>
.product-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.product-title {
  color: #333;
  margin-bottom: 20px;
}

.product-card {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.product-nav {
  background-color: #e3f2fd;
  padding: 10px;
  border-bottom: 1px solid #c8d6e0;
}

.nav-list {
  display: flex;
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  margin-right: 10px;
}

.nav-link {
  color: #333;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.nav-link:hover {
  background-color: #007bff;
  color: white;
  font-weight: bold;
}

.router-link-active {
  font-weight: bold;
  background-color: #007bff;
  color: white;
}

.product-content {
  padding: 20px;
}
</style>