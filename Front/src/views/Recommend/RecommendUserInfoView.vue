<template>
  <div class="recommend-products-container">
    <div v-if="store.recommendProductsData">
      <div v-if="store.recommendProductsData.ml_based.products.deposit">
        <div class="accordion" id="recommendProductsAccordion">
          <!-- 예금 섹션 -->
          <div class="accordion-item">
            <h3 class="accordion-header">
              <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseDeposit" aria-expanded="true" aria-controls="collapseDeposit">
                예금
              </button>
            </h3>
            <div id="collapseDeposit" class="accordion-collapse collapse show" data-bs-parent="#recommendProductsAccordion">
              <div v-if="store.recommendProductsData.rule_based.products.deposit.length === 0" class="accordion-body">
                <p>{{ store.loginuserinfo }}님께 적합한 상품이 없습니다.</p>
              </div>
              <div v-else class="accordion-body">
                <!-- highrate -->
                <div v-if="depositHighRateProducts.length > 0">
                  <h5 class="recommendation-type">HIGHRATE</h5>
                  <ul class="list-group">
                    <li class="list-group-item product-item" v-for="depositHighRateProduct in depositHighRateProducts" :key="depositHighRateProduct.id">
                      <div>
                        <h5 class="product-title"><a @click="findDepositProductDetail(depositHighRateProduct.product_name)">{{ depositHighRateProduct.product_name }}</a></h5>
                        <p class="product-bank">{{ depositHighRateProduct.bank_name }}</p>
                        <table class="table custom-table">
                          <tbody>
                            <tr>
                              <td>일반 금리</td>
                              <td>{{ depositHighRateProduct.interest_info.basic_rate }}%</td>
                            </tr>
                            <tr>
                              <td>우대 금리</td>
                              <td>{{ depositHighRateProduct.interest_info.max_rate }}%</td>
                            </tr>
                          </tbody>
                        </table>
                        <footer class="product-rank">고객님의 투자성향과 자산을 고려한 추천 중 {{ depositHighRateProduct.rank }}위 입니다.</footer>
                      </div>
                    </li>
                  </ul>
                </div>
                <hr class="section-divider">
                <!-- balanced -->
                <div v-if="depositBalanceProducts.length > 0">
                  <h5 class="recommendation-type">BALANCED</h5>
                  <ul class="list-group">
                    <li class="list-group-item product-item" v-for="depositBalacedProduct in depositBalanceProducts" :key="depositBalacedProduct.id">
                      <div>
                        <h5 class="product-title"><a @click="findDepositProductDetail(depositBalacedProduct.product_name)">{{ depositBalacedProduct.product_name }}</a></h5>
                        <p class="product-bank">{{ depositBalacedProduct.bank_name }}</p>
                        <table class="table custom-table">
                          <tbody>
                            <tr>
                              <td>일반 금리</td>
                              <td>{{ depositBalacedProduct.interest_info.basic_rate }}%</td>
                            </tr>
                            <tr>
                              <td>우대 금리</td>
                              <td>{{ depositBalacedProduct.interest_info.max_rate }}%</td>
                            </tr>
                          </tbody>
                        </table>
                        <footer class="product-rank">고객님의 투자성향과 자산을 고려한 추천 중 {{ depositBalacedProduct.rank }}위 입니다.</footer>
                      </div>
                    </li>
                  </ul>
                </div>
                <hr class="section-divider">
                <!-- custom -->
                <div v-if="depositCustomProducts.length > 0">
                  <h5 class="recommendation-type">CUSTOM</h5>
                  <ul class="list-group">
                    <li class="list-group-item product-item" v-for="depositCustomProduct in depositCustomProducts" :key="depositCustomProduct.id">
                      <div>
                        <h5 class="product-title"><a @click="findDepositProductDetail(depositCustomProduct.product_name)">{{ depositCustomProduct.product_name }}</a></h5>
                        <p class="product-bank">{{ depositCustomProduct.bank_name }}</p>
                        <table class="table custom-table">
                          <tbody>
                            <tr>
                              <td>일반 금리</td>
                              <td>{{ depositCustomProduct.interest_info.basic_rate }}%</td>
                            </tr>
                            <tr>
                              <td>우대 금리</td>
                              <td>{{ depositCustomProduct.interest_info.max_rate }}%</td>
                            </tr>
                          </tbody>
                        </table>
                        <footer class="product-rank">고객님의 투자성향과 자산을 고려한 추천 중 {{ depositCustomProduct.rank }}위 입니다.</footer>
                      </div>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 적금 섹션 -->
          <div class="accordion-item">
            <h3 class="accordion-header">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseSaving" aria-expanded="false" aria-controls="collapseSaving">
                적금
              </button>
            </h3>
            <div id="collapseSaving" class="accordion-collapse collapse show" data-bs-parent="#recommendProductsAccordion">
              <div v-if="store.recommendProductsData.ml_based.products.saving.length === 0" class="accordion-body">
                <p>{{ store.loginuserinfo }}님께 적합한 상품이 없습니다.</p>
              </div>
              <div v-else class="accordion-body">
                <!-- highrate -->
                <div v-if="savingHighRateProducts.length > 0">
                  <h5 class="recommendation-type">HIGHRATE</h5>
                  <ul class="list-group">
                    <li class="list-group-item product-item" v-for="savingHighRateProduct in savingHighRateProducts" :key="savingHighRateProduct.id">
                      <div>
                        <h5 class="product-title"><a @click="findSavingProductDetail(savingHighRateProduct.product_name)">{{ savingHighRateProduct.product_name }}</a></h5>
                        <p class="product-bank">{{ savingHighRateProduct.bank_name }}</p>
                        <table class="table custom-table">
                          <tbody>
                            <tr>
                              <td>일반 금리</td>
                              <td>{{ savingHighRateProduct.interest_info.basic_rate }}%</td>
                            </tr>
                            <tr>
                              <td>우대 금리</td>
                              <td>{{ savingHighRateProduct.interest_info.max_rate }}%</td>
                            </tr>
                          </tbody>
                        </table>
                        <footer class="product-rank">고객님의 투자성향과 자산을 고려한 추천 중 {{ savingHighRateProduct.rank }}위 입니다.</footer>
                      </div>
                    </li>
                  </ul>
                </div>
                <hr class="section-divider">
                <!-- balanced -->
                <div v-if="savingBalanceProducts.length > 0">
                  <h5 class="recommendation-type">BALANCED</h5>
                  <ul class="list-group">
                    <li class="list-group-item product-item" v-for="savingBalacedProduct in savingBalanceProducts" :key="savingBalacedProduct.id">
                      <div>
                        <h5 class="product-title"><a @click="findSavingProductDetail(savingBalacedProduct.product_name)">{{ savingBalacedProduct.product_name }}</a></h5>
                        <p class="product-bank">{{ savingBalacedProduct.bank_name }}</p>
                        <table class="table custom-table">
                          <tbody>
                            <tr>
                              <td>일반 금리</td>
                              <td>{{ savingBalacedProduct.interest_info.basic_rate }}%</td>
                            </tr>
                            <tr>
                              <td>우대 금리</td>
                              <td>{{ savingBalacedProduct.interest_info.max_rate }}%</td>
                            </tr>
                          </tbody>
                        </table>
                        <footer class="product-rank">고객님의 투자성향과 자산을 고려한 추천 중 {{ savingBalacedProduct.rank }}위 입니다.</footer>
                      </div>
                    </li>
                  </ul>
                </div>
                <hr class="section-divider">
                <!-- custom -->
                <div v-if="savingCustomProducts.length > 0">
                  <h5 class="recommendation-type">CUSTOM</h5>
                  <ul class="list-group">
                    <li class="list-group-item product-item" v-for="savingCustomProduct in savingCustomProducts" :key="savingCustomProduct.id">
                      <div>
                        <h5 class="product-title"><a @click="findSavingProductDetail(savingCustomProduct.product_name)">{{ savingCustomProduct.product_name }}</a></h5>
                        <p class="product-bank">{{ savingCustomProduct.bank_name }}</p>
                        <table class="table custom-table">
                          <tbody>
                            <tr>
                              <td>일반 금리</td>
                              <td>{{ savingCustomProduct.interest_info.basic_rate }}%</td>
                            </tr>
                            <tr>
                              <td>우대 금리</td>
                              <td>{{ savingCustomProduct.interest_info.max_rate }}%</td>
                            </tr>
                          </tbody>
                        </table>
                        <footer class="product-rank">고객님의 투자성향과 자산을 고려한 추천 중 {{ savingCustomProduct.rank }}위 입니다.</footer>
                      </div>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 주택 담보 대출 섹션 -->
          <div class="accordion-item">
            <h3 class="accordion-header">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseMortgage" aria-expanded="false" aria-controls="collapseMortgage">
                주택 담보 대출
              </button>
            </h3>
            <div id="collapseMortgage" class="accordion-collapse collapse show" data-bs-parent="#recommendProductsAccordion">
              <div v-if="store.recommendProductsData.ml_based.products.mortgage.length === 0" class="accordion-body">
                <p>{{ store.loginuserinfo }}님께 적합한 상품이 없습니다.</p>
              </div>
              <div v-else class="accordion-body">
                <!-- lowrate -->
                <div v-if="mortgageLowRateProducts.length > 0">
                  <h5 class="recommendation-type">LOWRATE</h5>
                  <ul class="list-group">
                    <li class="list-group-item product-item" v-for="mortgageLowRateProduct in mortgageLowRateProducts" :key="mortgageLowRateProduct.id">
                      <div>
                        <h5 class="product-title"><a @click="findMortgageProductDetail(mortgageLowRateProduct.product_name)">{{ mortgageLowRateProduct.product_name }}</a></h5>
                        <p class="product-bank">{{ mortgageLowRateProduct.bank_name }}</p>
                        <table class="table custom-table">
                          <tbody>
                            <tr>
                              <td>최저 금리</td>
                              <td>{{ mortgageLowRateProduct.interest_info.min_rate }}%</td>
                            </tr>
                            <tr>
                              <td>우대 금리</td>
                              <td>{{ mortgageLowRateProduct.interest_info.max_rate }}%</td>
                            </tr>
                          </tbody>
                        </table>
                        <footer class="product-rank">고객님의 투자성향과 자산을 고려한 추천 중 {{ mortgageLowRateProduct.rank }}위 입니다.</footer>
                      </div>
                    </li>
                  </ul>
                </div>
                <hr class="section-divider">
                <!-- custom -->
                <div v-if="mortgageCustomProducts.length > 0">
                  <h5 class="recommendation-type">CUSTOM</h5>
                  <ul class="list-group">
                    <li class="list-group-item product-item" v-for="mortgageCustomProduct in mortgageCustomProducts" :key="mortgageCustomProduct.id">
                      <div>
                        <h5 class="product-title"><a @click="findMortgageProductDetail(mortgageCustomProduct.product_name)">{{ mortgageCustomProduct.product_name }}</a></h5>
                        <p class="product-bank">{{ mortgageCustomProduct.bank_name }}</p>
                        <table class="table custom-table">
                          <tbody>
                            <tr>
                              <td>최저 금리</td>
                              <td>{{ mortgageCustomProduct.interest_info.min_rate }}%</td>
                            </tr>
                            <tr>
                              <td>우대 금리</td>
                              <td>{{ mortgageCustomProduct.interest_info.max_rate }}%</td>
                            </tr>
                          </tbody>
                        </table>
                        <footer class="product-rank">고객님의 투자성향과 자산을 고려한 추천 중 {{ mortgageCustomProduct.rank }}위 입니다.</footer>
                      </div>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useCounterStore } from '@/stores/counter';

