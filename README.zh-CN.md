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

BossAgent 是一个本地优先、可扩展的 AI Agent 工作台。用户输入一个目标或上传资料后，系统会调度多个专业 Agent 协作，覆盖机会判断、项目决策、情景推演、数据分析、内容生成、销售跟进、资料整理，并由“总裁办执行官”汇总成可下载报告。

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
| 资料整理 Agent | 已可用 | 读取 PDF、Word、Excel、CSV、TXT，提炼重点和行动清单。 |
| MiroFish 沙盘推演 Agent | 已可用 | 借鉴 MiroFish 多智能体社会反应模拟思路，做客户、员工、竞品、渠道和舆论反应推演。 |
| 数据分析 Agent | 已可用 | 借鉴 Data Analytics 插件工作流，做数据质量、指标摘要、图表预览和经营建议。 |

## 功能特性

| 功能 | 状态 |
| --- | --- |
| 多 Agent 协作流程 | 已可用 |
| Streamlit 本地界面 | 已可用 |
| OpenAI-compatible 模型配置 | 已可用 |
| 本地 GGUF 模型文件夹模式 | 实验中 |
| 文件上传和资料分析 | 已可用 |
| CSV / Excel 数据分析页面 | 已可用 |
| MiroFish 风格情景推演任务 | 已可用 |
| MiroFish x Data Analytics 独立演练沙盘 | 已可用 |
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

## Google Colab 运行教程

BossAgent 也可以在 Google Colab 上临时运行，适合快速演示 UI 和 mock 工作流。请不要在公开 Notebook 里硬编码 API Key，也不要上传客户隐私资料。

### 1. 克隆项目并安装依赖

```python
!git clone https://github.com/smclw/BossAgent.git
%cd BossAgent
!pip -q install -r requirements.txt
!cp .env.example .env
```

### 2. 用本地演示模式启动

```python
!printf "\\nLLM_PROVIDER=mock\\nUSE_MOCK_LLM=true\\n" >> .env
!streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > streamlit.log 2>&1 &
```

### 3. 生成可访问链接

Colab 里的 `localhost:8501` 不能直接从浏览器打开，需要用临时隧道暴露 Streamlit 页面：

```python
!wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
!chmod +x cloudflared
!./cloudflared tunnel --url http://localhost:8501
```

运行后打开输出里的 `https://...trycloudflare.com` 链接即可。使用期间请保持该 Colab 单元格运行。

### 可选：安全配置 API Key

如果要调用真实模型，建议把 Key 放在 Colab Secrets，不要直接写进 Notebook：

```python
from google.colab import userdata
api_key = userdata.get("OPENAI_API_KEY")

from pathlib import Path
env_path = Path(".env")
text = env_path.read_text()
text += f"\\nLLM_PROVIDER=openai-compatible\\nUSE_MOCK_LLM=false\\nOPENAI_API_KEY={api_key}\\n"
env_path.write_text(text)
```

### 可选：下载本地 GGUF 模型运行

如果不想使用 API Key，也可以在 Colab 里把 `.gguf` 模型下载到 `models/` 文件夹，然后让 BossAgent 直接读取本地模型。下面默认使用 Qwen3-14B Q4_K_M，比玩具级小模型更接近真实效果，但需要更多内存。Colab 建议使用 GPU 或高内存运行时。

```python
!pip -q install -r requirements-local.txt
!mkdir -p models

# Qwen3 14B GGUF 模型，适合更真实的本地模型演示。
# 也可以替换成其他 GGUF 直链。
GGUF_URL = "https://huggingface.co/Qwen/Qwen3-14B-GGUF/resolve/main/Qwen3-14B-Q4_K_M.gguf"
!wget -O models/local-model.gguf "$GGUF_URL"

from pathlib import Path
env_path = Path(".env")
text = env_path.read_text()
text += "\\nLLM_PROVIDER=local-folder\\nUSE_MOCK_LLM=false\\nLOCAL_MODEL_DIR=models\\nLOCAL_GPU_LAYERS=0\\n"
env_path.write_text(text)
```

然后按同样方式启动 Streamlit，并用临时隧道打开页面。应用启动后，左侧边栏也可以直接选择“本地模型文件夹（GGUF）”或“OpenAI-compatible API”。

注意：Qwen3-14B Q4_K_M 是数 GB 级模型。如果 Colab 内存不足，请切换到高内存/GPU 运行时，或把链接替换成更小的 GGUF 模型。

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

本地 GGUF 模式默认使用 `LOCAL_CONTEXT_WINDOW=16384`，并会在调用 `llama-cpp-python` 前自动压缩过长上下文。如果仍然出现 context window 报错，可以在 `.env` 里继续增大 `LOCAL_CONTEXT_WINDOW`、降低 `LOCAL_MAX_TOKENS`，或换用内存更充足的运行环境。

## MiroFish x Data Analytics 演练沙盘

“演练沙盘”是一个单独页面，用来把数据分析和多角色推演结合起来：

- Data Analytics 层：本地读取 CSV / Excel，生成字段、缺失值、数值摘要、类别分布和图表预览。
- MiroFish 推演层：把数据画像作为证据，模拟核心客户、观望客户、销售、交付、竞品、渠道、投资人和公众舆论的多轮反应。
- BossAgent 总控层：汇总数据证据、角色反应、风险、机会和下一步动作，输出可下载报告。

它适合新品发布、价格调整、销售成交、渠道招商、舆论传播和投资决策的事前演练。该模块不会自动执行外部动作，也不应被当成确定性预测。

## 使用场景

- 判断一个项目是否值得进入。
- 为新业务生成首批内容和销售话术。
- 整理客户资料、会议纪要、报价表和行业材料。
- 把资料分析结果变成老板能直接看懂的行动报告。
- 上传销售、客户或运营数据，做 Data Analytics 驱动的 MiroFish 沙盘演练。

## 路线图

- v0.1 本地 MVP：多 Agent 协作、任务输入、文件解析、历史记录、报告导出。已可用。
- v0.2 MiroFish 风格情景推演和本地 Data Analytics 工作流。已可用。
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
