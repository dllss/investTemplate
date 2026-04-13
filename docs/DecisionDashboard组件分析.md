# DecisionDashboard 组件结构分析

> **组件文件**：`.vitepress/theme/DecisionDashboard.vue`
> 
> **功能**：投资组合模拟持仓仪表盘，展示持仓、操作、决策记录

---

## 📋 目录

- [组件概述](#组件概述)
- [架构设计](#架构设计)
- [数据流](#数据流)
- [页面模式](#页面模式)
- [核心功能模块](#核心功能模块)
- [样式设计](#样式设计)
- [数据结构](#数据结构)

---

## 组件概述

### 核心功能

这是一个**单页应用（SPA）风格**的 Vue 组件，通过 `mode` prop 切换不同视图：

```
DecisionDashboard
├── mode="home"       → 总览页（默认）
├── mode="positions"  → 持仓详情
├── mode="today"      → 今日操作
└── mode="decisions"  → AI决策记录
```

### 技术栈

- **Vue 3 Composition API** (`<script setup>`)
- **响应式数据** (`ref`, `computed`)
- **生命周期钩子** (`onMounted`, `onBeforeUnmount`)
- **VitePress 集成** (`withBase` 处理路径)

---

## 架构设计

### 整体结构

```
┌─────────────────────────────────────────┐
│  <script setup>  (第1-139行)            │
│  ────────────────────────────            │
│  1. Props 定义 (第5-10行)               │
│  2. 响应式状态 (第12-14行)              │
│  3. 计算属性 (第16-98行)                │
│  4. 工具函数 (第26-102行)               │
│  5. 数据加载 (第104-128行)              │
│  6. 生命周期 (第130-138行)              │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│  <template>  (第141-369行)              │
│  ────────────────────────────            │
│  1. 通用头部 (第142-147行)              │
│  2. 加载/错误状态 (第149-151行)         │
│  3. 元数据 (第152-155行)                │
│  4. 关键指标 KPIs (第157-179行)         │
│  5. 今日操作横幅 (第181-186行)          │
│  6. 子摘要 (第188-195行)                │
│  7. 四个页面模块 (第197-366行)          │
│     ├── home (总览)                      │
│     ├── positions (持仓)                 │
│     ├── today (今日操作)                 │
│     └── decisions (AI决策)               │
└─────────────────────────────────────────┘
```

---

## 数据流

### 数据加载流程

```
┌──────────────────────────────────────────────┐
│  1. 组件挂载 (onMounted)                      │
│     ↓                                        │
│  2. 调用 loadData() 函数                      │
│     ↓                                        │
│  3. 尝试两个 JSON 数据源：                     │
│     ① /dashboard/dashboard_snapshot.json     │
│     ② /08-决策追踪/dashboard_snapshot.json   │
│     ↓                                        │
│  4. 第一个成功的响应：                         │
│     data.value = await res.json()           │
│     ↓                                        │
│  5. 渲染模板                                  │
└──────────────────────────────────────────────┘
```

### 核心数据结构

```javascript
// data.value 的结构
{
  meta: {
    latest_trade_date: "2026-04-13",    // 最新交易日
    generated_at: "2026-04-13 15:30"    // 数据生成时间
  },
  
  portfolio: {
    net_value: 499830,                  // 组合净值
    total_return_pct: -0.034,           // 累计收益率 %
    cash: 50000,                        // 现金余额
    market_value: 449830,               // 市值
    position_ratio_pct: 89.99,          // 仓位比例 %
    
    positions: [                        // 持仓列表
      {
        ticker: "01522.HK",
        name: "京投交通科技",
        code: "01522",
        shares: 342000,                 // 持仓股数
        avg_cost: 0.365,                // 平均成本
        close: 0.360,                   // 最新价
        change_pct: -1.37,              // 当日涨跌 %
        unrealized: -1710,              // 浮盈亏
        weight_pct: 25.1,               // 仓位占比 %
        status: "持有"
      },
      // ... 更多持仓
    ]
  },
  
  today_actions: [                      // 今日操作
    {
      date: "2026-04-13",
      ticker: "01522.HK",
      name: "京投交通科技",
      action: "BUY_ADD",                // 操作类型
      price: 0.360,
      shares: 10000,
      amount: 3600,
      reason: "跌破目标价，加仓"
    },
    // ...
  ],
  
  recent_actions: [                     // 最近20条操作
    // 同 today_actions 结构
  ],
  
  ai_decisions: {
    table_rows: [                       // AI决策表格
      {
        date: "2026-03-26",
        name: "京投交通科技",
        code: "01522",
        action: "买入",
        suggest_price: "0.365",
        current_price: "0.360",
        reason: "净现金>市值，PB 0.25倍",
        status: "🟢 已买入"
      },
      // ...
    ],
    raw_excerpt: "原始决策记录文本..."
  }
}
```

---

## 页面模式

### Mode 1: Home（总览页）

**入口**：`<DecisionDashboard mode="home" />`

**显示内容**：

```
┌─────────────────────────────────────────┐
│  📊 关键指标卡片（4个）                    │
│  ├── 组合净值: 499,830 HKD              │
│  ├── 累计收益率: -0.03%                  │
│  ├── 现金余额: 50,000 HKD                │
│  └── 仓位比例: 89.99%                    │
├─────────────────────────────────────────┤
│  🚨 今日操作横幅                          │
│  今日发生 1 笔自动操作（或无操作）          │
├─────────────────────────────────────────┤
│  📝 一句话看懂                            │
│  已投入约 45万元，当前市值约 44万9千元...   │
├─────────────────────────────────────────┤
│  🔗 模块导航                              │
│  [持仓] [今日操作] [决策记录]             │
└─────────────────────────────────────────┘
```

**代码位置**：第197-210行

```vue
<section v-if="showHome" class="dd-panel">
  <div class="dd-plain-summary">
    <strong>一句话看懂：</strong>
    已投入约 <strong>{{ humanHKD(investedCost) }}</strong>，
    当前市值约 <strong>{{ humanHKD(data.portfolio.market_value) }}</strong>
  </div>
  <h3>模块导航</h3>
  <div class="dd-home-links">
    <a :href="appLink('/模拟持仓/持仓')">持仓</a>
    <a :href="appLink('/模拟持仓/今日操作')">今日操作</a>
    <a :href="appLink('/模拟持仓/决策记录')">决策记录</a>
  </div>
</section>
```

---

### Mode 2: Positions（持仓详情）

**入口**：`<DecisionDashboard mode="positions" />`

**显示内容**：

```
┌─────────────────────────────────────────────────────────────┐
│  📊 当前真实持仓表格                                           │
│  ┌──────┬────────┬──────┬────────┬────────┬──────┬─────┐   │
│  │ 标的 │  代码  │ 股数 │ 成本价 │ 现价   │ 涨跌 │ 收益 │   │
│  ├──────┼────────┼──────┼────────┼────────┼──────┼─────┤   │
│  │ 京投 │ 01522  │342K  │ 0.365  │ 0.360  │-1.37%│-1.37%│   │
│  │ 汇贤 │ 87001  │250K  │ 0.500  │ 0.495  │-1.00%│-1.00%│   │
│  │ ...  │ ...    │ ...  │ ...    │ ...    │ ...  │ ... │   │
│  └──────┴────────┴──────┴────────┴────────┴──────┴─────┘   │
└─────────────────────────────────────────────────────────────┘
```

**代码位置**：第212-244行

**关键字段**：
- `shares`：持仓股数
- `avg_cost`：平均成本价
- `close`：最新收盘价
- `change_pct`：当日涨跌幅
- `holdingPct(p)`：持仓收益率（计算得出）
- `unrealized`：浮盈亏金额

---

### Mode 3: Today（今日操作）

**入口**：`<DecisionDashboard mode="today" />`

**显示内容**：

```
┌───────────────────────────────────────────────────────┐
│  🔔 今日操作流水                                        │
│  ┌────────┬──────┬──────┬──────┬──────┬────────┐     │
│  │  日期  │ 标的 │ 动作 │ 价格 │ 股数 │ 金额   │     │
│  ├────────┼──────┼──────┼──────┼──────┼────────┤     │
│  │04-13   │京投  │加仓  │0.360 │10000 │3,600   │     │
│  └────────┴──────┴──────┴──────┴──────┴────────┘     │
├───────────────────────────────────────────────────────┤
│  📜 最近操作流水（最多20条）                            │
│  ┌────────┬──────┬──────┬──────┬──────┬────────┐     │
│  │  日期  │ 标的 │ 动作 │ 价格 │ 股数 │ 金额   │     │
│  ├────────┼──────┼──────┼──────┼──────┼────────┤     │
│  │04-12   │汇贤  │建仓  │0.500 │125000│62,500  │     │
│  │04-10   │天津  │加仓  │2.450 │4000  │9,800   │     │
│  │ ...    │ ...  │ ... │ ...  │ ...  │ ...    │     │
│  └────────┴──────┴──────┴──────┴──────┴────────┘     │
└───────────────────────────────────────────────────────┘
```

**代码位置**：第246-299行

**操作类型映射**：
```javascript
const actionLabel = (a) => {
  if (a === 'BUY_ADD') return '加仓'
  if (a === 'SELL') return '卖出'
  if (a === 'INIT_BUY') return '建仓'
  return a || '-'
}
```

---

### Mode 4: Decisions（AI决策记录）

**入口**：`<DecisionDashboard mode="decisions" />`

**显示内容**：

```
┌────────────────────────────────────────────────────┐
│  📊 AI决策记录（只读）                               │
│                                                    │
│  🟢 正向建议                                        │
│  ┌─────────────────────────────────────────┐      │
│  │ 京投交通科技              🟢 已买入       │      │
│  │ 2026-03-26 · 01522 · 买入               │      │
│  │ 建议价: 0.365  当前价: 0.360             │      │
│  │ 净现金>市值，PB 0.25倍                   │      │
│  └─────────────────────────────────────────┘      │
│                                                    │
│  🟡 观察待验证                                      │
│  ┌─────────────────────────────────────────┐      │
│  │ 华润医药                  🟡 待验证       │      │
│  │ 2026-03-26 · 03320 · 观望               │      │
│  │ 建议价: 6.50  当前价: 6.45               │      │
│  │ 剔除净现金PE 3.6倍                       │      │
│  └─────────────────────────────────────────┘      │
│                                                    │
│  🔴 风险与回避                                      │
│  ┌─────────────────────────────────────────┐      │
│  │ 海底捞                    🔴 回避         │      │
│  │ 2026-03-24 · 06862 · 回避               │      │
│  │ 建议价: -  当前价: 16.88                 │      │
│  │ FCF倍数13.4倍，民营背景                  │      │
│  └─────────────────────────────────────────┘      │
│                                                    │
│  ▼ 查看原文摘要                                     │
└────────────────────────────────────────────────────┘
```

**代码位置**：第301-366行

**决策分类逻辑**（第62-98行）：

```javascript
const decisionGroups = computed(() => {
  const groups = {
    green: [],    // 正向建议（买入、加仓、正确）
    yellow: [],   // 观察待验证（持有、观望）
    red: [],      // 风险回避（卖出、错误、回避）
    other: []     // 其他
  }
  
  for (const r of decisionRows.value) {
    const status = `${r.status || ''}`.toLowerCase()
    const action = `${r.action || ''}`.toLowerCase()
    
    if (status.includes('🟢') || action.includes('买入')) {
      groups.green.push(r)
    } else if (status.includes('🔴') || action.includes('回避')) {
      groups.red.push(r)
    } else if (status.includes('🟡') || action.includes('观望')) {
      groups.yellow.push(r)
    }
  }
  
  return groups
})
```

---

## 核心功能模块

### 1. 响应式状态管理

```javascript
// 第12-14行
const loading = ref(true)      // 加载状态
const error = ref('')          // 错误信息
const data = ref(null)         // 数据源
```

### 2. 计算属性（派生状态）

```javascript
// 第16-24行：视图模式判断
const showHome = computed(() => props.mode === 'home')
const showPositions = computed(() => props.mode === 'positions')
const showToday = computed(() => props.mode === 'today')
const showDecisions = computed(() => props.mode === 'decisions')

// 第21-24行：计算总投入成本
const investedCost = computed(() => {
  const list = positions.value || []
  return list.reduce((sum, p) => 
    sum + Number(p.avg_cost || 0) * Number(p.shares || 0), 0
  )
})

// 第59行：判断今日是否有操作
const todayHasAction = computed(() => 
  (data.value?.today_actions || []).length > 0
)

// 第60-61行：简化数据访问
const positions = computed(() => 
  data.value?.portfolio?.positions || []
)
const decisionRows = computed(() => 
  data.value?.ai_decisions?.table_rows || []
)
```

### 3. 工具函数

#### 数字格式化

```javascript
// 第26-30行：金额格式化（保留2位小数）
const money = (n) =>
  new Intl.NumberFormat('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(Number(n || 0))
// 示例：money(124830.5) → "124,830.50"

// 第32-39行：人性化港元显示
const humanHKD = (n) => {
  const v = Math.round(Number(n || 0))
  const wan = Math.floor(v / 10000)
  const rest = v % 10000
  if (wan <= 0) return `${rest.toLocaleString('zh-CN')}元`
  if (rest === 0) return `${wan}万元`
  return `${wan}万${rest.toLocaleString('zh-CN')}元`
}
// 示例：humanHKD(124830) → "12万4830元"
//       humanHKD(450000) → "45万元"

// 第41-44行：百分比格式化
const pct = (n, digits = 2) => {
  const v = Number(n || 0)
  return `${v >= 0 ? '+' : ''}${v.toFixed(digits)}%`
}
// 示例：pct(-1.37) → "-1.37%"
//       pct(2.5) → "+2.50%"

// 第45-50行：计算持仓收益率
const holdingPct = (p) => {
  const cost = Number(p.avg_cost || 0)
  const close = Number(p.close || 0)
  if (!cost) return 0
  return ((close / cost) - 1) * 100
}
// 示例：holdingPct({avg_cost: 0.365, close: 0.360})
//       → ((0.360/0.365) - 1) * 100 = -1.37%
```

#### 文本映射

```javascript
// 第52-57行：操作类型中文化
const actionLabel = (a) => {
  if (a === 'BUY_ADD') return '加仓'
  if (a === 'SELL') return '卖出'
  if (a === 'INIT_BUY') return '建仓'
  return a || '-'
}
```

### 4. 数据加载逻辑

```javascript
// 第104-128行
async function loadData() {
  loading.value = true
  error.value = ''
  
  try {
    // 尝试两个数据源（降级策略）
    const candidates = [
      withBase('/dashboard/dashboard_snapshot.json'),      // 主数据源
      withBase('/08-决策追踪/dashboard_snapshot.json')     // 备用数据源
    ]
    
    let lastStatus = '404'
    for (const url of candidates) {
      const res = await fetch(url, { cache: 'no-store' })  // 禁用缓存
      if (res.ok) {
        data.value = await res.json()
        loading.value = false
        return
      }
      lastStatus = String(res.status)
    }
    
    throw new Error(`HTTP ${lastStatus}`)
  } catch (e) {
    error.value = `加载失败：${e instanceof Error ? e.message : '未知错误'}`
  } finally {
    loading.value = false
  }
}
```

### 5. 生命周期管理

```javascript
// 第130行：组件挂载时加载数据
onMounted(loadData)

// 第132-138行：样式管理（宽屏布局）
onMounted(() => {
  document.body.classList.add('dashboard-wide')
})

onBeforeUnmount(() => {
  document.body.classList.remove('dashboard-wide')
})
```

---

## 样式设计

### CSS 类名约定

```
dd-*           Dashboard 组件专用类名前缀
├── dd-header       头部
├── dd-loading      加载状态
├── dd-error        错误状态
├── dd-meta         元数据
├── dd-kpis         关键指标卡片区
├── dd-card         单个指标卡片
├── dd-banner       横幅提示
├── dd-subsummary   子页摘要
├── dd-panel        内容面板
├── dd-plain-summary 简洁摘要
├── dd-home-links   首页导航链接
├── dd-empty        空状态
├── dd-details      折叠详情
└── dd-raw          原始文本

decision-*     决策模块专用
├── decision-stream   决策流
├── decision-group    决策分组
├── decision-cards    卡片容器
└── decision-card     单个决策卡片
    ├── card-green    绿色（正向）
    ├── card-yellow   黄色（观察）
    └── card-red      红色（风险）

通用样式类
├── up             上涨样式（绿色）
└── down           下跌样式（红色）
```

### 条件样式绑定

```vue
<!-- 涨跌颜色 -->
<td :class="{ up: p.change_pct >= 0, down: p.change_pct < 0 }">
  {{ pct(p.change_pct, 2) }}
</td>

<!-- 横幅状态 -->
<div class="dd-banner" :class="todayHasAction ? 'warn' : 'ok'">
  ...
</div>
```

---

## 数据结构

### Props 接口

```typescript
interface Props {
  mode?: 'home' | 'positions' | 'today' | 'decisions'
  // 默认: 'home'
}
```

### 数据快照结构

```typescript
interface DashboardSnapshot {
  meta: {
    latest_trade_date: string      // "2026-04-13"
    generated_at: string           // "2026-04-13 15:30:00"
  }
  
  portfolio: {
    net_value: number              // 499830
    total_return_pct: number       // -0.034
    cash: number                   // 50000
    market_value: number           // 449830
    position_ratio_pct: number     // 89.99
    
    positions: Position[]
  }
  
  today_actions: Action[]
  recent_actions: Action[]
  
  ai_decisions: {
    table_rows: Decision[]
    raw_excerpt: string
  }
}

interface Position {
  ticker: string                   // "01522.HK"
  name: string                     // "京投交通科技"
  code: string                     // "01522"
  shares: number                   // 342000
  avg_cost: number                 // 0.365
  close: number                    // 0.360
  change_pct: number               // -1.37
  unrealized: number               // -1710
  weight_pct: number               // 25.1
  status: string                   // "持有"
}

interface Action {
  date: string                     // "2026-04-13"
  ticker: string                   // "01522.HK"
  name: string                     // "京投交通科技"
  action: string                   // "BUY_ADD" | "SELL" | "INIT_BUY"
  price: number                    // 0.360
  shares: number                   // 10000
  amount: number                   // 3600
  reason: string                   // "跌破目标价，加仓"
}

interface Decision {
  date: string                     // "2026-03-26"
  name: string                     // "京投交通科技"
  code: string                     // "01522"
  action: string                   // "买入" | "观望" | "回避"
  suggest_price: string            // "0.365"
  current_price: string            // "0.360"
  reason: string                   // "净现金>市值..."
  status: string                   // "🟢 已买入" | "🟡 待验证" | "🔴 回避"
}
```

---

## 技术亮点

### 1. 降级加载策略

```javascript
// 尝试两个数据源，提高可用性
const candidates = [
  withBase('/dashboard/dashboard_snapshot.json'),      // 优先
  withBase('/08-决策追踪/dashboard_snapshot.json')     // 降级
]
```

### 2. 安全的数据访问

```javascript
// 使用可选链 + 默认值，避免运行时错误
const positions = computed(() => 
  data.value?.portfolio?.positions || []
)
```

### 3. 样式隔离

```javascript
// 组件挂载时添加特殊样式类
onMounted(() => {
  document.body.classList.add('dashboard-wide')
})

// 组件卸载时清理
onBeforeUnmount(() => {
  document.body.classList.remove('dashboard-wide')
})
```

### 4. 智能分类逻辑

```javascript
// 根据关键词自动分类决策记录
if (status.includes('🟢') || action.includes('买入')) {
  groups.green.push(r)
}
```

### 5. 国际化数字格式

```javascript
// 使用 Intl.NumberFormat 标准化数字显示
new Intl.NumberFormat('zh-CN', {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2
})
```

---

## 使用示例

### 在 Markdown 中使用

**总览页**：
```markdown
# 模拟持仓

<DecisionDashboard />
<!-- 或显式指定 -->
<DecisionDashboard mode="home" />
```

**持仓详情**：
```markdown
# 持仓明细

<DecisionDashboard mode="positions" />
```

**今日操作**：
```markdown
# 今日操作

<DecisionDashboard mode="today" />
```

**AI决策记录**：
```markdown
# 决策记录

<DecisionDashboard mode="decisions" />
```

---

## 改进建议

### 1. 拆分子组件

当前所有逻辑在一个文件中，建议拆分：

```
DecisionDashboard.vue (主组件)
├── PortfolioKPIs.vue       (关键指标卡片)
├── PositionsTable.vue      (持仓表格)
├── ActionsTable.vue        (操作流水)
└── DecisionsCards.vue      (决策卡片)
```

### 2. 状态管理

如果数据需要跨组件共享，考虑使用 Pinia：

```javascript
// stores/portfolio.js
export const usePortfolioStore = defineStore('portfolio', () => {
  const data = ref(null)
  async function loadData() { ... }
  return { data, loadData }
})
```

### 3. 类型安全

使用 TypeScript 定义接口：

```typescript
// types/portfolio.ts
export interface Position {
  ticker: string
  name: string
  shares: number
  // ...
}
```

### 4. 错误边界

添加更细粒度的错误处理：

```vue
<Suspense>
  <template #default>
    <DecisionDashboard />
  </template>
  <template #fallback>
    <div>加载中...</div>
  </template>
</Suspense>
```

---

## 总结

### 组件特点

✅ **单一职责**：专注于投资组合仪表盘展示  
✅ **可配置**：通过 `mode` prop 切换不同视图  
✅ **数据驱动**：从 JSON 快照加载数据，无需后端  
✅ **容错性强**：降级加载、安全访问、错误提示  
✅ **用户友好**：人性化数字格式、颜色区分涨跌  

### 适用场景

- ✅ 个人投资组合管理
- ✅ 模拟交易记录
- ✅ AI投资决策追踪
- ✅ 静态网站 + 动态数据展示

### 核心价值

这个组件实现了**静态网站（VitePress）+ 动态数据（JSON）+ 交互体验（Vue）**的完美结合，无需后端服务器，仅靠定期更新 JSON 文件就能实现实时数据展示。

---

*最后更新：2026-04-13*