const router = useRouter()
const store = useCounterStore()

const depositHighRateProducts = computed(() => {
  if (store.recommendProductsData) {
    return store.recommendProductsData.rule_based.products.deposit.filter((product) => {
      return product.recommendation_type === 'HIGH_RATE'
    })
  }
  return []
})

const depositBalanceProducts = computed(() => {
  if (store.recommendProductsData) {
    return store.recommendProductsData.rule_based.products.deposit.filter((product) => {
      return product.recommendation_type === 'BALANCED'
    })
  }
  return []
})

const depositCustomProducts = computed(() => {
  if (store.recommendProductsData) {
    return store.recommendProductsData.rule_based.products.deposit.filter((product) => {
      return product.recommendation_type === 'CUSTOM'
    })
  }
  return []
})

const savingHighRateProducts = computed(() => {
  if (store.recommendProductsData) {
    return store.recommendProductsData.rule_based.products.saving.filter((product) => {
      return product.recommendation_type === 'HIGH_RATE'
    })
  }
  return []
})

const savingBalanceProducts = computed(() => {
  if (store.recommendProductsData) {
    return store.recommendProductsData.rule_based.products.saving.filter((product) => {
      return product.recommendation_type === 'BALANCED'
    })
  }
  return []
})

const savingCustomProducts = computed(() => {
  if (store.recommendProductsData) {
    return store.recommendProductsData.rule_based.products.saving.filter((product) => {
      return product.recommendation_type === 'CUSTOM'
    })
  }
  return []
})

