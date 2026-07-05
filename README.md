# BossAgent

**The AI Workforce OS for founders, operators, and ambitious builders.**

Configure a team of 24/7 AI employees to research, plan, write, analyze, follow up, and produce execution-ready reports.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-ff4b4b)
![OpenAI Compatible](https://img.shields.io/badge/Models-OpenAI--compatible-6AE3FF)
![Contributions Welcome](https://img.shields.io/badge/Contributions-welcome-41FFB1)

English · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Français](README.fr.md)

---

## Project Introduction

BossAgent is a local-first, extensible AI Agent workspace that helps founders, operators, creators, and teams configure a coordinated team of AI employees.

It is not another chatbot. BossAgent turns business goals into multi-agent workflows: opportunity research, project judgment, content generation, sales follow-up, document analysis, and final executive reporting.

## Why BossAgent

AI should not just chat. It should work.

Founders do not need another empty conversation box. They need an AI team that can split a goal into specialized work, keep context, and return a useful operating report.

BossAgent is designed as a practical MVP for local demos, commercial experiments, and future integrations with tools such as CrewAI, Dify, n8n, WeCom, Feishu, and browser automation.

## Core Agents

| Agent | Status | Responsibility |
| --- | --- | --- |
| Chief of Staff Agent | Available | Decomposes tasks, coordinates specialist agents, and summarizes the final report. |
| Opportunity Radar Agent | Available | Finds trends, industry windows, opportunity signals, required resources, and risks. |
| Strategy Advisor Agent | Available | Judges whether a project is worth entering and designs low-cost validation paths. |
| Content Clone Agent | Available | Drafts social posts, Xiaohongshu content, short-video scripts, and livestream talk tracks. |
| Sales Follow-up Agent | Available | Creates customer segmentation, follow-up scripts, quote communication, and deal motion. |
| Document Analyst Agent | Available | Reads PDF, Word, Excel, and TXT files, then extracts summaries and action lists. |

## Features

| Feature | Status |
| --- | --- |
| Multi-agent workflow orchestration | Available |
| Streamlit local UI | Available |
| OpenAI-compatible model support | Available |
| Local GGUF model folder mode | Experimental |
| File upload and document analysis | Available |
| SQLite task history | Available |
| Markdown / DOCX report export | Available |
| CrewAI-native orchestration | Planned |
| Browser automation and external actions | Planned, human confirmation required |
| Team workspace and permissions | Planned |

## Screenshots / Preview

Screenshots coming soon.

- Dashboard Preview
- Multi-agent Workflow Preview
- Report Output Preview

## Quick Start

```bash
git clone https://github.com/smclw/BossAgent.git
cd BossAgent
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m streamlit run app.py
```

If you want to activate the environment in PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

Open the local URL printed by Streamlit, usually `http://localhost:8501`.

## Configuration

BossAgent reads model and runtime settings from `.env`.

```env
LLM_PROVIDER=mock
OPENAI_API_KEY=
MODEL_NAME=gpt-4.1-mini
API_BASE_URL=https://api.openai.com/v1
USE_MOCK_LLM=true
TEMPERATURE=0.4
LOCAL_MODEL_DIR=models
```

Supported model paths:

- OpenAI-compatible APIs: OpenAI, DeepSeek, Qwen DashScope compatible mode, Ollama, LM Studio, and similar endpoints.
- Local folder mode: experimental direct loading of `.gguf` models via `llama-cpp-python`.

For direct local GGUF loading:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-local.txt
```

Then put a `.gguf` model into `models/` or set `LOCAL_MODEL_DIR` to a full `.gguf` file path.

## Roadmap

- v0.1 Local MVP: multi-agent workflow, task input, file parsing, history, and report export. Available.
- v0.2 More specialized agents: founder assistant, research assistant, marketing assistant, and operations assistant. Planned.
- v0.3 Knowledge base and long-term memory. Planned.
- v0.4 Browser automation, email, spreadsheets, Feishu, WeCom, Dify, and n8n connectors. Planned.
- v0.5 Team workspace, multi-user mode, and permissions. Planned.
- v1.0 Deployable AI Workforce OS. Planned.

## Contributing

Contributions are welcome:

- Build new agents.
- Improve workflows.
- Add model providers.
- Improve the UI.
- Add connectors.
- Translate documentation.
- Report bugs and propose product ideas.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## Security

- Never commit API keys.
- Never upload private customer data.
- Do not execute uploaded files.
- External actions such as sending, deleting, paying, ordering, or modifying third-party systems must require human confirmation.

See [SECURITY.md](SECURITY.md) for details.

## License

BossAgent is released under the [MIT License](LICENSE).
