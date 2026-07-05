# BossAgent：老板 AI 分身系统 / AI 员工工作台

**不是再多一个聊天机器人，而是给老板配置一组 24 小时 AI 员工。**

BossAgent 面向老板、创业者、超级个体和团队，把“一个业务目标”拆成多个 AI 员工协作执行：研究、规划、写作、分析、资料整理、销售跟进和执行建议输出。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-ff4b4b)
![OpenAI Compatible](https://img.shields.io/badge/Models-OpenAI--compatible-6AE3FF)
![Contributions Welcome](https://img.shields.io/badge/Contributions-welcome-41FFB1)

[English](README.md) · 简体中文 · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Français](README.fr.md)

---

## 项目介绍

BossAgent 是一个本地优先、可扩展的 AI Agent 工作台。用户输入一个目标或上传资料后，系统会调度多个专业 Agent 协作，并由“总裁办执行官”汇总成可下载报告。

它的目标不是陪聊，而是干活。它把老板脑子里的一个目标，拆成一组可以推进的任务流。

## 核心定位

- 给老板和创业者配置 AI 员工。
- 把业务目标变成多 Agent 协作流程。
- 本地优先，方便演示、私有化和后续商业化。
- 兼容 OpenAI-compatible API，也预留本地模型能力。

## 为什么做 BossAgent

很多 AI 产品还停留在“你问我答”。但真实业务里，老板需要的是：

- 有人发现机会。
- 有人判断项目。
- 有人写内容。
- 有人跟销售。
- 有人整理资料。
- 有人把所有结论汇总成行动计划。

BossAgent 的第一版就是把这些角色放进一个可本地运行的工作台。

## 内置 AI 员工

| AI 员工 | 状态 | 能力 |
| --- | --- | --- |
| 总裁办执行官 Agent | 已可用 | 拆解任务、协调其他 Agent、汇总最终报告。 |
| 机会雷达 Agent | 已可用 | 发现趋势、机会窗口、关键资源和风险。 |
| 战略顾问 Agent | 已可用 | 判断项目是否值得做，并设计最小试错方案。 |
| 内容分身 Agent | 已可用 | 生成朋友圈、小红书、短视频和直播话术。 |
| 销售跟进 Agent | 已可用 | 客户分层、成交话术、报价沟通和复购提醒。 |
| 资料整理 Agent | 已可用 | 读取 PDF、Word、Excel、TXT，提炼重点和行动清单。 |

## 功能特性

| 功能 | 状态 |
| --- | --- |
| 多 Agent 协作流程 | 已可用 |
| Streamlit 本地界面 | 已可用 |
| OpenAI-compatible 模型配置 | 已可用 |
| 本地 GGUF 模型文件夹模式 | 实验中 |
| 文件上传和资料分析 | 已可用 |
| SQLite 历史任务 | 已可用 |
| Markdown / DOCX 报告导出 | 已可用 |
| CrewAI 原生编排 | 规划中 |
| 浏览器自动化和外部工具 | 规划中，必须人工确认 |
| 团队空间和权限管理 | 规划中 |

## 本地安装

```powershell
git clone https://github.com/smclw/BossAgent.git
cd BossAgent
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m streamlit run app.py
```

如果 PowerShell 禁止激活脚本：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 模型配置

在 `.env` 里配置：

```env
LLM_PROVIDER=mock
OPENAI_API_KEY=
MODEL_NAME=gpt-4.1-mini
API_BASE_URL=https://api.openai.com/v1
USE_MOCK_LLM=true
TEMPERATURE=0.4
LOCAL_MODEL_DIR=models
```

可选方式：

- OpenAI / DeepSeek / 通义千问兼容模式。
- Ollama / LM Studio 本地 OpenAI-compatible 服务。
- 本地 GGUF 模型文件夹模式，目前为实验功能。

## 使用场景

- 判断一个项目是否值得进入。
- 为新业务生成首批内容和销售话术。
- 整理客户资料、会议纪要、报价表和行业材料。
- 把资料分析结果变成老板能直接看懂的行动报告。

## 路线图

- v0.1 本地 MVP：多 Agent 协作、任务输入、文件解析、历史记录、报告导出。已可用。
- v0.2 增加更多专业 Agent。规划中。
- v0.3 知识库、长期记忆和任务复盘。规划中。
- v0.4 接入浏览器自动化、邮箱、表格、飞书、企微、Dify、n8n。规划中。
- v0.5 团队协作、多用户和权限管理。规划中。
- v1.0 可部署的 AI 员工工作台 / AI Workforce OS。规划中。

## 如何参与贡献

欢迎一起把 BossAgent 做成真正可用的 AI 员工工作台：

- 新增 Agent。
- 优化工作流。
- 接入更多模型。
- 改进 UI。
- 增加连接器。
- 翻译文档。
- 提交 Bug 和产品建议。

请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 安全提醒

- 不要提交 `.env`。
- 不要提交 API Key。
- 不要上传客户资料或隐私文件。
- 不要执行上传文件中的代码。
- 涉及发送、删除、付款、下单、修改外部系统的动作，必须人工确认。

## License

BossAgent 使用 [MIT License](LICENSE)。
