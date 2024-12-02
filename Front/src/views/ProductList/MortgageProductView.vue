<template>
  <div class="product-list-container">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3 class="product-title">주택 담보 대출 상품</h3>
      
      <!-- 검색 -->
      <div class="search-form">
        <form @submit.prevent="searchProducts">
          <div class="input-group">
            <input 
              type="text" 
              class="form-control search-input" 
              v-model="searchTerm" 
              placeholder="은행명을 입력하세요"
            >
            <button class="btn search-btn" type="submit">검색</button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="store.mortgageProducts" class="table-responsive">
      <table class="table custom-table">
        <thead>
          <tr>
            <th scope="col">금융 회사명</th>
            <th scope="col">상품명</th>
            <th scope="col">아파트 + 고정</th>
            <th scope="col">아파트 + 변동</th>
            <th scope="col">아파트외 + 고정</th>
            <th scope="col">아파트외 + 변동</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in paginatedProducts" :key="product.id">
            <td>{{ product.kor_co_nm }}</td>
            <td>
              <RouterLink :to="{ name: 'mortgage-product-detail', params: { 'id': product.id }}" class="product-link">
                {{ product.fin_prdt_nm }}
              </RouterLink>
            </td>
            <td>{{ product.apt_fixed }}</td>
            <td>{{ product.apt_nonfixed }}</td>
            <td>{{ product.nonapt_fixed }}</td>
            <td>{{ product.nonapt_nonfixed }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="text-center">
      <div class="spinner-border m-5" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- 페이지네이션 -->
    <nav aria-label="Page navigation" class="mt-4">
      <ul class="pagination justify-content-center">
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">이전</a>
        </li>
        <li v-for="page in totalPages" :key="page" class="page-item" :class="{ active: currentPage === page }">
          <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
        </li>
        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
          <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">다음</a>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()

const currentPage = ref(1)
const itemsPerPage = 10
const searchTerm = ref('')

const filteredProducts = computed(() => {
  if (!searchTerm.value) {
    return store.mortgageProducts
  }
  return store.mortgageProducts.filter(product => 
    product.kor_co_nm.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
})

const totalPages = computed(() => Math.ceil(filteredProducts.value.length / itemsPerPage))

const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredProducts.value.slice(start, end)
})

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

const searchProducts = () => {
  currentPage.value = 1 
}
</script>

<style scoped>
.product-list-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.product-title {
  color: #333;
  margin-bottom: 20px;
}

.search-form {
  width: 300px;
}

.search-input {
  border-radius: 4px 0 0 4px;
}

.search-btn {
  background-color: #e3f2fd;
  color: #333;
  border: 1px solid #ced4da;
  border-left: none;
}

.custom-table {
  border-collapse: separate;
  border-spacing: 0;
  text-align: center;
  border-top: 2px solid #0275d8;
  border-bottom: 2px solid #0275d8;
}

.custom-table th {
  background-color: #e3f2fd;
  color: #333;
  font-weight: bold;
  border-bottom: 3px double #dee2e6;
}

.custom-table td {
  border-bottom: 1px solid #dee2e6;
  vertical-align: middle;
}

.custom-table tr:hover {
  background-color: #f8f9fa;
}

.product-link {
  color: #007bff;
  text-decoration: none;
}

.product-link:hover {
  text-decoration: underline;
}

.pagination {
  margin-top: 20px;
}

.page-link {
  color: #333;
  border: 1px solid #dee2e6;
}

.page-item.active .page-link {
  background-color: #007bff;
  border-color: #007bff;
  color: white;
}
</style>