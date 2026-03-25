<script setup>
import { ref, defineEmits } from 'vue'

const props = defineProps({
  contents: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['contentClick'])

const expandedContent = ref(null)

function toggleContent(id) {
  expandedContent.value = expandedContent.value === id ? null : id
}

function handleContentClick(content) {
  // 在新标签页打开内容详情页
  const url = `#/content/${content.id}`
  window.open(url, '_blank')
}

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
</script>

<template>
  <div class="content-list">
    <h2 class="section-title">
      <span class="icon">📚</span>
      知识探索
    </h2>
    <div class="contents-container">
      <div 
        v-for="content in contents" 
        :key="content.id"
        class="content-card"
        :class="{ expanded: expandedContent === content.id }"
      >
        <div 
          class="content-header"
          @click="handleContentClick(content)"
        >
          <div class="content-icon">
            {{ getSubjectIcon(content.subject) }}
          </div>
          <div class="content-info">
            <h3 class="content-title">{{ content.title }}</h3>
            <p class="content-preview">{{ content.description }}</p>
            <span class="content-type">{{ getTypeIcon(content.type) }} {{ content.type === 'question' ? '计算问题' : '知识文章' }}</span>
          </div>
          <div 
            class="expand-icon"
            @click.stop="toggleContent(content.id)"
          >
            {{ expandedContent === content.id ? '▼' : '▶' }}
          </div>
        </div>
        
        <div v-if="expandedContent === content.id" class="content-details">
          <div class="refutation">
            <h4>🔍 科学解释</h4>
            <p>{{ content.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.content-list {
  background: #f8f9fa;
  border-radius: 15px;
  padding: 25px;
}

.section-title {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.icon {
  font-size: 1.8rem;
}

.contents-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.content-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: all 0.3s ease;
}

.content-card:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.content-card.expanded {
  box-shadow: 0 6px 30px rgba(0, 0, 0, 0.15);
}

.content-header {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.content-header:hover {
  background-color: #f5f7fa;
}

.content-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.content-info {
  flex: 1;
  min-width: 0;
}

.content-title {
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 8px;
  font-weight: 600;
}

.content-preview {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.5;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.content-type {
  display: inline-block;
  margin-top: 8px;
  padding: 4px 10px;
  background: #e3f2fd;
  color: #1976d2;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

.expand-icon {
  font-size: 1.2rem;
  color: #667eea;
  cursor: pointer;
  padding: 5px;
  border-radius: 50%;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.expand-icon:hover {
  background: #f0f4ff;
}

.content-details {
  padding: 0 20px 20px;
  border-top: 1px solid #eee;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.refutation {
  padding-top: 15px;
}

.refutation h4 {
  color: #667eea;
  margin-bottom: 10px;
  font-size: 1rem;
}

.refutation p {
  color: #555;
  line-height: 1.8;
  font-size: 0.95rem;
}

@media (max-width: 768px) {
  .content-list {
    padding: 15px;
  }

  .content-header {
    padding: 15px;
  }

  .content-icon {
    font-size: 1.5rem;
  }

  .content-title {
    font-size: 1.1rem;
  }

  .content-preview {
    font-size: 0.9rem;
    -webkit-line-clamp: 2;
  }
}
</style>
