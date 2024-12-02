<template>
  <div class="profile-container">
    <div class="row">
      <div v-if="userInfo" class="col-12 col-lg-4 mb-4">
        <div class="profile-card">
          <h4 class="card-title mb-4">{{ store.loginusername }}님의 정보</h4>
          <!-- <p>{{ userInfo }}</p> -->
          <table class="table custom-table" v-if="userInfo">
            <tbody>
              <tr>
                <th>닉네임</th>
                <td>{{ userInfo.username }}</td>
              </tr>
              <tr>
                <th>가입 이메일</th>
                <td>{{ userInfo.email }}</td>
              </tr>
              <tr>
                <th>생일</th>
                <td>{{ userInfo.birthdate }}</td>
              </tr>
              <tr>
                <th>자산</th>
                <td>{{ userInfo.assets }}</td>
              </tr>
              <tr>
                <th>연 소득</th>
                <td>{{ userInfo.annual_income }}</td>
              </tr>
              <tr>
                <th>투자 성향</th>
                <td>{{ userInfo.investment_type }}</td>
              </tr>
              <tr>
                <th>주 거래 은행</th>
                <td>{{ userInfo.primary_bank }}</td>
              </tr>
            </tbody>
          </table>
          <button class="btn btn-danger" @click="signout">회원 탈퇴</button>
        </div>
      </div>
      <div class="col-12 col-lg-8">
        <div class="product-card">
          <h4 class="card-title mb-4">{{ store.loginusername }}님이 가입한 상품 목록</h4>
          <div class="accordion" id="recommendProductsAccordion">
            <!-- 예금 섹션 -->
            <div class="accordion-item">
              <h3 class="accordion-header">
                <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseDeposit" aria-expanded="true" aria-controls="collapseDeposit">
                  예금
                </button>
              </h3>
              <div id="collapseDeposit" class="accordion-collapse collapse show" data-bs-parent="#recommendProductsAccordion">
                <div v-if="myRegisterDepositProducts.length === 0" class="accordion-body">
                  <p>{{ store.loginusername }}님이 가입한 상품이 없습니다.</p>
                </div>
                <div v-else class="accordion-body">
                  <div class="table-responsive">
                    <table class="table custom-table">
                      <thead>
                        <tr>
                          <th scope="col">금융 회사명</th>
                          <th scope="col">상품명</th>
                          <th scope="col">금리</th>
                          <th scope="col">저축 기간</th>
                          <th scope="col"></th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="myDepositProduct in myRegisterDepositProducts" :key="myDepositProduct.id">
                          <td>{{ myDepositProduct.product_info.kor_co_nm }}</td>
                          <td>{{ myDepositProduct.product_info.fin_prdt_nm }}</td>
                          <td>
                            <span v-for="myDepositProductOption in myDepositProduct.product_info.options" :key="myDepositProductOption.id">
                              <span v-if="myDepositProductOption.id === myDepositProduct.option">{{ myDepositProductOption.intr_rate }}%</span>
                            </span>
                          </td>
                          <td>
                            <span v-for="myDepositProductOption in myDepositProduct.product_info.options" :key="myDepositProductOption.id">
                              <span v-if="myDepositProductOption.id === myDepositProduct.option">{{ myDepositProductOption.save_trm }}개월</span>
                            </span>
                          </td>
                          <td>
                            <button class="btn btn-danger" @click.prevent="cancelProduct('deposit', myDepositProduct.id)">해지하기</button>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
            <!-- 적금 섹션 -->
            <div class="accordion-item">
              <h3 class="accordion-header">
                <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseSaving" aria-expanded="true" aria-controls="collapseDeposit">
                  적금
                </button>
              </h3>
              <div id="collapseSaving" class="accordion-collapse collapse show" data-bs-parent="#recommendProductsAccordion">
                <div v-if="myRegisterSavingProducts.length === 0" class="accordion-body">
                  <p>{{ store.loginusername }}님이 가입한 상품이 없습니다.</p>
                </div>
                <div v-else class="accordion-body">
                  <div class="table-responsive">
                    <table class="table custom-table">
                      <thead>
                        <tr>
                          <th scope="col">금융 회사명</th>
                          <th scope="col">상품명</th>
                          <th scope="col">금리</th>
                          <th scope="col">저축 기간</th>
                          <th scope="col"></th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="mySavingProduct in myRegisterSavingProducts" :key="mySavingProduct.id">
                          <td>{{ mySavingProduct.product_info.kor_co_nm }}</td>
                          <td>{{ mySavingProduct.product_info.fin_prdt_nm }}</td>
                          <td>
                            <span v-for="mySavingProductOption in mySavingProduct.product_info.options" :key="mySavingProductOption.id">
                              <span v-if="mySavingProductOption.id === mySavingProduct.option">{{ mySavingProductOption.intr_rate }}%</span>
                            </span>
                          </td>
                          <td>
                            <span v-for="mySavingProductOption in mySavingProduct.product_info.options" :key="mySavingProductOption.id">
                              <span v-if="mySavingProductOption.id === mySavingProduct.option">{{ mySavingProductOption.save_trm }}개월</span>
                            </span>
                          </td>
                          <td>
                            <button class="btn btn-danger" @click.prevent="cancelProduct('saving', mySavingProduct.id)">해지하기</button>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
            <!-- Mortgage 섹션 -->
            <div class="accordion-item">
              <h3 class="accordion-header">
                <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseMortgage" aria-expanded="true" aria-controls="collapseDeposit">
                  주택 담보 대출
                </button>
              </h3>
              <div id="collapseMortgage" class="accordion-collapse collapse show" data-bs-parent="#recommendProductsAccordion">
                <div v-if="myRegisterMortgageProducts.length === 0" class="accordion-body">
                  <p>{{ store.loginusername }}님이 가입한 상품이 없습니다.</p>
                </div>
                <div v-else class="accordion-body">
                  <div class="table-responsive">
                    <table class="table custom-table">
                      <thead>
                        <tr>
                          <th scope="col">금융 회사명</th>
                          <th scope="col">상품명</th>
                          <th scope="col">최저 금리</th>
                          <th scope="col">최고 금리</th>
                          <th scope="col">비고</th>
                          <th scope="col"></th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="myMortgageProduct in myRegisterMortgageProducts" :key="myMortgageProduct.id">
                          <td>{{ myMortgageProduct.product_info.kor_co_nm }}</td>
                          <td>{{ myMortgageProduct.product_info.fin_prdt_nm }}</td>
                          <td>
                            <span v-for="myMortgageProductOption in myMortgageProduct.product_info.options" :key="myMortgageProductOption.id">
                              <span v-if="myMortgageProductOption.id === myMortgageProduct.option">{{ myMortgageProductOption.lend_rate_min }}%</span>
                            </span>
                          </td>
                          <td>
                            <span v-for="myMortgageProductOption in myMortgageProduct.product_info.options" :key="myMortgageProductOption.id">
                              <span v-if="myMortgageProductOption.id === myMortgageProduct.option">{{ myMortgageProductOption.lend_rate_max }}%</span>
                            </span>
                          </td>
                          <td>
                            <span v-for="myMortgageProductOption in myMortgageProduct.product_info.options" :key="myMortgageProductOption.id">
                              <span v-if="myMortgageProductOption.id === myMortgageProduct.option">{{ myMortgageProductOption.lend_rate_type_nm }}</span>
                            </span>
                          </td>
                          <td>
                            <button class="btn btn-danger" @click="cancelProduct('mortgage', myMortgageProduct.id)">해지하기</button>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- 차트 섹션 -->
        <div class="chart-card mt-4">
          <h4 class="card-title mb-4">금리 비교 차트</h4>
          <div style="height: 400px;">
            <Bar :data="chartDataComputed" :options="chartOptions" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import { useCounterStore } from '@/stores/counter'
