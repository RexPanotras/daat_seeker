<script setup>
import { ref, computed } from 'vue'

const sum = ref(0)
const n = ref('')
const loading = ref(false)
const error = ref('')
const overflow = ref(false)

const API_BASE_URL = 'http://localhost:8086/api'

const isValidInput = computed(() => {
  return n.value && !isNaN(n.value) && parseInt(n.value) >= 0
})

async function calculateSum() {
  if (!isValidInput.value) {
    error.value = '请输入非负整数'
    return
  }

  loading.value = true
  error.value = ''
  overflow.value = false

  try {
    const response = await fetch(`${API_BASE_URL}/calculate/sum1ton`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ n: parseInt(n.value) })
    })

    if (!response.ok) {
      throw new Error('计算失败')
    }

    const data = await response.json()
    sum.value = data.sum
    overflow.value = data.overflow || false
  } catch (err) {
    error.value = err.message
    console.error('计算失败:', err)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="calculator-container">
    <h3>计算1~n的和</h3>
    
    <div class="input-section">
      <label for="n">输入n:</label>
      <input 
        type="number" 
        id="n" 
        v-model="n" 
        placeholder="请输入非负整数"
        min="0"
        step="1"
      />
      <button 
        @click="calculateSum" 
        :disabled="!isValidInput || loading"
      >
        {{ loading ? '计算中...' : '计算' }}
      </button>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-if="sum !== 0 || n" class="result-section">
      <h4>计算结果:</h4>
      <p v-if="overflow" class="overflow-warning">
        注意：计算结果可能已溢出
      </p>
      <p class="result">
        1 + 2 + 3 + ... + {{ n }} = {{ sum }}
      </p>
    </div>

    <div class="description-section">
      <h4>问题描述</h4>
      <p>
        计算1到n的和是一个基本的数学问题，其公式为：1 + 2 + 3 + ... + n = n(n+1)/2。
      </p>
      <p>
        当n增大时，这个和会无限增大，是一个发散的级数，不会收敛到任何有限值。
      </p>
      <p>
        注意：虽然在某些数学分支（如黎曼ζ函数的解析延拓）中，形式上有1 + 2 + 3 + ... = -1/12的表达式，但这只是一种数学技巧，并非实际求和的结果。在常规的算术意义下，这个级数是发散的。
      </p>
    </div>
  </div>
</template>

<style scoped>
.calculator-container {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
}

.calculator-container h3 {
  margin-top: 0;
  color: #333;
  border-bottom: 2px solid #007bff;
  padding-bottom: 10px;
}

.input-section {
  margin: 20px 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.input-section label {
  font-weight: bold;
  min-width: 80px;
}

.input-section input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.input-section button {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.input-section button:hover {
  background-color: #0069d9;
}

.input-section button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.error-message {
  color: red;
  margin: 10px 0;
  padding: 10px;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
}

.result-section {
  margin: 20px 0;
  padding: 15px;
  background-color: #e7f3ff;
  border: 1px solid #b3d7ff;
  border-radius: 4px;
}

.result-section h4 {
  margin-top: 0;
  color: #0066cc;
}

.overflow-warning {
  color: #ff6b00;
  font-weight: bold;
  margin: 10px 0;
}

.result {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin: 10px 0;
}

.description-section {
  margin-top: 30px;
  padding: 20px;
  background-color: #f0f0f0;
  border-radius: 4px;
  border-left: 4px solid #6c757d;
}

.description-section h4 {
  margin-top: 0;
  color: #555;
}

.description-section p {
  margin: 10px 0;
  line-height: 1.5;
  color: #333;
}
</style>
