# VitePress Frontmatter 和主题配置详解

> **核心问题**：`layout: home`、`hero`、`name` 这些配置是怎么知道要配置的？

---

## 📋 目录

- [什么是 Frontmatter](#什么是-frontmatter)
- [VitePress 默认主题](#vitepress-默认主题)
- [Home 布局配置](#home-布局配置)
- [其他布局类型](#其他布局类型)
- [完整配置示例](#完整配置示例)
- [官方学习资源](#官方学习资源)

---

## 什么是 Frontmatter

### 简单解释

**Frontmatter** 是 Markdown 文件顶部用 `---` 包裹的 **YAML 格式配置**：

```markdown
---
这里是 Frontmatter 配置区域
可以配置页面的特殊行为
---

下面是正常的 Markdown 内容
# 标题
正文...
```

### 实际例子

```markdown
---
layout: home          ← Frontmatter 配置
title: 我的网站
description: 描述
---

# 欢迎来到我的网站  ← Markdown 内容
```

---

## VitePress 默认主题

### 默认主题提供的功能

VitePress 自带一个**默认主题** (`vitepress/theme`)，它预定义了：

1. **布局类型**
   - `home` - 首页布局（漂亮的大标题、按钮、特色卡片）
   - `doc` - 文档布局（普通页面，默认）
   - `page` - 页面布局（无侧边栏）

2. **首页特殊配置**
   - `hero` - 英雄区（大标题区域）
   - `features` - 特色功能卡片

3. **其他配置**
   - `title` - 页面标题
   - `sidebar` - 是否显示侧边栏
   - `navbar` - 是否显示导航栏
   - 等等...

---

## Home 布局配置

### 完整结构解析

让我们逐行解析你的 `index.md`：

```yaml
---
layout: home          # ← 第2行：使用 home 布局

hero:                 # ← 第4行：英雄区配置（大标题区域）
  name: 投资分析模板    # 主标题
  text: 系统化价值投资框架  # 副标题
  tagline: 港股/A股...  # 标语（更小的文字）
  image:              # 图片配置
    src: /logo.svg    # 图片路径
    alt: 投资分析模板   # 图片描述
  actions:            # 按钮配置
    - theme: brand    # 按钮主题（蓝色）
      text: 🚀 开始使用  # 按钮文字
      link: /个股分析标准模版  # 跳转链接
    - theme: alt      # 按钮主题（灰色）
      text: 📊 估值模型
      link: /template/06-估值与安全边际

features:             # 特色功能卡片
  - icon: 🎯          # 图标
    title: 四流派投资体系  # 卡片标题
    details: 纯硬收息...  # 卡片描述
  - icon: 📋
    title: 标准化分析模板
    details: V5.5.10...
---
```

### 这些配置是哪来的？

**答案**：来自 VitePress 默认主题的源码！

```
VitePress 源码
    ↓
vitepress/theme-default
    ↓
定义了 home 布局的配置项
    ↓
我们在 Frontmatter 中使用这些配置
```

---

## 配置项详解

### 1. `layout` - 页面布局

```yaml
---
layout: home    # 首页布局
# 或
layout: doc     # 文档布局（默认，可省略）
# 或
layout: page    # 页面布局（无侧边栏）
---
```

**效果对比**：

| 布局 | 特点 | 适用场景 |
|------|------|----------|
| `home` | 大标题、按钮、卡片 | 网站首页 |
| `doc` | 侧边栏、目录 | 文档页面（默认）|
| `page` | 无侧边栏 | 独立页面 |

### 2. `hero` - 英雄区（首页大标题）

```yaml
hero:
  name: 主标题          # 大号文字
  text: 副标题          # 中号文字
  tagline: 标语         # 小号文字
  image:               # 可选：右侧图片
    src: /logo.svg
    alt: Logo描述
  actions:             # 按钮组
    - theme: brand     # 主要按钮（蓝色）
      text: 按钮文字
      link: /path
    - theme: alt       # 次要按钮（灰色）
      text: 按钮文字
      link: /path
```

**渲染效果**：

```
┌────────────────────────────────────────┐
│                                        │
│         投资分析模板                    │  ← name（超大）
│      系统化价值投资框架                  │  ← text（大）
│  港股/A股个股研究的标准化方法论...       │  ← tagline（中）
│                                        │
│  [🚀 开始使用]  [📊 估值模型]            │  ← actions（按钮）
│                                        │
└────────────────────────────────────────┘
```

### 3. `features` - 特色功能卡片

```yaml
features:
  - icon: 🎯                    # Emoji 图标
    title: 四流派投资体系         # 卡片标题
    details: 纯硬收息/价值发现... # 卡片描述
  
  - icon: 📋
    title: 标准化分析模板
    details: V5.5.10版本...
  
  - icon: 🤖
    title: AI 辅助分析
    details: 人机协作提效
```

**渲染效果**：

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   🎯         │  │   📋         │  │   🤖         │
│ 四流派投资体系 │  │ 标准化分析模板 │  │ AI辅助分析    │
│ 纯硬收息/... │  │ V5.5.10...   │  │ 人机协作...   │
└──────────────┘  └──────────────┘  └──────────────┘
```

### 4. 其他常用配置

```yaml
---
# 页面元信息
title: 自定义标题              # 覆盖默认标题
titleTemplate: false          # 禁用标题模板

# SEO
description: 页面描述          # meta description
head:                         # 自定义 <head> 标签
  - - meta
    - name: keywords
      content: 投资,港股,A股

# 布局控制
navbar: false                 # 隐藏导航栏
sidebar: false                # 隐藏侧边栏
aside: false                  # 隐藏右侧目录
outline: [2, 3]               # 目录显示 h2-h3

# 页脚
editLink: false               # 隐藏"编辑此页"
lastUpdated: false            # 隐藏"最后更新时间"
prev: false                   # 隐藏"上一页"
next: false                   # 隐藏"下一页"
---
```

---

## 其他布局类型

### Doc 布局（默认）

```markdown
---
# 不写 layout，默认就是 doc 布局
title: 我的文档页
---

# 文档标题

这是普通的文档页面，会显示：
- 左侧边栏
- 右侧目录
- 导航栏
```

### Page 布局

```markdown
---
layout: page
title: 关于我们
---

# 关于我们

这是一个独立页面，不显示侧边栏。
适合"关于我们"、"联系方式"等页面。
```

---

## 完整配置示例

### 示例 1：首页（Home）

```markdown
---
layout: home

hero:
  name: 我的项目
  text: 让开发更简单
  tagline: 一个强大的工具集合
  image:
    src: /hero-image.png
    alt: Hero Image
  actions:
    - theme: brand
      text: 快速开始
      link: /guide/
    - theme: alt
      text: 在 GitHub 查看
      link: https://github.com/yourname/yourrepo

features:
  - icon: ⚡️
    title: 极速启动
    details: 基于 Vite，启动速度极快
  - icon: 🛠️
    title: 丰富功能
    details: 开箱即用的功能集
  - icon: 📦
    title: 优化构建
    details: 自动优化的生产构建
---
```

### 示例 2：普通文档页

```markdown
---
title: 快速开始
description: 5分钟上手指南
outline: [2, 3]
---

# 快速开始

## 安装

\`\`\`bash
npm install
\`\`\`

## 使用

\`\`\`javascript
import { something } from 'package'
\`\`\`
```

### 示例 3：独立页面

```markdown
---
layout: page
title: 关于我们
navbar: true
sidebar: false
---

# 关于我们

我们是一个致力于...
```

---

## 怎么知道有哪些配置？

### 方法 1：查看官方文档（推荐）

VitePress 官方文档详细列出了所有配置：

**🔗 官方文档**：https://vitepress.dev/

#### 关键文档页面

| 文档页面 | 内容 | 链接 |
|---------|------|------|
| **Frontmatter Config** | 所有 Frontmatter 配置 | https://vitepress.dev/reference/frontmatter-config |
| **Default Theme: Home Page** | Home 布局配置 | https://vitepress.dev/reference/default-theme-home-page |
| **Default Theme Config** | 默认主题配置 | https://vitepress.dev/reference/default-theme-config |
| **Markdown Extensions** | Markdown 扩展 | https://vitepress.dev/guide/markdown |

### 方法 2：查看源码

VitePress 是开源的，可以查看源码：

```bash
# 在你的项目中查看 VitePress 源码
node_modules/vitepress/types/default-theme.d.ts
```

### 方法 3：查看示例

VitePress 官网本身就是用 VitePress 构建的！

**官网源码**：https://github.com/vuejs/vitepress/tree/main/docs

---

## 官方学习资源

### 📚 VitePress 官方文档

**主页**：https://vitepress.dev/

**中文文档**：https://cn.vitepress.dev/

#### 推荐阅读顺序

1. **快速开始**
   - https://vitepress.dev/guide/getting-started
   - 5分钟了解 VitePress

2. **配置首页**
   - https://vitepress.dev/reference/default-theme-home-page
   - 了解 `hero` 和 `features` 配置

3. **Frontmatter 配置**
   - https://vitepress.dev/reference/frontmatter-config
   - 所有可用的页面配置

4. **Markdown 扩展**
   - https://vitepress.dev/guide/markdown
   - 提示框、代码块高亮等

5. **默认主题配置**
   - https://vitepress.dev/reference/default-theme-config
   - 导航栏、侧边栏等全局配置

### 📖 学习路径

```
第1天：快速开始
    ↓ 创建项目，启动开发服务器
第2天：配置首页
    ↓ 学习 hero 和 features
第3天：编写文档
    ↓ 学习 Markdown 扩展
第4天：自定义主题
    ↓ 学习主题配置和自定义组件
第5天：部署上线
    ↓ 构建静态网站并部署
```

### 🎓 实战教程

#### 教程 1：从零搭建文档网站

```bash
# 1. 创建项目
npm init
npm add -D vitepress

# 2. 初始化
npx vitepress init

# 3. 启动开发
npm run docs:dev

# 4. 修改 index.md
---
layout: home
hero:
  name: 我的项目
---

# 5. 访问 http://localhost:5173
```

#### 教程 2：自定义首页

**编辑 `index.md`**：

```markdown
---
layout: home

hero:
  name: VitePress
  text: Vite & Vue 驱动的静态网站生成器
  tagline: 简单、强大、高性能
  actions:
    - theme: brand
      text: 快速开始
      link: /guide/what-is-vitepress
    - theme: alt
      text: View on GitHub
      link: https://github.com/vuejs/vitepress

features:
  - title: "Vite: 新时代的前端构建工具"
    details: 享受 Vite 的开发体验，即时服务器启动，快如闪电的热模块替换 (HMR)。
  - title: 专为技术文档而设计
    details: 默认主题专为技术文档设计，提供了许多开箱即用的功能。
  - title: 用 Vue 增强你的内容
    details: 在 Markdown 中使用 Vue 组件，同时使用 Vue 来开发自定义主题。
---
```

---

## 配置速查表

### Home 布局完整配置

```yaml
---
layout: home

# 英雄区
hero:
  name: string              # 主标题
  text: string              # 副标题
  tagline: string           # 标语
  image:
    src: string             # 图片路径
    alt: string             # 图片描述
  actions:
    - theme: brand | alt    # 按钮主题
      text: string          # 按钮文字
      link: string          # 跳转链接

# 特色功能
features:
  - icon: string            # Emoji 或图片
    title: string           # 标题
    details: string         # 描述
    link: string            # 可选：点击跳转
    linkText: string        # 可选：链接文字
---
```

### 通用配置

```yaml
---
# 布局
layout: home | doc | page

# 元信息
title: string
description: string
head: Array

# 显示控制
navbar: boolean
sidebar: boolean
aside: boolean
outline: number | [number, number] | 'deep' | false

# 页脚控制
editLink: boolean
lastUpdated: boolean
prev: boolean | string | { text: string, link: string }
next: boolean | string | { text: string, link: string }
---
```

---

## 常见问题

### Q1: 为什么我的配置不生效？

**可能原因**：

1. **Frontmatter 格式错误**
   ```yaml
   # ❌ 错误：缩进不对
   hero:
   name: 标题
   
   # ✅ 正确：使用2空格缩进
   hero:
     name: 标题
   ```

2. **拼写错误**
   ```yaml
   # ❌ 错误
   heros:    # 应该是 hero
   
   # ✅ 正确
   hero:
   ```

3. **配置不存在**
   ```yaml
   # ❌ 错误：没有这个配置
   hero:
     myCustomField: xxx
   
   # ✅ 正确：使用文档中的配置
   hero:
     name: xxx
   ```

### Q2: 可以自定义配置项吗？

**答**：可以！在 Frontmatter 中添加自定义字段，然后在组件中读取。

```markdown
---
myCustomField: 123
---
```

在组件中：
```vue
<script setup>
import { useData } from 'vitepress'
const { frontmatter } = useData()
console.log(frontmatter.value.myCustomField)  // 123
</script>
```

### Q3: Home 布局必须用在 index.md 吗？

**答**：不是！任何 Markdown 文件都可以用 `layout: home`。

```markdown
<!-- about.md -->
---
layout: home
hero:
  name: 关于我们
---
```

访问 `/about` 也会显示首页布局。

---

## 实用技巧

### 技巧 1：多语言首页

```markdown
<!-- index.md (中文) -->
---
layout: home
hero:
  name: 投资分析模板
  text: 系统化价值投资框架
---

<!-- en/index.md (英文) -->
---
layout: home
hero:
  name: Investment Analysis Template
  text: Systematic Value Investment Framework
---
```

### 技巧 2：条件显示

```markdown
---
layout: home
hero:
  name: 我的项目
  actions:
    - theme: brand
      text: 开始
      link: /guide/
    # 根据环境显示不同按钮
---
```

### 技巧 3：图片优化

```yaml
hero:
  image:
    src: /hero.png
    alt: Hero Image
    # 可以使用相对路径或绝对URL
    # 放在 public/ 目录下的图片
```

---

## 总结

### 核心知识点

1. **Frontmatter** 是 Markdown 顶部的 YAML 配置
2. **VitePress 默认主题**提供了预定义的配置项
3. **`layout: home`** 启用首页布局
4. **`hero` 和 `features`** 是首页的核心配置

### 学习资源

| 资源 | 链接 |
|------|------|
| 官方文档 | https://vitepress.dev/ |
| 中文文档 | https://cn.vitepress.dev/ |
| GitHub | https://github.com/vuejs/vitepress |
| 示例 | https://github.com/vuejs/vitepress/tree/main/docs |

### 快速记忆

```yaml
---
layout: home          # 使用首页布局
hero:                # 大标题区域
  name: 主标题
  text: 副标题
  actions:           # 按钮
features:            # 功能卡片
  - icon: 🎯
    title: 标题
---
```

### 下一步

1. ✅ 阅读官方文档：https://vitepress.dev/reference/default-theme-home-page
2. ✅ 查看示例：https://github.com/vuejs/vitepress/blob/main/docs/index.md
3. ✅ 动手实践：修改你的 `index.md`，看看效果

---

*最后更新：2026-04-13*
