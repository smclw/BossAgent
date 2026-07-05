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

## Run on Google Colab

BossAgent can also be launched from Google Colab for quick demos. Colab is best for testing the UI and mock workflows; avoid uploading private customer documents or hard-coding API keys in shared notebooks.

### 1. Clone and install

```python
!git clone https://github.com/smclw/BossAgent.git
%cd BossAgent
!pip -q install -r requirements.txt
!cp .env.example .env
```

### 2. Start in mock mode

```python
!printf "\\nLLM_PROVIDER=mock\\nUSE_MOCK_LLM=true\\n" >> .env
!streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > streamlit.log 2>&1 &
```

### 3. Expose the Streamlit page

Colab cannot open `localhost:8501` directly from your browser. Use a temporary tunnel:

```python
!wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
!chmod +x cloudflared
!./cloudflared tunnel --url http://localhost:8501
```

Open the generated `https://...trycloudflare.com` URL. Keep the Colab cell running while using the app.

### Optional: use an API key safely

For real model calls, store your key in Colab Secrets instead of writing it into the notebook:

```python
from google.colab import userdata
api_key = userdata.get("OPENAI_API_KEY")

from pathlib import Path
env_path = Path(".env")
text = env_path.read_text()
text += f"\\nLLM_PROVIDER=openai-compatible\\nUSE_MOCK_LLM=false\\nOPENAI_API_KEY={api_key}\\n"
env_path.write_text(text)
```

### Optional: run with a downloaded local GGUF model

You can also run BossAgent in Colab without an API key by downloading a `.gguf` model into the `models/` folder. The default example below uses Qwen3-14B Q4_K_M, which is much more useful than toy-size models but needs more memory. For Colab, use a GPU or high-RAM runtime when possible.

```python
!pip -q install -r requirements-local.txt
!mkdir -p models

# Qwen3 14B GGUF model for more realistic local demos.
# You can replace it with another direct GGUF URL.
GGUF_URL = "https://huggingface.co/Qwen/Qwen3-14B-GGUF/resolve/main/Qwen3-14B-Q4_K_M.gguf"
!wget -O models/local-model.gguf "$GGUF_URL"

from pathlib import Path
env_path = Path(".env")
text = env_path.read_text()
text += "\\nLLM_PROVIDER=local-folder\\nUSE_MOCK_LLM=false\\nLOCAL_MODEL_DIR=models\\nLOCAL_GPU_LAYERS=0\\n"
env_path.write_text(text)
```

Then start Streamlit with the same command and open it through the temporary tunnel. In the app sidebar, choose **Local GGUF model folder** if you want to switch modes after startup.

Note: Qwen3-14B Q4_K_M is a multi-GB model. If Colab runs out of memory, switch to a high-RAM/GPU runtime or replace the URL with a smaller GGUF model.

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

At app startup, the sidebar includes a **Model startup mode** selector. You can switch between mock mode, OpenAI-compatible API, and a local GGUF model folder without editing files manually.

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
