<script setup>
import { ref, onMounted, nextTick, onUpdated } from 'vue'

const n = ref(100)

// 渲染LaTeX公式
function renderMath() {
  if (window.renderMathInElement) {
    nextTick(() => {
      window.renderMathInElement(document.body, {
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
  // 等待KaTeX加载完成
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderMath)
  } else {
    renderMath()
  }
})

// 组件更新后重新渲染数学公式
onUpdated(() => {
  renderMath()
})
const target = ref(10)
const result1 = ref(null)
const result2 = ref(null)
const loading1 = ref(false)
const loading2 = ref(false)
const error1 = ref(null)
const error2 = ref(null)

const API_BASE_URL = 'http://localhost:8086/api'

async function calculateHarmonic() {
  if (n.value < 1) {
    error1.value = '请输入大于0的整数'
    return
  }
  
  loading1.value = true
  error1.value = null
  result1.value = null
  
  try {
    const response = await fetch(`${API_BASE_URL}/calculate/harmonic`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ n: n.value })
    })
    
    if (!response.ok) {
      const err = await response.json()
      throw new Error(err.error || '计算失败')
    }
    
    result1.value = await response.json()
  } catch (err) {
    error1.value = err.message
    console.error('计算调和级数失败:', err)
  } finally {
    loading1.value = false
  }
}

async function findHarmonicN() {
  if (target.value <= 0) {
    error2.value = '请输入大于0的数值'
    return
  }
  
  loading2.value = true
  error2.value = null
  result2.value = null
  
  try {
    const response = await fetch(`${API_BASE_URL}/calculate/harmonic/inverse`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ target: target.value })
    })
    
    if (!response.ok) {
      const err = await response.json()
      throw new Error(err.error || '计算失败')
    }
    
    result2.value = await response.json()
  } catch (err) {
    error2.value = err.message
    console.error('寻找调和级数项数失败:', err)
  } finally {
    loading2.value = false
  }
}
</script>

