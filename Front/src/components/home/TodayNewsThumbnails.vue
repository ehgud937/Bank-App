<template>
  <div>
    <div class="news-grid" v-show="store.newsData">
      <div v-for="(article, index) in store.newsData.articles" :key="index" class="grid-item" @click="goToArticle(article.url)">
        <img :src="article.thumbnail_url" class="thumbnail" :alt="article.title" />
        <div class="overlay">
          <div class="title"><small>{{ article.title }}</small></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();

function goToArticle(url) {
  window.open(url, '_blank');
}
</script>

<style scoped>
.news-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 10px;
  padding: 10px;
}

.grid-item {
  position: relative;
  cursor: pointer;
}

.thumbnail {
  width: 100%;
  height: auto;
  border-radius: 5px;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5); 
  color: white;
  opacity: 0; /* 초기 상태에서는 보이지 않음 */
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 5px;
  transition: opacity 0.3s ease; 
}

.grid-item:hover .overlay {
  opacity: 1; /* 호버 시 제목 표시 */
}

.title {
  padding: 10px;
}
</style>