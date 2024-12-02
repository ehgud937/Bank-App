<template>
  <div class="recommend-products-container" v-if="store.recommendProductsData">
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
            <div v-if="store.recommendProductsData.ml_based.products.deposit.length === 0" class="accordion-body">
              <p>{{ store.loginuserinfo }}님께 적합한 상품이 없습니다.</p>
            </div>
            <div v-else class="accordion-body">
              <ul class="list-group">
                <li class="list-group-item product-item" v-for="depositProduct in store.recommendProductsData.ml_based.products.deposit" :key="depositProduct.id">
                  <h5 class="product-title"><a @click="findDepositProductDetail(depositProduct.product_name)">{{ depositProduct.product_name }}</a></h5>
                  <p class="product-bank">{{ depositProduct.bank_name }}</p>
                  <table class="table custom-table">
                    <tbody>
                      <tr>
                        <td>일반 금리</td>
                        <td>{{ depositProduct.interest_info.basic_rate }}%</td>
                      </tr>
                      <tr>
                        <td>우대 금리</td>
                        <td>{{ depositProduct.interest_info.max_rate }}%</td>
                      </tr>
                    </tbody>
                  </table>
                  <footer class="product-rank">나와 비슷한 사용자가 선택한 상품 중 {{ depositProduct.rank }}위 입니다.</footer>
                </li>
              </ul>
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
              <ul class="list-group">
                <li class="list-group-item product-item" v-for="savingProduct in store.recommendProductsData.ml_based.products.saving" :key="savingProduct.id">
                  <h5 class="product-title"><a @click="findSavingProductDetail(savingProduct.product_name)">{{ savingProduct.product_name }}</a></h5>
                  <p class="product-bank">{{ savingProduct.bank_name }}</p>
                  <table class="table custom-table">
                    <tbody>
                      <tr>
                        <td>일반 금리</td>
                        <td>{{ savingProduct.interest_info.basic_rate }}%</td>
                      </tr>
                      <tr>
                        <td>우대 금리</td>
                        <td>{{ savingProduct.interest_info.max_rate }}%</td>
                      </tr>
                    </tbody>
                  </table>
                  <footer class="product-rank">나와 비슷한 사용자가 선택한 상품 중 {{ savingProduct.rank }}위 입니다.</footer>
                </li>
              </ul>
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
              <ul class="list-group">
                <li class="list-group-item product-item" v-for="mortgageProduct in store.recommendProductsData.ml_based.products.mortgage" :key="mortgageProduct.id">
                  <h5 class="product-title"><a @click="findMortgageProductDetail(mortgageProduct.product_name)">{{ mortgageProduct.product_name }}</a></h5>
                  <p class="product-bank">{{ mortgageProduct.bank_name }}</p>
                  <table class="table custom-table">
                    <tbody>
                      <tr>
                        <td>최저 금리</td>
                        <td>{{ mortgageProduct.interest_info.min_rate }}%</td>
                      </tr>
                      <tr>
                        <td>최고 금리</td>
                        <td>{{ mortgageProduct.interest_info.max_rate }}%</td>
                      </tr>
                    </tbody>
                  </table>
                  <footer class="product-rank">나와 비슷한 사용자가 선택한 상품 중 {{ mortgageProduct.rank }}위 입니다.</footer>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useCounterStore } from '@/stores/counter';

const router = useRouter()
const store = useCounterStore()

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
</style>