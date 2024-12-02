<template>
  <div class="row exchange-container">
    <div class="col-12 p-2">
      <ExchangeRateItemView />
    </div>

    <!-- 환율표 -->
    <div class="col-12 p-2">
      <div class="card exchange-card">
        <div class="card-body">
          <h2 class="card-title section-title">오늘의 환율표</h2>
          <div class="table-responsive">
            <table class="table text-center custom-table" v-if="store.exchangeRateData">
              <thead>
                <tr>
                  <th scope="col">국가 통화명</th>
                  <th scope="col">장부가격</th>
                  <th scope="col">전신환 매입률</th>
                  <th scope="col">전신환 매도율</th>
                </tr>
              </thead>
              <tbody>
                <template v-for="(exchangeRate, index) in store.exchangeRateData" :key="exchangeRate.id">
                  <tr :class="{ 'row-divider': index > 0 }">
                    <td>{{ exchangeRate.cur_nm }}</td>
                    <td>{{ exchangeRate.bkpr }}원</td>
                    <td>{{ exchangeRate.ttb }}원</td>
                    <td>{{ exchangeRate.tts }}원</td>
                  </tr>
                </template>
              </tbody>
            </table>
          </div>
        </div>
      </div>    
    </div>
  </div>
</template>

<script setup>
import ExchangeRateItemView from './Exchange/ExchangeRateItemView.vue';

import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
</script>

<style scoped>
.exchange-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.exchange-card {
  border: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  background-color: #ffffff;
}

.exchange-section {
  margin-bottom: 20px;
}

.section-title {
  color: black;
  margin-bottom: 15px;
}

.custom-select, .custom-input {
  border: 1px solid #ced4da;
  border-radius: 4px;
  padding: 8px 12px;
}

.custom-select:focus, .custom-input:focus {
  border-color: #80bdff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.result {
  margin-top: 15px;
  font-weight: bold;
  color: #28a745;
}

.divider {
  border-top: 1px solid #e9ecef;
  margin: 20px 0;
}

.custom-table {
  border-collapse: separate;
  border-spacing: 0 8px;
}

.custom-table th, .custom-table td {
  border: none;
  padding: 12px;
}

.custom-table thead th {
  background-color: #e3f2fd;
  color: black;
  font-weight: bold;
}

.custom-table tbody tr {
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.custom-table tbody tr:hover {
  background-color: #f8f9fa;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.row-divider {
  border-top: 1px solid #e9ecef;
}

@media (max-width: 768px) {
  .exchange-container {
    padding: 10px;
  }
  
  .custom-table {
    font-size: 14px;
  }
}
</style>