<template>
    <div>
      <div class="card exchange-card">
        <div class="card-body">        
          <!-- 원화 -> 외화 환전 -->
          <div class="exchange-section">
            <h5 class="section-title">원화 환전하기</h5>
            <div class="input-group">
              <select class="form-select custom-select" v-model="selectedForeignCurrency">
                <option value="" disabled selected>외화 선택</option>
                <option v-for="currency in currencies" :key="currency.cur_unit" :value="currency.cur_unit">
                  {{ currency.cur_nm }} ({{ currency.cur_unit }})
                </option>
              </select>
              <input type="number" class="form-control custom-input" v-model="krwAmount" placeholder="원화 금액 입력">
              <span class="input-group-text">KRW</span>
            </div>
            <h6 class="result" v-if="krwToForeignResult">환전 결과: {{ krwToForeignResult }}</h6>
          </div>
          <hr class="divider">
  
          <!-- 외화 -> 원화 환전 -->
          <div class="exchange-section">
            <h5 class="section-title">외화 환전하기</h5>
            <div class="input-group">
              <select class="form-select custom-select" v-model="selectedForeignCurrencyForKRW">
                <option value="" disabled selected>외화 선택</option>
                <option v-for="currency in currencies" :key="currency.cur_unit" :value="currency.cur_unit">
                  {{ currency.cur_nm }} ({{ currency.cur_unit }})
                </option>
              </select>
              <input type="number" class="form-control custom-input" v-model="foreignAmount" placeholder="외화 금액 입력">
              <span class="input-group-text">{{ selectedForeignCurrencyForKRW }}</span>
            </div>
            <h6 class="result" v-if="foreignToKrwResult">환전 결과: {{ foreignToKrwResult }}</h6>
          </div>
        </div>
      </div>   
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import { useCounterStore } from '@/stores/counter'
  
  const store = useCounterStore()
  
  const krwAmount = ref(null)
  const foreignAmount = ref(null)
  const selectedForeignCurrency = ref('')
  const selectedForeignCurrencyForKRW = ref('')
  
  const currencies = computed(() => {
    return store.exchangeRateData.filter(currency => currency.cur_unit !== 'KRW')
  })
  
  const krwToForeignResult = computed(() => {
    if (!krwAmount.value || !selectedForeignCurrency.value) return null
    
    const targetCurrency = store.exchangeRateData.find(rate => rate.cur_unit === selectedForeignCurrency.value)
    if (!targetCurrency) return null
  
    let rate = targetCurrency.bkpr
    let result = krwAmount.value / rate
  
    if (selectedForeignCurrency.value === 'JPY(100)' || selectedForeignCurrency.value === 'IDR(100)') {
      result *= 100
    }
  
    return `${result.toLocaleString('ko-KR', { maximumFractionDigits: 2 })} ${selectedForeignCurrency.value}`
  })
  
  const foreignToKrwResult = computed(() => {
    if (!foreignAmount.value || !selectedForeignCurrencyForKRW.value) return null
    
    const sourceCurrency = store.exchangeRateData.find(rate => rate.cur_unit === selectedForeignCurrencyForKRW.value)
    if (!sourceCurrency) return null
  
    let rate = sourceCurrency.bkpr
    let result = foreignAmount.value * rate
  
    if (selectedForeignCurrencyForKRW.value === 'JPY(100)' || selectedForeignCurrencyForKRW.value === 'IDR(100)') {
      result /= 100
    }
  
    return `${result.toLocaleString('ko-KR', { maximumFractionDigits: 0 })} KRW`
  })
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