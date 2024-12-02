<template>
  <div class="news-container">
    <div class="news-card">
      <h4 class="card-title">오늘의 주요 금융 헤드라인</h4>
      <TodayNewsThumbnails />
      <hr>
      <div v-if="store.newsData" class="news-list">
        <ol class="list-group list-group-flush">
          <li v-for="(news, index) in store.newsData.articles" :key="news.id" class="list-group-item">
            <div class="d-flex justify-content-between align-items-center">
              <a :href="news.url" class="news-link">{{ news.title }}</a>
              <span class="news-press">{{ news.press }}</span>
            </div>
          </li>
        </ol>
      </div>
    </div>
  </div>
</template>

<script setup>
import TodayNewsThumbnails from './TodayNewsThumbnails.vue';

import { useCounterStore } from '@/stores/counter';

const store = useCounterStore()
</script>

<style scoped>
.news-container {
  margin: 0;
}

.news-card {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.card-title {
  color: #333;
  font-weight: bold;
  padding-left: 10px;
  margin-bottom: 19px;
}

.news-list {
  padding-left: 10px;
  padding-right: 10px;
}

.list-group-item {
  border: none;
  border-bottom: 1px solid #dee2e6;
  padding: 8px 0;
}

.list-group-item:last-child {
  border-bottom: none;
}

.news-link {
  color: #333;
  text-decoration: none;
  transition: all 0.3s ease;
}

.news-link:hover {
  color: #0060c6;
  font-weight: bold;
}

.news-press {
  font-size: 0.9em;
  color: #6c757d;
}
</style>