# VitePress 工作原理详解

> **核心问题**：
> 1. `<DecisionDashboard mode="today" />` 怎么知道用哪个文件？
> 2. `npm run docs:dev` 启动后，`http://localhost:5173/` 怎么展示页面？

---

## 问题 1：组件是如何找到的？

### 完整流程图

```
模拟持仓/今日操作.md
    ↓ 写了
<DecisionDashboard mode="today" />
    ↓ 但是怎么知道这个组件在哪里？
    ↓
.vitepress/theme/index.js
    ↓ 在这里注册了！
import DecisionDashboard from './DecisionDashboard.vue'
app.component('DecisionDashboard', DecisionDashboard)
    ↓
DecisionDashboard 变成全局组件
    ↓
所有 Markdown 文件都可以用 <DecisionDashboard />
```

---

## 详细步骤拆解

### 第 1 步：注册组件（`.vitepress/theme/index.js`）

```javascript
// .vitepress/theme/index.js
import DefaultTheme from 'vitepress/theme'
import './custom.css'
import DecisionDashboard from './DecisionDashboard.vue'  // ← 第3行：导入组件

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    // 第8行：注册为全局组件
    // 第一个参数 'DecisionDashboard' 是组件名称
    // 第二个参数是组件对象
    app.component('DecisionDashboard', DecisionDashboard)
  }
}
```

**关键代码解读**：

```javascript
app.component('DecisionDashboard', DecisionDashboard)
           ↑                      ↑
      在 Markdown 中             从这个文件导入
      使用的名称                 ./DecisionDashboard.vue
```

这行代码做了什么？

```
1. 从 ./DecisionDashboard.vue 导入组件
2. 注册为 Vue 全局组件，名称是 'DecisionDashboard'
3. 之后任何 Markdown 文件都可以用 <DecisionDashboard />
```

### 第 2 步：在 Markdown 中使用（`模拟持仓/今日操作.md`）

```markdown
# 今日操作

<DecisionDashboard mode="today" />
```

**为什么可以直接用？**

因为在 `.vitepress/theme/index.js` 中已经注册为**全局组件**：

```javascript
app.component('DecisionDashboard', DecisionDashboard)
```

### 第 3 步：VitePress 处理 Markdown

```
VitePress 读取 Markdown
    ↓
发现 <DecisionDashboard mode="today" />
    ↓
查找全局组件 'DecisionDashboard'
    ↓
找到了！（在 theme/index.js 注册过）
    ↓
加载 .vitepress/theme/DecisionDashboard.vue
    ↓
渲染组件
```

---

## 类比理解

### 类比 1：餐厅菜单

```
.vitepress/theme/index.js  = 餐厅菜单
    ↓
app.component('DecisionDashboard', ...)  = 添加"宫保鸡丁"到菜单

模拟持仓/今日操作.md  = 顾客点菜
    ↓
<DecisionDashboard />  = 点了"宫保鸡丁"
    ↓
厨房（VitePress）查菜单，找到"宫保鸡丁"
    ↓
从厨房（DecisionDashboard.vue）做菜（渲染组件）
```

### 类比 2：导入联系人

```
手机通讯录（theme/index.js）
    ↓
添加联系人：
  名字: "张三"
  实际人: 13800138000

短信（Markdown）
    ↓
发给 "张三"
    ↓
手机自动找到 "张三" = 13800138000
    ↓
发送短信
```

---

## 问题 2：URL 路由是怎么工作的？

### VitePress 路由机制

#### 核心规则：文件路径 = URL 路径

```
文件路径                          →  URL 路径
────────────────────────────────────────────────────
index.md                         →  /
README.md                        →  /README
个股分析标准模版.md                 →  /个股分析标准模版
模拟持仓/持仓.md                   →  /模拟持仓/持仓
模拟持仓/今日操作.md                →  /模拟持仓/今日操作
template/01-数据核查.md           →  /template/01-数据核查
07-分析输出/保利物业_06049.md     →  /07-分析输出/保利物业_06049
```

### 完整流程图

