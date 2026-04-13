# VitePress 使用说明

> **一句话解释**：VitePress 是一个把 Markdown 文档自动变成漂亮网站的工具
> 
> **更新时间**：2026-04-13

---

## 📋 目录

- [什么是 VitePress](#什么是-vitepress)
- [为什么使用 VitePress](#为什么使用-vitepress)
- [快速上手](#快速上手)
- [工作原理](#工作原理)
- [核心配置](#核心配置)
- [常用操作](#常用操作)
- [进阶功能](#进阶功能)
- [常见问题](#常见问题)

---

## 什么是 VitePress

### 简单理解

```
你写 Markdown 文件
        ↓
  VitePress 自动处理
        ↓
  得到漂亮的网站
```

**VitePress** = **Vite**（超快构建工具）+ **Press**（出版/发布）

### 类比理解

| 传统方式 | VitePress 方式 |
|---------|---------------|
| 手写 HTML 代码（复杂） | 写 Markdown 文档（简单）|
| 手动创建导航栏 | 自动生成导航 |
| 手动设计样式 | 自动美化样式 |
| 没有搜索功能 | 自带全文搜索 |
| 修改后需刷新 | 自动热更新 |

**结论**：用 VitePress 写文档，就像用 Word 而不是用记事本写文章 —— 简单、美观、高效。

---

## 为什么使用 VitePress

### 我们的项目需求

1. **大量文档内容**
   - 10章分析模板
   - 15+ 个股分析报告
   - 决策记录、持仓管理
   - 使用指南、技术文档

2. **需要结构化展示**
   - 清晰的导航栏
   - 自动的侧边栏
   - 页内目录
   - 搜索功能

3. **需要动态交互**
   - 模拟持仓仪表盘
   - 数据可视化
   - 实时更新

### VitePress 的优势

| 需求 | VitePress 解决方案 |
|------|-------------------|
| 写文档 | 用 Markdown（比 HTML 简单 10 倍）|
| 导航栏 | 配置文件自动生成 |
| 侧边栏 | 根据文件结构自动生成 |
| 样式美化 | 自带漂亮主题 |
| 搜索功能 | 内置全文搜索 |
| 动态内容 | 可嵌入 Vue 组件 |
| 开发体验 | 修改后 < 1秒 看到效果 |
| 部署 | 一键生成静态网站 |

---

## 快速上手

### 第一步：启动开发服务器

```bash
# 在项目根目录
npm run docs:dev
```

**结果**：
- 终端显示：`Local: http://localhost:5173/`
- 浏览器打开这个地址
- 看到完整的网站！

### 第二步：修改内容

**打开任意 Markdown 文件，比如**：
```bash
# 用编辑器打开
open README.md
```

**修改内容**：
```markdown
# 投资分析模板

这是修改后的内容
```

**保存文件**，浏览器**自动刷新**，立即看到效果！

### 第三步：添加新页面

**创建新文件**：
```bash
# 创建新的 Markdown 文件
touch 我的新页面.md
```

**编辑内容**：
```markdown
# 我的新页面

这是新页面的内容

## 第一节
...
```

**保存后**，访问 `http://localhost:5173/我的新页面` 就能看到！

### 第四步：构建生产版本

```bash
# 构建静态网站
npm run docs:build

# 生成的文件在 .vitepress/dist/
```

---

## 工作原理

### 完整流程图

```
┌─────────────────────────────────────────────────┐
│  第1步：项目文件结构                              │
│  ──────────────────────────────                │
│  index.md                  ← 首页               │
│  README.md                 ← 项目介绍            │
│  个股分析标准模版.md        ← 分析框架            │
│  template/                                      │
│    ├── 01-数据核查.md      ← 模板章节            │
│    ├── 02-央国企筛选.md                          │
│    └── ...                                      │
│  07-分析输出/                                    │
│    ├── 保利物业_06049.md   ← 分析报告            │
│    └── ...                                      │
│  模拟持仓/                                       │
│    ├── 持仓.md             ← 带Vue组件的页面      │
│    └── ...                                      │
└─────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────┐
│  第2步：VitePress 读取配置                        │
│  ──────────────────────────────                │
│  .vitepress/config.mjs                          │
│    - 网站标题：投资分析模板                        │
│    - 导航栏：首页、模拟持仓、分析模板、版本日志      │
│    - 侧边栏：根据文件自动生成                       │
│    - 主题配置：搜索、页脚、样式等                   │
└─────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────┐
│  第3步：Markdown 转换                             │
│  ──────────────────────────────                │
│  # 标题          →  <h1>标题</h1>               │
│  **粗体**        →  <strong>粗体</strong>       │
│  - 列表          →  <ul><li>列表</li></ul>      │
│  [链接](url)     →  <a href="url">链接</a>      │
│  ```code```      →  <pre><code>...</code></pre> │
│  | 表格 |        →  <table>...</table>          │
└─────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────┐
│  第4步：Vite 开发服务器                           │
│  ──────────────────────────────                │
│  - 启动：http://localhost:5173                  │
│  - 热更新：修改文件 < 1秒看到效果                  │
│  - 自动刷新：无需手动刷新浏览器                     │
└─────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────┐
│  第5步：浏览器显示                                │
│  ──────────────────────────────                │
│  ✅ 漂亮的网站界面                                │
│  ✅ 顶部导航栏（首页、模拟持仓...）                 │
│  ✅ 左侧边栏（文档目录）                           │
│  ✅ 右侧目录（页面大纲）                           │
│  ✅ 搜索框（全文搜索）                             │
│  ✅ 美化的表格、代码块、引用                        │
│  ✅ 交互式 Vue 组件（仪表盘）                      │
└─────────────────────────────────────────────────┘
```

### Vite 的作用

**Vite** 是一个超快的前端构建工具：

1. **开发服务器**
   - 启动速度极快（< 1秒）
   - 热模块替换（HMR）：修改立即生效
   - 按需加载：只加载当前需要的内容

2. **模块处理**
   - 自动处理 ES Module 导入
   - 编译 Vue 组件
   - 处理 CSS/图片等资源

3. **生产构建**
   - 代码压缩（HTML/CSS/JS）
   - Tree-shaking（移除未使用代码）
   - 代码分割（按需加载）
   - 优化性能

---

## 核心配置

### 1. `.vitepress/config.mjs` - 主配置文件

这是 VitePress 的"中央控制台"：

```javascript
import { defineConfig } from 'vitepress'

export default defineConfig({
  // 网站基本信息
  title: '投资分析模板',
  description: '港股/A股个股投资分析框架',
  lang: 'zh-CN',
  
  // 主题配置
  themeConfig: {
    // 顶部导航栏
    nav: [
      { text: '首页', link: '/' },
      { text: '🎯 模拟持仓', link: '/模拟持仓/持仓' },
      { text: '分析模板', link: '/个股分析标准模版' }
    ],
    
    // 左侧边栏
    sidebar: {
      '/': [
        {
          text: '📋 分析模板',
          items: [
            { text: '01-数据核查', link: '/template/01-数据核查...' },
            { text: '02-央国企筛选', link: '/template/02-央国企...' }
          ]
        }
      ]
    },
    
    // 搜索功能
    search: {
      provider: 'local'
    }
  }
})
```

### 2. `.vitepress/theme/index.js` - 主题扩展

用于注册自定义 Vue 组件：

```javascript
import DefaultTheme from 'vitepress/theme'
import DecisionDashboard from './DecisionDashboard.vue'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    // 注册全局组件
    app.component('DecisionDashboard', DecisionDashboard)
  }
}
```

### 3. 目录结构

```
investTemplate/
├── .vitepress/              # VitePress 配置目录
│   ├── config.mjs          # 网站配置
│   ├── theme/              # 自定义主题
│   │   ├── index.js        # 主题入口
│   │   ├── DecisionDashboard.vue  # 自定义组件
│   │   └── custom.css      # 自定义样式
│   └── dist/               # 构建输出目录（自动生成）
│
├── index.md                # 首页（特殊：使用 home 布局）
├── README.md               # 项目介绍
├── 个股分析标准模版.md      # 普通页面
│
├── template/               # 模板目录
│   ├── 01-数据核查.md
│   └── ...
│
├── 07-分析输出/            # 分析报告目录
│   ├── index.md           # 目录索引
│   └── 保利物业_06049.md
│
└── 模拟持仓/               # 持仓管理目录
    ├── 持仓.md            # 可嵌入 Vue 组件
    └── ...
```

---

## 常用操作

### 操作1：修改导航栏

**需求**：在顶部导航添加"使用指南"链接

**步骤**：

1. 编辑 `.vitepress/config.mjs`
2. 找到 `nav` 配置
3. 添加新项

```javascript
nav: [
  { text: '首页', link: '/' },
  { text: '🎯 模拟持仓', link: '/模拟持仓/持仓' },
  { text: '📘 使用指南', link: '/USAGE' },  // ← 新增
  { text: '分析模板', link: '/个股分析标准模版' }
]
```

4. 保存，浏览器自动刷新，导航栏立即更新！

### 操作2：添加新的分析报告

**需求**：添加"工商银行"分析报告

**步骤**：

1. 创建文件：`07-分析输出/工商银行_01398_投资分析报告.md`

```markdown
# 工商银行 (01398.HK) 投资分析报告

**一句话结论**：🐢🍊 极品金龟，PB 0.4倍，股息率8%

## 第一章：数据核查
...
```

2. 更新侧边栏配置：`.vitepress/config.mjs`

```javascript
sidebar: {
  '/': [
    {
      text: '📈 个股分析报告',
      items: [
        { text: '保利物业_06049', link: '/07-分析输出/保利物业_06049...' },
        { text: '工商银行_01398', link: '/07-分析输出/工商银行_01398...' }, // ← 新增
        // ...
      ]
    }
  ]
}
```

3. 保存，侧边栏立即显示新报告！

### 操作3：在页面中嵌入 Vue 组件

**需求**：在"模拟持仓"页面显示交互式仪表盘

**步骤**：

1. 确保组件已注册（`.vitepress/theme/index.js`）

```javascript
app.component('DecisionDashboard', DecisionDashboard)
```

2. 在 Markdown 中使用

```markdown
# 模拟持仓

<DecisionDashboard />
```

3. 保存，页面立即显示交互式仪表盘！

### 操作4：修改网站标题和描述

**编辑** `.vitepress/config.mjs`：

```javascript
export default defineConfig({
  title: '我的投资分析系统',        // ← 浏览器标签标题
  description: '个人价值投资分析工具',  // ← SEO 描述
  // ...
})
```

### 操作5：添加首页特色卡片

**编辑** `index.md`：

```markdown
---
layout: home

features:
  - icon: 🎯
    title: 四流派投资体系
    details: 纯硬收息 / 价值发现 / 烟蒂股 / 关联方资源型
  
  - icon: 📋
    title: 我的新功能           # ← 新增卡片
    details: 这是新功能的描述
---
```

---

## 进阶功能

### 1. Markdown 增强语法

VitePress 支持扩展的 Markdown 语法：

#### 容器（提示框）

```markdown
::: tip 提示
这是一个提示
:::

::: warning 警告
这是一个警告
:::

::: danger 危险
这是一个危险提示
:::

::: details 点击展开
这是隐藏的内容
:::
```

#### 代码块高亮

```markdown
```javascript{2,4-6}
export default {
  data() {  // ← 第2行高亮
    return {
      msg: 'Hello'  // ← 第4-6行高亮
    }
  }
}
\`\`\`
```

#### 自定义容器

```markdown
::: info 数据来源
数据来源：2023年年报（S级数据源）
:::
```

### 2. 使用 Vue 组件的特性

在 Markdown 中可以使用 Vue 语法：

```markdown
# 动态内容

今天是：{{ new Date().toLocaleDateString() }}

<button @click="count++">点击次数：{{ count }}</button>

<script setup>
import { ref } from 'vue'
const count = ref(0)
</script>
```

### 3. 导入其他文件内容

```markdown
# 包含其他文件

<!--@include: ./snippet.md-->
```

### 4. 数学公式（需要插件）

```markdown
行内公式：$E = mc^2$

块级公式：
$$
\frac{FCF}{市值} < 3
$$
```

### 5. 自定义样式

创建 `.vitepress/theme/custom.css`：

```css
/* 自定义表格样式 */
table {
  border-collapse: collapse;
  width: 100%;
}

/* 自定义标题颜色 */
h1 {
  color: #2c3e50;
}

/* 自定义代码块背景 */
code {
  background-color: #f3f4f6;
}
```

在 `.vitepress/theme/index.js` 导入：

```javascript
import './custom.css'
```

---

## 常见问题

### Q1: 修改配置后没有生效？

**原因**：某些配置需要重启开发服务器

**解决**：
```bash
# 停止服务器（Ctrl + C）
# 重新启动
npm run docs:dev
```

### Q2: 页面显示 404？

**可能原因**：
1. 文件路径不对
2. 链接地址错误
3. 文件名包含特殊字符

**解决**：
- 检查文件是否存在
- 确认链接地址与文件路径一致
- 避免使用空格，用 `-` 或 `_` 代替

### Q3: 侧边栏没有显示新页面？

**原因**：侧边栏需要在 `config.mjs` 中手动配置

**解决**：
在 `.vitepress/config.mjs` 的 `sidebar` 中添加：

```javascript
sidebar: {
  '/': [
    {
      text: '我的分类',
      items: [
        { text: '新页面', link: '/my-new-page' }  // ← 添加
      ]
    }
  ]
}
```

### Q4: Vue 组件不显示？

**检查清单**：
- [ ] 组件已在 `.vitepress/theme/index.js` 注册
- [ ] Markdown 中使用了正确的组件名
- [ ] 组件语法正确（首字母大写）
- [ ] 浏览器控制台没有错误

### Q5: 构建失败？

**常见错误**：

1. **死链接错误**
```
Error: [vitepress] Dead link found.
```

**解决**：在 `config.mjs` 添加：
```javascript
ignoreDeadLinks: true
```

2. **Vue 组件错误**
```
Error: Cannot find module './component.vue'
```

**解决**：检查组件路径是否正确

### Q6: 本地能看到，部署后样式丢失？

**原因**：可能是 base 路径配置问题

**解决**：
```javascript
// .vitepress/config.mjs
export default defineConfig({
  base: '/your-repo-name/',  // GitHub Pages 需要设置
  // ...
})
```

### Q7: 如何优化加载速度？

**建议**：
1. 图片压缩
2. 减少页面大小（拆分长文档）
3. 使用代码分割
4. 懒加载组件

```javascript
// 动态导入组件
const DecisionDashboard = () => import('./DecisionDashboard.vue')
```

---

## 实用技巧

### 技巧1：快速生成侧边栏

使用脚本自动扫描文件生成侧边栏配置：

```javascript
// scripts/generate-sidebar.js
import fs from 'fs'
import path from 'path'

function generateSidebar(dir) {
  const files = fs.readdirSync(dir)
  return files
    .filter(f => f.endsWith('.md'))
    .map(f => ({
      text: f.replace('.md', ''),
      link: `/${dir}/${f.replace('.md', '')}`
    }))
}

console.log(JSON.stringify(generateSidebar('07-分析输出'), null, 2))
```

### 技巧2：使用环境变量

```javascript
// .vitepress/config.mjs
export default defineConfig({
  title: process.env.SITE_TITLE || '投资分析模板',
  // ...
})
```

### 技巧3：添加阅读时长估算

在 frontmatter 中添加：

```markdown
---
title: 保利物业分析报告
readingTime: 15分钟
---

# 保利物业 (06049.HK)
```

### 技巧4：自动生成目录索引

创建 `07-分析输出/index.md`：

```markdown
# 分析报告列表

<script setup>
import { data as reports } from './reports.data.js'
</script>

<div v-for="report in reports" :key="report.path">
  <a :href="report.path">{{ report.title }}</a>
</div>
```

---

## 部署

### 部署到 Vercel（推荐）

1. 构建网站
```bash
npm run docs:build
```

2. 创建 `vercel.json`
```json
{
  "buildCommand": "npm run docs:build",
  "outputDirectory": ".vitepress/dist"
}
```

3. 推送到 GitHub，连接 Vercel

### 部署到 GitHub Pages

1. 修改 `config.mjs`
```javascript
base: '/your-repo-name/'
```

2. 创建 `.github/workflows/deploy.yml`
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm install
      - run: npm run docs:build
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: .vitepress/dist
```

---

## 学习资源

- **VitePress 官方文档**：https://vitepress.dev/
- **Vite 官方文档**：https://vitejs.dev/
- **Markdown 语法**：https://markdown.com.cn/
- **Vue 3 文档**：https://cn.vuejs.org/

---

## 总结

### VitePress 的核心价值

```
写 Markdown（专注内容）
        ↓
  VitePress 自动处理（零配置）
        ↓
  得到专业网站（立即可用）
```

### 三句话总结

1. **简单**：只需会写 Markdown，无需学 HTML/CSS
2. **强大**：自动生成导航、搜索、美化样式
3. **灵活**：可嵌入 Vue 组件，实现复杂交互

### 下一步

- ✅ 启动开发服务器：`npm run docs:dev`
- ✅ 修改一个 Markdown 文件，看看效果
- ✅ 添加一个新页面
- ✅ 自定义导航和侧边栏

**记住**：VitePress 让你专注内容创作，技术细节它来搞定！

---

*最后更新：2026-04-13*
