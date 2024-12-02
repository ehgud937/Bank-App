<template>
  <div class="community-nav">
    <RouterLink class="nav-item" :to="{ name: 'community_all' }">전체</RouterLink>
    <RouterLink class="nav-item" :to="{ name: 'community_notice' }">공지</RouterLink>
    <RouterLink class="nav-item" :to="{ name: 'community_free' }">자유</RouterLink>
    <RouterLink class="nav-item" :to="{ name: 'community_ask' }">질문</RouterLink>
    <RouterLink class="nav-item" :to="{ name: 'community_review' }">후기</RouterLink>
    <RouterLink class="nav-item" :to="{ name: 'community_etc' }">기타</RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';
</script>

<style scoped>
.community-nav {
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
  color: #007bff;
  transform: translateX(5px);
  font-weight: bold;
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