```
┌─────────────────────────────────────────────────┐
│  第1步：启动开发服务器                            │
│  ────────────────────────────                   │
│  $ npm run docs:dev                             │
│  ↓                                              │
│  VitePress 启动 Vite 开发服务器                  │
│  ↓                                              │
│  监听 http://localhost:5173                     │
└─────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────┐
│  第2步：扫描项目文件                              │
│  ────────────────────────────                   │
│  VitePress 扫描项目根目录所有 .md 文件            │
│  ↓                                              │
│  index.md                                       │
│  README.md                                      │
│  个股分析标准模版.md                              │
│  模拟持仓/持仓.md                                 │
│  模拟持仓/今日操作.md                             │
│  ...                                            │
│  ↓                                              │
│  自动生成路由映射表                               │
└─────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────┐
│  第3步：浏览器访问 URL                            │
│  ────────────────────────────                   │
│  用户访问: http://localhost:5173/模拟持仓/今日操作 │
│  ↓                                              │
│  VitePress 查找路由映射表                        │
│  ↓                                              │
│  /模拟持仓/今日操作 → 模拟持仓/今日操作.md         │
└─────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────┐
│  第4步：处理 Markdown                            │
│  ────────────────────────────                   │
│  读取 模拟持仓/今日操作.md                        │
│  ↓                                              │
│  内容:                                           │
│  # 今日操作                                      │
│  <DecisionDashboard mode="today" />             │
│  ↓                                              │
│  转换为 HTML + Vue 组件                          │
└─────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────┐
│  第5步：渲染页面                                  │
│  ────────────────────────────                   │
│  应用主题 (.vitepress/theme/index.js)           │
│  ↓                                              │
│  加载全局组件 (DecisionDashboard)                │
│  ↓                                              │
│  渲染 Vue 组件                                   │
│  ↓                                              │
│  返回完整 HTML 给浏览器                          │
└─────────────────────────────────────────────────┘
```

---

## 实际例子演示

### 例子 1：访问首页

**你在浏览器输入**：
```
http://localhost:5173/
```

**VitePress 处理流程**：

```javascript
// 1. 匹配 URL
URL: /
    ↓
// 2. 查找文件
查找根目录的 index.md
    ↓
// 3. 读取内容
---
layout: home

hero:
  name: 投资分析模板
  text: 系统化价值投资框架
---
    ↓
// 4. 应用 home 布局
使用特殊的首页布局
    ↓
// 5. 渲染
显示漂亮的首页
```

### 例子 2：访问"今日操作"

**你点击导航栏的"今日操作"**：
```
http://localhost:5173/模拟持仓/今日操作
```

**VitePress 处理流程**：

```javascript
// 1. 匹配 URL
URL: /模拟持仓/今日操作
    ↓
// 2. 查找文件
查找 模拟持仓/今日操作.md
    ↓
// 3. 读取内容
# 今日操作

<DecisionDashboard mode="today" />
    ↓
// 4. 解析 Markdown
标题: <h1>今日操作</h1>
组件: <DecisionDashboard mode="today" />
    ↓
// 5. 查找组件
在全局组件中找到 'DecisionDashboard'
    ↓
// 6. 加载组件文件
.vitepress/theme/DecisionDashboard.vue
    ↓
// 7. 渲染 Vue 组件
传入 props: { mode: 'today' }
    ↓
// 8. 返回完整页面
HTML + 侧边栏 + 导航栏 + 组件
```

### 例子 3：导航配置的作用

**在 `.vitepress/config.mjs` 中**：

```javascript
nav: [
  { text: '🎯 模拟持仓', link: '/模拟持仓/持仓' },
]
```

**这行配置的作用**：

```
1. 在顶部导航栏显示 "🎯 模拟持仓" 链接
2. 点击后跳转到 /模拟持仓/持仓
3. VitePress 查找 模拟持仓/持仓.md
4. 渲染该文件
```

**注意**：`link` 的值**必须对应实际的文件路径**（去掉 `.md`）

---

## 关键文件的作用

### 1. `.vitepress/theme/index.js` - 主题入口

```javascript
import DefaultTheme from 'vitepress/theme'
import './custom.css'
import DecisionDashboard from './DecisionDashboard.vue'

export default {
  extends: DefaultTheme,              // 继承默认主题
  enhanceApp({ app }) {               // 增强 Vue 应用
    app.component('DecisionDashboard', DecisionDashboard)  // 注册全局组件
  }
}
```

**作用**：
- 定义网站的主题
- 注册全局组件
- 加载自定义样式

### 2. `.vitepress/config.mjs` - 网站配置

```javascript
export default defineConfig({
  title: '投资分析模板',           // 网站标题
  
  themeConfig: {
    nav: [ ... ],                  // 导航栏配置
    sidebar: { ... },              // 侧边栏配置
  }
})
```

**作用**：
- 配置网站标题、描述
- 配置导航栏
- 配置侧边栏
- 配置搜索、页脚等

### 3. Markdown 文件 - 页面内容

```markdown
# 今日操作

<DecisionDashboard mode="today" />
```

**作用**：
- 定义页面内容
- 可以使用全局注册的 Vue 组件

---

## 完整的数据流

### 启动时

```
npm run docs:dev
    ↓
启动 Vite 开发服务器
    ↓
加载 .vitepress/config.mjs (网站配置)
    ↓
加载 .vitepress/theme/index.js (主题配置)
    ↓
注册全局组件 (DecisionDashboard)
    ↓
扫描所有 .md 文件，生成路由
    ↓
监听 http://localhost:5173
```

