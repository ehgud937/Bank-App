<!-- BankMap.vue -->
<template>
  <div class="container bank-map-container">
    <div class="search-form">
      <input 
        type="text" 
        v-model="searchQuery"
        placeholder="은행명을 입력하세요" 
        class="form-control search-input"
      >
      <button class="btn search-btn" style="background-color: #e3f2fd;" @click="searchBanks">검색</button>
      <button class="btn search-btn" style="background-color: #e3f2fd;" @click="getNearbyBanks">주변 은행 찾기</button>
    </div>
    <div class="content-container">
      <div id="map" class="map"></div>
      <div v-if="banks.length" class="bank-list">
        <div 
          v-for="bank in banks" 
          :key="bank.id"
          class="bank-item card mb-2 p-3"
          @click="moveToBank(bank)"
        >
          <h5>{{ bank.place_name }}</h5>
          <p class="mb-1">주소: {{ bank.address_name }}</p>
          <p class="mb-1">도로명: {{ bank.road_address_name }}</p>
          <p class="mb-1" v-if="bank.phone">전화번호: {{ bank.phone }}</p>
          <p class="mb-0" v-if="bank.distance">거리: {{ Math.round(bank.distance) }}m</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const kakaoApiKey = import.meta.env.VITE_KAKAO_JS_API_KEY;

const API_URL = 'http://127.0.0.1:8000/api/v1/kakaomap'
const searchQuery = ref('')
const banks = ref([])
let map = null
let markers = []
let infowindow = null

onMounted(() => {
  const script = document.createElement('script')
  script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${kakaoApiKey}&libraries=services&autoload=false`
  script.onload = () => {
    kakao.maps.load(initializeMap)
  }
  document.head.appendChild(script)
})

const initializeMap = () => {
  const container = document.getElementById('map')
  const options = {
    center: new kakao.maps.LatLng(37.5665, 126.9780),
    level: 3
  }
  map = new kakao.maps.Map(container, options)
  infowindow = new kakao.maps.InfoWindow({ zIndex: 1 })
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
      params: { query: searchQuery.value }
    })
    banks.value = response.data.documents
    createMarkers(banks.value)
  } catch (error) {
    console.error('은행 검색 실패:', error)
  }
}

const getNearbyBanks = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        try {
          const response = await axios.get(`${API_URL}/nearby/`, {
            params: {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            }
          })
          banks.value = response.data.documents
          createMarkers(banks.value)
          
          const currentPosition = new kakao.maps.LatLng(
            position.coords.latitude,
            position.coords.longitude
          )
          map.setCenter(currentPosition)
        } catch (error) {
          console.error('주변 은행 검색 실패:', error)
        }
      },
      (error) => {
        console.error('위치 정보를 가져올 수 없습니다:', error)
        alert('위치 정보 접근을 허용해주세요.')
      }
    )
  } else {
    alert('이 브라우저에서는 위치 기반 서비스를 사용할 수 없습니다.')
  }
}
</script>

<style scoped>
.bank-map-container {
  padding: 20px;
  height: calc(100vh - 120px);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.search-form {
  display: flex;
  gap: 10px;
  width: auto;
}

.search-input {
  flex-grow: 1;
}

.search-btn {
  background-color: #e3f2fd;
  color: #000000;
  border: 1px solid #dee2e6;
}

.content-container {
  display: flex;
  gap: 20px;
  flex: 1;
  min-height: 0;
}

.map {
  flex: 1;
  height: 100%;
  border-radius: 8px;
}

.bank-list {
  width: 300px;
  overflow-y: auto;
}

.bank-item {
  cursor: pointer;
  transition: background-color 0.2s;
}

.bank-item:hover {
  background-color: #e3f2fd;
}
</style>