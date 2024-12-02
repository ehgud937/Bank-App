<template>
  <div class="footer site-footer">
    <div class="container">
      <div class="footer-bottom">
        <p>&copy; 2024 김도형, 이성준. All rights reserved.</p>
        <div class="social-links">
          <a href="#" title="GitHub"><i class="fab fa-github"></i></a>
          <a href="#" title="LinkedIn"><i class="fab fa-linkedin"></i></a>
          <a href="#" title="Twitter"><i class="fab fa-twitter"></i></a>
        </div>
      </div>

      <div class="footer-content">
        <div class="footer-section project-info">
          <h3 @click="toggleSection('projectInfo')">
            <i class="fas fa-project-diagram"></i> 프로젝트 정보
            <i :class="['fas', projectInfo ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
          </h3>
          <div :class="['dropdown-content', { 'show': projectInfo }]">
            <p><strong>SSAFY 1학기 금융 관통 프로젝트</strong></p>
            <p><i class="fas fa-code-branch"></i> 버전: Beta 1.0</p>
          </div>
        </div>
        <div class="footer-section tech-stack">
          <h3 @click="toggleSection('techStack')">
            <i class="fas fa-laptop-code"></i> 기술 스택
            <i :class="['fas', techStack ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
          </h3>
          <ul :class="['dropdown-content', { 'show': techStack }]">
            <li><i class="fab fa-python"></i> Python</li>
            <li><i class="fab fa-django"></i> Django</li>
            <li><i class="fab fa-js-square"></i> JavaScript</li>
            <li><i class="fab fa-html5"></i> HTML</li>
            <li><i class="fab fa-vuejs"></i> Vue</li>
          </ul>
        </div>
        <div class="footer-section api-list">
          <h3 @click="toggleSection('apiList')">
            <i class="fas fa-plug"></i> 사용된 API
            <i :class="['fas', apiList ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
          </h3>
          <ul :class="['dropdown-content', { 'show': apiList }]">
            <li><i class="fas fa-chart-line"></i> 금융감독원 API</li>
            <li><i class="fas fa-exchange-alt"></i> 한국수출입은행 API</li>
            <li><i class="fas fa-robot"></i> OpenAI API</li>
            <li><i class="fas fa-map-marked-alt"></i> 카카오맵 API</li>
            <li><i class="fas fa-sign-in-alt"></i> 카카오 로그인 API</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const projectInfo = ref(false);
const techStack = ref(false);
const apiList = ref(false);

const toggleSection = (section) => {
  switch(section) {
    case 'projectInfo':
      projectInfo.value = !projectInfo.value;
      break;
    case 'techStack':
      techStack.value = !techStack.value;
      break;
    case 'apiList':
      apiList.value = !apiList.value;
      break;
  }
};
</script>

<style scoped>
.footer {
  background: linear-gradient(to left, #e3f2fd, #a1c6ea);
}

.site-footer {
  background-color: #f8f9fa;
  padding: 40px 0;
  color: #333;
  font-family: Arial, sans-serif;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 50px;
  display: flex;
  justify-content: space-between;
}

.footer-content {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.footer-section {
  flex: 1;
  margin-bottom: 20px;
  min-width: 200px;
}

.footer-section h3 {
  font-size: 18px;
  margin-bottom: 15px;
  color: #007bff;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-section ul {
  list-style-type: none;
  padding: 0;
}

.footer-section li {
  margin-bottom: 8px;
}

.footer-bottom {
  text-align: center;
}

.social-links {
  margin-top: 15px;
}

.social-links a {
  color: #007bff;
  font-size: 20px;
  margin: 0 10px;
  transition: color 0.3s ease;
}

.social-links a:hover {
  color: #0056b3;
}

.fas, .fab {
  margin-right: 5px;
}

.dropdown-content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease-out;
}

.dropdown-content.show {
  max-height: 500px; /* Adjust this value as needed */
  transition: max-height 0.3s ease-in;
}

ul > li {
  text-align: center;
}
</style>