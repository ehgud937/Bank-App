<template>
  <div class="carousel-container">
    <div class="carousel-wrapper">
      <div class="carousel-slide">
        <div class="main-image-container">
          <img :src="main_img" alt="Main Image" class="main-image">
          <div class="button-container d-none d-lg-block">
            <h2 class="fw-bold">내 집 마련을 위한</h2>
            <h2 class="mb-4 fw-bold">스마트한 자산 관리의 시작</h2>
            <button v-if="store.isLogin" class="btn btn-primary btn-sm">
              <RouterLink class="nav-link" :to="{ name: 'recommend' }">시작하기</RouterLink>
            </button>
            <button v-else class="btn btn-primary btn-sm">
              <RouterLink class="nav-link" :to="{ name: 'login' }">로그인하고 시작하기</RouterLink>
            </button>
          </div>
        </div>
      </div>
      <div class="container carousel-slide">
        <div class="content-container">
          <div class="d-flex row">
            <div class="d-flex flex-column col-sm-12 col-md-9 gap-2">
              <TodayNews />
            </div>
            <div class="d-flex flex-column col-sm-12 col-md-3 gap-2">
              <TodayExchangeRate />
              <TodayKeyword />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import TodayExchangeRate from '@/components/home/TodayExchangeRate.vue';
import TodayNews from '@/components/home/TodayNews.vue';
import TodayKeyword from '@/components/home/TodayKeyword.vue';

import main_img from '@/assets/main_carousel_img/main_img.jpg'

import { onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter';
import { RouterLink } from 'vue-router';

const store = useCounterStore()

onMounted(() => {
  console.log('환율')
  store.saveExchangeRate()

  console.log('예금')
  store.saveDepositProducts()

  console.log('적금')
  store.saveSavingtProducts()

  console.log('주담대')
  store.saveMortgagetProducts()

  console.log('뉴스')
  store.getNewsData()

  console.log('키워드')
  store.getkeywordsData()
})
</script>

<style scoped>
.carousel-container {
  width: 100%;
  height: 100vh;
  overflow-y: scroll;
  scroll-snap-type: y mandatory;
}

.carousel-wrapper {
  height: 200vh;
}

.carousel-slide {
  height: 100vh;
  scroll-snap-align: start;
  width: 100%;
}

.main-image-container, .content-container {
  height: 100%;
  width: 100%;
}

.main-image-container {
  position: relative;
  overflow: hidden;
}

.main-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.button-container {
  position: absolute;
  top: 50%;
  right: 5%;
  transform: translateY(-50%);
  text-align: right;
  color: rgb(16, 88, 182);
  text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.5);
}

.content-container {
  padding: 20px;
  box-sizing: border-box;
}

/* 반응형 디자인을 위한 미디어 쿼리 */
@media (max-width: 768px) {
  .button-container {
    right: 50%;
    transform: translate(50%, -50%);
    text-align: center;
  }
}

.main-image {
  width: 100%;
  object-fit: cover;
  transition: filter 0.3s ease-in-out;
}

.main-image-container::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.15);
  opacity: 0;
  transition: opacity 0.3s ease-in-out;
}

.main-image-container:hover::after {
  opacity: 1;
}

.button-container {
  position: absolute;
  top: 50%;
  left: 46%;
  transform: translate(-50%, -50%);
  width: 100%;
  z-index: 1;
}

.btn-sm {
  padding: 10px 20px;
  font-size: 1.2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
}

.nav-link {
  color: white;
  text-decoration: none;
}
</style>