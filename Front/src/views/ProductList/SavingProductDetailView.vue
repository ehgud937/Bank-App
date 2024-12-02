<template>
  <div class="product-detail-container">
    <div class="product-detail-card">
      <!-- <div class="card-header">
        <button class="btn btn-link back-link" @click="goSavingProductList">적금 상품 목록</button>
      </div> -->
      <div v-if="savingProductDetail" class="card-body">
        <div class="d-flex justify-content-between">
          <h2 class="product-title">{{ savingProductDetail.fin_prdt_nm }}</h2>
          <h5>{{ savingProductDetail.kor_co_nm }}</h5>
        </div>
        <hr>

        <div class="product-info">
          <h5>상세 정보</h5>
          <p>{{ savingProductDetail.etc_note }}</p>
          <p><small>상품 코드: {{ savingProductDetail.fin_prdt_cd }}</small></p>
        </div>
        <hr>

        <div class="d-flex justify-content-between align-items-center mb-3">
          <h5>옵션</h5>
          <div class="input-group p-0" style="max-width: 400px;">
            <span class="input-group-text"  for="depositAmount">월 납입액 (원)</span>
            <input class="form-control" type="number" id="monthlyDeposit" v-model="monthlyDeposit" @input="calculateInterest">
          </div>
        </div>

        <div class="table-responsive">
          <table class="table custom-table" v-if="savingProductOptions">
            <caption>
              ※ 기본 입력된 월 납입액은, 회원 정보에 입력된 월 수입을 기반으로 설정 되었습니다. (월 소득의 30%)
            </caption>
            <caption>
              ※ 이 계산은 최고 우대 금리를 적용하여 산출된 예상 금액으로, 실제 이자는 다를 수 있습니다. 
              중도 해지 없이 만기까지 유지한다고 가정하며, 세금 및 수수료는 고려되지 않았습니다. 
              단리와 복리 상품의 이자 계산 방식이 다르므로 참고하시기 바랍니다. 
              정확한 정보는 반드시 해당 금융 기관에 문의하시기 바랍니다."
            </caption>
            <thead>
              <tr>
                <th scope="col">저축 금리 유형</th>
                <th scope="col">금리</th>
                <th scope="col">최고 우대 금리</th>
                <th scope="col">저축 기간</th>
                <th scope="col">예상 이자</th>
                <th scope="col"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="option in savingProductOptions" :key="option.id">
                <td>{{ option.intr_rate_type_nm }}</td>
                <td>{{ option.intr_rate }}%</td>
                <td>{{ option.intr_rate2 }}%</td>
                <td>{{ option.save_trm }}개월</td>
                <td>{{ calculateInterestForOption(option) }}원</td>
                <td>
                  <button class="btn btn-primary" @click="registerSavingProduct(option.id)">가입하기</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <hr>

      <!-- 지도 컨테이너 -->
      <div class="card-body" v-if="savingProductDetail">
        <h5 class="map-title">{{ savingProductDetail.kor_co_nm }} 지점 위치</h5>
        <div class="bank-map-container">
          <div class="content-container">
            <div id="map" class="map"></div>
            <div v-if="banks.length" class="bank-list">
              <div 
                v-for="bank in banks" 
                :key="bank.id"
                class="bank-item"
                @click="moveToBank(bank)"
              >
                <h5>{{ bank.place_name }}</h5>
                <p>주소: {{ bank.address_name }}</p>
                <p>도로명: {{ bank.road_address_name }}</p>
                <p v-if="bank.phone">전화번호: {{ bank.phone }}</p>
                <p v-if="bank.distance">거리: {{ Math.round(bank.distance) }}m</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router' 
import { useCounterStore } from '@/stores/counter';

const route = useRoute()
const router = useRouter()
const store = useCounterStore()

const savingProductId = ref(route.params.id)
const savingProductDetail = ref(null)
const savingProductOptions = ref(null)

const monthlyDeposit = ref(100000) // 기본값 10만원

onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/products/saving_detail/${savingProductId.value}/`,
  })
    .then((response) => {
      console.log(response)
      savingProductDetail.value = response.data
      savingProductOptions.value = response.data.options
      
      // 기뵨 월 납입액 설정 (월봉의 30%, 1의 자리에서 반올림)
      if (store.loginUserInfo && store.loginUserInfo.annual_income) {
        monthlyDeposit.value = Math.round((store.loginUserInfo.annual_income / 12) / 10) * 3
      }
      
      calculateInterest() // 초기 이자 계산
      initializeMap()
      searchBanks()
    })
    .catch((error) => {
      console.log(error)
    })
})

const goSavingProductList = function () {
  router.push({ name: 'saving-product' })
}

const calculateInterest = () => {
  if (savingProductOptions.value) {
    savingProductOptions.value.forEach(option => {
      option.expectedInterest = calculateInterestForOption(option)
    })
  }
}

const calculateInterestForOption = (option) => {
  const monthly = parseFloat(monthlyDeposit.value)
  const rate = parseFloat(option.intr_rate2) / 100 // 최고 우대 금리 사용
  const months = parseFloat(option.save_trm)
  let interest = 0

  if (option.intr_rate_type_nm === '단리') {
    // 단리 계산식
    interest = (monthly * months * (months + 1) / 2) * (rate / 12)
  } else if (option.intr_rate_type_nm === '복리') {
    // 복리 계산식
    for (let i = 1; i <= months; i++) {
      interest += monthly * Math.pow(1 + rate / 12, months - i + 1) - monthly
    }
  }

  // 1의 자리에서 반올림
  return Math.round(interest / 10) * 10 .toLocaleString()
}


const registerSavingProduct = function (optionId) {
  if (confirm('정말로 이 상품에 가입하시겠습니까?')) {
    axios({
      method: 'post',
      url: `${store.API_URL}/register/saving/${savingProductId.value}/${optionId}/`,
      headers: {
        Authorization: `Token ${store.token}`,
      }
    })
      .then((response) => {
        console.log(response)
        alert('성공적으로 가입되었습니다.')
      })
      .catch((error) => {
        console.log(error)
        alert('상품 가입 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.')
      })
  }
}

// 지도 관련 코드
const kakaoApiKey = import.meta.env.VITE_KAKAO_JS_API_KEY;

const API_URL = 'http://127.0.0.1:8000/api/v1/kakaomap'
const searchQuery = ref('')
const banks = ref([])

let map = null
let markers = []
let infowindow = null

const initializeMap = () => {
  const script = document.createElement('script')
  script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${kakaoApiKey}&libraries=services&autoload=false`
  script.onload = () => {
    kakao.maps.load(() => {
      const container = document.getElementById('map')
      const options = {
        center: new kakao.maps.LatLng(37.5665, 126.9780),
        level: 3
      }
      map = new kakao.maps.Map(container, options)
      infowindow = new kakao.maps.InfoWindow({ zIndex: 1 })
    })
  }
  document.head.appendChild(script)
}

const createMarkers = (banks) => {
  markers.forEach(marker => marker.setMap(null))
  markers = []

  banks.forEach(bank => {
    const marker = new kakao.maps.Marker({
      position: new kakao.maps.LatLng(bank.y, bank.x),
      map: map
    })
    
    kakao.maps.event.addListener(marker, 'click', () => {
      showInfoWindow(marker, bank)
    })

    markers.push(marker)
  })

  if (markers.length > 0) {
    const bounds = new kakao.maps.LatLngBounds()
    markers.forEach(marker => bounds.extend(marker.getPosition()))
    map.setBounds(bounds)
  }
}

const showInfoWindow = (marker, bank) => {
  const content = `
    <div style="padding:5px;font-size:12px;">
      <strong>${bank.place_name}</strong><br>
      주소: ${bank.address_name}<br>
      도로명: ${bank.road_address_name}<br>
      ${bank.phone ? `전화번호: ${bank.phone}<br>` : ''}
      ${bank.distance ? `거리: ${Math.round(bank.distance)}m` : ''}
    </div>
  `
  infowindow.setContent(content)
  infowindow.open(map, marker)
}

const moveToBank = (bank) => {
  const moveLatLng = new kakao.maps.LatLng(bank.y, bank.x)
  map.setCenter(moveLatLng)
  map.setLevel(2)
  
  const marker = markers.find(m => 
    m.getPosition().getLat() === parseFloat(bank.y) && 
    m.getPosition().getLng() === parseFloat(bank.x)
  )
  
  if (marker) {
    showInfoWindow(marker, bank)
  }
}

const searchBanks = async () => {
  try {
    const response = await axios.get(`${API_URL}/search/`, {
      params: { query: savingProductDetail.value ? savingProductDetail.value.kor_co_nm : searchQuery.value }
    })
    banks.value = response.data.documents
    createMarkers(banks.value)
  } catch (error) {
    console.error('은행 검색 실패:', error)
  }
}
</script>

<style scoped>
.product-detail-container {
  max-width: 1000px;
  margin: 0 auto;
}

.product-detail-card {
  background-color: #ffffff;
  border-radius: 8px;
  /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); */
  overflow: hidden;
}

.card-header {
  background-color: #f8f9fa;
  padding: 15px;
  border-bottom: 1px solid #dee2e6;
}

.back-link {
  color: #007bff;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.back-link:hover {
  background-color: #007bff;
  color: white;
  font-weight: bold;
}

.card-body {
  padding: 20px;
}

.product-title {
  color: #007bff;
  margin-bottom: 10px;
}

.product-info h5 {
  margin-bottom: 10px;
}


.custom-table {
  border-collapse: separate;
  border-spacing: 0;
  text-align: center;
  border-top: 2px solid #0275d8;
  border-bottom: 2px solid #0275d8;
  margin-top: 20px;
  margin-bottom: 20px;
}

.custom-table th, .custom-table td {
  border-bottom: 1px solid #dee2e6;
  padding: 12px;
  vertical-align: middle;
}

.custom-table th {
  background-color: #e3f2fd;
  color: #333;
  font-weight: bold;
  border-bottom: 3px double #dee2e6;
}

.custom-table tr:last-child td {
  border-bottom: none;
}

.custom-table tr:hover {
  background-color: #f8f9fa;
}

.map-title {
  margin-top: 30px;
  margin-bottom: 15px;
}

.bank-map-container {
  height: 500px;
}

.content-container {
  display: flex;
  gap: 20px;
  height: 100%;
}

.map {
  flex: 1;
  border-radius: 8px;
}

.bank-list {
  width: 300px;
  overflow-y: auto;
}

.bank-item {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.bank-item:hover {
  background-color: #e3f2fd;
}

.bank-item h5 {
  margin-bottom: 10px;
}

.bank-item p {
  margin-bottom: 5px;
}
</style>