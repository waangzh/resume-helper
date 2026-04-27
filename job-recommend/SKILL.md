---
name: job-recommend
description: 岗位推荐与投递清单 Skill。用于根据岗位画像、候选人资料、城市偏好和求职阶段，寻找具体岗位详情页，生成推荐清单或 Excel 投递清单，并在用户明确确认岗位后辅助投递。适合”推荐可投岗位””帮我找实习””生成投递清单””确认这些岗位后帮我投递”等任务。
---

# Job Recommend

## 流程

1. 读取岗位画像、候选人能力、城市偏好、实习/校招等约束。
2. 搜索公开招聘渠道或用户提供的招聘平台链接。
3. 只保留可访问、有明确岗位信息的岗位详情页；不得用公司官网首页、招聘首页、搜索结果页替代详情页。
4. 输出 `JobRecommendation` 表格，初始状态为”待用户确认”，并导出为格式规范的 `.xlsx` 岗位推荐清单。
5. 若网络或平台访问不可用，输出搜索关键词、筛选规则和待用户自行确认清单，不编造岗位。
6. 用户明确选择岗位并确认投递后，执行”确认后投递流程”。

## 浏览器操作工具

### 推荐工具（优先使用）

| 工具 | 功能 | 调用方式 | 适用场景 |
|------|------|----------|----------|
| `autoglm-browser-agent` | 智能浏览器自动化 | `autoclaw task=”...”` | 岗位搜索、打开页面、表单填写、投递操作 |
| `autoglm-websearch` | 网络搜索 | `python websearch.py “关键词”` | 岗位关键词搜索 |
| `autoglm-open-link` | 打开链接获取内容 | `python open-link.py “URL”` | 读取岗位详情页正文 |

**autoglm-browser-agent 调用示例：**
```bash
# 搜索岗位
autoclaw task=”打开BOSS直聘搜索Java后端实习岗位，收集前5个岗位的名称、公司、城市、薪资”

# 投递岗位（用户确认后）
autoclaw task=”打开岗位页面 https://www.zhipin.com/job_detail/xxx，填写投递表单并上传简历”
```

### 替代工具（无 autoglm 时使用）

| 工具 | 功能 | 适用场景 |
|------|------|----------|
| `mcp__tavily__tavily_search` | 网页搜索 | 岗位关键词搜索 |
| `WebSearch` | 网页搜索 | 岗位关键词搜索 |
| `WebFetch` | 获取网页内容 | 读取岗位详情页 |
| `mcp__chrome-devtools__*` | Chrome DevTools 操作 | 浏览器自动化、表单填写 |
| `mcp__plugin_playwright_playwright__*` | Playwright 浏览器操作 | 浏览器自动化、投递流程 |
| `agent-browser` skill | 浏览器自动化 | 表单填写、投递操作 |

**替代工具调用示例：**
```bash
# 搜索岗位
mcp__tavily__tavily_search query=”Java后端实习 北京 BOSS直聘”

# 打开岗位页面
WebFetch url=”https://www.zhipin.com/job_detail/xxx”

# 投递操作
mcp__plugin_playwright_playwright__browser_navigate url=”https://www.zhipin.com/job_detail/xxx”
mcp__plugin_playwright_playwright__browser_fill_form selector=”#name” value=”张三”
```

### 无浏览器工具时

若以上工具均不可用：
1. 输出搜索关键词和筛选规则
2. 提供平台入口链接
3. 生成待用户自行确认的岗位清单模板
4. 不编造岗位或链接

## 支持平台

- BOSS 直聘、拉勾、猎聘、智联招聘、前程无忧
- 牛客、实习僧、LinkedIn
- 公司官网 ATS

## 推荐字段

| 字段 | 说明 | 必填 |
|------|------|------|
| title | 岗位名称 | 是 |
| company | 公司名称 | 是 |
| city | 城市 | 是 |
| education_requirement | 学历要求 | 是 |
| keywords | 技术关键词 | 是 |
| url | 岗位详情页链接 | 是 |
| url_type | 链接类型（必须为岗位详情页） | 是 |
| platform | 平台 | 是 |
| source | 来源 | 是 |
| retrieved_at | 检索日期 | 是 |
| reason | 推荐理由 | 是 |
| apply_requirements | 投递要求 | 否 |
| status | 状态 | 是 |
| notes | 备注 | 否 |

## Excel 输出规范

- 文件名：`岗位推荐清单-{目标岗位}-{YYYYMMDD}.xlsx`
- 首行冻结，启用筛选，列宽适配
- 链接列必须是可点击超链接
- 岗位详情页必须精准到具体岗位页面

## 确认后投递流程

仅在用户明确表达”投递这几个岗位””确认投递第 1、3 个岗位”等指令后执行：

1. 确认使用的简历文件
2. 逐个打开用户选择的岗位详情页
3. 若需要登录，让用户自行完成登录
4. 填充表单字段，上传简历
5. 若平台有最终提交按钮且用户已明确授权，可提交申请
6. 记录 `ApplicationAttempt`

## 投递状态

| 状态 | 说明 |
|------|------|
| 待用户确认 | 初始状态 |
| 用户已选择 | 用户已确认投递 |
| 已打开 | 已打开岗位页面 |
| 已投递 | 投递成功 |
| 投递受阻 | 遇到障碍需处理 |
| 已跳过 | 用户跳过 |

## 合规边界

- 未经用户明确选择岗位并确认投递，不提交申请
- 不保存账号密码；需要登录时用户自行登录
- 不批量海投；每次只投用户明确选择的岗位
- 不绕过平台访问限制
- 不推荐无法确认存在的岗位
- 对过期、来源不明或信息不足的岗位标记风险

## 资源

- `references/search-and-compliance.md`：搜索策略、合规规则、投递记录格式
- `scripts/export_job_recommendations.py`：Excel 导出脚本