<template>
  <div class="harmonic-calculator">
    <div class="calculator-grid">
      <!-- 调和级数计算 -->
      <div class="calculator-card">
        <h3 class="card-title">
          <span class="icon">📊</span>
          调和级数计算
        </h3>
        <p class="card-desc">
          计算 H<sub>n</sub> = 1 + 1/2 + 1/3 + ... + 1/n 的和
        </p>
        
        <div class="input-group">
          <label for="n">项数 n:</label>
          <input 
            id="n"
            v-model.number="n"
            type="number"
            min="1"
            placeholder="输入正整数"
          />
        </div>
        
        <button 
          class="calculate-btn"
          :disabled="loading1"
          @click="calculateHarmonic"
        >
          <span v-if="loading1" class="btn-spinner"></span>
          <span v-else>🚀 计算</span>
        </button>
        
        <div v-if="error1" class="error-msg">
          ⚠️ {{ error1 }}
        </div>
        
        <div v-if="result1" class="result">
          <h4>📈 计算结果</h4>
          <div v-if="n <= 1000000000" class="result-item">
            <span class="label">精确和:</span>
            <span class="value">{{ result1.sum.toFixed(10) }}</span>
          </div>
          <div class="result-item">
            <span class="label">近似值:</span>
            <span class="value">{{ result1.approx.toFixed(10) }}</span>
          </div>
          <div v-if="n > 1000000000" class="info-msg">
            ⚠️ 由于n值过大，只计算近似值
          </div>
          <div class="formula">
            H<sub>{{ n }}</sub> ≈ ln({{ n }}) + γ
          </div>
        </div>
      </div>
      
      <!-- 寻找项数 -->
      <div class="calculator-card">
        <h3 class="card-title">
          <span class="icon">🔍</span>
          寻找调和级数项数
        </h3>
        <p class="card-desc">
          找到使 H<sub>n</sub> ≥ 目标值的最小项数 n（n不超过44）
        </p>
        
        <div class="input-group">
          <label for="target">目标值:</label>
          <input 
            id="target"
            v-model.number="target"
            type="number"
            min="0.1"
            step="0.1"
            placeholder="输入目标值"
          />
        </div>
        
        <button 
          class="calculate-btn"
          :disabled="loading2"
          @click="findHarmonicN"
        >
          <span v-if="loading2" class="btn-spinner"></span>
          <span v-else>🚀 计算</span>
        </button>
        
        <div v-if="error2" class="error-msg">
          ⚠️ {{ error2 }}
        </div>
        
        <div v-if="result2" class="result">
          <h4>📈 计算结果</h4>
          <div class="result-item">
            <span class="label">最小项数 n:</span>
            <span class="value highlight">{{ result2.n.toLocaleString() }}</span>
          </div>
          <div class="result-item">
            <span class="label">实际和:</span>
            <span class="value">{{ result2.sum.toFixed(10) }}</span>
          </div>
          <div class="result-item">
            <span class="label">是否达标:</span>
            <span class="value" :class="result2.exceeds ? 'success' : 'fail'">
              {{ result2.exceeds ? '✅ 是' : '❌ 否' }}
            </span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 知识说明 -->
    <div class="info-section">
      <h3 class="info-title">📚 关于调和级数</h3>
      <div class="info-content">
        <p>
          <strong>调和级数</strong>是数学中最著名的发散级数之一，形式为：
        </p>
        <div class="math-formula">
          $$H_n = 1 + \frac{1}{2} + \frac{1}{3} + \frac{1}{4} + \cdots + \frac{1}{n} = \sum_{i=1}^{n} \frac{1}{i}$$
        </div>
        <p>
          尽管调和级数的增长速度非常缓慢（近似于 $\ln(n) + \gamma$，其中 $\gamma \approx 0.5772$ 是欧拉-马歇罗尼常数），
          但随着 $n$ 增大，其和会无限增大。这是数学分析中的经典结论，由中世纪数学家尼克尔·奥雷姆首次证明。
        </p>
        
        <!-- 发散性证明 -->
        <div class="proof-section">
          <h4 class="proof-title">📐 调和级数发散性证明（奥雷姆证明法）</h4>
          <div class="proof-content">
            <p><strong>定理：</strong>调和级数 $H_n = \sum_{n=1}^{\infty} \frac{1}{n}$ 是发散的。</p>
            
            <p><strong>证明：</strong></p>
            <p>我们将调和级数的项按以下方式分组：</p>
            
            <div class="math-formula">
              $$H = 1 + \frac{1}{2} + \underbrace{\left(\frac{1}{3} + \frac{1}{4}\right)}_{\text{第1组}} + \underbrace{\left(\frac{1}{5} + \frac{1}{6} + \frac{1}{7} + \frac{1}{8}\right)}_{\text{第2组}} + \underbrace{\left(\frac{1}{9} + \cdots + \frac{1}{16}\right)}_{\text{第3组}} + \cdots$$
            </div>
            
            <p>观察每组的下界：</p>
            <ul class="proof-steps">
              <li>第1组（2项）：$\frac{1}{3} + \frac{1}{4} > \frac{1}{4} + \frac{1}{4} = \frac{2}{4} = \frac{1}{2}$</li>
              <li>第2组（4项）：$\frac{1}{5} + \frac{1}{6} + \frac{1}{7} + \frac{1}{8} > 4 \times \frac{1}{8} = \frac{1}{2}$</li>
              <li>第3组（8项）：$\frac{1}{9} + \cdots + \frac{1}{16} > 8 \times \frac{1}{16} = \frac{1}{2}$</li>
              <li>第 $k$ 组（$2^k$ 项）：$> 2^k \times \frac{1}{2^{k+1}} = \frac{1}{2}$</li>
            </ul>
            
            <p>因此：</p>
            <div class="math-formula">
              $$H > 1 + \frac{1}{2} + \frac{1}{2} + \frac{1}{2} + \frac{1}{2} + \cdots = \infty$$
            </div>
            
            <p><strong>结论：</strong>由于调和级数的部分和可以无限增大，故调和级数<strong>发散</strong>。</p>
          </div>
        </div>
        
        <!-- 近似公式 -->
        <div class="approximation-section">
          <h4 class="approx-title">📊 近似公式</h4>
          <p>对于大 $n$，调和级数可以用以下公式近似：</p>
          <div class="math-formula">
            $$H_n \approx \ln(n) + \gamma + \frac{1}{2n} - \frac{1}{12n^2} + \frac{1}{120n^4} - \cdots$$
          </div>
          <p>其中 $\gamma \approx 0.5772156649$ 是欧拉-马歇罗尼常数。</p>
        </div>
        
        <div class="key-points">
          <div class="point">
            <span class="point-icon">🔢</span>
            <span>调和级数是<strong>发散</strong>的</span>
          </div>
          <div class="point">
            <span class="point-icon">📈</span>
            <span>增长近似于 $\ln(n) + \gamma$</span>
          </div>
          <div class="point">
            <span class="point-icon">⚡</span>
            <span>本系统使用<strong>并发计算</strong>优化性能</span>
          </div>
          <div class="point">
            <span class="point-icon">💾</span>
            <span>计算结果已<strong>缓存</strong>，重复查询更快</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.harmonic-calculator {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.calculator-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 25px;
}