### 访问页面时

```
浏览器请求 /模拟持仓/今日操作
    ↓
查找路由表
    ↓
找到 模拟持仓/今日操作.md
    ↓
读取文件内容
    ↓
解析 Markdown
    ↓
发现 <DecisionDashboard mode="today" />
    ↓
查找全局组件 'DecisionDashboard'
    ↓
加载 .vitepress/theme/DecisionDashboard.vue
    ↓
渲染 Vue 组件（传入 props: { mode: 'today' }）
    ↓
组件内部执行：
  - loadData() 加载 JSON 数据
  - showToday = true（因为 mode === 'today'）
  - 渲染今日操作表格
    ↓
返回完整 HTML
    ↓
浏览器显示页面
```

---

## 常见问题

### Q1: 为什么必须在 `theme/index.js` 注册组件？

**答**：如果不注册，Markdown 中无法使用该组件。

```markdown
<!-- ❌ 如果没有注册 -->
<DecisionDashboard mode="today" />
<!-- 错误: Component DecisionDashboard not found -->

<!-- ✅ 注册后才能用 -->
<DecisionDashboard mode="today" />
```

### Q2: 可以只在某个页面导入组件吗？

**答**：可以！使用 `<script setup>`

```markdown
# 今日操作

<script setup>
import DecisionDashboard from '../.vitepress/theme/DecisionDashboard.vue'
</script>

<DecisionDashboard mode="today" />
```

**但不推荐**：
- 每个页面都要重复导入
- 路径容易写错
- 不如全局注册方便

### Q3: 为什么 URL 是 `/模拟持仓/今日操作` 而不是 `/模拟持仓/今日操作.md`？

**答**：VitePress 自动去掉 `.md` 后缀，让 URL 更美观。

```
文件: 模拟持仓/今日操作.md
URL:  /模拟持仓/今日操作  ← 自动去掉 .md
```

### Q4: 如果文件路径和 URL 不匹配会怎样？

**答**：404 错误！

```javascript
// config.mjs
nav: [
  { text: '今日操作', link: '/模拟持仓/今天操作' }  // ← 文件名是"今日操作"
]

// 点击后 → 404 Not Found
// 因为找不到 模拟持仓/今天操作.md
```

### Q5: 可以改变路由规则吗？

**答**：不能。VitePress 的路由是固定的：

```
文件路径 = URL 路径（去掉 .md）
```

如果需要自定义路由，考虑用 Nuxt.js 或 Next.js。

---

## 调试技巧

### 技巧 1：查看路由映射

打开浏览器控制台：

```javascript
// 查看当前路由
console.log(location.pathname)
// 输出: /模拟持仓/今日操作

// 查看对应的文件
// VitePress 会去找 模拟持仓/今日操作.md
```

### 技巧 2：检查组件是否注册

```javascript
// 在浏览器控制台
console.log(app._context.components)
// 应该能看到 'DecisionDashboard'
```

### 技巧 3：查看文件是否存在

```bash
# 在终端
ls 模拟持仓/今日操作.md
# 如果文件存在，输出文件名
# 如果不存在，输出 "No such file"
```

---

## 对比：VitePress vs 传统网站

### 传统网站（需要手动配置路由）

```javascript
// router.js (需要手动写)
const routes = [
  { path: '/', component: Home },
  { path: '/about', component: About },
  { path: '/contact', component: Contact },
  // 每个页面都要手动添加！
]
```

### VitePress（自动生成路由）

```
index.md          → 自动生成路由 /
about.md          → 自动生成路由 /about
contact.md        → 自动生成路由 /contact
模拟持仓/持仓.md    → 自动生成路由 /模拟持仓/持仓

🎉 无需手动配置路由！
```

---

## 总结

### 核心原理

1. **组件注册**：
   ```javascript
   .vitepress/theme/index.js 中
   app.component('DecisionDashboard', DecisionDashboard)
   ```
   这使得所有 Markdown 都能用 `<DecisionDashboard />`

2. **路由映射**：
   ```
   文件路径 = URL 路径
   模拟持仓/今日操作.md → /模拟持仓/今日操作
   ```
   VitePress 自动扫描 `.md` 文件生成路由

### 记忆口诀

```
theme/index.js - 注册组件全局用
config.mjs     - 配置导航和侧边
Markdown文件   - 写内容就能自动路由
```

### 工作流程一句话

```
写 Markdown → VitePress 自动生成路由 → 找到对应文件 → 
解析内容 → 渲染组件 → 展示页面
```

你现在明白了吗？
- `<DecisionDashboard />` 能用，是因为在 `theme/index.js` 注册了
- URL 对应页面，是因为 VitePress 自动将文件路径映射为 URL

---

*最后更新：2026-04-13*
