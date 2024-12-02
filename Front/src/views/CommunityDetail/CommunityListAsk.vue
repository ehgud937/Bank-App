<template>
  <div>
    <div class="board-top">
      <h2 class="board-title">질문 게시판</h2>
      <!-- 검색바 -->
      <form class="search-form" @submit.prevent="searchArticles">
        <div class="input-group">
          <input type="text" class="form-control search-input" placeholder="검색어를 입력하세요." aria-label="search" v-model="inputSearch">
          <button type="submit" class="btn search-btn">검색</button>
        </div>
      </form>
    </div>
    <div class="table-responsive">
      <table class="table custom-table">
        <thead>
          <tr>
            <th scope="col">글 번호</th>
            <th scope="col">제목</th>
            <th scope="col">작성일</th>
            <th scope="col">작성자</th>
            <th scope="col">좋아요</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="article in paginatedArticles" :key="article.id">
            <td>{{ article.id }}</td>
            <td><RouterLink :to="{ name: 'article-detail', params: { 'id': article.id }}" class="article-link">{{ article.title }}</RouterLink></td>
            <td>{{ formatDate(article.created_at) }}</td>
            <td>{{ article.username }}</td>
            <td>{{ article.like_count }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 페이지네이션 -->
    <nav aria-label="Page navigation" class="mt-4">
      <ul class="pagination justify-content-center">
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)" aria-label="Previous">
            <span aria-hidden="true">&laquo;</span>
          </a>
        </li>
        <li class="page-item" v-for="page in totalPages" :key="page" :class="{ active: currentPage === page }">
          <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
        </li>
        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
          <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)" aria-label="Next">
            <span aria-hidden="true">&raquo;</span>
          </a>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore()

const inputSearch = ref('') // 사용자가 입력하는 검색어
const searchQuery = ref('') // 실제로 검색에 사용되는 검색어

const currentPage = ref(1)
const itemsPerPage = 10

const filteredArticles = computed(() => {
  if (store.articlesData) {
    return store.articlesData.filter(article => 
      article.category === 'ASK' &&
      (!searchQuery.value || article.title.includes(searchQuery.value))
    )
  }
  return []
})

const totalPages = computed(() => {
  return Math.ceil(filteredArticles.value.length / itemsPerPage)
})

const paginatedArticles = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredArticles.value.slice(start, end)
})

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

const fetchArticles = () => {
  store.getArticlesData()
}

const searchArticles = () => {
  searchQuery.value = inputSearch.value // 검색 버튼 클릭 시 실제 검색어 업데이트
  currentPage.value = 1 // 새로운 검색 시 첫 페이지로 이동
}

const formatDate = (dateString) => {
  return `${dateString.slice(0, 10)} ${dateString.slice(11, 16)}`
}

onMounted(() => {
  fetchArticles()
})
</script>

<style scoped>
.board-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.board-title {
  color: #000000;
}

.custom-table {
  border-collapse: separate;
  border-spacing: 0;
  text-align: center;
}

.custom-table th {
  background-color: #e3f2fd;
  color: #000000;
  font-weight: bold;
  border-bottom: 2px solid #dee2e6;
}

.custom-table td {
  border-bottom: 1px solid #dee2e6;
  vertical-align: middle;
  color: #000000;
}

.custom-table tr:hover {
  background-color: #f8f9fa;
}

.article-link {
  color: #000000;
  text-decoration: none;
}

.article-link:hover {
  text-decoration: underline;
}

.pagination {
  margin-top: 20px;
}

.page-link {
  color: #000000;
  border: 1px solid #dee2e6;
  transition: all 0.3s ease;
}

.page-link:hover {
  background-color: #e9ecef;
}

.page-item.active .page-link {
  background-color: #007bff;
  border-color: #007bff;
  color: #ffffff;
}

.search-form {
  display: flex;
  gap: 10px;
  margin: 20px;
  width: auto;
}

.search-input {
  flex-grow: 1;
}

.search-btn {
  background-color: #e3f2fd;
  color: #000000;
  border: 1px solid #dee2e6;
}

.search-btn:hover {
  background-color: #d0e5f5;
}
</style>