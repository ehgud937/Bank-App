<template>
  <div class="keywords-container">
    <div class="keywords-card">
      <h4 class="card-title">실시간 인기 키워드</h4>
      <hr>
      <div v-if="store.keywordsData" class="keywords-list">
        <ol class="list-group list-group-flush">
          <li v-for="(keyword, index) in store.keywordsData" :key="keyword.id" class="list-group-item">
            <span class="keyword-rank">{{ index + 1 }}</span>
            <a class="keyword-link" :href="`https://www.google.com/search?q=${keyword.keyword}`">
              {{ keyword.keyword }}
            </a>
          </li>
        </ol>
      </div>
    </div>
  </div>
</template>


<script setup>
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore()
</script>

<style scoped>
.keywords-container {
  margin: 0;
}

.keywords-card {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.card-title {
  color: #333;
  font-weight: bold;
  margin-bottom: 19px;
}

.keywords-list {
  padding-left: 0;
}

.list-group-item {
  border: none;
  border-bottom: 1px solid #dee2e6;
  padding: 8px 0;
  display: flex;
  align-items: center;
}

.list-group-item:last-child {
  border-bottom: none;
}

.keyword-rank {
  font-weight: bold;
  color: #0060c6;
  margin-right: 15px;
  min-width: 25px;
  text-align: center;
}

.keyword-link {
  color: #333;
  text-decoration: none;
  transition: all 0.3s ease;
}

.keyword-link:hover {
  color: #0060c6;
  font-weight: bold;
}
</style>