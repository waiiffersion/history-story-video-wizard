# History Story Video Wizard

一个面向 Codex / Agent 的历史故事视频 Skill：把“选题与史料”推进为“可追溯文案、锁定配音、分镜、字幕、成片质检和发布包”，同时阻止史实越界、返工扩散和隐私外泄。

它不是爆款承诺，也不替你登录、上传或发布。它解决的是更朴素的问题：**让每一步有输入、有门禁、有证据、有回退边界。**

## 它能做什么

- 把每个重要表述追溯到具体来源与证据强度，而不是给整篇文章贴一个“有史料”标签。
- 把知识点改写成人物处境、异常行动、选择、代价和认知变化。
- 先锁文案，再生成配音；先锁配音，再做字幕时间轴和分镜。
- 先做视觉样片和高风险镜头，再批量生产素材。
- 用状态文件和哈希避免“旧文案、旧配音、旧字幕混进新成片”。
- 对视频执行可自动化的媒体检查，并明确区分 `PASS`、`FAIL`、`NOT_VERIFIED`。
- 发布前扫描本地路径、密钥、授权头、会话信息和自定义敏感词。

## 安装

把本仓库复制到你的 Codex Skills 目录，或让 Codex 从 GitHub 仓库安装此 Skill。

## 工作流

```text
题目与边界
  -> 证据表
  -> 故事承诺
  -> 口播草稿
  -> 文案审计
  -> 文案批准
  -> 配音锁定
  -> 字幕时间轴
  -> 分镜锁定
  -> 视觉样片
  -> 素材
  -> 候选成片
  -> 媒体质检
  -> 最终批准
  -> 发布包
```

任何上游内容变化，都会使下游产物失效。`文案审计通过`、`用户认可成片`、`授权上传`、`公开发布`始终是四件不同的事。

## 快速开始

```bash
python3 scripts/project_state.py init work/demo
cp assets/templates/evidence-table.md work/demo/EVIDENCE.md
cp assets/templates/story-promise.md work/demo/STORY_PROMISE.md
python3 scripts/project_state.py advance work/demo EVIDENCE_READY --evidence work/demo/EVIDENCE.md
python3 scripts/privacy_scan.py .
```

完整的虚构演示见 [examples/synthetic-case](examples/synthetic-case)。它不对应真实人物或真实历史，只用于展示格式和边界。

## 三个小工具

- `scripts/project_state.py`：创建、推进和校验生产状态；每次推进保存证据文件哈希。
- `scripts/privacy_scan.py`：发现个人主目录、疑似密钥、授权头、私钥、Cookie/Session 和自定义禁词。
- `scripts/media_qc.py`：在 FFmpeg/FFprobe 可用时检查封装、视频流、音频流、快启、黑帧和长静音；工具缺失时返回 `NOT_VERIFIED`。

## 边界

- 不自动登录任何平台。
- 不自动上传、定时或发布。
- 不包含真实项目素材、真实账号、私人路径、登录信息、授权记录或未公开文案。
- 不保证流量；它提高的是证据纪律、故事可听性、流程稳定性和成片可验证性。

## 许可

MIT