.calculator-card {
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
  border-radius: 15px;
  padding: 25px;
  border: 1px solid #e0e0e0;
}

.card-title {
  font-size: 1.3rem;
  color: #333;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.icon {
  font-size: 1.5rem;
}

.card-desc {
  color: #666;
  font-size: 0.95rem;
  margin-bottom: 20px;
  line-height: 1.5;
}

.input-group {
  margin-bottom: 20px;
}

.input-group label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
}

.input-group input {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.input-group input:focus {
  outline: none;
  border-color: #667eea;
}

.calculate-btn {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.calculate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.calculate-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-msg {
  margin-top: 15px;
  padding: 12px;
  background: #ffebee;
  color: #c62828;
  border-radius: 8px;
  font-size: 0.9rem;
}

.info-msg {
  margin-top: 15px;
  padding: 12px;
  background: #e3f2fd;
  color: #1976d2;
  border-radius: 8px;
  font-size: 0.9rem;
}

.result {
  margin-top: 20px;
  padding: 20px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.result h4 {
  color: #667eea;
  margin-bottom: 15px;
  font-size: 1rem;
}

.result-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.result-item:last-child {
  border-bottom: none;
}

.result-item .label {
  color: #666;
  font-weight: 500;
}

.result-item .value {
  font-family: 'Courier New', monospace;
  color: #333;
  font-weight: 600;
}

.result-item .value.highlight {
  color: #667eea;
  font-size: 1.2rem;
}

.result-item .value.success {
  color: #4caf50;
}

.result-item .value.fail {
  color: #f44336;
}

.formula {
  margin-top: 15px;
  padding: 12px;
  background: #f0f4ff;
  border-radius: 8px;
  font-family: 'Courier New', monospace;
  text-align: center;
  color: #667eea;
  font-size: 0.95rem;
}

/* 知识说明部分 */
.info-section {
  background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
  border-radius: 15px;
  padding: 25px;
  border: 1px solid #667eea30;
}

.info-title {
  font-size: 1.3rem;
  color: #333;
  margin-bottom: 15px;
}

.info-content {
  color: #444;
  line-height: 1.8;
}

.info-content p {
  margin-bottom: 15px;
}

.math-formula {
  background: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  font-family: 'Times New Roman', serif;
  font-size: 1.1rem;
  color: #333;
  margin: 15px 0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  overflow-x: auto;
}

/* 证明部分样式 */
.proof-section {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin: 20px 0;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.08);
  border-left: 4px solid #667eea;
}

.proof-title {
  font-size: 1.1rem;
  color: #667eea;
  margin-bottom: 15px;
  font-weight: 600;
}

.proof-content {
  color: #444;
  line-height: 1.8;
}

.proof-content p {
  margin-bottom: 12px;
}

.proof-steps {
  list-style: none;
  padding: 0;
  margin: 15px 0;
}

.proof-steps li {
  padding: 8px 0;
  padding-left: 20px;
  position: relative;
  border-bottom: 1px dashed #eee;
}

.proof-steps li:last-child {
  border-bottom: none;
}

.proof-steps li::before {
  content: '→';
  position: absolute;
  left: 0;
  color: #667eea;
  font-weight: bold;
}

/* 近似公式部分样式 */
.approximation-section {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin: 20px 0;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.08);
  border-left: 4px solid #4caf50;
}

.approx-title {
  font-size: 1.1rem;
  color: #4caf50;
  margin-bottom: 15px;
  font-weight: 600;
}

.key-points {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 20px;
}

.point {
  background: white;
  padding: 15px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.point-icon {
  font-size: 1.5rem;
}

@media (max-width: 768px) {
  .calculator-grid {
    grid-template-columns: 1fr;
  }
  
  .key-points {
    grid-template-columns: 1fr;
  }
}
</style>
