<template>
  <div class="modify-comment-container">
    <div class="modify-comment-card">
      <div class="card-body">
        <h4 class="card-title mb-3">댓글 수정</h4>
        <form @submit.prevent="modifyComment">
          <div class="mb-3">
            <textarea class="form-control custom-input" placeholder="내용을 입력하세요." aria-label="Username" aria-describedby="basic-addon1" v-model="inputContent"></textarea>
          </div>
          <input type="submit" class="btn btn-primary btn-block" value="수정">
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter';
import axios from 'axios'

const store = useCounterStore()
const route = useRoute()
const router = useRouter()

const articleId = ref(route.params.id)
const commentId = ref(route.params.cid)

const inputContent = ref(null)

onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/community/articles/${articleId.value}/`,
    headers: {
      Authorization: `Token ${store.token}`
    },
  })
    .then((response) => {
      console.log(response.data)
      const comments = response.data.comments

      const specificComment = comments.find(comment => comment.id === Number(commentId.value))

      if (specificComment) {
        inputContent.value = specificComment.content
      } else {
        console.log('Comment not found')
      }
    })
    .catch((error) => {
      console.log(error)
    })
})

const modifyComment = function () {
  axios({
    method: 'put',
    url: `${store.API_URL}/community/articles/${articleId.value}/comments/${commentId.value}/`,
    headers: {
      Authorization: `Token ${store.token}`
    },
    data: {
      content: inputContent.value
    }
  })
    .then((response) => {
      console.log(response)
      router.push({ name: 'article-detail', params: { 'id': articleId.value } })
    })
    .catch((error) => {
      console.log(error)
    })
}

</script>

<style scoped>
.modify-comment-container {
  display: flex;
  justify-content: center;
  align-items: start;
  min-height: 50vh;
}

.modify-comment-card {
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