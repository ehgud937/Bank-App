<template>
  <div class="d-flex flex-column justify-content-center align-items-center gap-3 card">
    <!-- 게시글 목록 -->
    <div>
      <ol class="list-group list-group-flush">
        <div class="list-group-item"v-for="article in articles" :key="article.id">
          <li>{{ article.title }}</li>
        </div>
      </ol>
    </div>

    <!-- 페이지네이션 -->
    <nav aria-label="Page navigation example">
      <ul class="pagination">
        <li class="page-item">
          <a class="page-link" href="#" aria-label="Previous">
            <span aria-hidden="true">&laquo;</span>
          </a>
        </li>
        <li class="page-item"><a class="page-link" href="#">1</a></li>
        <li class="page-item"><a class="page-link" href="#">2</a></li>
        <li class="page-item"><a class="page-link" href="#">3</a></li>
        <li class="page-item">
          <a class="page-link" href="#" aria-label="Next">
            <span aria-hidden="true">&raquo;</span>
          </a>
        </li>
      </ul>
    </nav>

    <!-- 검색바 -->
    <form class="d-flex flex-row gap-2">
      <div>
        <input type="text" class="form-control" placeholder="검색어를 입력하세요." aria-label="search" aria-describedby="basic-addon1" v-model="inputText">
      </div>
      <div>
        <input type="submit" value="검색" class="btn" style="background-color: #e3f2fd;">
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const inputText = ref('')

const articles = [
  { id: 1, title: '삼전 어디까지 떨어지는가'},
  { id: 2, title: '엔비디아 그들은 누구인가'},
  { id: 3, title: '주가조작 진실은?'},
  { id: 4, title: '하이닉스 앞으로의 전망은?'},
  { id: 5, title: '국민 주식? 삼성전자, 카카오의 추락'},
  { id: 6, title: '집나간 외국인 복귀 언제쯤..'},
  { id: 7, title: '코스피 보유주식 비중 연 중 최저'},
  { id: 8, title: '삼성전자 임원 60명, 회사 주식 158억원 매입…23만주'},
  { id: 9, title: '트럼프 시대, 돈 움직인다…'},
  { id: 10, title: '예금 헐고 마통 받아 美 주식·코인'},
]
</script>

<style   scoped>

</style>