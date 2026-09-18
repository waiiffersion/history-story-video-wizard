# History Story Video Wizard 设计说明

## 目标

建立一个可公开安装的 Agent Skill，把历史题材从材料审计、故事化口播、配音、字幕、分镜、素材到成片质检组织成一条可恢复、可追溯的工作流。

## 公开承诺

输入一个历史选题及可用材料，输出：

1. 主张与来源对应的证据表；
2. 有人物、冲突、变化和认知回报的口播稿；
3. 以已锁定音频为时间基准的字幕和分镜；
4. 经高风险样镜、素材和最终媒体门检查的发布包。

Skill 不承诺自动获得流量，不代替历史学家或真人观众验收，不自动登录、上传或发布至任何平台。

## 公开边界

- 不包含个人姓名、账号、邮箱、绝对路径、设备状态、登录信息或持续授权。
- 不包含未公开文案、图片、音频、成片、哈希或平台后台数据。
- 不把一个项目的固定声线、发布节奏、外部生成器或项目路径写成通用规则。
- 只使用虚构示例和合成测试资产。
- 对外发布前执行隐私扫描，扫描失败时不得推送。

## 状态机

`BRIEF_READY → EVIDENCE_READY → STORY_DRAFTED → TEXT_AUDIT_PASS → TEXT_APPROVED → NARRATION_LOCKED → SUBTITLE_TIMING_LOCKED → STORYBOARD_LOCKED → VISUAL_PILOT_PASS → ASSET_READY → RENDERED_CANDIDATE → MEDIA_QA_PASS → FINAL_APPROVED → RELEASE_PACKAGE_READY`

状态只能顺序前进。每次前进记录时间、证据文件、SHA-256 和备注。文本改变会使文本之后的产物失效，但不自动删除用户资产。

## 文件结构

- `SKILL.md`：触发条件、核心状态机、强制边界和按需路由。
- `references/evidence.md`：来源身份、争议材料和表述确定性。
- `references/storytelling.md`：知识转故事、开头、口语、场景、结尾及回归审计。
- `references/production.md`：配音、字幕、分镜、高风险样镜、素材和渲染顺序。
- `references/media-qa.md`：机器门、完整视听验收和发布包。
- `assets/templates/`：项目摘要、证据表、故事承诺卡、审计表、分镜和发布记录模板。
- `scripts/project_state.py`：初始化、查看、前进和验证状态。
- `scripts/privacy_scan.py`：检测秘钥、凭据、用户绝对路径和内部项目标识。
- `scripts/media_qc.py`：使用 FFmpeg/FFprobe 验证可配置的竖屏成片技术指标。
- `tests/`：状态、隐私和媒体解析的可重复测试。

## 用户交互

每轮说明当前状态、本轮动作、交付物、剩余阻塞和下一状态。只在文本锁定、最终成片认可、付费、账号操作或公开发布等会改变外部状态的节点要求确认。

## 许可与发布

代码和文档采用 MIT License。仓库公开后提供中英文 README、安装指令、虚构演示、CI 和版本标签。
