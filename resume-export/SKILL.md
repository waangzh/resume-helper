---
name: resume-export
description: 简历文件导出与即时预览 Skill。用于把 TailoredResume 生成完整、可编辑文字、可投递的静态 HTML/CSS 简历预览；PDF 仅在用户明确要求时通过浏览器打印导出。支持技术岗和通用岗两种模板结构。适合”生成可编辑 HTML 简历””即时预览简历””导出 PDF 简历””把简历做成可投递文件”等任务。
---

# Resume Export

## 流程

1. 读取 `TailoredResume` 和用户指定格式；未指定时默认生成 HTML 预览。
2. 根据 `TailoredResume.role_category` 选择模板：
   - 技术岗：使用技术岗模块（技术技能、项目经历、实习经历）
   - 通用岗：使用通用岗模块（实习经历、校园经历、社会实践、技能与证书）
3. 验证输入 Markdown 格式是否符合 `resume-tailor/references/resume-standards.md` 的格式规范。
4. 读取 `references/export-formats.md` 确定格式、命名、排版和失败兜底；读取 `references/layout-quality-constraints.md` 控制字号、行高、留白、照片位和内容密度；需要参考图风格时读取 `references/visual-template-guide.md`。
5. 生成完整简历正文，不只输出后续材料片段。
6. 优先生成可打开的 `resume.html` 供即时预览；HTML 页面必须包含”编辑””重置””上传照片”和”导出 PDF”按钮，支持页面内全部简历文字实时编辑、上传真实照片后再打印导出。
7. 输出 `ResumeDocument`，包含文件路径、格式说明、生成时间和待确认项。

## 模板类型

### 技术岗模板

模块结构：基本信息 → 教育背景 → 技术技能 → 项目经历 → 实习经历 → 竞赛奖项

### 通用岗模板

模块结构：基本信息 → 教育背景 → 实习经历 → 校园经历 → 社会实践 → 竞赛奖项 → 技能与证书

## Markdown 格式要求（输入验证）

> 解析脚本依赖特定格式，格式错误会导致 HTML 预览排版混乱。

**必须符合 `resume-tailor/references/resume-standards.md` 的格式规范：**

- 分隔符：基本信息、教育背景字段间使用 **两个以上空格** 或 **Tab**
- 求职意向：只显示岗位，格式为 `求职意向：{岗位}`
- 教育背景：必须三行完整（学校专业时间行、成绩行、课程行）
- 项目标题：`### {项目名}  {时间}`（两个以上空格分隔）
- 校园/社会实践标题：`### {组织} / {职务}  {时间}`
- Bullet：每条以 `- ` 开头（短横线 + 空格）

**格式不符合时：** 在输出中明确标注格式问题，提示需要修正的位置。

## 导出要求

- HTML 是主交付物，应可直接用浏览器打开，并支持页面内文字实时编辑。
- 用户要求其他文件格式时，说明当前技能只维护 HTML 与可选 PDF。
- HTML 简历正文区域内的姓名、求职意向、基础信息、栏目标题、段落、项目名和 bullet 都必须是可编辑 DOM 文本，不得图片化。
- HTML 应包含照片位置和上传照片按钮，用户选择本地图片后应立即显示在简历照片区域，并随 PDF 一起导出。
- HTML 不提供拖动头像、移动 section、调整页边距等布局微调能力；页面元素位置由模板 CSS 固定，避免破坏版式。
- PDF 不是默认输出；用户明确要求时，从 HTML/CSS 通过浏览器打印导出。
- 所有生成的简历材料必须放在当前工作目录下的 `简历材料/` 文件夹中，除非用户明确指定其他路径。
- 文件名统一为 `{姓名}-{岗位}-简历.{ext}`。

## 资源

- `resume-tailor/references/resume-standards.md`：**Markdown 格式规范（输入验证）**
- `references/export-formats.md`：格式策略和命名规则
- `references/layout-quality-constraints.md`：HTML 版式质量和验收约束
- `references/visual-template-guide.md`：参考图沉淀的版式规则
- `assets/templates/resume.md`：技术岗草稿模板
- `assets/templates/resume-general.md`：通用岗草稿模板
- `assets/templates/resume-web/`：HTML/CSS 模板
- `scripts/render_resume_web.py`：Markdown → HTML 解析脚本
- `scripts/export_html_pdf.py`：HTML → PDF 导出脚本