import axios from 'axios'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const router = useRouter()
const store = useCounterStore()

const userInfo = store.loginUserInfo
const myRegisterDepositProducts = ref([])
const myRegisterSavingProducts = ref([])
const myRegisterMortgageProducts = ref([])

const chartData = ref({
  labels: [],
  datasets: [
    {
      label: '기본 금리',
      backgroundColor: '#f87979',
      data: []
    },
    {
      label: '우대 금리',
      backgroundColor: '#7acbf9',
      data: []
    }
  ]
})

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: '금리 (%)'
      }
    }
  },
  plugins: {
    legend: {
      display: true
    }
  }
})

const chartDataComputed = computed(() => chartData.value)

onMounted(() => {
  fetchMyProducts()
})

const fetchMyProducts = () => {
  axios({
    method: 'get',
    url: `${store.API_URL}/register/my-registers/`,
    headers: { Authorization: `Token ${store.token}` }
  })
    .then((response) => {
      console.log(response)
      myRegisterDepositProducts.value = response.data.deposits.filter((product) => product.status === 'PENDING')
      myRegisterSavingProducts.value = response.data.savings.filter((product) => product.status === 'PENDING')
      myRegisterMortgageProducts.value = response.data.mortgages.filter((product) => product.status === 'PENDING')
      updateChartData()
    })
    .catch((error) => {
      console.log(error)
    })
}

