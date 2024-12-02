import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'
export const useCounterStore = defineStore('counter', () => {
  const router = useRouter()

  const API_URL = "http://127.0.0.1:8000"

  const loginUserInfo = ref(null)
  const loginusername = ref(null)
  const token = ref(null)

  const articlesData = ref([])
  const newsData = ref([])
  const keywordsData = ref([])
  
  const recommendProductsData = ref([])

  const depositProducts = ref(null)
  const savingProducts = ref(null)
  const mortgageProducts = ref(null)

  const exchangeRateData = ref(null)
  const exchangeRateDataDB = ref(null)
  const majorExchangeRate = ref(null)

  const messages = ref([])
  const conversation_id = ref('')

  // 로그인 요청 액션
  const login = function (payload) {
    const { email, password } = payload
    
    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        email, password  
      }
    })
      .then((response) => {
        console.log(response)
        token.value = response.data.key
        console.log(token)
        getUserInfo()
        router.push({name: 'home'})
      })
      .catch((error) => {
        console.log(error)
      })
  }

  // 회원 가입 요청 액션
  const signup = function (payload) {
    const { email, password1, password2, username, birthdate, assets, annual_income, investment_type, primary_bank } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        email,
        username,
        password1,
        password2,
        birthdate,
        assets,
        annual_income,
        investment_type,
        primary_bank,
      }
    })
      .then((response) => {
        console.log(response)
        console.log('회원 가입 성공')
        const password = password1
        login({ email, password })
      })
      .catch((error) => {
        console.log(error)
      })
  }

  // 로그아웃 요청 액션
  const logout = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
      headers: {
        Authorization: `Token ${token.value}`,
      }
    })
      .then((response) => {
        console.log(response)

        token.value = null

        loginusername.value = null
        loginUserInfo.value = null

        recommendProductsData.value = null

        messages.value = []
        conversation_id.value = ''

        axios.defaults.headers.common['Authorization']
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        router.push({ name: 'login' })
      })
      .catch((error) => {
        console.log(error)
      })
  }

  const signout = function (inputPw) {
    axios({
      method: 'delete',
      url: `${API_URL}/api/v1/accounts/delete/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
      data: {
        password: inputPw
      }
    })
      .then((response) => {
        console.log(response)
        alert('회원 탈퇴가 완료되었습니다.')

        token.value = null

        loginusername.value = null
        loginUserInfo.value = null

        recommendProductsData.value = null

        messages.value = []
        conversation_id.value = ''

        axios.defaults.headers.common['Authorization']
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        router.push({ name: 'home' })
      })
      .catch((error) => {
        console.log(error)
        alert('회원 탈퇴 중 오류가 발생했습니다.')
      })
  }

  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    }
    else {
      return true
    }
  })

  // 유저 정보 가져오기
  const getUserInfo = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/accounts/profile/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then((response) => {
        console.log(response)
        console.log(response.data)
        loginUserInfo.value = response.data
        loginusername.value = response.data.username
        recommendProductsData.value = null // 로그인 시 추천 데이터 혹시 모르니 한 번 더 초기화
      })
      .catch((error) => {
        console.log(error)
      })
  }

  const kakaoLogin = function () {
    const KAKAO_CLIENT_ID = 'c998aa1e3e93c0a65fe1ff709a8672d0'  // settings.py에서 가져온 client_id
    const REDIRECT_URI = 'http://localhost:5173/accounts/kakao/callback'
    const KAKAO_AUTH_URL = `https://kauth.kakao.com/oauth/authorize?client_id=${KAKAO_CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=code`
    
    window.location.href = KAKAO_AUTH_URL
  }
  
  const handleKakaoCallback = async function (code) {
    try {
      const response = await axios.get(`${API_URL}/api/v1/accounts/kakao/callback/?code=${code}`)

      token.value = response.data.key
      loginusername.value = response.data.nickname
      console.log(response.data)
      
      // 토큰을 로컬 스토리지에 저장
      // localStorage.setItem('token', token.value)
      
      // 사용자 정보를 로컬 스토리지에 저장
      const user = { email: loginusername.value }
      localStorage.setItem('user', JSON.stringify(user))
      
      // axios 기본 헤더에 토큰 설정
      axios.defaults.headers.common['Authorization'] = `Token ${token.value}`

      getUserInfo()
      if (response.data.needsAdditionalInfo) {
        // 추가 정보 입력이 필요한 경우
        router.push({ name: 'modify-profile' })
      } else {
        // 추가 정보 입력이 필요 없는 경우
        router.push({ name: 'home' })
      }
    } catch (error) {
      console.error('Kakao callback error:', error)
      router.push({ name: 'login' })
    }
  }
  
  // 앱 시작시 로그인 상태 복구
  const initializeAuth = () => {
    const savedToken = localStorage.getItem('token')
    const savedUser = localStorage.getItem('user')
    
    if (savedToken && savedUser) {
      token.value = savedToken
      const user = JSON.parse(savedUser)
      loginusername.value = user.email
      axios.defaults.headers.common['Authorization'] = `Token ${savedToken}`
    }
  }

  // 회원 정보 수정
  const modifyProfile = function (payload) {
    const { username, birthdate, assets, annual_income, investment_type, primary_bank } = payload

    axios({
      method: 'put',
      url: `${API_URL}/api/v1/accounts/profile/update/`,
      headers: {
        Authorization: `Token ${token.value}`,
      },
      data: {
        username,
        birthdate,
        assets,
        annual_income,
        investment_type,
        primary_bank,
      }
    })
      .then((response) => {
        console.log(response)
        getUserInfo()
        router.push({ name: 'profile' })
      })
      .catch((error) => {
        console.log(error)
      })
  }

  // 예금 데이터 먼저 저장
  const saveDepositProducts = function () {
    axios({
      method: 'get',
      url: `${API_URL}/products/save-deposit-products/`
    })
      .then((response) => {
        console.log(response)
        getDepositProducts()
      })
      .catch((error) => {
        console.log(error)
      })
  }

  // 예금 데이터 불러오기 및 가공
  const getDepositProducts = function () {
    axios({
      method: 'get',
      url: `${API_URL}/products/deposit-get-all/`
    })
      .then((response) => {
        console.log(response)
        const processedData = response.data.map(product => {
          const result = {
            id: product.id,
            kor_co_nm: product.kor_co_nm,
            fin_prdt_nm: product.fin_prdt_nm,
            save_trm_6: '-',
            save_trm_12: '-',
            save_trm_24: '-',
            save_trm_36: '-'
          }
          
          product.options.forEach(option => {
            if ([6, 12, 24, 36].includes(option.save_trm)) {
              result[`save_trm_${option.save_trm}`] = option.intr_rate
            }
          })
          
          return result
        })
        
        depositProducts.value = processedData
      })
      .catch((error) => {
        console.log(error)
      })
  }

    // 적금 데이터 먼저 저장
    const saveSavingtProducts = function () {
      axios({
        method: 'get',
        url: `${API_URL}/products/save-saving-products/`
      })
        .then((response) => {
          console.log(response)
          getSavingProducts()
        })
        .catch((error) => {
          console.log(error)
        })
    }
  
  // 적금 데이터 불러오기 및 가공
  const getSavingProducts = function () {
    axios({
      method: 'get',
      url: `${API_URL}/products/saving-get-all/`
    })
      .then((response) => {
        console.log(response)
        const processedData = response.data.map(product => {
          const result = {
            id: product.id,
            kor_co_nm: product.kor_co_nm,
            fin_prdt_nm: product.fin_prdt_nm,
            save_trm_6: '-',
            save_trm_12: '-',
            save_trm_24: '-',
            save_trm_36: '-'
          }
          
          product.options.forEach(option => {
            if ([6, 12, 24, 36].includes(option.save_trm)) {
              result[`save_trm_${option.save_trm}`] = option.intr_rate
            }
          })
          
          return result
        })
        
        savingProducts.value = processedData
      })
      .catch((error) => {
        console.log(error)
      })
  }
  
    // 대출 데이터 먼저 저장
    const saveMortgagetProducts = function () {
      axios({
        method: 'get',
        url: `${API_URL}/products/save-mortgage-products/`
      })
        .then((response) => {
          console.log(response)
          getMortgageProducts()
        })
        .catch((error) => {
          console.log(error)
        })
    }
  
  // 대출 데이터 불러오기 및 가공
  const getMortgageProducts = function () {
    axios({
      method: 'get',
      url: `${API_URL}/products/mortgage-get-all/`
    })
      .then((response) => {
        console.log(response)
        const processedData = response.data.map(product => {
          const result = {
            id: product.id,
            kor_co_nm: product.kor_co_nm,
            fin_prdt_nm: product.fin_prdt_nm,
            apt_fixed: '-',
            apt_nonfixed: '-',
            nonapt_fixed: '-',
            nonapt_nonfixed: '-'
          }
          
          product.options.forEach(option => {
            const isApartment = option.mrtg_type === 'A'
            const isFixed = option.lend_rate_type === 'F'
            
            if (isApartment && isFixed) {
              result.apt_fixed = option.lend_rate_min
            } else if (isApartment && !isFixed) {
              result.apt_nonfixed = option.lend_rate_min
            } else if (!isApartment && isFixed) {
              result.nonapt_fixed = option.lend_rate_min
            } else if (!isApartment && !isFixed) {
              result.nonapt_nonfixed = option.lend_rate_min
            }
          })
          
          return result
        })
        
        mortgageProducts.value = processedData
      })
      .catch((error) => {
        console.log(error)
      })
  } 

    // 환율 데이터 불러오기
    const saveExchangeRate = function () {
      axios({
        method: 'get',
        url: `${API_URL}/exchange/save-exchange-rate/`
      })
        .then((response) => {
          console.log(response)
          exchangeRateData.value = response.data
          getDbExchangeRate()
          getMajorExchangeRate()
        })
        .catch((error) => {
          console.log(error)
        })
    }

    //DB에 있는 환율 데이터 불러오기
    const getDbExchangeRate = function () {
      axios({
        method: 'get',
        url: `${API_URL}/exchange/exchange-get-all/`
      })
        .then((response) => {
          console.log(response)
          exchangeRateDataDB.value = response.data
        })
        .catch((error) => {
          console.log(error)
        })
    }

  // 주요국가 환율 정보 가져오기
  const getMajorExchangeRate = function () {
    console.log(123123)
    console.log(exchangeRateDataDB)
    majorExchangeRate.value = exchangeRateData.value.filter((exchangeRate) => {
      if (exchangeRate.cur_unit === "USD" || exchangeRate.cur_unit === "JPY(100)" || exchangeRate.cur_unit === "EUR" || exchangeRate.cur_unit === "CNH" ) {
        return exchangeRate
      }
    })
  }

  // 즐겨찾기 여부 확인
  const isFavorite = (exchangeId) => {
    return favoriteExchangeIds.value.includes(exchangeId)
  }

  // 즐겨찾기 토글
  const toggleFavorite = (exchange) => {
    const index = favoriteExchangeIds.value.indexOf(exchange.id)
    if (index === -1) {
      favoriteExchangeIds.value.push(exchange.id)
      favoriteExchangeData.value.push(exchange)
      alert('즐겨찾기에 추가합니다.')
    } else {
      favoriteExchangeIds.value.splice(index, 1)
      const dataIndex = favoriteExchangeData.value.findIndex(item => item.id === exchange.id)
      if (dataIndex !== -1) {
        favoriteExchangeData.value.splice(dataIndex, 1)
      }
      alert('즐겨찾기에서 제거합니다.')
    }
  }

  // addToFavorite 함수 수정
  const addToFavorite = function (exchange) {
    toggleFavorite(exchange)
    if (isFavorite(exchange.id)) {
      alert('즐겨찾기에 추가되었습니다.')
    } else {
      alert('즐겨찾기에서 제거되었습니다.')
    }
  }

  // 게시글 데이터 불러오기
  const getArticlesData = function () {
    axios({
      method: 'get',
      url: `${API_URL}/community/articles/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then((response) => {
        articlesData.value = response.data
      })
      .catch((error) => {
        console.log(error)
      })
  }

  // 사용자 추천 상품 불러오기
  const getRecommendProductsData = function () {
    axios({
      method: 'get',
      url: `${API_URL}/recommend/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then((response) => {
        console.log(response)
        recommendProductsData.value = response.data
      })
      .catch((error) => {
        console.log(error)
      })
  }

  // 뉴스 데이터 가져오기
  const getNewsData = function () {
    axios({
      method: 'get',
      url: `${API_URL}/news/`
    })
      .then((response) => {
        console.log(response)
        newsData.value = response.data
      })
      .catch((error) => {
        console.log(error)
      })
  }

  // 키워드 데이터 가져오기
  const getkeywordsData = function () {
    axios({
      method: 'get',
      url: `${API_URL}/news/trending/`
    })
      .then((response) => {
        console.log(response)
        keywordsData.value = response.data
      })
      .catch((error) => {
        console.log(error)
      })
  }

  const clearMessage = function () {
    conversation_id.value = ''
    messages.value = []
  }

  return { 
    token,
    API_URL, 
    isLogin, 
    loginusername, 
    loginUserInfo,
    recommendProductsData,
    depositProducts,
    savingProducts,
    mortgageProducts,
    exchangeRateData,
    exchangeRateDataDB,
    majorExchangeRate,
    articlesData,
    newsData,
    keywordsData,
    messages,
    conversation_id,
    login, 
    signup, 
    logout,
    signout,
    kakaoLogin,
    handleKakaoCallback,
    initializeAuth,
    modifyProfile,
    saveDepositProducts,
    getDepositProducts,
    saveSavingtProducts,
    getSavingProducts,
    saveMortgagetProducts,
    getMortgageProducts,
    saveExchangeRate,
    getMajorExchangeRate,
    getDbExchangeRate,
    isFavorite,
    toggleFavorite,
    addToFavorite,
    getArticlesData,
    getRecommendProductsData,
    getNewsData,
    getkeywordsData,
    clearMessage,
  }
}, { persist: true })
