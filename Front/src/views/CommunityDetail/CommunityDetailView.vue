<template>
  <div v-if="articleInfo" class="article-detail">
    <div>
      <div v-if="articleInfo">
        <h3 class="article-title">{{ articleInfo.title }}</h3>
        <div class="article-meta">
          <span style="color: #757575;">{{ articleCreateAt }}</span>
          <span>{{ articleInfo.username }}</span>
        </div>
        <hr>
        <p class="article-body">{{ articleInfo.content }}</p>
      </div>
      <div v-else-if="isLoading" class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p v-else>게시글을 찾을 수 없습니다.</p>

      <div class="btn-section">
        <div class="like-section">
          <button class="like-button" @click="toggleLike">
            <span v-show="isLiked">❤️</span>
            <span v-show="!isLiked">🤍</span>
          </button>
          <span class="like-count">{{ articleInfo.like_count }}</span>
        </div>
  
        <div v-if="store.loginusername === articleInfo.username" class="article-actions">
          <RouterLink :to="{ name: 'modify-article', params: { 'id': articleId }}" class="btn btn-primary">
            게시글 수정
          </RouterLink>
          <button @click.prevent="deleteArticle" class="btn btn-danger">게시글 삭제</button>
        </div>
      </div>
    </div>

    <hr>

    <div>
      <h5 class="comment-title">댓글 목록</h5>
      <p>{{ articleInfo.comment_count }}개의 댓글이 달렸습니다.</p>
      
      <!-- 댓글 목록 -->
      <div v-if="articleInfo.comments" class="comment-list">
        <div v-for="comment in reversedComments" :key="comment.id" class="comment">
          <div class="comment-header">
            <div class="comment-user">
              <img src="@/assets/common/blank-profile.png" alt="Avatar" class="user-avatar">
              <div>
                <h6 class="mb-0">{{ comment.username }}</h6>
                <small style="color: #757575;">{{ formatDate(comment.created_at) }}</small>
              </div>
            </div>
            <div v-if="store.loginusername === comment.username" class="comment-actions">
              <RouterLink :to="{ name: 'modify-comment', params: { 'id': articleId, 'cid': comment.id } }" class="btn btn-sm comment-modify">
                수정
              </RouterLink>
              <button @click.prevent="deleteComment(comment.id)" class="btn btn-sm comment-remove">삭제</button>
            </div>
          </div>
          <p class="comment-content">{{ comment.content }}</p>
        </div>
      </div>
      <hr>

      <!-- 댓글 쓰기 -->
      <div class="comment-form">
        <h5>댓글 쓰기</h5>
        <form @submit.prevent="createComment" class="comment-inner-form">
          <textarea class="form-control" placeholder="내용을 입력하세요." v-model="inputComment"></textarea>
          <button type="submit" class="btn btn-primary">게시</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router' 
import { useCounterStore } from '@/stores/counter';

const route = useRoute()
const router = useRouter()
const store = useCounterStore()

const isLoading = ref(true)

const articleId = ref(Number(route.params.id))
const articleInfo = ref({comments: []})
const articleCreateAt = ref('')

const inputComment = ref('')
const reversedComments = computed(() => {
  return [...articleInfo.value.comments].reverse()
})

const isLiked = computed(() => {
  return articleInfo.value.like_users?.includes(store.loginUserInfo.id) || false
})

const formatDate = (dateString) => {
  return `${dateString.slice(0, 10)} ${dateString.slice(11, 16)}`
}

const fetchArticleInfo = () => {
  axios({
    method: 'get',
    url: `${store.API_URL}/community/articles/${articleId.value}/`,
    headers: {
      Authorization: `Token ${store.token}`
    },
  })
    .then((response) => {
      console.log(response)
      articleInfo.value = response.data
      articleCreateAt.value = formatDate(articleInfo.value.created_at)
      isLoading.value = false
    })
    .catch((error) => {
      console.log(error)
      isLoading.value = false
    })
}

onMounted(fetchArticleInfo)

const deleteArticle = function () {
  axios({
    method: 'delete',
    url: `${store.API_URL}/community/articles/${articleId.value}/`,
    headers: {
      Authorization: `Token ${store.token}`
    },
  })
    .then((response) => {
      console.log(response)
      router.push({ name: 'community_all' })
    })
    .catch((error) => {
      console.log(error)
    })
}

const createComment = function () {
  axios({
    method: 'post',
    url: `${store.API_URL}/community/articles/${articleId.value}/comments/`,
    headers: {
      Authorization: `Token ${store.token}`
    },
    data: {
      content: inputComment.value
    }
  })
    .then((response) => {
      console.log(response)
      inputComment.value = '' // 입력 필드 초기화
      fetchArticleInfo() // 게시글 정보 (댓글 포함) 새로 가져오기
    })
    .catch((error) => {
      console.log(error)
    })
}

const deleteComment = function (commentId) {
  axios({
    method: 'delete',
    url: `${store.API_URL}/community/articles/${articleId.value}/comments/${commentId}/`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then((response) => {
      console.log(response)
      fetchArticleInfo()
    })
    .catch((error) => {
      console.log(error)
    })
}

const toggleLike = function() {
  axios({
    method: 'post',
    url: `${store.API_URL}/community/articles/${articleId.value}/like/`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then((response) => {
      console.log(response)
      fetchArticleInfo()
      console.log(isLiked.value)
    })
    .catch((error) => {
      console.log(error)
    })
}

</script>

<style scoped>
.article-detail {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.card {
  border: none;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
  margin-bottom: 20px;
}

.article-title {
  font-size: 2rem;
  margin-bottom: 10px;
}

.article-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 15px;
}

.article-actions {
  display: flex;
  gap: 10px;
  justify-content: end;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.article-body {
  line-height: 1.6;
}

.like-section {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  margin: 20px 0;
  padding: 10px 0;
  /* border-top: 1px solid #eee;
  border-bottom: 1px solid #eee; */
}

.like-button {
  background: none;
  border: none;
  font-size: 1.2em;
  cursor: pointer;
  color: #555;
  margin-right: 10px;
}

.like-count {
  font-weight: bold;
}

.btn-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comment-list {
  margin-top: 20px;
}

.comment {
  background-color: #f0f2f5;
  border-radius: 8px;
  padding: 15px 20px 5px 20px;
  margin-bottom: 15px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 5px;
}

.comment-user {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.comment-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  margin-right: 10px;
}

.comment-content {
  margin-top: 5px;
}

.comment-actions {
  display: flex;
  gap: 10px;
}

.comment-inner-form {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  align-items: center;
}

.comment-form textarea {
  width: 100%;
  border-radius: 8px;
  /* padding: 10px 15px; */
  border: 1px solid #ccc;
  resize: none;
}

.btn-primary {
  background-color: #1877f2;
  border-color: #1877f2;
}

.btn-primary:hover {
  background-color: #166fe5;
  border-color: #166fe5;
}

.comment-modify {
  background-color: #87c3ff;
  border-color: #87c3ff;
  transition: all ease 0.3s;
}

.comment-modify:hover {
  background-color: #1877f2;
  border-color: #1877f2;
  color: white;
  font-weight: bold;
}

.comment-remove {
  background-color: #eaa1a7;
  border-color: #eaa1a7;
  transition: all ease 0.3s;
}

.comment-remove:hover {
  background-color: #f21818;
  border-color: #f21818;
  color: white;
  font-weight: bold;
}
</style>