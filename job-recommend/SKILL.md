---
name: job-recommend
description: 岗位推荐与投递清单 Skill。用于根据岗位画像、候选人资料、城市偏好和求职阶段，寻找具体岗位详情页，生成推荐清单或 Excel 投递清单，并在用户明确确认岗位后辅助投递。支持技术岗和通用岗的不同搜索策略。适合”推荐可投岗位””帮我找实习””生成投递清单””确认这些岗位后帮我投递”等任务。
---

# Job Recommend

## 流程

1. 读取岗位画像、候选人能力、城市偏好、实习/校招等约束。
2. 根据 `JobProfile.role_category` 选择搜索策略：
   - 技术岗：岗位名 + 核心技术 + 城市
   - 通用岗：岗位名 + 核心能力关键词 + 城市
3. 搜索公开招聘渠道或用户提供的招聘平台链接。
4. 只保留可访问、有明确岗位信息的岗位详情页；不得用公司官网首页、招聘首页、搜索结果页替代详情页。
5. 输出 `JobRecommendation` 表格，初始状态为”待用户确认”，并导出为格式规范的 `.xlsx` 岗位推荐清单。
6. 若网络或平台访问不可用，输出搜索关键词、筛选规则和待用户自行确认清单，不编造岗位。
7. 用户明确选择岗位并确认投递后，执行”确认后投递流程”。

## 浏览器操作工具

### 推荐工具：autoglm-browser-agent

AutoClaw 内置的智能浏览器自动化工具，位于 `~/.openclaw-autoclaw/skills/autoglm-browser-agent/`。

**调用方式：**

```bash
autoclaw task=”任务描述”
```

**首次使用准备：**

