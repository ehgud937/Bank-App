<template>
  <div class="create-article-container">
    <div class="card create-article-card">
      <div class="card-body">
        <h3 class="card-title mb-4">새 게시글 작성</h3>
        <hr>
        <form @submit.prevent="createArticle">
          <div class="mb-3">
            <select name="category" id="category" class="form-select custom-select" required v-model="inputCategory">
              <option disabled value="" selected>카테고리를 선택하세요</option>
              <option v-if="store.loginusername === 'admin'" value="NOTIFICATION">공지</option>
              <option value="FREE">자유</option>
              <option value="ASK">질문</option>
              <option value="REVIEW">후기</option>
              <option value="ETC">기타</option>
            </select>
          </div>
          <div class="mb-3">
            <input type="text" class="form-control custom-input" placeholder="제목을 입력하세요" v-model="inputTitle">
          </div>
          <div class="mb-3">
            <textarea class="form-control custom-textarea" placeholder="내용을 입력하세요" rows="5" v-model="inputContent"></textarea>
          </div>
          <button type="submit" class="btn btn-primary btn-block">게시하기</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter';
import axios from 'axios'

const store = useCounterStore()
const router = useRouter()

const inputCategory = ref(null)
const inputTitle = ref(null)
const inputContent = ref(null)
const articles = ref([])

const createArticle = function () {
  axios({
    method: 'post',
    url: `${store.API_URL}/community/articles/`,
    headers: {
      Authorization: `Token ${store.token}`
    },
    data: {
      category: inputCategory.value,
      title: inputTitle.value,
      content: inputContent.value,
    }
  })
    .then((response) => {
      console.log(response)
      articles.value = response.data
      router.push({ name: 'community_all' })
    })
    .catch((error) => {
      console.log(error)
    })
}

</script>

<style scoped>
.create-article-container {
  display: flex;
  justify-content: center;
  align-items: start;
  min-height: 50vh;
}

.create-article-card {
  width: 100%;
  border: none;
  border-radius: 8px;
}

.card-title {
  color: #1c1e21;
  font-weight: bold;
}

.custom-select,
.custom-input,
.custom-textarea {
  border-radius: 8px;
  border: 1px solid #dddfe2;
  font-size: 17px;
  padding: 14px 16px;
  transition: border .3s ease;
  width: 100%;
}

.custom-select:focus,
.custom-input:focus,
.custom-textarea:focus {
  border-color: #1877f2;
  box-shadow: 0 0 0 2px rgba(24, 119, 242, 0.2);
}

.btn-primary {
  background-color: #1877f2;
  border: none;
  padding: 10px 20px;
  transition: background-color .3s ease;
}

.btn-primary:hover {
  background-color: #166fe5;
}

.btn-block {
  display: block;
  width: 100%;
}
</style>