---
name: experience-filter
description: 经历归因与筛选 Skill。用于根据目标岗位画像和 CandidateProfile 判断哪些项目、实习、竞赛或课程经历应突出、保留、弱化、合并或追问。适合“帮我选哪些经历写进 Java 后端简历”“判断这些经历和岗位是否匹配”等任务。
---

# Experience Filter

## 流程

1. 读取 `JobProfile` 和 `CandidateProfile`。
2. 对每条经历按岗位相关度、证据强度、可追问性、成果表达潜力评分。
3. 输出经历处理建议：突出、保留、弱化、合并、删除、待确认。
4. 给出排序理由，供 `$resume-tailor` 生成简历时使用。

## 筛选标准

- 优先突出能证明核心技能的项目和实习。
- 竞赛、课程设计可保留，但要转化为岗位相关能力。
- 与岗位无关且占篇幅的经历应弱化或合并。
- 没有证据支撑的经历不进入主简历，只进入待确认项。

## 资源

需要评分细则时读取 `references/scoring-rubric.md`。
