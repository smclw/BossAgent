# Contributing to BossAgent

Thank you for helping build BossAgent into a practical AI Workforce OS.

## How to Contribute

1. Fork the repository.
2. Create a branch:

```bash
git checkout -b feature/your-change
```

3. Make a focused change.
4. Run the relevant checks.
5. Open a pull request with a clear description.

## Pull Request Naming

Use concise titles:

- `feat: add a new agent`
- `fix: handle empty uploaded files`
- `docs: update quickstart`
- `ui: improve task dashboard`

## Issues

When opening an issue, include:

- What you expected.
- What happened.
- Steps to reproduce.
- Your OS and Python version.
- Logs or screenshots when useful.

## Code Style

- Keep changes focused.
- Prefer existing project patterns.
- Avoid committing local data, uploaded files, or generated reports.
- Add comments only where they clarify non-obvious logic.

## Documentation

Documentation changes are welcome. If you update `README.md`, check whether multilingual README files should also be updated.

## Adding a New Agent

New agents should document:

- Role and positioning.
- Input format.
- Output format.
- Prompt / system instruction.
- Optional tools.
- Error handling.
- Example task.

The current MVP keeps agent definitions in `bossagent/agents.py`. Future versions may split agents into separate modules.

## Multilingual README Maintenance

- `README.md` is the source version.
- Keep language navigation links consistent.
- Preserve key product terms such as BossAgent, AI Agent, AI Workforce OS, and OpenAI-compatible API.
- Mark unfinished features as Planned or Experimental.

## Security Checklist Before Submitting

- No `.env`.
- No API keys or tokens.
- No customer data.
- No private uploaded files.
- No local databases.
- No virtual environments or cache files.
