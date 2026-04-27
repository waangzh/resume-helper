---
name: job-target-profile
description: 岗位画像 Skill。用于用户给出岗位名称、岗位 JD、招聘链接或目标方向时，提取岗位职责、核心技能、加分项、高频关键词、实习/校招差异和面试方向，并输出 JobProfile。适合”分析这个岗位””Java 后端需要什么””根据 JD 生成岗位画像”等任务。
---

# Job Target Profile

## 流程

1. 优先读取用户提供的 JD、招聘链接或岗位描述；没有 JD 时使用 `references/tech-role-baselines.md` 的技术岗基线。
2. 抽取岗位名称、岗位类型、职责、核心技能、加分技能、关键词、面试方向。
3. 区分”来自 JD 的要求”和”根据岗位常识推断的要求”。
4. 输出 `JobProfile`，并列出影响简历定制的关键词。

## 输出字段

| 字段 | 说明 | 来源 |
|------|------|------|
| target_role | 岗位名称 | 用户输入或 JD |
| role_type | 实习/校招/社招/待确认 | 用户输入或 JD |
| responsibilities | 常见职责 | JD 或基线 |
| core_skills | 核心技能要求 | JD 或基线 |
| bonus_skills | 加分项 | JD 或推断 |
| keywords | 高频关键词 | JD 提取 |
| interview_focus | 面试方向 | JD 或基线 |
| source | 来源标识 | 用户输入/JD/推断 |

## 输出要求

- 用表格或结构化列表呈现，便于后续 skill 复用
- 若岗位方向过宽，收敛到最可能的技术岗方向，并标记”待确认”
- 若涉及最新招聘要求或具体公司岗位，先搜索公开来源；无法联网时只输出通用画像和待补来源

## 质量边界

- 不把加分项写成硬性要求
- 不根据单个 JD 泛化所有岗位
- 对实习、校招、社招要求分别标注

## 资源

- `references/tech-role-baselines.md`：技术岗基线（无 JD 时使用）
