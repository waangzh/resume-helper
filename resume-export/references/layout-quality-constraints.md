# 简历 HTML 版式质量约束

本文件定义 HTML 预览的视觉质量标准。Markdown 格式约束见 `resume-tailor/references/resume-standards.md`。

---

## 职责分层

| 层级 | 文件 | 职责 |
|------|------|------|
| Markdown 输出 | `resume-tailor/references/resume-standards.md` | 定义分隔符、模块结构、字段格式 |
| 解析脚本 | `scripts/render_resume_web.py` | 将 Markdown 解析为 HTML 结构 |
| CSS 样式 | `assets/templates/resume-web/resume.css` | 定义字号、行高、间距、颜色 |

**关键原则：间距、字号、颜色由 CSS 层控制，Markdown 层只负责结构和内容。**

---

## 内容结构约束（Markdown 层）

> 由 `resume-tailor` 生成的 Markdown 必须遵守，详见 `resume-tailor/references/resume-standards.md`

### 分隔符约定

| 用途 | 分隔符 | 示例 |
|------|--------|------|
| 基本信息字段间 | 两个以上空格 或 Tab | `年龄：22  性别：男` |
| 求职意向 | 只显示岗位 | `求职意向：Java后端实习` |
| 教育背景字段间 | 两个以上空格 | `**湖南大学**  **计算机（本科）**  2021-2025` |
| 项目标题 | 两个以上空格 | `### 项目名  2023.09 - 2024.01` |
| 竞赛奖项字段间 | 两个以上空格 | `蓝桥杯  省赛一等奖  2024.03`（渲染为左中右三列加粗） |

### 模块结构

- 一级标题只放姓名，不附加其他信息
- 求职意向使用固定格式：`求职意向：{岗位}`（只显示岗位，不包含其他信息）
- 基本信息三行：年龄/性别、籍贯/工作年限、电话/邮箱
- 教育背景固定三行：学校专业时间行、成绩行、课程行
- 项目标题格式：`### {项目名}  {时间}` 或 `### {项目名}  {中间字段}  {时间}`（不含项目类型）
- 实习标题格式：`### {公司} / {部门} / {岗位}  {时间}`
- 竞赛奖项格式：`- {奖项名称}  {获奖等级}  {时间}`

### 项目标题结构

```
<div class="resume-project-title">
  <span class="resume-project-name">{项目名称}</span>
  <span class="resume-project-middle">{中间字段}</span>
  <span class="resume-project-period">{时间}</span>
</div>
```

**布局：项目名称左对齐，时间右对齐，中间字段居中**

### 竞赛奖项结构

```
<div class="resume-award-item">
  <strong class="resume-award-name">{奖项名称}</strong>
  <strong class="resume-award-level">{获奖等级}</strong>
  <strong class="resume-award-period">{时间}</strong>
</div>
```

**布局：奖项名称左对齐，时间右对齐，获奖等级居中，三列全部加粗**

---

## HTML 结构约束（解析层）

> 由 `render_resume_web.py` 解析生成，确保 HTML 结构正确

### 页眉结构

```
<header class="resume-profile">
  <aside class="resume-photo">...</aside>
  <div class="resume-profile-main">
    <h1 class="resume-title">{姓名}</h1>
    <p class="resume-intent">求职意向：...</p>
    <div class="resume-contact">...</div>
  </div>
</header>
```

### 教育背景结构

```
<section class="resume-section">
  <h2 class="resume-section-title">教育背景</h2>
  <div class="resume-education-summary">
    <strong>{时间}</strong><strong>{学校}</strong><strong>{专业}（{学历}）</strong>
  </div>
  <p class="resume-education-detail is-score">专业成绩：...</p>
  <p class="resume-education-detail is-courses">主修课程：...</p>
</section>
```

**三列全部加粗显示：时间、学校、专业（学历）**

### 解析规则

- 基本信息字段识别：竖线 `\|`、Tab、或 **两个以上空格**
- 教育背景第一行识别：需要至少 3 项内容（学校、专业学历、时间）
- 项目标题识别：`### ` 开头的行，时间在行尾

---

## 视觉约束（CSS 层）

> 由 `resume.css` 实现，不影响 Markdown 输出

### 页面布局

- A4 页面宽度：`width: 210mm`
- 页面内边距：`padding: 12px 17mm 16mm`（约 17-18mm 左右边距）
- 内容区最小高度：`min-height: 297mm`

### 页眉信息区

| 元素 | 尺寸/间距 | CSS 属性 |
|------|----------|----------|
| 照片区 | 98px × 126px，无边框 | `width: 98px; height: 126px` |
| 照片垂直位置 | 页眉高度居中 | `align-items: center` |
| 照片与文字区间距 | 约 50px | `column-gap: 50px` |
| 基础信息两列间距 | 约 48px | `column-gap: 48px` |
| 每项内部三列 | 图标 22px + 标签 60px + 内容自适应 | `grid-template-columns: 22px 60px minmax(0, 1fr)` |

### 文字样式

| 元素 | 字号 | 行高 |
|------|------|------|
| 正文 | 13.5px | 1.62 |
| 姓名 | 30px | 1.1 |
| 模块标题 | 18px | 1.35 |
| 项目/实习标题 | 14px | - |

### 间距控制

| 元素 | 间距 |
|------|------|
| 模块间距 | `margin-top: 16px` |
| 标题下分隔线 | `border-bottom: 1px solid` |
| bullet 列表 | `margin: 5px 0 9px 18px` |

---

## 打印与 PDF 约束

- 打印时隐藏工具栏：`.preview-toolbar { display: none; }`
- 保留模块标题背景色：`print-color-adjust: exact`
- 禁止分页断裂：`break-inside: avoid` 应用于 section、subtitle、bullet

---

## 生成与验收

- 默认先生成 HTML 预览，PDF 仅从最终 HTML 打印生成
- HTML 预览提供正文文字编辑功能，不提供布局微调
- 生成 HTML 后检查：
  - 页面是否存在文本重叠
  - 照片是否遮挡正文
  - 标题是否贴边
  - 列表是否过密
  - 工具栏是否进入打印区域
- 如果内容无法在一页内清晰排下，**在 Markdown 层压缩内容**（删减 bullet 或项目），不通过降低字号强行塞满
