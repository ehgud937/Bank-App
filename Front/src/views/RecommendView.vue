<template>
  <div class="container">
    <div class="container d-flex row">
      <h3 v-show="store.isLogin" class="mt-3 ms-3">{{ store.loginusername }}님에게 추천하는 상품 목록</h3>
      <div class="recommend-container mb-2 col-sm-12 col-md-3">
        <div class="recommend-nav">
          <RouterLink class="nav-item" :to="{ name: 'recommend_for_you' }">머신 러닝 기반 추천</RouterLink>
          <RouterLink class="nav-item" :to="{ name: 'recommend_user_info' }">사용자 정보 기반 추천</RouterLink>
        </div>
      </div>  
      <div class="recommend-view-container mb-2 col-sm-12 col-md-9">
        <RouterView />
      </div>
    </div>
  </div>

</template>

<script setup>
import { onMounted } from 'vue';
import { RouterLink, RouterView } from 'vue-router';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore()

onMounted(() => {
  store.getRecommendProductsData()
})


</script>

<style scoped>
.recommend-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.recommend-view-container {
  max-width: 1200px;
  padding: 20px;
  background-color: #ffffff;
  height: 100%;
}

.recommend-nav {
  display: flex;
  flex-direction: column;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 4px rgba(0.3, 0.3, 0.1, 0.1);
}

.nav-item {
  padding: 12px 16px;
  color: #333;
  text-decoration: none;
  transition: all 0.3s ease;
  border-bottom: 1px solid #e9ecef;
  background-color: #ffffff;
}

.nav-item:last-child {
  border-bottom: none;
}

.nav-item:hover {
  background-color: #f8f9fa;
  font-weight: bold;
  color: #007bff;
  transform: translateX(5px);
}

.router-link-active {
  font-weight: bold;
  background-color: #e3f2fd;
  color: #007bff;
  border-left: 4px solid #007bff;
}

.router-link-exact-active {
  color: #007bff;
}
</style>