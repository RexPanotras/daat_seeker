<script setup>
import { ref } from 'vue'

const x = ref(100)
const t = ref(0.000001)
const v = ref(100000000)
const result = ref(null)
const loading = ref(false)
const error = ref(null)

const API_BASE_URL = 'http://localhost:8086/api'
const LIGHT_SPEED = 299792458 // 光速 m/s

async function calculateLorentz() {
  if (v.value >= LIGHT_SPEED) {
    error.value = '速度必须小于光速 (299,792,458 m/s)'
    return
  }
  
  if (v.value < 0) {
    error.value = '速度不能为负数'
    return
  }
  
  loading.value = true
  error.value = null
  result.value = null
  
  try {
    const response = await fetch(`${API_BASE_URL}/calculate/lorentz`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 
        x: x.value,
        t: t.value,
        v: v.value
      })
    })
    
    if (!response.ok) {
      const err = await response.json()
      throw new Error(err.error || '计算失败')
    }
    
    result.value = await response.json()
  } catch (err) {
    error.value = err.message
    console.error('计算洛伦兹变换失败:', err)
  } finally {
    loading.value = false
  }
}

function formatNumber(num) {
  if (Math.abs(num) < 0.001 || Math.abs(num) > 1000000) {
    return num.toExponential(6)
  }
  return num.toFixed(6)
}

function getVelocityPercentage() {
  return ((v.value / LIGHT_SPEED) * 100).toFixed(2)
}
</script>

