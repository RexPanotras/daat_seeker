<script setup>
import { computed, onMounted, onUpdated, nextTick, watch } from 'vue'
import { marked } from 'marked'

const props = defineProps({
  content: {
    type: String,
    required: true
  }
})

// 配置marked选项
marked.setOptions({
  breaks: true,        // 支持换行
  gfm: true,          // 支持GitHub Flavored Markdown
  headerIds: true,    // 为标题生成ID
  mangle: false,      // 不转义HTML
  sanitize: false,    // 不进行HTML转义（我们使用DOMPurify或信任内容）
  smartLists: true,   // 智能列表
  smartypants: true,  // 智能标点
  xhtml: false        // 不生成自闭合标签
})

// 解析Markdown
const renderedContent = computed(() => {
  if (!props.content) return ''
  return marked.parse(props.content)
})

// 渲染LaTeX公式
function renderMath() {
  if (window.renderMathInElement) {
    nextTick(() => {
      const elements = document.querySelectorAll('.markdown-body')
      elements.forEach(el => {
        window.renderMathInElement(el, {
          delimiters: [
            {left: '$$', right: '$$', display: true},
            {left: '$', right: '$', display: false}
          ],
          throwOnError: false
        })
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

// 监听内容变化，重新渲染数学公式
watch(() => props.content, () => {
  renderMath()
}, { immediate: true })
</script>

<template>
  <div class="markdown-body" v-html="renderedContent"></div>
</template>

<style scoped>
.markdown-body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif;
  font-size: 16px;
  line-height: 1.6;
  color: #24292f;
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
}

.markdown-body :deep(h1) {
  font-size: 2em;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
  padding-bottom: 0.3em;
  border-bottom: 1px solid #d0d7de;
  color: #1f2328;
}

.markdown-body :deep(h2) {
  font-size: 1.5em;
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
  padding-bottom: 0.3em;
  border-bottom: 1px solid #d0d7de;
  color: #1f2328;
}

.markdown-body :deep(h3) {
  font-size: 1.25em;
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
  color: #1f2328;
}

.markdown-body :deep(h4),
.markdown-body :deep(h5),
.markdown-body :deep(h6) {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
  color: #1f2328;
}

.markdown-body :deep(p) {
  margin-top: 0;
  margin-bottom: 16px;
}

.markdown-body :deep(a) {
  color: #0969da;
  text-decoration: none;
}

.markdown-body :deep(a:hover) {
  text-decoration: underline;
}

.markdown-body :deep(strong) {
  font-weight: 600;
  color: #1f2328;
}

.markdown-body :deep(em) {
  font-style: italic;
}

.markdown-body :deep(code) {
  padding: 0.2em 0.4em;
  margin: 0;
  font-size: 85%;
  background-color: rgba(175, 184, 193, 0.2);
  border-radius: 6px;
  font-family: ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace;
}

.markdown-body :deep(pre) {
  padding: 16px;
  overflow: auto;
  font-size: 85%;
  line-height: 1.45;
  background-color: #f6f8fa;
  border-radius: 6px;
  margin-bottom: 16px;
}

.markdown-body :deep(pre code) {
  display: inline;
  padding: 0;
  margin: 0;
  overflow: visible;
  line-height: inherit;
  word-wrap: normal;
  background-color: transparent;
  border: 0;
}

.markdown-body :deep(blockquote) {
  margin: 0;
  padding: 0 1em;
  color: #656d76;
  border-left: 0.25em solid #d0d7de;
  margin-bottom: 16px;
}

.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  margin-top: 0;
  margin-bottom: 16px;
  padding-left: 2em;
}

.markdown-body :deep(ul) {
  list-style-type: disc;
}

.markdown-body :deep(ol) {
  list-style-type: decimal;
}

.markdown-body :deep(li) {
  margin: 0.25em 0;
}

.markdown-body :deep(li > ul),
.markdown-body :deep(li > ol) {
  margin-top: 0;
  margin-bottom: 0;
}

.markdown-body :deep(hr) {
  height: 0.25em;
  padding: 0;
  margin: 24px 0;
  background-color: #d0d7de;
  border: 0;
}

.markdown-body :deep(table) {
  border-spacing: 0;
  border-collapse: collapse;
  margin-bottom: 16px;
  width: 100%;
  overflow: auto;
  display: block;
}

.markdown-body :deep(table th) {
  font-weight: 600;
  padding: 6px 13px;
  border: 1px solid #d0d7de;
  background-color: #f6f8fa;
}

.markdown-body :deep(table td) {
  padding: 6px 13px;
  border: 1px solid #d0d7de;
}

.markdown-body :deep(table tr:nth-child(2n)) {
  background-color: #f6f8fa;
}

.markdown-body :deep(img) {
  max-width: 100%;
  box-sizing: content-box;
  background-color: #ffffff;
  border-radius: 6px;
}

.markdown-body :deep(.highlight) {
  margin-bottom: 16px;
}

.markdown-body :deep(.highlight pre) {
  margin-bottom: 0;
  word-break: normal;
}

/* 数学公式样式 */
.markdown-body :deep(.math) {
  display: block;
  text-align: center;
  margin: 1em 0;
  font-family: 'Times New Roman', serif;
  font-style: italic;
}

.markdown-body :deep(.math-inline) {
  font-family: 'Times New Roman', serif;
  font-style: italic;
}

@media (max-width: 768px) {
  .markdown-body {
    padding: 15px;
    font-size: 14px;
  }
  
  .markdown-body :deep(h1) {
    font-size: 1.5em;
  }
  
  .markdown-body :deep(h2) {
    font-size: 1.25em;
  }
  
  .markdown-body :deep(h3) {
    font-size: 1.1em;
  }
  
  .markdown-body :deep(pre) {
    padding: 12px;
  }
}
</style>
