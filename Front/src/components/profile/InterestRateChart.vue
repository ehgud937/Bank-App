<template>
  <div style="height: 400px; width: 100%;">
    <Bar ref="chartRef" :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch, nextTick } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const props = defineProps({
  depositProducts: Array,
  savingProducts: Array
})

const chartData = reactive({
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

const chartOptions = {
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
  }
}

const updateChartData = () => {
  const labels = []
  const intrRates = []
  const intrRates2 = []

  props.depositProducts.forEach(product => {
    if (product.status === 'PENDING') {
      labels.push(product.product_info.fin_prdt_nm + ' (예금)')
      const option = product.product_info.options[0] // 첫 번째 옵션 사용
      if (option) {
        intrRates.push(option.intr_rate)
        intrRates2.push(option.intr_rate2)
      } else {
        console.warn(`No options found for product: ${product.product_info.fin_prdt_nm}`)
      }
    }
  })

  props.savingProducts.forEach(product => {
    if (product.status === 'PENDING') {
      labels.push(product.product_info.fin_prdt_nm + ' (적금)')
      const option = product.product_info.options[0] // 첫 번째 옵션 사용
      if (option) {
        intrRates.push(option.intr_rate)
        intrRates2.push(option.intr_rate2)
      } else {
        console.warn(`No options found for product: ${product.product_info.fin_prdt_nm}`)
      }
    }
  })

  chartData.labels = labels
  chartData.datasets[0].data = intrRates
  chartData.datasets[1].data = intrRates2

  console.log(chartData)
}

onMounted(() => {
  updateChartData()
})

watch(() => [props.depositProducts, props.savingProducts], () => {
  nextTick(() => {
    updateChartData()
  })
}, { deep: true })
</script>
