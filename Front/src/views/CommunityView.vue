<template>
  <div class="community-container">
    <div class="row">
      <div class="col-sm-12 col-md-3">
        <div class="sidebar-card">
          <CommunitySide />
          <div class="mt-3">
            <RouterLink class="create-article-btn" :to="{ name: 'create-article' }">게시글 작성</RouterLink>
          </div>
        </div>
      </div>  
      <div class="col-sm-12 col-md-9">
        <div class="content-card">
          <RouterView />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
import CommunitySide from '@/components/community/CommunitySide.vue';
</script>

<style scoped>
.community-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.sidebar-card, .content-card {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 20px;
  height: 100%;
}

.create-article-btn {
  display: block;
  background-color: #007bff;
  color: #ffffff;
  text-align: center;
  padding: 10px;
  border-radius: 4px;
  text-decoration: none;
  transition: all 0.3s ease;
}

.create-article-btn:hover {
  background-color: #0056b3;
  font-weight: bold;
}

@media (max-width: 768px) {
  .community-container {
    padding: 10px;
  }
  
  .sidebar-card, .content-card {
    margin-bottom: 20px;
  }
}
</style>