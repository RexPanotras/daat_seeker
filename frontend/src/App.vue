<script setup>
import { ref, onMounted, computed } from 'vue'
import ContentList from './components/ContentList.vue'
import ContentDetail from './components/ContentDetail.vue'
import SubjectList from './components/SubjectList.vue'
import HarmonicCalculator from './components/HarmonicCalculator.vue'
import LorentzCalculator from './components/LorentzCalculator.vue'

const subjects = ref([])
const contents = ref([])
const loading = ref(false)
const error = ref(null)
const selectedSubject = ref('')
const currentCalculator = ref(null)
const currentContent = ref(null)

const API_BASE_URL = 'http://localhost:8086/api'

// 简单的路由逻辑
const currentRoute = ref(window.location.hash)

// 监听hash变化
window.addEventListener('hashchange', () => {
  currentRoute.value = window.location.hash
  handleRoute()
})

// 解析当前路由
const routeInfo = computed(() => {
  const hash = currentRoute.value
  if (hash.startsWith('#/content/')) {
    const contentId = hash.replace('#/content/', '')
    return { type: 'content', id: contentId }
  }
  return { type: 'home' }
})

// 处理路由
async function handleRoute() {
  const route = routeInfo.value
  if (route.type === 'content' && route.id) {
    await fetchContentById(route.id)
  } else {
    currentContent.value = null
    currentCalculator.value = null
  }
}

// 根据ID获取内容
async function fetchContentById(id) {
  try {
    const response = await fetch(`${API_BASE_URL}/contents/${id}`)
    if (!response.ok) throw new Error('获取内容失败')
    currentContent.value = await response.json()
  } catch (err) {
    console.error('获取内容失败:', err)
    error.value = err.message
  }
}

async function fetchSubjects() {
  loading.value = true
  error.value = null
  try {
    const response = await fetch(`${API_BASE_URL}/subjects`)
    if (!response.ok) throw new Error('获取学科列表失败')
    subjects.value = await response.json()
  } catch (err) {
    error.value = err.message
    console.error('获取学科列表失败:', err)
  } finally {
    loading.value = false
  }
}

async function fetchContents(subject = '') {
  loading.value = true
  error.value = null
  try {
    const url = subject 
      ? `${API_BASE_URL}/contents?subject=${subject}`
      : `${API_BASE_URL}/contents`
    const response = await fetch(url)
    if (!response.ok) throw new Error('获取内容列表失败')
    contents.value = await response.json()
  } catch (err) {
    error.value = err.message
    console.error('获取内容列表失败:', err)
  } finally {
    loading.value = false
  }
}

function selectSubject(subject) {
  selectedSubject.value = subject
  fetchContents(subject)
}

// 学科图标映射 - 与SubjectList组件保持一致
const subjectIcons = {
  '全部': '📚',
  '数学': '🔢',
  '物理学': '⚛️',
  '化学': '⚗️',
  '生物学': '🧬',
  '计算机科学': '💻',
  '地理学': '🌍',
  '逻辑学': '🧩'
}

function getSubjectIcon(subject) {
  return subjectIcons[subject] || '📖'
}

function handleContentClick(content) {
  // 在新标签页打开内容详情页
  const url = `#/content/${content.id}`
  window.open(url, '_blank')
}

function goHome() {
  window.location.hash = ''
  currentContent.value = null
  currentCalculator.value = null
}

onMounted(() => {
  fetchSubjects()
  fetchContents()
  handleRoute() // 处理初始路由
})
</script>

<template>
  <div class="app">
    <header class="header">
      <div class="container">
        <h1 class="logo">
          <span class="logo-icon">🔬</span>
          DA'AT Seeker
        </h1>
        <p class="subtitle">知识追寻者 - 科学计算与知识服务平台</p>
      </div>
    </header>

    <main class="main">
      <div class="container">
        <!-- 学科列表 -->
        <SubjectList 
          :subjects="subjects" 
          :selectedSubject="selectedSubject"
          @subjectClick="selectSubject" 
        />

        <!-- 错误提示 -->
        <div v-if="error" class="error-message">
          <span class="error-icon">⚠️</span>
          {{ error }}
        </div>

        <!-- 加载状态 -->
        <div v-if="loading" class="loading">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>

        <!-- 内容区域 -->
        <div v-else class="content">
          <!-- 内容详情页（用于新标签页） -->
          <ContentDetail 
            v-if="currentContent" 
            :content="currentContent" 
            @back="goHome"
          />
          <!-- 内容列表 -->
          <ContentList v-else :contents="contents" @content-click="handleContentClick" />
        </div>
      </div>
    </main>

    <footer class="footer">
      <div class="container">
        <p>DA'AT Seeker - 科学计算与知识服务平台</p>
        <p class="tech-stack">Powered by Flask + Vue + SQLite</p>
      </div>
    </footer>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  background: linear-gradient(135deg, #1a73e8 0%, #34a853 100%);
  min-height: 100vh;
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Header */
.header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 20px 0;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
}

.logo {
  font-size: 2rem;
  font-weight: 700;
  color: #1a73e8;
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-icon {
  font-size: 2.5rem;
}

.subtitle {
  color: #666;
  margin-top: 5px;
  font-size: 1rem;
}

/* Main */
.main {
  flex: 1;
  padding: 30px 0;
}

/* Tabs */
.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: none;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 25px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.tab-icon {
  font-size: 1.2rem;
}

.tab-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.tab-btn.active {
  background: #1a73e8;
  color: white;
}

/* Error Message */
.error-message {
  background: #ffebee;
  color: #c62828;
  padding: 15px 20px;
  border-radius: 10px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.error-icon {
  font-size: 1.2rem;
}

/* Loading */
.loading {
  text-align: center;
  padding: 60px 20px;
  color: white;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Content */
.content {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.tab-content {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.grid-2 {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 30px;
}

/* Back Button */
.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  margin-bottom: 20px;
  border: none;
  background: #f0f0f0;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background: #e0e0e0;
  transform: translateX(-3px);
}

/* Calculator View */
.calculator-view {
  animation: fadeIn 0.3s ease;
}

/* Footer */
.footer {
  background: rgba(0, 0, 0, 0.2);
  color: white;
  text-align: center;
  padding: 20px 0;
}

.tech-stack {
  font-size: 0.9rem;
  opacity: 0.8;
  margin-top: 5px;
}

/* Responsive */
@media (max-width: 768px) {
  .logo {
    font-size: 1.5rem;
  }
  
  .tabs {
    justify-content: center;
  }
  
  .tab-btn {
    padding: 10px 16px;
    font-size: 0.9rem;
  }
  
  .grid-2 {
    grid-template-columns: 1fr;
  }
  
  .content {
    padding: 20px;
  }
}
</style>
