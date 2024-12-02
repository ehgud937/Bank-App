<!-- views/KakaoCallback.vue -->
<template>
  <div class="d-flex justify-content-center align-items-center" style="height: 100vh">
    <div v-if="loading" class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
    <div v-else-if="needsAdditionalInfo" class="text-center">
      <h2>추가 정보가 필요합니다</h2>
      <router-link to="/additional-info" class="btn btn-primary">
        추가 정보 입력하기
      </router-link>
    </div>
    <div v-else-if="error" class="text-center text-danger">
      <h2>오류가 발생했습니다</h2>
      <p>{{ error }}</p>
      <button @click="retryLogin" class="btn btn-primary">다시 시도</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const router = useRouter()
const loading = ref(true)
const needsAdditionalInfo = ref(false)
const error = ref(null)

const retryLogin = () => {
  router.push({ name: 'login' })
}

onMounted(async () => {
  const code = new URL(window.location.href).searchParams.get('code')
  if (code) {
    try {
      const result = await store.handleKakaoCallback(code)
      console.log("Kakao callback result:", result)  // 응답 구조 로깅
      if (result && typeof result === 'object') {
        if ('needsAdditionalInfo' in result) {
          needsAdditionalInfo.value = result.needsAdditionalInfo
          if (!result.needsAdditionalInfo) {
            router.push({ name: 'home' })
          }
        } else {
          throw new Error('서버 응답에 필요한 정보가 없습니다.')
        }
      } else {
        throw new Error('서버 응답이 예상과 다릅니다.')
      }
    } catch (err) {
      console.error('카카오 로그인 처리 중 오류:', err)
      error.value = err.message || '로그인 처리 중 오류가 발생했습니다.'
    }
  } else {
    error.value = '카카오 인증 코드를 받지 못했습니다.'
  }
  loading.value = false
})
</script>