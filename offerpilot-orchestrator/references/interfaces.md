# OfferPilot 数据契约

> 本文档定义跨 skill 的数据结构。Markdown 格式规范见 `resume-tailor/references/resume-standards.md`。

## 格式契约分层

| 层级 | 文件 | 职责 |
|------|------|------|
| Markdown 输出 | `resume-tailor/references/resume-standards.md` | 分隔符、模块结构、字段格式 |
| 解析脚本 | `resume-export/scripts/render_resume_web.py` | Markdown → HTML 结构 |
| CSS 样式 | `resume-export/assets/templates/resume-web/resume.css` | 字号、行高、间距、颜色 |

**关键原则：** 间距、字号、颜色由 CSS 层控制，Markdown 层只负责结构和内容。

---

## JobProfile

- `target_role`: 岗位名称。
- `role_type`: 实习、校招、社招或待确认。
- `role_category`: 岗位类别，技术岗或通用岗。
- `responsibilities`: 常见职责。
- `core_skills`: 核心技能要求。
- `bonus_skills`: 加分项。
- `keywords`: 高频关键词。
- `interview_focus`: 常见面试方向。
- `suitable_experiences`: 适合的经历类型（用于经历筛选）。
- `source`: 用户输入、JD、公开资料或推断。

## CandidateProfile

- `basic_info`: 姓名、电话、邮箱、城市等；缺失则待确认。
- `education`: 学校、专业、学历、时间、成绩或排名。
- `skills`: 技术栈，区分已证实、待确认、建议补强。
- `experiences`: 项目、实习、竞赛、科研、社团经历。
- `evidence`: 每条经历对应的来源片段、文件名或链接。
- `uncertain_items`: 无法确认但影响生成质量的信息。

## TailoredResume

- `basic_info`
- `education`
- `role_category`: 岗位类别，技术岗或通用岗。
- `skills`: 技术技能（技术岗）或技能与证书（通用岗）。
- `projects`: 项目经历（技术岗）。
- `internships`: 实习经历。
- `campus_experience`: 校园经历（通用岗），学生会/社团/班级职务。
- `social_practice`: 社会实践（通用岗），志愿服务/兼职/活动。
- `competitions`: 竞赛奖项。
- `target_role_title`
- `resume_summary`: 可选；仅在能提供具体岗位价值时使用。
- `layout`: 一页优先、模块顺序、重点经历排序。
- `pending_confirmations`

简历只能改写用户已有经历；不能把学习建议写成已掌握能力。

## ResumeDocument

- `output_dir`: 固定默认当前工作目录下的 `简历材料/`。
- `html_preview_path`: 静态 HTML/CSS 即时预览路径。
- `html_editable`: HTML 预览是否支持页面内实时编辑。
- `html_photo_upload`: HTML 预览是否支持用户本地上传照片并随 PDF 打印。
- `pdf_path`: 可选。PDF 定稿或预览路径；仅用户明确要求时由 HTML 打印导出，无法导出时标记原因。
- `format_profile`: 页边距、字体、字号、标题层级、行距。
- `target_role`: 对应岗位版本。
- `generated_at`
- `pending_confirmations`: 影响简历真实性或完整性的待确认项，**不在 HTML 中渲染**，只在交付摘要中展示。

文件命名固定为 `{姓名}-{岗位}-简历.{ext}`；默认扩展名为 `.html`，用户明确要求 PDF 时额外生成 `.pdf`。姓名缺失时用 `候选人`，岗位缺失时用 `目标岗位`。

## JobRecommendation

- `title`
- `company`
- `city`
- `education_requirement`
- `keywords`
- `url`
- `url_type`: 必须为岗位详情页。
- `platform`: BOSS 直聘、拉勾、猎聘、智联招聘、前程无忧、牛客、实习僧、公司 ATS 等。
- `source`
- `retrieved_at`
- `reason`
- `status`: 待用户确认、用户已选择、已打开、已投递、投递受阻、已跳过。
- `apply_requirements`: 登录、附件、在线表单、附加问题等。

## ApplicationAttempt

- `job`: 对应 `JobRecommendation`。
- `resume_document`: 使用的简历文件。
- `cover_note`: 可选投递说明。
- `user_confirmation`: 用户明确确认的原句或时间。
- `actions_taken`: 打开页面、填充字段、上传附件、提交申请等。
- `result`: 成功、停在最终确认、失败、需用户登录、平台限制。
- `evidence`: 页面标题、岗位链接、时间、失败原因。

## JobMaterials

后续求职材料输出为普通文档内容，包含已生成简历文件、岗位目标概览、匹配度分析、面试重点题目、学习补强资料、精准推荐岗位清单、确认后投递记录。它不是首要交付物；首要交付物是 `ResumeDocument`。
