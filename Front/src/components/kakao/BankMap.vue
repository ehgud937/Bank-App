<!-- bankmap.vue -->
<template>
  <div class="bank-map-container">
    <!-- 검색바 -->
    <div class="search-bar">
      <input 
        type="text" 
        v-model="searchQuery"
        placeholder="은행명을 입력하세요" 
        class="form-control"
      >
      <button class="btn" style="background-color: #e3f2fd;" @click="searchBanks">검색</button>
      <button class="btn" style="background-color: #e3f2fd;" @click="getNearbyBanks">주변 은행 찾기</button>
    </div>

    <div class="content-container">
      <!-- 지도 -->
      <div id="map" class="map"></div>

      <!-- 검색 결과 목록 -->
      <div class="bank-list">
        <div v-if="banks.length" class="list-container">
          <div 
            v-for="bank in banks" 
            :key="bank.id" 
            class="bank-item card mb-2 p-3"
            @click="moveToBank(bank)"
            @mouseover="highlightMarker(bank)"
          >
            <h5>{{ bank.place_name }}</h5>
            <p class="mb-1">주소: {{ bank.address_name }}</p>
            <p class="mb-1">도로명: {{ bank.road_address_name }}</p>
            <p class="mb-1" v-if="bank.phone">전화번호: {{ bank.phone }}</p>
            <p class="mb-0" v-if="bank.distance">거리: {{ Math.round(bank.distance) }}m</p>
          </div>
        </div>
        <div v-else-if="searched" class="no-result">
          검색 결과가 없습니다.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/api/v1/kakaomap'
const searchQuery = ref('')
const banks = ref([])
const searched = ref(false)
let map = null
let markers = []

const mapInstance = ref(null)

onMounted(() => {
  const initializeMap = () => {
    if (window.kakao && window.kakao.maps) {
      const container = document.getElementById('map')
      const options = {
        center: new window.kakao.maps.LatLng(37.5665, 126.9780),
        level: 3
      }
      mapInstance.value = new window.kakao.maps.Map(container, options)
      map = mapInstance.value  // 전역 map 변수에도 할당
    } else {
      setTimeout(initializeMap, 100)
    }
  }

  initializeMap()
})

const createMarkers = (banks) => {
  if (!window.kakao || !window.kakao.maps) {
    setTimeout(() => createMarkers(banks), 100)
    return
  }

  // 기존 마커 삭제
  markers.forEach(marker => marker.setMap(null))
  markers = []

  // 새로운 마커 생성
  banks.forEach(bank => {
    const marker = new window.kakao.maps.Marker({
      position: new window.kakao.maps.LatLng(bank.y, bank.x),
      map: mapInstance.value
    })
    markers.push(marker)
  })

  // 모든 마커가 보이도록 지도 범위 재설정
  if (markers.length > 0) {
    const bounds = new window.kakao.maps.LatLngBounds()
    markers.forEach(marker => bounds.extend(marker.getPosition()))
    mapInstance.value.setBounds(bounds)
  }
}
// 은행 위치로 이동
const moveToBank = (bank) => {
  if (!window.kakao || !window.kakao.maps) return

  const moveLatLng = new window.kakao.maps.LatLng(bank.y, bank.x)
  mapInstance.value.setCenter(moveLatLng)
  mapInstance.value.setLevel(2)
}

// 키워드로 은행 검색
const searchBanks = async () => {
  if (!searchQuery.value) return
  
  try {
    const response = await axios.get(`${API_URL}/search/`, {
      params: {
        query: searchQuery.value
      }
    })
    banks.value = response.data.documents
    searched.value = true
    createMarkers(banks.value)
  } catch (error) {
    console.error('은행 검색 실패:', error)
  }
}

// 현재 위치 기반 주변 은행 검색
const getNearbyBanks = () => {
  if (!window.kakao || !window.kakao.maps) {
    alert('지도를 불러오는 중입니다. 잠시 후 다시 시도해주세요.')
    return
  }

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
          searched.value = true
          createMarkers(banks.value)
          
          // 현재 위치로 지도 이동
          const currentLocation = new window.kakao.maps.LatLng(
            position.coords.latitude,
            position.coords.longitude
          )
          mapInstance.value.setCenter(currentLocation)
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

.search-bar {
  display: flex;
  gap: 10px;
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

.no-result {
  text-align: center;
  padding: 20px;
  color: #666;
}
</style>