const mortgageLowRateProducts = computed(() => {
  if (store.recommendProductsData) {
    return store.recommendProductsData.rule_based.products.mortgage.filter((product) => {
      return product.recommendation_type === 'LOW_RATE'
    })
  }
  return []
})

const mortgageCustomProducts = computed(() => {
  if (store.recommendProductsData) {
    return store.recommendProductsData.rule_based.products.mortgage.filter((product) => {
      return product.recommendation_type === 'CUSTOM'
    })
  }
  return []
})

const findDepositProductDetail = function(depositProductName) {
  const targetProduct = store.depositProducts.find((element) => {
    if (element.fin_prdt_nm === depositProductName) {
      return element
    }
  })
  console.log(targetProduct.id)
  router.push({ name: 'deposit-product-detail', params: { 'id': targetProduct.id } })
}

const findSavingProductDetail = function(savingProductName) {
  const targetProduct = store.savingProducts.find((element) => {
    if (element.fin_prdt_nm === savingProductName) {
      return element
    }
  })
  console.log(targetProduct.id)
  router.push({ name: 'saving-product-detail', params: { 'id': targetProduct.id } })
}

const findMortgageProductDetail = function(mortgageProductName) {
  const targetProduct = store.mortgageProducts.find((element) => {
    if (element.fin_prdt_nm === mortgageProductName) {
      return element
    }
  })
  console.log(targetProduct.id)
  router.push({ name: 'mortgage-product-detail', params: { 'id': targetProduct.id } })
}
</script>

<style scoped>
.recommend-products-container {
  max-width: 800px;
  margin: 0 auto;
}

.accordion-item {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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

.recommendation-type {
  color: rgb(8, 74, 145);
  margin: 5px 0px 15px 15px;
  font-weight: bold;
}

.product-item {
  border: none;
  border-bottom: 1px solid #dee2e6;
  padding: 15px;
}

.product-item:last-child {
  border-bottom: none;
}

.product-title {
  color: #007bff;
  margin-bottom: 10px;
  transition: all ease 0.3s;
}

.product-title:hover {
  color: rgb(8, 74, 145);
  font-weight: bold;
  text-decoration: underline;
}

.product-bank {
  color: #6c757d;
  margin-bottom: 15px;
}

.custom-table {
  margin-bottom: 15px;
}

.custom-table td {
  border: none;
  padding: 5px 0;
}

.custom-table td:first-child {
  font-weight: bold;
  color: #495057;
}

.product-rank {
  font-size: 0.9em;
  color: #6c757d;
}

.section-divider {
  margin: 20px 0;
  border-top: 1px solid #474747;
}
</style>