# Architecture

BossAgent is designed as a local-first MVP that can later be upgraded into a web app, CrewAI-native workflow, or enterprise tool connector.

## Frontend Entry

- `app.py`
- Streamlit application with pages for home, new task, upload, history, and settings.

## Backend Logic

- `bossagent/config.py`: environment variables and runtime paths.
- `bossagent/llm.py`: model provider abstraction.
- `bossagent/orchestrator.py`: task-to-agent routing and result aggregation.
- `bossagent/agents.py`: built-in agent roles and prompts.
- `bossagent/storage.py`: SQLite task history.
- `bossagent/documents.py`: file text extraction.
- `bossagent/export.py`: Markdown and DOCX export.
- `bossagent/safety.py`: high-risk keyword warning.

## Agent Orchestration

The current MVP uses a Python orchestration layer. It keeps the boundary clear so future versions can replace or extend it with CrewAI Crew / Task / Agent objects.

## Model Configuration

BossAgent supports:

- Mock mode for offline demos.
- OpenAI-compatible APIs such as OpenAI, DeepSeek, Qwen compatible mode, Ollama, and LM Studio.
- Experimental local GGUF loading through `llama-cpp-python`.

Configuration lives in `.env`.

## File Upload and Parsing

Supported files:

- PDF.
- DOCX.
- XLSX / XLS.
- TXT.

Uploaded files are only read for text extraction. BossAgent must not execute code from uploaded files.

## Task History

Task records are stored in SQLite under `data/bossagent.db`. The database is ignored by Git.

Stored fields include:

- Task type.
- User goal.
- Uploaded file names.
- Agent outputs.
- Final report.
- Created time.

## Report Export

Reports can be exported as:

- Markdown.
- DOCX.

Exports are written to `exports/`, which is ignored by Git except for `.gitkeep`.

## Extending Agents

To add an agent:

1. Add an `AgentSpec` in `bossagent/agents.py`.
2. Define role, goal, and output requirements.
3. Update `TASK_AGENT_MAP` in `bossagent/orchestrator.py`.
4. Add UI labels or routing as needed.

## Future Integrations

Planned integration paths:

- Browser automation for supervised workflows.
- n8n for automation pipelines.
- Dify for knowledge and app orchestration.
- Feishu / WeCom for enterprise communication.
- Email and spreadsheets for operational workflows.

All external write actions must require explicit human confirmation.
