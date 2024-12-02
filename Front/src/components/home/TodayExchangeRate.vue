<template>
  <div class="exchange-rate-container">
    <div class="exchange-rate-card">
      <h4 class="card-title">주요 국가 환율</h4>
      <hr>
      <div class="table-responsive">
        <table class="table custom-table" v-if="store.majorExchangeRate">
          <thead>
            <!-- <tr>
              <th scope="col">국가 통화명</th>
              <th scope="col">장부가격</th>
            </tr> -->
          </thead>
          <tbody>
            <tr v-for="exchangeRate in store.majorExchangeRate" :key="exchangeRate.id">
              <td>{{ exchangeRate.cur_nm }}</td>
              <td>{{ exchangeRate.bkpr }}원</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore()
</script>

<style scoped>
.exchange-rate-container {
  margin: 0;
}

.exchange-rate-card {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.card-title {
  color: #333;
  font-weight: bold;
  margin-bottom: 19px;
}

.custom-table {
  border-collapse: separate;
  border-spacing: 0;
  text-align: center;
  border-radius: 30px;
}

.custom-table th, .custom-table td {
  border-bottom: 1px solid #dee2e6;
  padding: 8px;
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
</style>