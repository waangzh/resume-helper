---
name: resume-export
description: 简历文件导出与即时预览 Skill。用于把 TailoredResume 生成完整、可编辑文字、可投递的静态 HTML/CSS 简历预览；PDF 仅在用户明确要求时通过浏览器打印导出。适合“生成可编辑 HTML 简历”“即时预览简历”“导出 PDF 简历”“把简历做成可投递文件”等任务。
---

# Resume Export

## 流程

1. 读取 `TailoredResume` 和用户指定格式；未指定时默认生成 HTML 预览。
2. 读取 `references/export-formats.md` 确定格式、命名、排版和失败兜底；读取 `references/layout-quality-constraints.md` 控制字号、行高、留白、照片位和内容密度；需要参考图风格时读取 `references/visual-template-guide.md`。
3. 生成完整简历正文，不只输出后续材料片段。
4. 优先生成可打开的 `resume.html` 供即时预览；HTML 页面必须包含“编辑”“重置”“上传照片”和“导出 PDF”按钮，支持页面内全部简历文字实时编辑、上传真实照片后再打印导出。
5. 输出 `ResumeDocument`，包含文件路径、格式说明、生成时间和待确认项。

## 导出要求

- HTML 是主交付物，应可直接用浏览器打开，并支持页面内文字实时编辑。
- 用户要求其他文件格式时，说明当前技能只维护 HTML 与可选 PDF。
- HTML 简历正文区域内的姓名、求职意向、基础信息、栏目标题、段落、项目名和 bullet 都必须是可编辑 DOM 文本，不得图片化；装饰性伪元素只能用于横线等非文字视觉效果，不用于生成标题块缺口。
- HTML 应包含照片位置和上传照片按钮，用户选择本地图片后应立即显示在简历照片区域，并随 PDF 一起导出。
- HTML 不提供拖动头像、移动 section、调整页边距等布局微调能力；页面元素位置由模板 CSS 固定，避免破坏版式。
- PDF 不是默认输出；用户明确要求时，从 HTML/CSS 通过浏览器打印导出。无法使用浏览器导出时说明原因，并保留 HTML 交付物。
- 所有生成的简历材料必须放在当前工作目录下的 `简历材料/` 文件夹中，除非用户明确指定其他路径。
- 文件名统一为 `{姓名}-{岗位}-简历.{ext}`，例如 `张三-Java后端实习-简历.html`、`张三-Java后端实习-简历.pdf`。
- 生成后在结果摘要或后续求职材料清单中列出所有简历文件路径。

## 版式要求

- 默认一页优先，内容简洁，ATS 友好；用户要求“参考模板/更美观/蓝色简历”时可选择 `classic-blue`、`teal-ribbon`、`light-blue-band`。
- 不使用复杂表格、图片化文字或技能进度条。
- 使用标准模块：页眉基本信息、教育背景、技术技能、项目经历、实习经历（若有）、竞赛奖项、自我评价（可选）。
- 页眉基本信息严格参考用户给定图片的结构：左侧照片，右侧为姓名、求职意向摘要、两列三行基础信息；除配色可随风格变化外，照片与文字的组合、分割线、字段顺序和网格排布保持一致。
- `teal-ribbon` 使用 `assets/templates/resume-web/resume.css` 中的深青矩形标题条、横线分区、窄页边距和紧凑排版；不得引入婚姻、技能进度条等不适合内容。
- HTML 工具栏必须包含编辑、重置、上传照片和导出 PDF 控制；不得包含布局微调或移动元素控制；打印/PDF 导出时工具栏必须隐藏。

## 资源

- 读取 `references/export-formats.md` 获取格式策略。
- 读取 `references/layout-quality-constraints.md` 获取 HTML 版式质量和验收约束。
- 读取 `references/visual-template-guide.md` 获取参考图沉淀的版式规则。
- 可使用 `assets/templates/resume.md` 作为内部草稿模板，但不要把 `.md` 作为最终简历交付物。
- 使用 `assets/templates/resume-web/` 生成静态 HTML/CSS 预览。
- 生成 HTML 时运行 `scripts/render_resume_web.py`。
- 用户明确要求 PDF 时，在 HTML 生成后运行 `scripts/export_html_pdf.py`。
