<script setup>
import { defineProps, defineEmits, computed } from 'vue'

const props = defineProps({
  subjects: {
    type: Array,
    required: true
  },
  selectedSubject: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['subjectClick'])

// 学科图标映射 - 理工科与逻辑学
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

// 默认图标
const defaultIcon = '📚'

// 获取学科图标
function getSubjectIcon(subject) {
  return subjectIcons[subject] || defaultIcon
}

// 包含"全部"的学科列表
const subjectsWithAll = computed(() => {
  return ['全部', ...props.subjects]
})

function handleSubjectClick(subject) {
  // 如果点击"全部"，传递空字符串表示不过滤
  const emitValue = subject === '全部' ? '' : subject
  emit('subjectClick', emitValue)
}

function isSelected(subject) {
  if (subject === '全部') {
    return props.selectedSubject === ''
  }
  return props.selectedSubject === subject
}
</script>

<template>
  <nav class="subject-tabs">
    <button 
      v-for="subject in subjectsWithAll" 
      :key="subject"
      :class="['subject-btn', { active: isSelected(subject) }]"
      @click="handleSubjectClick(subject)"
    >
      <span class="btn-icon">{{ getSubjectIcon(subject) }}</span>
      {{ subject }}
    </button>
  </nav>
</template>

<style scoped>
.subject-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.subject-btn {
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

.btn-icon {
  font-size: 1.2rem;
}

.subject-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.subject-btn.active {
  background: #1a73e8;
  color: white;
}

@media (max-width: 768px) {
  .subject-tabs {
    gap: 8px;
    margin-bottom: 20px;
  }
  
  .subject-btn {
    padding: 10px 18px;
    font-size: 0.9rem;
  }
  
  .btn-icon {
    font-size: 1rem;
  }
}
</style>