const updateChartData = () => {
  const labels = []
  const intrRates = []
  const intrRates2 = []

  myRegisterDepositProducts.value.forEach(product => {
    labels.push(product.product_info.fin_prdt_nm + ' (예금)')
    const option = product.product_info.options.find(opt => opt.id === product.option)
    if (option) {
      intrRates.push(option.intr_rate)
      intrRates2.push(option.intr_rate2)
    }
  })

  myRegisterSavingProducts.value.forEach(product => {
    labels.push(product.product_info.fin_prdt_nm + ' (적금)')
    const option = product.product_info.options.find(opt => opt.id === product.option)
    if (option) {
      intrRates.push(option.intr_rate)
      intrRates2.push(option.intr_rate2)
    }
  })

  chartData.value = {
    labels: labels,
    datasets: [
      {
        label: '기본 금리',
        backgroundColor: '#f87979',
        data: intrRates
      },
      {
        label: '우대 금리',
        backgroundColor: '#7acbf9',
        data: intrRates2
      }
    ]
  }

  console.log(chartData.value)
}

const cancelProduct = function(productType, registerId) {
  if (confirm('정말로 이 상품을 해지하시겠습니까?')) {
    axios({
      method: 'delete',
      url: `${store.API_URL}/register/cancel/${productType}/${registerId}/`,
      headers: { Authorization: `Token ${store.token}` }
    })
      .then((response) => {
        console.log(response)
        removeProductFromList(productType, registerId)
        alert('상품이 성공적으로 해지되었습니다.')
        updateChartData()
      })
      .catch((error) => {
        console.log(error)
        alert('상품 해지 중 오류가 발생했습니다.')
      })
  }
}

const removeProductFromList = (productType, registerId) => {
  switch (productType) {
    case 'deposit':
      myRegisterDepositProducts.value = myRegisterDepositProducts.value.filter(product => product.id !== registerId)
      break
    case 'saving':
      myRegisterSavingProducts.value = myRegisterSavingProducts.value.filter(product => product.id !== registerId)
      break
    case 'mortgage':
      myRegisterMortgageProducts.value = myRegisterMortgageProducts.value.filter(product => product.id !== registerId)
      break
  }
}

const signout = function () {
  router.push({ name: 'signout' })
}
</script>

<style scoped>
.profile-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.profile-card, .product-card, .chart-card {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.card-title {
  color: #333;
  font-weight: bold;
  margin-bottom: 20px;
}

.custom-table {
  border-collapse: separate;
  border-spacing: 0;
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
}

.custom-table tr:last-child td {
  border-bottom: none;
}

.custom-table tr:hover {
  background-color: #f8f9fa;
}

.accordion-button:not(.collapsed) {
  background-color: #e3f2fd;
  color: #333;
}

.btn-danger {
  background-color: #dc3545;
  border-color: #dc3545;
}

.btn-danger:hover {
  background-color: #c82333;
  border-color: #bd2130;
}
</style>