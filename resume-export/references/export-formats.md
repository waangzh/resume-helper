# 简历导出格式策略

## 默认交付

- `.html`：即时预览版本，可直接用浏览器打开，包含编辑、重置、上传照片和导出 PDF 按钮，也作为 PDF 打印源。
- `.pdf`：非默认输出；用户明确要求时，由 HTML/CSS 通过浏览器打印生成。
- 当前只维护 HTML 与可选 PDF 两类交付物。

## 文件命名

输出目录：

- 所有生成的简历材料必须放在当前工作目录下的 `简历材料/` 文件夹中，除非用户明确指定其他路径。
- 包括 HTML 预览、用户要求导出的 PDF，以及后续生成的相关简历材料。

文件名优先格式：

`{姓名}-{岗位}-简历.{ext}`

无法确认姓名或城市时：

`候选人-{岗位或目标岗位}-简历.{ext}`

示例：

- `张三-Java后端实习-简历.html`
- `张三-Java后端实习-简历.pdf`

## HTML 版式

- A4 页面，常规页边距或窄页边距。
- 生成时必须同时满足 `references/layout-quality-constraints.md` 中的字号、行高、留白、照片位和内容密度约束。
- 中文字体优先微软雅黑、苹方、Noto Sans CJK 或等价系统字体。
- 正文紧凑易读，标题层级清晰。
- 项目 bullet 使用短句，避免多级嵌套。
- 联系方式使用普通文本，不能放在图片中。

## 可选视觉风格

- `plain`: 默认简洁 ATS 风格，黑白标题。
- `classic-blue`: 参考 `assets/reference-images/classic-blue.png`，蓝色主标题和细分隔线。
- `teal-ribbon`: 参考 `assets/reference-images/teal-ribbon.png`，深青模块标题和紧凑分隔。
- `light-blue-band`: 参考 `assets/reference-images/light-blue-band.png`，浅蓝模块条，适合更清晰的视觉分区。

若用户没有要求视觉模板，优先使用 `plain` 或 `classic-blue`。技术岗投递时避免技能进度条；照片位置仅作为可选上传区，用户未上传时不得编造照片信息。

## PDF 导出

- PDF 默认从最终 HTML/CSS 预览渲染，不单独改内容。
- 若用户在 HTML 页面中实时编辑内容，应以当前页面内容为准通过浏览器打印导出。
- 使用 Chrome/Edge headless 打印时，应保留 `@page A4`、打印样式和分页控制。
- 浏览器导出失败时不要阻塞任务；返回原因和可编辑文件路径。
- 不维护独立 PDF 排版脚本；PDF 必须来自 HTML 预览。

## 投递版本控制

- 每个目标岗位可生成一个单独版本。
- 不同岗位版本不得互相覆盖。
- 文件路径应写入结果摘要或后续求职材料清单的“已生成简历”部分。

## HTML 预览编辑

- HTML 页面必须有“编辑”按钮，启用后简历正文区域可直接修改。
- HTML 页面必须有“完成编辑”状态，关闭编辑后保留修改后的显示。
- HTML 页面中的简历文字都必须可编辑，包括姓名、联系方式、栏目标题、正文段落、项目标题、bullet 和照片占位文字。
- 重要文字必须来自 HTML DOM，不得用 CSS `content` 伪元素生成；CSS 伪元素只可用于装饰性横线、斜切 ribbon 等。
- HTML 页面应把编辑内容暂存在浏览器本地存储中，刷新后不立即丢失。
- HTML 页面应有“重置”按钮，用于恢复到初始生成内容。
- HTML 页面必须有“上传照片”按钮，允许用户选择本地图片并放入简历照片区域。
- 用户上传的照片应以浏览器本地数据形式保存在页面状态中，刷新后尽量保留，不上传到外部服务。
- 打印或导出 PDF 时隐藏工具栏，只保留简历正文。

## 脚本用法

生成 HTML 预览：

```powershell
python resume-export/scripts/render_resume_web.py `
  --input path/to/resume.md `
  --html path/to/resume.html `
  --style classic-blue
```

单独从 HTML 导出 PDF：

```powershell
python resume-export/scripts/export_html_pdf.py `
  --html path/to/resume.html `
  --pdf path/to/resume.pdf
```

`--style` 可选：`plain`、`classic-blue`、`teal-ribbon`、`light-blue-band`。脚本适合简洁 Markdown 简历，不处理复杂表格或多栏布局。
