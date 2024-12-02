<template>
  <div class="product-detail-container">
    <div class="product-detail-card">
      <!-- <div class="card-header">
        <button class="btn btn-link back-link" @click="goMortgageProductList">주택 담보 대출 상품 목록</button>
      </div> -->
      <div v-if="mortgageProductDetail" class="card-body">

        <div class="d-flex justify-content-between">
          <h2 class="product-title">{{ mortgageProductDetail.fin_prdt_nm }}</h2>
          <h5>{{ mortgageProductDetail.kor_co_nm }}</h5>
        </div>
        <hr>

        <div class="product-info">
          <h5>상세 정보</h5>
          <p>{{ mortgageProductDetail.dly_rate }}</p>

          <table class="table custom-table">
            <tbody>
              <tr>
                <th>대출 부대비용</th>
                <td>{{ mortgageProductDetail.loan_inci_expn }}</td>
              </tr>
              <tr>
                <th>중도 상환 수수료</th>
                <td>{{ mortgageProductDetail.erly_rpay_fee }}</td>
              </tr>
              <tr>
                <th>대출 한도</th>
                <td>{{ mortgageProductDetail.loan_lmt }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <hr>
        <div class="accordion" id="accordionExample">
          <div class="accordion-item">
            <h2 class="accordion-header">
              <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                <h5 class="m-0">대출 이자 계산기</h5>
              </button>
            </h2>
            <div id="collapseOne" class="accordion-collapse collapse show" data-bs-parent="#accordionExample">
              <div class="accordion-body">
                <div class="row">
                  <div class="loan-eligibility-check col-12 col-lg-6">
                    <div class="cal-form-group">
                      <label for="dsr">DSR 비율 (%)</label>
                      <input type="number" id="dsr" v-model="dsr" class="cal-form-control">
                    </div>
                    <div class="cal-form-group">
                      <label for="ltv">LTV 비율 (%)</label>
                      <input type="number" id="ltv" v-model="ltv" class="cal-form-control">
                    </div>
                    <div class="cal-form-group">
                      <label for="housePrice">구매하고자 하는 주택의 가격 (원)</label>
                      <input type="number" id="housePrice" v-model="housePrice" class="cal-form-control">
                    </div>
                    <div class="cal-form-group">
                      <label for="annualIncome">연간 소득 (원)</label>
                      <input type="number" id="annualIncome" v-model="annualIncome" class="cal-form-control">
                    </div>
                    <div class="cal-form-group">
                      <label for="currentAssets">현재 자산 (원)</label>
                      <input type="number" id="currentAssets" v-model="currentAssets" class="cal-form-control">
                    </div>
                    <div class="cal-form-group">
                      <label>
                        <input type="checkbox" v-model="isApartment"> 아파트
                      </label>
                    </div>
                    <div class="d-flex gap-2">
                      <button class="btn btn-violet">
                        <a href="https://hogangnono.com/" style="text-decoration: none; color: white;">주택 가격 조회하기</a>
                      </button>
                      <button class="btn btn-primary" @click="checkEligibility">대출 가능 여부 확인</button>
                    </div>
                  </div>
          
                  <div v-if="eligibilityResult" class="eligibility-result col-12 col-lg-6">
                    <h5 style="padding: 15px;">대출 가능 여부 결과</h5>
                    <p class="eligibility-result mb-0"><strong>{{ eligibilityResult }}</strong></p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="my-2">
          <h6 @click="toggleNotice" class="notice-title">
            ※ 계산 방식 및 주의사항
            <i :class="['fas', showNotice ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
          </h6>
          <div v-show="showNotice" class="notice-content">
            <small>
              1. LTV(담보인정비율)와 DSR(총부채원리금상환비율) 기준:<br>
              &nbsp&nbsp&nbsp&nbsp본 계산기는 LTV와 DSR 중 더 낮은 대출 가능 금액을 기준으로 계산합니다.<br>
              &nbsp&nbsp&nbsp&nbsp실제 대출 가능 금액은 금융기관의 심사 기준에 따라 다를 수 있습니다.<br><br>
              2. 금리 적용:<br>
              &nbsp&nbsp&nbsp&nbsp계산된 이자는 현재 제공된 최저 금리를 기준으로 하며, 실제 적용 금리는 개인의 신용도와 대출 조건에 따라 달라질 수 있습니다.<br>
              &nbsp&nbsp&nbsp&nbsp고정금리와 변동금리 옵션을 모두 제공하나, 실제 선택 가능한 금리 유형은 상품에 따라 다를 수 있습니다.<br><br>
              3. 대출 기간:<br>
              &nbsp&nbsp&nbsp&nbsp계산에 사용된 대출 기간은 30년을 가정하고 있습니다. 실제 대출 기간은 상품과 개인 상황에 따라 다를 수 있으며, 이에 따라 월 상환액과 총 이자액이 변동될 수 있습니다.<br><br>
              4. 아파트 여부:<br>
              &nbsp&nbsp&nbsp&nbsp아파트와 비아파트의 대출 조건이 다를 수 있으므로, 정확한 주택 유형을 선택해주세요.<br><br>
              5. 추가 비용:<br>
              &nbsp&nbsp&nbsp&nbsp계산된 금액에는 대출 부대비용, 보증료, 세금 등이 포함되지 않았습니다. 실제 대출 시 이러한 추가 비용을 고려해야 합니다.<br><br>
              6. 최종 결정:<br>
              &nbsp&nbsp&nbsp&nbsp이 계산기의 결과는 참고용이며, 실제 대출 가능 여부와 조건은 금융기관의 상세한 심사를 통해 결정됩니다.<br>
              &nbsp&nbsp&nbsp&nbsp중요한 재무 결정을 내리기 전에 반드시 전문가와 상담하시기 바랍니다.<br><br>
              7. 정책 변동:<br>
              &nbsp&nbsp&nbsp&nbsp주택담보대출 관련 정책은 수시로 변경될 수 있으므로, 최신 정보를 확인하시기 바랍니다.<br><br>
              이 계산기는 대출 가능성을 예측하고 이해하는 데 도움을 주기 위한 도구입니다. 정확한 대출 조건과 가능 여부는 반드시 해당 금융기관에 문의하시기 바랍니다.<br>
            </small>
          </div>
        </div>
        <hr>

        <h5 class="options-title">옵션</h5>
        <div class="table-responsive">
          <table class="table custom-table" v-if="mortgageProductOptions">
            <thead>
              <tr>
                <th scope="col">담보 유형</th>
                <th scope="col">대출 상환 유형</th>
                <th scope="col">대출 금리 유형</th>
                <th scope="col">최저 금리</th>
                <th scope="col">최고 금리</th>
                <th scope="col"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="option in mortgageProductOptions" :key="option.id">
                <td>{{ option.mrtg_type_nm }}</td>
                <td>{{ option.rpay_type_nm }}</td>
                <td>{{ option.lend_rate_type_nm }}</td>
                <td>{{ option.lend_rate_min }}%</td>
                <td>{{ option.lend_rate_max }}%</td>
                <td>
                  <button class="btn btn-primary" @click="registerMortgageProduct(option.id)">가입하기</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <hr>

      <!-- 지도 컨테이너 -->
      <div class="card-body" v-if="mortgageProductDetail">
        <h5 class="map-title">{{ mortgageProductDetail.kor_co_nm }} 지점 위치</h5>
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

const mortgageProductId = ref(route.params.id)
const mortgageProductDetail = ref(null)
const mortgageProductOptions = ref(null)

const dsr = ref(40)
const ltv = ref(0)
const housePrice = ref(0)
const annualIncome = ref(0)
const currentAssets = ref(0)
const eligibilityResult = ref('')
const isApartment = ref(false)

const showNotice = ref(false);

onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/products/mortgage_detail/${mortgageProductId.value}/`,
  })
    .then((response) => {
      console.log(response)
      mortgageProductDetail.value = response.data
      mortgageProductOptions.value = response.data.options
      if (store.loginUserInfo && store.loginUserInfo.annual_income) {
        annualIncome.value = store.loginUserInfo.annual_income
      }
      if (store.loginUserInfo && store.loginUserInfo.assets) {
        currentAssets.value = store.loginUserInfo.assets
      }
      initializeMap()
      searchBanks()
    })
    .catch((error) => {
      console.log()
      console.log(error)
    })
})

const goMortgageProductList = function () {
  router.push({ name: 'mortgage-product' })
}


const registerMortgageProduct = function (optionId) {
  if (confirm('정말로 이 상품에 가입하시겠습니까?')) {
    axios({
      method: 'post',
      url: `${store.API_URL}/register/mortgage/${mortgageProductId.value}/${optionId}/`,
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

const checkEligibility = () => {
  // LTV 기반 최대 대출 가능 금액
  const maxLoanAmountLTV = Math.ceil(housePrice.value * (ltv.value / 100))

  // DSR 기반 최대 대출 가능 금액
  const monthlyIncome = annualIncome.value / 12
  const maxMonthlyPayment = monthlyIncome * (dsr.value / 100)
  const maxLoanAmountDSR = Math.ceil(calculateMaxLoanAmountDSR(maxMonthlyPayment))

  // LTV와 DSR 중 더 낮은 대출 가능 금액 선택
  const maxLoanAmount = Math.min(maxLoanAmountLTV, maxLoanAmountDSR)

  const requiredDownPayment = Math.ceil(housePrice.value - maxLoanAmount)

  if (currentAssets.value >= requiredDownPayment) {
    eligibilityResult.value = `대출 가능 금액: ${maxLoanAmount.toLocaleString()} 원\n\n`
    calculateInterest(maxLoanAmount)
  } else {
    const additionalAssets = Math.ceil(requiredDownPayment - currentAssets.value)
    eligibilityResult.value = `대출이 불가능합니다.\n추가로 필요한 자산: ${additionalAssets.toLocaleString()} 원`
  }
}

const calculateMaxLoanAmountDSR = (maxMonthlyPayment) => {
  // 예시: 30년 만기, 연 3% 이자율 가정
  const monthlyRate = 0.03 / 12
  const numberOfPayments = 30 * 12
  return maxMonthlyPayment * ((1 - Math.pow(1 + monthlyRate, -numberOfPayments)) / monthlyRate)
}

const calculateInterest = (loanAmount) => {
  if (mortgageProductOptions.value) {
    const filteredOptions = filterMortgageOptions(mortgageProductOptions.value, isApartment.value)
    
    const fixedRateOptions = filteredOptions.filter(option => option.lend_rate_type_nm === '고정금리')
    const variableRateOptions = filteredOptions.filter(option => option.lend_rate_type_nm === '변동금리')

    if (fixedRateOptions.length > 0) {
      const lowestFixedRate = Math.min(...fixedRateOptions.map(option => option.lend_rate_min))
      const monthlyFixedInterest = Math.ceil((loanAmount * (lowestFixedRate / 100)) / 12)
      eligibilityResult.value += `고정금리 월 이자 (최저 금리 ${lowestFixedRate}% 기준): ${monthlyFixedInterest.toLocaleString()} 원\n`
    } else {
      eligibilityResult.value += '고정금리 옵션이 없습니다.\n'
    }

    if (variableRateOptions.length > 0) {
      const lowestVariableRate = Math.min(...variableRateOptions.map(option => option.lend_rate_min))
      const monthlyVariableInterest = Math.ceil((loanAmount * (lowestVariableRate / 100)) / 12)
      eligibilityResult.value += `변동금리 월 이자 (최저 금리 ${lowestVariableRate}% 기준): ${monthlyVariableInterest.toLocaleString()} 원\n`
    } else {
      eligibilityResult.value += '변동금리 옵션이 없습니다.\n'
    }

    if (fixedRateOptions.length === 0 && variableRateOptions.length === 0) {
      eligibilityResult.value += '선택한 조건에 맞는 대출 상품이 없습니다.'
    }
  }
}

const filterMortgageOptions = (options, isApartment) => {
  return options.filter(option => 
    (isApartment && option.mrtg_type_nm === '아파트') || 
    (!isApartment && option.mrtg_type_nm !== '아파트')
  )
}

const toggleNotice = () => {
  showNotice.value = !showNotice.value;
};

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
      params: { query: mortgageProductDetail.value ? mortgageProductDetail.value.kor_co_nm : searchQuery.value }
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
  margin-bottom: 20px;
}

.product-info h5 {
  margin-bottom: 10px;
}

.options-title {
  margin-top: 25px;
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
  border-bottom: 1px solid #dee2e6;
}

.custom-table tr:last-child td {
  border-bottom: none;
}

.custom-table tr:hover {
  background-color: #f8f9fa;
}

.loan-eligibility-check {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  margin-bottom: 20px;
}

.cal-form-group {
  margin-bottom: 15px;
}

.cal-form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.cal-form-control {
  width: 100%;
  padding: 8px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  max-width: 300px;
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

.eligibility-result {
  background-color: #e3f2fd;
  padding: 15px;
  border-radius: 8px;
  white-space: pre-wrap;
}

.notice-title {
  padding: 10px;
  margin: 0;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.notice-content {
  padding: 15px;
}

.notice-content small {
  display: block;
  line-height: 1.6;
}

.btn-violet {
  background-color: #642EFE;
  border-color: #642EFE;
  color: white;
  transition: all 0.3s ease, all 0.3s ease;
}

.btn-violet:hover {
  background-color: #4B088A;
  border-color: #4B088A;
  color: white;
}

.accordion-item {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.accordion-button {
  background-color: #e3f2fd;
  color: #333;
  font-weight: bold;
}

.accordion-button:not(.collapsed) {
  background-color: #007bff;
  color: #ffffff;
}
</style>