<template>
  <div class="lorentz-calculator">
    <div class="calculator-layout">
      <!-- 输入区域 -->
      <div class="input-section">
        <h3 class="section-title">
          <span class="icon">⚡</span>
          洛伦兹变换计算
        </h3>
        <p class="section-desc">
          计算狭义相对论中的洛伦兹变换，观察不同惯性参考系中的时空坐标
        </p>
        
        <div class="inputs-grid">
          <div class="input-group">
            <label for="x">
              <span class="input-icon">📏</span>
              位置 x (m)
            </label>
            <input 
              id="x"
              v-model.number="x"
              type="number"
              step="any"
              placeholder="输入位置坐标"
            />
          </div>
          
          <div class="input-group">
            <label for="t">
              <span class="input-icon">⏱️</span>
              时间 t (s)
            </label>
            <input 
              id="t"
              v-model.number="t"
              type="number"
              step="any"
              placeholder="输入时间"
            />
          </div>
          
          <div class="input-group">
            <label for="v">
              <span class="input-icon">🚀</span>
              相对速度 v (m/s)
            </label>
            <input 
              id="v"
              v-model.number="v"
              type="number"
              step="any"
              placeholder="输入相对速度"
            />
            <div class="velocity-info">
              <span class="velocity-percent">{{ getVelocityPercentage() }}% 光速</span>
              <div class="velocity-bar">
                <div 
                  class="velocity-fill"
                  :style="{ width: getVelocityPercentage() + '%' }"
                ></div>
              </div>
            </div>
          </div>
        </div>
        
        <button 
          class="calculate-btn"
          :disabled="loading"
          @click="calculateLorentz"
        >
          <span v-if="loading" class="btn-spinner"></span>
          <span v-else>🚀 计算洛伦兹变换</span>
        </button>
        
        <div v-if="error" class="error-msg">
          ⚠️ {{ error }}
        </div>
      </div>
      
      <!-- 结果区域 -->
      <div v-if="result" class="result-section">
        <h3 class="section-title">
          <span class="icon">📊</span>
          计算结果
        </h3>
        
        <div class="result-card">
          <div class="gamma-display">
            <div class="gamma-label">洛伦兹因子 γ</div>
            <div class="gamma-value">{{ result.gamma.toFixed(6) }}</div>
            <div class="gamma-formula">γ = 1/√(1-v²/c²)</div>
          </div>
          
          <div class="coordinates">
            <div class="coordinate-item">
              <div class="coord-label">变换后位置 x'</div>
              <div class="coord-value">{{ formatNumber(result.xPrime) }} m</div>
              <div class="coord-formula">x' = γ(x - vt)</div>
            </div>
            
            <div class="coordinate-item">
              <div class="coord-label">变换后时间 t'</div>
              <div class="coord-value">{{ formatNumber(result.tPrime) }} s</div>
              <div class="coord-formula">t' = γ(t - vx/c²)</div>
            </div>
          </div>
          
          <div class="effects">
            <h4>🌟 相对论效应</h4>
            <div class="effect-list">
              <div class="effect-item">
                <span class="effect-name">长度收缩:</span>
                <span class="effect-value">
                  {{ (1/result.gamma * 100).toFixed(2) }}%
                </span>
              </div>
              <div class="effect-item">
                <span class="effect-name">时间膨胀:</span>
                <span class="effect-value">
                  {{ result.gamma.toFixed(2) }}x
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 知识说明 -->
    <div class="info-section">
      <h3 class="info-title">📚 关于洛伦兹变换</h3>
      <div class="info-content">
        <p>
          <strong>洛伦兹变换</strong>是狭义相对论的核心，描述了两个惯性参考系之间的时空坐标转换。
          它基于两个基本假设：相对性原理和光速不变原理。
        </p>
        
        <div class="formulas-grid">
          <div class="formula-card">
            <h4>📐 变换公式</h4>
            <div class="formula-list">
              <code>x' = γ(x - vt)</code>
              <code>t' = γ(t - vx/c²)</code>
              <code>γ = 1/√(1-v²/c²)</code>
            </div>
          </div>
          
          <div class="formula-card">
            <h4>🌟 物理效应</h4>
            <div class="effects-list">
              <div class="effect">
                <span class="effect-icon">📏</span>
                <div>
                  <strong>长度收缩</strong>
                  <p>运动方向上的长度会缩短</p>
                </div>
              </div>
              <div class="effect">
                <span class="effect-icon">⏱️</span>
                <div>
                  <strong>时间膨胀</strong>
                  <p>运动时钟走得更慢</p>
                </div>
              </div>
              <div class="effect">
                <span class="effect-icon">🔄</span>
                <div>
                  <strong>同时性的相对性</strong>
                  <p>不同参考系对同时性的判断不同</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="key-points">
          <div class="point">
            <span class="point-icon">⚡</span>
            <span>已被无数实验验证</span>
          </div>
          <div class="point">
            <span class="point-icon">🛰️</span>
            <span>GPS卫星必须考虑时间膨胀效应</span>
          </div>
          <div class="point">
            <span class="point-icon">🔬</span>
            <span>粒子加速器中的时间膨胀已被观测</span>
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
.lorentz-calculator {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.calculator-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

@media (max-width: 900px) {
  .calculator-layout {
    grid-template-columns: 1fr;
  }
}

/* 输入区域 */
.input-section {
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
  border-radius: 15px;
  padding: 25px;
  border: 1px solid #e0e0e0;
}

.section-title {
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

.section-desc {
  color: #666;
  font-size: 0.95rem;
  margin-bottom: 25px;
  line-height: 1.5;
}

.inputs-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 25px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #333;
  font-weight: 500;
  font-size: 0.95rem;
}

.input-icon {
  font-size: 1.2rem;
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

.velocity-info {
  margin-top: 8px;
}

.velocity-percent {
  font-size: 0.85rem;
  color: #667eea;
  font-weight: 600;
}

.velocity-bar {
  width: 100%;
  height: 6px;
  background: #e0e0e0;
  border-radius: 3px;
  margin-top: 5px;
  overflow: hidden;
}

.velocity-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 3px;
  transition: width 0.3s ease;
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

/* 结果区域 */
.result-section {
  background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
  border-radius: 15px;
  padding: 25px;
  border: 1px solid #667eea30;
}

.result-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.gamma-display {
  text-align: center;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
  color: white;
  margin-bottom: 20px;
}

.gamma-label {
  font-size: 0.9rem;
  opacity: 0.9;
  margin-bottom: 5px;
}

.gamma-value {
  font-size: 2rem;
  font-weight: 700;
  font-family: 'Courier New', monospace;
}

.gamma-formula {
  font-size: 0.85rem;
  opacity: 0.8;
  margin-top: 5px;
}

.coordinates {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
}

.coordinate-item {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 10px;
  border-left: 4px solid #667eea;
}

.coord-label {
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 5px;
}

.coord-value {
  font-size: 1.3rem;
  font-weight: 600;
  color: #333;
  font-family: 'Courier New', monospace;
}

.coord-formula {
  font-size: 0.8rem;
  color: #667eea;
  margin-top: 5px;
  font-family: 'Courier New', monospace;
}

.effects {
  background: #f0f4ff;
  padding: 15px;
  border-radius: 10px;
}

.effects h4 {
  color: #667eea;
  margin-bottom: 12px;
  font-size: 1rem;
}

.effect-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.effect-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #e0e0e0;
}

.effect-item:last-child {
  border-bottom: none;
}

.effect-name {
  color: #666;
}

.effect-value {
  font-weight: 600;
  color: #667eea;
}

/* 知识说明 */
.info-section {
  background: linear-gradient(135deg, #667eea08 0%, #764ba208 100%);
  border-radius: 15px;
  padding: 25px;
  border: 1px solid #667eea20;
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
  margin-bottom: 20px;
}

.formulas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin: 20px 0;
}

.formula-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.formula-card h4 {
  color: #667eea;
  margin-bottom: 15px;
  font-size: 1.1rem;
}

.formula-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.formula-list code {
  background: #f0f4ff;
  padding: 12px;
  border-radius: 8px;
  font-family: 'Courier New', monospace;
  color: #333;
  font-size: 0.95rem;
  border-left: 3px solid #667eea;
}

.effects-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.effect {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.effect-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.effect div {
  flex: 1;
}

.effect strong {
  color: #333;
  display: block;
  margin-bottom: 3px;
}

.effect p {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
}

.key-points {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 25px;
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
  .calculator-layout {
    grid-template-columns: 1fr;
  }
  
  .formulas-grid {
    grid-template-columns: 1fr;
  }
  
  .key-points {
    grid-template-columns: 1fr;
  }
}
</style>