1. 安装浏览器扩展：
   - Chrome：[AutoGLM 扩展（Chrome Web Store）](https://chromewebstore.google.com/detail/autoglm/jelniggicmclhfgnlapbkgfibmgelfnp)
   - Edge：[AutoGLM 扩展（Edge Add-ons）](https://microsoftedge.microsoft.com/addons/detail/autoglm/ljlnbmmmgnflklegiafalpieckpihffn)

2. 确认配置：首次使用时需确认浏览器偏好（Chrome/Edge）和信任模式

**关键使用规则：**

| 规则 | 说明 |
|------|------|
| task 参数 | 必须原样照抄用户需求，不能擅自扩展或改写 |
| 数量默认值 | 用户未指定数量时，默认收集 5 个岗位 |
| 结果获取 | 命令结束后用 Read 工具读取 `~/.openclaw-autoclaw/browser_result_{session_id}.md` |
| 每轮限制 | 只能调用一次，不能自动重试 |
| 超时设置 | shell timeout 必须是 7200 秒（2小时） |
| 禁止 poll | 不要使用 process poll 获取结果 |

**岗位搜索示例：**

```bash
# 搜索岗位（用户未指定数量，默认5个）
autoclaw task=”打开BOSS直聘搜索Java后端实习岗位，收集前5个岗位的名称、公司、城市、薪资”

# 用户指定数量
autoclaw task=”打开BOSS直聘搜索管培生校招岗位，收集前3个岗位的名称、公司、城市、学历要求”

# 投递岗位（用户确认后）
autoclaw task=”打开岗位页面 https://www.zhipin.com/job_detail/xxx，填写投递表单并上传简历”
```

**结果处理流程：**

```
1. 执行 autoclaw 命令
2. 等待命令执行结束
3. 用 Read 工具读取结果文件：
   - 从 shell 输出提取 Result: <文件路径>
   - 或读取 ~/.openclaw-autoclaw/session_pool.json 获取最新 session_id
   - 然后读取 ~/.openclaw-autoclaw/browser_result_{session_id}.md
4. 从结果中提取岗位信息，写入 Excel
```

**遇到登录/验证码时：**

1. 浏览器会暂停，返回 `[INTERACT_REQUIRED]` 标记
2. 告知用户手动完成登录
3. 用户确认后，带 `session_id` 和 `tab_id` 继续执行

### 辅助工具

| 工具 | 功能 | 适用场景 |
|------|------|----------|
| `autoglm-websearch` | 网络搜索 | 快速关键词搜索，无需登录 |
| `autoglm-open-link` | 打开链接 | 读取岗位详情页正文 |

**autoglm-websearch 调用：**

```bash
python ~/.openclaw-autoclaw/skills/autoglm-websearch/websearch.py “Java后端实习 北京”
```

### 替代工具（autoglm 不可用时）

| 工具 | 功能 | 适用场景 |
|------|------|----------|
| `mcp__tavily__tavily_search` | 网页搜索 | 岗位关键词搜索 |
| `WebSearch` | 网页搜索 | 岗位关键词搜索 |
| `WebFetch` | 获取网页内容 | 读取岗位详情页 |

### 无浏览器工具时

若以上工具均不可用：
1. 输出搜索关键词和筛选规则
2. 提供平台入口链接
3. 生成待用户自行确认的岗位清单模板
4. **不编造岗位或链接**

## 搜索执行要求

**必须执行真实搜索：**
1. 调用 `autoglm-browser-agent` 或 `autoglm-websearch` 进行网络搜索
2. 从搜索结果中提取真实岗位信息
3. 验证岗位详情页链接可访问

**禁止行为：**
- 不调用工具直接输出假数据/示例数据
- 编造不存在的岗位、公司或链接
- 使用过时的岗位信息

**工具不可用时：**
- 明确告知用户”当前无法访问招聘平台”
- 输出搜索关键词和平台入口链接
- 提供空白清单模板供用户手动填写
- 不输出假的岗位数据

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
| keywords | 技术关键词/能力关键词 | 是 |
| url | 岗位详情页链接 | 是 |
| url_type | 链接类型（必须为岗位详情页） | 是 |
| platform | 平台 | 是 |
| source | 来源 | 是 |
| retrieved_at | 检索日期 | 是 |
| reason | 推荐理由 | 是 |
| apply_requirements | 投递要求 | 否 |
| status | 状态 | 是 |
| notes | 备注 | 否 |

## 搜索关键词

### 技术岗搜索关键词

| 岗位 | 核心关键词 | 组合示例 |
|------|------------|----------|
| Java后端 | Java、Spring、MySQL、Redis | "Java后端实习 北京 Spring" |
| 前端开发 | 前端、Vue、React、JavaScript | "前端开发校招 上海 Vue" |
| 测试开发 | 测试、自动化、Python、接口测试 | "测试开发实习 深圳 自动化" |
| 算法实习 | 算法、机器学习、Python、深度学习 | "算法实习 杭州 机器学习" |

### 通用岗搜索关键词

| 岗位 | 核心关键词 | 组合示例 |
|------|------------|----------|
| 管培生 | 管培生、管理培训生、储备干部 | "管培生校招 北京" |
| 产品运营 | 运营、产品运营、用户运营、内容运营 | "产品运营实习 上海" |
| 人力资源 | HR、人力资源、招聘、人事专员 | "人力资源实习 深圳" |
| 市场销售 | 销售、市场专员、商务拓展、BD | "销售代表 杭州" |
| 行政助理 | 行政、助理、文员、前台 | "行政助理实习 北京" |

### 通用岗搜索技巧

1. **岗位名称变体**：同一岗位可能有多种叫法
   - 管培生 → 管理培训生、储备干部、管培
   - 运营 → 产品运营、用户运营、内容运营、活动运营
   - 人力 → HR、人事、招聘专员、HRBP

2. **平台偏好**：
   - BOSS直聘：通用岗岗位多，适合初级岗位
   - 智联招聘、前程无忧：传统行业岗位多
   - 实习僧、牛客：实习岗位集中
   - LinkedIn：外企、高端岗位

3. **筛选条件**：
   - 学历要求与用户匹配
   - 工作经验要求（实习/校招/社招）
   - 行业偏好（互联网、金融、快消等）

## Excel 输出规范

- 文件名：`岗位推荐清单-{目标岗位}-{YYYYMMDD}.xlsx`
- 首行冻结，启用筛选，列宽适配
- 链接列必须是可点击超链接
- 岗位详情页必须精准到具体岗位页面

### 导出脚本使用

使用 `scripts/export_job_recommendations.py` 导出岗位推荐清单：

```bash
python job-recommend/scripts/export_job_recommendations.py \
  --input jobs.json \
  --output 岗位推荐清单-管培生-20240315.xlsx
```

**参数说明：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `--input` | 是 | 输入文件路径，支持 CSV 或 JSON 格式 |
| `--output` | 是 | 输出 Excel 文件路径 |

**输入格式要求（JSON）：**

```json
[
  {
    "title": "管培生",
    "company": "XX公司",
    "city": "北京",
    "platform": "BOSS直聘",
    "education_requirement": "本科及以上",
    "keywords": ["沟通", "团队协作"],
    "url": "https://www.zhipin.com/job_detail/xxx",
    "source": "BOSS直聘搜索",
    "retrieved_at": "2024-03-15",
    "reason": "能力要求匹配",
    "status": "待用户确认"
  }
]
```

**输入格式要求（CSV）：**

首行为字段名，支持中英文字段映射：

```csv
岗位名称,公司名称,城市,平台,学历要求,技术关键词,岗位详情页,来源,检索日期,推荐理由,状态
管培生,XX公司,北京,BOSS直聘,本科及以上,沟通,团队协作,https://...,BOSS直聘搜索,2024-03-15,能力要求匹配,待用户确认
```

**字段映射：**

| 表头 | 支持的字段名 |
|------|--------------|
| 岗位名称 | title, job_title, name |
| 公司名称 | company, company_name |
| 城市 | city, location |
| 平台 | platform |
| 学历要求 | education_requirement, education |
| 技术关键词 | keywords, skills |
| 岗位详情页 | url, link, job_url |
| 来源 | source |
| 检索日期 | retrieved_at, date |
| 推荐理由 | reason |
| 投递要求 | apply_requirements |
| 状态 | status |
| 备注 | note, notes |

**依赖：**

```bash
pip install openpyxl
```

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
- `job-target-profile/references/tech-role-baselines.md`：技术岗基线
- `job-target-profile/references/general-role-baselines.md`：通用岗基线
