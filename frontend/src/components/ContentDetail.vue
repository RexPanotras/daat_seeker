<script setup>
import { ref, onMounted, nextTick, onUpdated } from 'vue'
import HarmonicCalculator from './HarmonicCalculator.vue'
import LorentzCalculator from './LorentzCalculator.vue'
import MarkdownRenderer from './MarkdownRenderer.vue'

const props = defineProps({
  content: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['back'])

function goBack() {
  emit('back')
}

// 渲染LaTeX公式
function renderMath() {
  if (window.renderMathInElement) {
    nextTick(() => {
      window.renderMathInElement(document.querySelector('.content-detail') || document.body, {
        delimiters: [
          {left: '$$', right: '$$', display: true},
          {left: '$', right: '$', display: false}
        ],
        throwOnError: false
      })
    })
  }
}

onMounted(() => {
  renderMath()
})

onUpdated(() => {
  renderMath()
})

function getSubjectIcon(subject) {
  const icons = {
    '数学': '🔢',
    '物理学': '⚛️'
  }
  return icons[subject] || '📖'
}

function getTypeIcon(type) {
  return type === 'question' ? '❓' : '📄'
}

function getTypeLabel(type) {
  return type === 'question' ? '计算问题' : '知识文章'
}
</script>

<template>
  <div class="content-detail">
    <button class="back-btn" @click="goBack">
      ← 返回知识探索
    </button>
    
    <div class="detail-header">
      <div class="subject-badge">
        <span class="subject-icon">{{ getSubjectIcon(content.subject) }}</span>
        <span class="subject-name">{{ content.subject }}</span>
      </div>
      <div class="type-badge">
        <span class="type-icon">{{ getTypeIcon(content.type) }}</span>
        <span class="type-name">{{ getTypeLabel(content.type) }}</span>
      </div>
    </div>
    
    <h1 class="detail-title">{{ content.title }}</h1>
    
    <div class="detail-description">
      <h3>🔍 科学解释</h3>
      <p>{{ content.description }}</p>
    </div>
    
    <!-- 计算问题显示计算器 -->
    <div v-if="content.type === 'question'" class="calculator-section">
      <h3>🧮 计算工具</h3>
      <HarmonicCalculator v-if="content.interface && content.interface.includes('harmonic') && !content.interface.includes('inverse')" />
      <HarmonicCalculator v-else-if="content.interface && content.interface.includes('harmonic') && content.interface.includes('inverse')" />
      <LorentzCalculator v-else-if="content.interface && content.interface.includes('lorentz')" />
    </div>
    
    <!-- 文章类型显示Markdown内容 -->
    <div v-else class="article-section">
      <h3>📖 详细内容</h3>
      <div class="article-content">
        <MarkdownRenderer :content="content.description" />
      </div>
    </div>
    
    <div class="tags-section">
      <h3>🏷️ 标签</h3>
      <div class="tags">
        <span v-for="tag in content.tags.split(',')" :key="tag" class="tag">
          {{ tag.trim() }}
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.content-detail {
  background: white;
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.back-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  margin-bottom: 20px;
  transition: all 0.3s ease;
}

.back-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.detail-header {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.subject-badge,
.type-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 15px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

.subject-badge {
  background: #e3f2fd;
  color: #1976d2;
}

.type-badge {
  background: #f3e5f5;
  color: #7b1fa2;
}

.subject-icon,
.type-icon {
  font-size: 1.2rem;
}

.detail-title {
  font-size: 2rem;
  color: #333;
  margin-bottom: 25px;
  line-height: 1.3;
}

.detail-description {
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
  border-radius: 12px;
  padding: 25px;
  margin-bottom: 25px;
  border-left: 4px solid #667eea;
}

.detail-description h3 {
  color: #667eea;
  margin-bottom: 15px;
  font-size: 1.2rem;
}

.detail-description p {
  color: #555;
  line-height: 1.8;
  font-size: 1rem;
}

.calculator-section,
.article-section {
  margin-bottom: 25px;
}

.calculator-section h3,
.article-section h3 {
  color: #333;
  margin-bottom: 15px;
  font-size: 1.2rem;
}

.article-content {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 20px;
  color: #666;
  line-height: 1.8;
}

.tags-section h3 {
  color: #333;
  margin-bottom: 15px;
  font-size: 1.2rem;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag {
  background: #e3f2fd;
  color: #1976d2;
  padding: 6px 12px;
  border-radius: 15px;
  font-size: 0.85rem;
  font-weight: 500;
}

@media (max-width: 768px) {
  .content-detail {
    padding: 20px;
  }
  
  .detail-title {
    font-size: 1.5rem;
  }
  
  .detail-header {
    gap: 10px;
  }
  
  .subject-badge,
  .type-badge {
    padding: 6px 12px;
    font-size: 0.85rem;
  }
}
</style>
